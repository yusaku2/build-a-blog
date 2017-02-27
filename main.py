#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2

template_dir=os.path.join(os.path.dirname(__file__),'templates')
webapp2.Route('/blog/<id:\d+>', ViewPostHandler)

jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
          autoescape=True)
from google.appengine.ext import db

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a,**kw)

    def render_str(self, template, **params):
        t= jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class NewPost(Handler):
    title=self.request.get("title")
    bloge=self.request.get("bloge")
    def post(self):
        if title and bloge:
            b=Bloge(title=title, bloge=bloge)
            b.put()
            self.redirect('/')

        else:
            error="Please enter a title and post!"
            self.render_front(title, bloge, error)

    def get(self):
class ViewPostHandler(Handler):
    def get(self, id):

        self.response.write(bloge.id)

class Bloge(db.Model):
    title=db.StringProperty(required=True)
    bloge=db.TextProperty(required=True)
    created=db.DateTimeProperty(auto_now_add=True)

class MainPage(Handler):
    def render_front(self, title="", bloge="", error=""):
        posts=db.GqlQuery("SELECT * FROM Bloge ORDER BY  created DESC LIMIT 5")
        self.render("front.html",title=title, bloge=bloge, error=error)
        
    def get(self):
        self.render_front()

    def post(self):
        title=self.request.get("title")
        bloge=self.request.get("bloge")

        if title and bloge:
            b=Bloge(title=title, bloge=bloge)
            b.put()
            self.redirect('/')

        else:
            error="Please enter a title and post!"
            self.render_front(title, bloge, error)



app = webapp2.WSGIApplication([
    ('/', MainPage),
     ('/blog', BlogView)
     ('/newpost', newpost)

], debug=True)
