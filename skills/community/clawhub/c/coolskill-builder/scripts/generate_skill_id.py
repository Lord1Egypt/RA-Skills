#!/usr/bin/env python3
import sys,random,string,json,os

D=['data','text','web','file','api','calc','str','time','hash','net','img','crypto','geo','fin','dev','ml','nlp','sys','media','db']
F=['parse','fmt','conv','gen','calc','hash','fetch','compress','split','merge','search','filter','sort','validate','transform','extract','analyze','render','encode','decode','scan','convert','process','clean','transform']

def gid(dom='',func=''):
    d=dom or random.choice(D)
    f=func or random.choice(F)
    r=''.join(random.choices(string.ascii_lowercase+string.digits,k=3))
    return f'{d}-{f}-{r}'

def nid(idx,p='registry/index.json'):
    if os.path.exists(p):
        with open(p)as f:i=json.load(f)
    else:i={'skills':{}}
    s=i['skills']
    while 1:
        x=gid()
        if x not in s:return x

if __name__=='__main__':
    dom=sys.argv[1]if len(sys.argv)>1 else''
    func=sys.argv[2]if len(sys.argv)>2 else''
    print(nid(gid(dom,func)))
