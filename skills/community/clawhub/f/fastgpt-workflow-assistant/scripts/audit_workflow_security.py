#!/usr/bin/env python3
"""Read-only FastGPT-compatible JSON inventory and heuristic security review.

No supplied code, URL, expression or tool is executed. Output deliberately omits
prompts, request bodies, raw code and credential values. Findings require review.
"""
from __future__ import annotations
import argparse
from collections import Counter, deque
import hashlib
import ipaddress
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

SENSITIVE = re.compile(r"password|passwd|pwd|token|secret|cookie|authorization|credential|api[_-]?key|密码|密钥", re.I)
SECRET_TEXT = re.compile(r"\bBearer\s+(?!\{\{)[\w.~+/=-]{12,}|\bsk-[\w-]{12,}|(?:api[_-]?key|token|password)\s*[:=]\s*[\"']?[\w.~+/=-]{12,}", re.I)
REF = re.compile(r"\{\{\$?([\w-]+)\.([\w-]+)\$?\}\}")
CODE_HINTS = {
    'dynamic_execution': r'\b(?:eval|exec|__import__)\s*\(|\bnew\s+Function\s*\(',
    'process_or_filesystem': r'child_process|\bsubprocess\b|\bos\.system\s*\(|\b(?:exec|spawn)Sync\s*\(|\brequire\s*\(\s*[\"\'](?:fs|node:fs)',
    'network_call': r'\bfetch\s*\(|\bXMLHttpRequest\b|\baxios\s*[.(]|https?\.request\s*\(',
    'encoded_content': r'\batob\s*\(|Buffer\.from\([^\n]{0,160}[\"\']base64|payload_base64',
}

def walk(value, path='$'):
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk(child, path+'.'+str(key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, f'{path}[{index}]')

def reference(value):
    return isinstance(value, list) and len(value) == 2 and all(isinstance(v, str) for v in value)

def masked_url(value):
    """Only a bounded, redacted destination. Query/fragment/userinfo never escape."""
    if not isinstance(value, str):
        return {'destination': '<nonliteral>', 'dynamic': True}
    if '{{' in value:
        return {'destination': '<dynamic expression>', 'dynamic': True}
    try:
        u = urlsplit(value)
        if u.scheme not in ('http','https') or not u.hostname:
            return {'destination': '<unresolved URL>', 'dynamic': False}
        host=u.hostname
        # Preserve host for policy matching, redact destination path entirely:
        # webhook paths themselves may be credentials, even without a query.
        port=f':{u.port}' if u.port else ''
        private=False
        try: private=not ipaddress.ip_address(host).is_global
        except ValueError: pass
        return {'destination':f'{u.scheme}://{host}{port}/<path-redacted>',
                'host':host,'scheme':u.scheme,'private_or_special_ip':private,
                'userinfo_present':bool(u.username or u.password),
                'query_or_fragment_present':bool(u.query or u.fragment),'dynamic':False}
    except (ValueError, TypeError):
        return {'destination':'<malformed URL>', 'dynamic':False}

def audit(data, *, allowed_hosts=None):
    if not isinstance(data,dict) or not isinstance(data.get('nodes'),list) or not isinstance(data.get('edges'),list):
        raise ValueError('Expected an object with nodes and edges arrays')
    nodes=[n for n in data['nodes'] if isinstance(n,dict)]
    edges=[e for e in data['edges'] if isinstance(e,dict)]
    ids={str(n.get('nodeId',n.get('id',''))) for n in nodes}
    graph={k:[] for k in ids}
    for e in edges:
        if e.get('source') in graph and e.get('target') in ids:
            graph[e['source']].append(e['target'])
    # Structural reachability includes implicit loop entries, not branch execution.
    for n in nodes:
        if n.get('flowNodeType')=='loopRun':
            nid=str(n.get('nodeId',n.get('id','')))
            for child in nodes:
                if child.get('parentNodeId')==nid and child.get('flowNodeType')=='loopRunStart':
                    graph[nid].append(str(child.get('nodeId',child.get('id',''))))
    pending=deque(str(n.get('nodeId',n.get('id',''))) for n in nodes if n.get('flowNodeType')=='workflowStart')
    reached=set()
    while pending:
        k=pending.popleft()
        if k in reached: continue
        reached.add(k);pending.extend(graph.get(k,[]))
    findings=[];http=[];models=[];retrieval=[];code=[];stores=[];refs=[]
    def add(rule,priority,nid,location,statement,verify,confidence='review_required'):
        findings.append(dict(rule=rule,priority=priority,node_id=nid,location=location,
                             observation=statement,confidence=confidence,verification=verify))
    for index,n in enumerate(nodes):
        nid=str(n.get('nodeId',n.get('id','')));typ=str(n.get('flowNodeType',''))
        raw_inputs=n.get('inputs')
        inputs=[i for i in raw_inputs if isinstance(i,dict)] if isinstance(raw_inputs,list) else []
        fields={str(i.get('key','')):i.get('value') for i in inputs}
        base=f'$.nodes[{index}]'
        for ii,item in enumerate(inputs):
            k=str(item.get('key',''));v=item.get('value');p=f'{base}.inputs[{ii}].value'
            if reference(v) and v[0] in ids|{'VARIABLE_NODE_ID','SYSTEM_VARIABLE_NODE_ID'}:
                refs.append(dict(source=v[0],output=v[1],target=nid,input=k))
            for _,value in walk(v):
                if reference(value) and value[0] in ids|{'VARIABLE_NODE_ID','SYSTEM_VARIABLE_NODE_ID'} and value != v:
                    refs.append(dict(source=value[0],output=value[1],target=nid,input=k))
                if isinstance(value,str):
                    for src,output in REF.findall(value):
                        refs.append(dict(source=src,output=output,target=nid,input=k))
            # Managed credential containers are opaque; don't print or label them plaintext.
            if k=='system_header_secret': continue
            matches=False
            for subpath,value in walk(v):
                if isinstance(value,str) and SECRET_TEXT.search(value): matches=True
                if isinstance(value,dict):
                    for key,child in value.items():
                        if SENSITIVE.search(str(key)) and isinstance(child,str) and child.strip() and '{{' not in child and len(child)>5:
                            matches=True
            if SENSITIVE.search(k) and isinstance(v,str) and v.strip() and '{{' not in v:
                matches=True
            # Header key/value pairs need joint inspection, not only key names.
            if k=='system_httpHeader' and isinstance(v,list):
                matches |= any(isinstance(x,dict) and SENSITIVE.search(str(x.get('key',''))) and isinstance(x.get('value'),str) and x['value'].strip() and '{{' not in x['value'] for x in v)
            if matches:
                add('SEC001','high',nid,p,'Possible literal credential; value suppressed.',
                    'Confirm whether it is a real credential or a dummy example; move real values to managed credentials and assess rotation.')
        if 'http' in typ.lower():
            dest=masked_url(fields.get('system_httpReqUrl'))
            headers=fields.get('system_httpHeader')
            headers=headers if isinstance(headers,list) else []
            auth=bool(fields.get('system_header_secret')) or any(isinstance(h,dict) and SENSITIVE.search(str(h.get('key',''))) for h in headers)
            http.append(dict(node_id=nid,method=fields.get('system_httpMethod'),destination=dest,
                             credential_configuration_visible=bool(auth),structurally_reachable=nid in reached,
                             timeout=fields.get('system_httpTimeout')))
            add('SEC010','high',nid,base,'HTTP sink exists; identity, task ownership and server authorization are outside this export.',
                'Inspect backend workflow/subworkflows and test unauthorized/cross-user access in an authorized test environment.')
            if dest.get('dynamic'):add('SEC011','high',nid,base,'Dynamic/unresolved outbound destination.', 'Trace user/knowledge/tool inputs into the URL; enforce backend destination and redirect policies.')
            if dest.get('scheme')=='http':add('SEC012','medium',nid,base,'Plain HTTP transport configured.', 'Assess sensitive payload and network boundary; use TLS or document compensating controls.','confirmed_configuration')
            if not auth:add('SEC013','medium',nid,base,'No explicit authentication configuration recognized in this node.', 'Check gateway, network and server authentication; this does not prove anonymous access.')
            if dest.get('userinfo_present') or dest.get('query_or_fragment_present'):
                add('SEC014','medium',nid,base,'URL contains userinfo/query/fragment; content suppressed.', 'Check URL credentials, signed-link lifetime and log exposure.')
            if allowed_hosts is not None and dest.get('host') and dest['host'].lower() not in allowed_hosts:
                add('SEC015','high',nid,base,'Destination host is outside the supplied policy.', 'Verify policy and business need; do not call the destination.','policy_mismatch')
        if typ in ('chatNode','classifyQuestion'):
            models.append(dict(node_id=nid,vision=bool(fields.get('aiChatVision')),history=fields.get('history'),
                               receives_file_reference=bool(fields.get('fileUrlList')),quote_reference_present=bool(fields.get('quoteQA'))))
            add('SEC020','medium',nid,base,'User/context/knowledge or files can reach a model.', 'Verify actual model gateway, hosting/retention policy, data classification and prompt-injection/tool authority boundaries.')
        if typ=='datasetSearchNode':retrieval.append(dict(node_id=nid,configured_datasets=len(fields.get('datasets') or [])))
        if typ in ('code','codeRun','sandbox'):
            value=str(fields.get('code') or '')
            hints=[name for name,pat in CODE_HINTS.items() if re.search(pat,value,re.I)]
            code.append(dict(node_id=nid,heuristic_hints=hints))
            for hint in hints:
                add('SEC030','high' if hint in ('dynamic_execution','process_or_filesystem') else 'medium',nid,base,
                    f'Code pattern requiring review: {hint}; no code executed.',
                    'Read context and sandbox permissions; distinguish serialization from hidden payloads. Pattern presence is not proof of malicious behavior.')
        if typ=='variableUpdate':stores.append(dict(node_id=nid,kind='conversation_variable_update'))
    # Explicit gap list avoids treating zero pattern hits as proof of security.
    return dict(schema_version='1.0',mode='static_read_only',summary=dict(nodes=len(nodes),edges=len(edges),http_nodes=len(http),model_nodes=len(models),findings=len(findings),priorities=dict(Counter(x['priority'] for x in findings))),
                inventory=dict(http=http,models=models,retrieval=retrieval,code=code,state_writes=stores),
                reference_edges=refs,findings=findings,
                limitations=['No code, URL, expressions or tools in the supplied JSON were executed.',
                             'Reachability is structural and overapproximates conditional execution.',
                             'Model IDs, node names and read-only labels do not prove deployment location, authorization or downstream behavior.',
                             'No complete taint analysis, deobfuscation, malware detection, runtime testing or safety certification.',
                             'Node IDs, hosts and reference names can be organization-sensitive; keep this report restricted until reviewed.'])

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('workflow',type=Path);p.add_argument('--output',type=Path)
    p.add_argument('--policy',type=Path,help='Optional JSON object with allowed_hosts list; absence does not imply public hosts are prohibited.')
    a=p.parse_args()
    try:
        if a.workflow.stat().st_size>50*1024*1024: raise ValueError('JSON exceeds the 50 MiB local parsing limit')
        allowed=None
        if a.policy:
            policy=json.loads(a.policy.read_text(encoding='utf-8-sig'))
            if not isinstance(policy,dict) or not isinstance(policy.get('allowed_hosts'),list) or not all(isinstance(h,str) for h in policy['allowed_hosts']):raise ValueError('allowed_hosts must be a list of host strings')
            allowed={h.lower() for h in policy['allowed_hosts']}
        raw=a.workflow.read_bytes();report=audit(json.loads(raw.decode('utf-8-sig')),allowed_hosts=allowed)
        report['source_sha256']=hashlib.sha256(raw).hexdigest()
        text=json.dumps(report,ensure_ascii=False,indent=2)
        if a.output:
            if a.output.resolve()==a.workflow.resolve():raise ValueError('Report must not overwrite the input')
            a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text+'\n',encoding='utf-8')
            print(json.dumps({'status':'review_required','summary':report['summary'],'report_written':True},ensure_ascii=False))
        else:print(text)
        return 0 # Findings are review evidence, not automatic execution/approval decisions.
    except (ValueError,TypeError,OSError,RecursionError):
        print(json.dumps({'status':'error','message':'Cannot parse input/policy or write output; inspect local files. Raw values suppressed.'}))
        return 2
if __name__=='__main__':raise SystemExit(main())
