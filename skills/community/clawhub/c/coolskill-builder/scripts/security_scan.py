#!/usr/bin/env python3
import sys,json,re,os

W={'sys','json','os','re','math','random','datetime','itertools','collections','typing','inspect','hashlib','base64','urllib.request','http.client','socket','ssl','time','uuid','string','warnings','traceback','io','csv','html.parser','pathlib','fnmatch','glob','copy','functools','enum','dataclasses','contextlib','builtins'}
D=r'^(eval|exec|compile|os\.system|subprocess|pty)\b'
K=r'([a-zA-Z0-9_-]{20,}|(sk-|pk-|AKIA|ghp-|gpt-)[a-zA-Z0-9]+|(password|passwd|pwd|secret|token|api_key)\s*=\s*["\'][^"\']+["\'])'
N={'urllib.request','http.client','socket'}

def sc(p):
    r={'L1':('PASS',''),'L2':('PASS',''),'L3':('PASS',''),'L4':('PASS',''),'L5':('PASS',''),'ok':1,'d':[]}
    try:
        with open(p)as f:c=f.read()
    except Exception as e:r['ok']=0;r['d'].append(f'read_err: {e}');return r
    im=re.findall(r'^(?:import\s+([\w.]+)|from\s+([\w.]+)\s+import)',c,re.M)
    for a,b in im:
        m=a or b
        if m.split('.')[0]not in W and m not in W:r['L1']=('FAIL',f'bad_import: {m}');r['ok']=0;break
    if re.search(r'requirements\.txt|setup\.py|pyproject\.toml|pip\s+install',c):r['L1']=('FAIL','third_party_ref');r['ok']=0
    if any(x in c for x in['eval(','exec(','compile(','os.system(','subprocess.','pty.']):r['L2']=('FAIL','dangerous_call');r['ok']=0
    if re.search(K,c):r['L3']=('FAIL','hardcoded_secret');r['ok']=0
    pe=json.loads(open(p.replace('impl.py','skill.yaml')).read())if os.path.exists(p.replace('impl.py','skill.yaml'))else{}
    pm=pe.get('props',{}).get('perms','').split(',')if isinstance(pe.get('props',{}).get('perms',''),str)else pe.get('props',{}).get('perms',[])
    if'net'not in pm and any(x in c for x in N):r['L4']=('FAIL','network_without_perm');r['ok']=0
    if'traceback.format_exc()'in c or'sys.exc_info()'in c or'os.environ'in c:r['L5']=('FAIL','info_leak');r['ok']=0
    return r

if __name__=='__main__':
    if len(sys.argv)<2:print('usage: security_scan.py <impl.py path>');sys.exit(1)
    r=sc(sys.argv[1])
    print(json.dumps(r,ensure_ascii=False,separators=(',',':')))
    sys.exit(0 if r['ok']else 1)
