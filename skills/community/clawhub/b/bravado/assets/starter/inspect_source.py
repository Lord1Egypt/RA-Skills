"""Collect factual source notes from a public website or GitHub repository.

This is an intake aid. It never writes a script or treats page claims as verified.
The Bravado agent must inspect the live product and approve the creative brief.
"""
import argparse, json, re, urllib.request, urllib.error
from urllib.parse import urlparse
from html.parser import HTMLParser
from pathlib import Path

class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.title='';self.headings=[];self.description='';self.og={};self.css=[]
        self.active=None;self.text=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ['title','h1','h2','h3']:self.active=tag;self.text=[]
        if tag=='meta':
            key=a.get('property',a.get('name','')).lower();value=a.get('content','')
            if key=='description':self.description=value
            if key.startswith('og:'):self.og[key]=value
        if tag=='link' and a.get('rel')=='stylesheet':self.css.append(a.get('href',''))
    def handle_data(self,data):
        if self.active:self.text.append(data)
    def handle_endtag(self,tag):
        if self.active==tag:
            s=' '.join(' '.join(self.text).split())
            if s:
                if tag=='title':self.title=s
                else:self.headings.append({'level':tag,'text':s})
            self.active=None

def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Bravado/0.1 (project source inspection)'})
    with urllib.request.urlopen(req,timeout=20) as r:
        data=r.read(1_000_000)
        return data.decode('utf-8','replace'),r.geturl()

def inspect(url):
    if not url.startswith(('https://','http://')):raise ValueError('Provide a full https:// URL')
    parsed=urlparse(url)
    output={'input_url':url,'source_type':'site','redirected_url':None,'claims_to_verify':[],
            'creative_notes':[],'limitations':[]}
    if parsed.netloc.lower()=='github.com':
        parts=[p for p in parsed.path.split('/') if p]
        if len(parts)<2:raise ValueError('Provide a GitHub repository URL, not just a user profile')
        owner,repo=parts[:2];output['source_type']='github_repository'
        api=f'https://api.github.com/repos/{owner}/{repo}'
        body,final=get(api);data=json.loads(body)
        output.update({'redirected_url':final,'name':data.get('name'),'description':data.get('description'),
                       'homepage':data.get('homepage'),'default_branch':data.get('default_branch'),
                       'topics':data.get('topics',[]),'visibility':data.get('visibility')})
        try:
            readme,_=get(f'https://api.github.com/repos/{owner}/{repo}/readme')
            obj=json.loads(readme)
            if obj.get('encoding')=='base64':
                import base64
                content=base64.b64decode(obj.get('content','')).decode('utf-8','replace')
                output['readme_excerpt']=content[:8000]
        except urllib.error.HTTPError as e:output['limitations'].append(f'README unavailable: HTTP {e.code}')
        output['creative_notes'].append('Inspect the running product or screenshots; README copy alone is insufficient for visual identity.')
    else:
        body,final=get(url);page=Page();page.feed(body)
        output.update({'redirected_url':final,'title':page.title,'description':page.description,
                       'headings':page.headings[:30],'open_graph':page.og,'stylesheets':page.css[:15]})
        for color,count in sorted(((c,body.lower().count(c)) for c in set(re.findall(r'#[0-9a-fA-F]{6}\b',body))),key=lambda pair:-pair[1])[:10]:
            output.setdefault('inline_color_candidates',[]).append({'hex':color,'mentions':count})
        output['creative_notes'].append('Inspect screenshots at desktop and mobile size; scraped metadata omits layout, motion, and audio.')
    output['claims_to_verify'].append('Check all metrics, availability states, pricing, and product promises against the current source before scripting.')
    return output

def main():
    p=argparse.ArgumentParser();p.add_argument('url');p.add_argument('--out',default='output/source-notes.json')
    a=p.parse_args();result=inspect(a.url);path=Path(a.out);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(path)
if __name__=='__main__':main()
