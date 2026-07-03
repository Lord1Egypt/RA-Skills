#!/usr/bin/env python3
import sys,json,os,subprocess,re

def v(p):
    r={'syntax':0,'imports':0,'run_sig':0,'return_fmt':0,'token_ok':0,'ok':0,'d':[]}
    try:
        with open(p)as f:c=f.read()
    except Exception as e:r['d'].append(f'read_err: {e}');return r
    try:compile(c,'<impl>','exec');r['syntax']=1
    except SyntaxError as e:r['d'].append(f'syntax: {e}')
    if'def run('in c:r['run_sig']=1
    else:r['d'].append('missing_run')
    if"r['s']"in c and"r['d']"in c:r['return_fmt']=1
    else:r['d'].append('bad_return_fmt')
    if c.count(' ')<=len(c)*0.3:r['token_ok']=1
    else:r['d'].append('too_many_spaces')
    r['ok']=all([r['syntax'],r['run_sig'],r['return_fmt'],r['token_ok']])
    return r

if __name__=='__main__':
    if len(sys.argv)<2:print('usage: validate_impl.py <impl.py path>');sys.exit(1)
    r=v(sys.argv[1])
    print(json.dumps(r,ensure_ascii=False,separators=(',',':')))
    sys.exit(0 if r['ok']else 1)
