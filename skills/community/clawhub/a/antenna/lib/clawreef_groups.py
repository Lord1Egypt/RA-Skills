"""Signed host group operations with pinned retries and existing route schema.

The journal holds non-secret operation metadata only, never message bodies.
A server success and local route write are deliberately separate outcomes.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile
import urllib.parse

UUID=r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
ALIAS=r'[a-z0-9][a-z0-9._-]{0,63}'

def private_json(r,path,default=None):
    try:fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    except FileNotFoundError:return default
    with os.fdopen(fd) as f:
        st=os.fstat(f.fileno())
        r.fail(stat.S_ISREG(st.st_mode) and st.st_uid==os.getuid() and st.st_mode&0o777==0o600 and st.st_size<=1048576,
            'UNSAFE_LOCAL_STATE','Unsafe local group state.')
        return json.load(f)

def atomic(path,data):
    fd,tmp=tempfile.mkstemp(prefix='.clawreef-group-',dir=path.parent)
    try:
        with os.fdopen(fd,'w') as f:json.dump(data,f,ensure_ascii=True);f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
        fd=os.open(path.parent,os.O_DIRECTORY);os.fsync(fd);os.close(fd)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

def binding(r,reference):
    # Reload, not the snapshot held at command start. Resolve aliases before and
    # after network waits; pending work must not follow a changed alias revision.
    r.policy,r.config,r.peer,r.host,r.candidates=r.cli.local_state()
    key=r.context(reference)
    _,_,b=r.policy.resolve(r.config,reference)
    r.fail(b['canonical_key']==key,'STALE_BINDING','Receiving conversation changed.',6)
    return b

def check_binding(r,b):
    try:current=binding(r,b['original_reference'])
    except r.cli.Failure:
        raise r.cli.Failure('STALE_BINDING','Saved receiving binding is no longer valid; no redirection performed.',6) from None
    r.fail(current==b,'STALE_BINDING','Saved receiving binding changed; no redirection performed.',6)

def routes(r,data,alias=None,expected_key=None):
    gid=data.get('group_id')
    r.fail(isinstance(gid,str) and re.fullmatch(UUID,gid),'INVALID_RESPONSE','Invalid group identity.',5)
    r.fail(data.get('membership') in ('active','absent'),'INVALID_RESPONSE','Invalid membership state.',5)
    routefile=r.cli.ROOT/'antenna-public-groups.json'
    # Serialize with legacy install/refresh/remove (same lock in shell adapter).
    import fcntl
    fd=os.open(str(routefile)+'.lock',os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW|os.O_NONBLOCK,0o600)
    try:
        st=os.fstat(fd);r.fail(stat.S_ISREG(st.st_mode) and st.st_uid==os.getuid() and not st.st_mode&0o077,'UNSAFE_LOCAL_STATE','Unsafe route lock.')
        fcntl.flock(fd,fcntl.LOCK_EX)
        current=private_json(r,routefile,{})
        r.fail(isinstance(current,dict),'UNSAFE_LOCAL_STATE','Invalid existing group routes.')
        for k,v in current.items():
            r.fail(re.fullmatch(ALIAS,k) and isinstance(v,dict) and set(v)=={'group_id','name','relay_peer'} and isinstance(v['group_id'],str) and re.fullmatch(UUID,v['group_id']) and isinstance(v['name'],str) and 0<len(v['name'])<=128 and isinstance(v['relay_peer'],str) and re.fullmatch(ALIAS,v['relay_peer']), 'UNSAFE_LOCAL_STATE','Invalid existing group routes.')
        old=[k for k,v in current.items() if v['group_id']==gid]
        r.fail(len(old)<=1,'UNSAFE_LOCAL_STATE','Duplicate local routes for this group.')
        if data['membership']=='absent':
            r.fail(data.get('route') is None,'INVALID_RESPONSE','Absent membership must not include a route.',5)
            # Do not remove a same-ID route belonging to a different relay.
            if old:
                peers=json.loads((r.cli.ROOT/'antenna-peers.json').read_text())
                relay=peers.get(current[old[0]]['relay_peer'],{})
                r.fail(r.service_peer(relay),'ROUTE_CONFLICT','Existing route belongs to another relay.')
                del current[old[0]];atomic(routefile,current)
            return {'server_state':'membership_absent','local_state':'removed' if old else 'absent','group_id':gid}
        incoming=data.get('route')
        r.fail(isinstance(incoming,dict) and len(incoming)==1,'INVALID_RESPONSE','Expected one route.',5)
        name,value=next(iter(incoming.items()))
        r.fail(re.fullmatch(ALIAS,name) and isinstance(value,dict) and set(value)=={'group_id','name','relay_peer'} and value['group_id']==gid and isinstance(value['name'],str) and 0<len(value['name'])<=128 and isinstance(value['relay_peer'],str) and re.fullmatch(ALIAS,value['relay_peer']),'INVALID_RESPONSE','Invalid route payload.',5)
        peers=json.loads((r.cli.ROOT/'antenna-peers.json').read_text());relay=peers.get(value['relay_peer'],{})
        r.fail(relay.get('auth_mode')=='ed25519-v1' and r.service_peer(relay),'PAIRING_REQUIRED','Route must use the paired service.')
        canonical=data.get('canonical_session_key')
        if canonical is not None:binding(r,canonical)
        if expected_key is not None:r.fail(canonical==expected_key,'DESTINATION_CONFLICT','Current group destination differs from the requested conversation.',6)
        if old:r.fail(current[old[0]]['relay_peer']==value['relay_peer'],'ROUTE_CONFLICT','Existing route uses a different relay.')
        name=old[0] if old else (alias or name)
        r.fail(re.fullmatch(ALIAS,name),'INVALID_ALIAS','Invalid local group alias.',2)
        r.fail(name not in current or name in old,'ROUTE_CONFLICT','Local alias already belongs to another group.')
        current[name]=value;atomic(routefile,current)
        return {'server_state':'membership_active','local_state':'installed','group_id':gid,'alias':name}
    finally:os.close(fd)

def run(r,o):
    action=o.group_command
    r.fail(action in ('browse','themes','show','create','join','leave','reconcile','resume'),'INVALID_ARGUMENT','Choose a supported group command.',2)
    r.fail(not o.request and not o.local_only,'INVALID_ARGUMENT','Group commands use signed host requests.',2)
    r.fail(action in ('create','join') or not o.session,'INVALID_ARGUMENT','--session applies to create/join.',2)
    r.fail(action in ('create','join','reconcile') or not o.alias,'INVALID_ARGUMENT','--alias applies to create/join/reconcile.',2)
    r.fail(action=='create' or not (o.name or o.slug or o.description),'INVALID_ARGUMENT','Creation fields apply only to create.',2)
    r.fail(action in ('create','browse') or not o.theme,'INVALID_ARGUMENT','Theme options apply to create/browse.',2)
    r.fail(action in ('browse','themes') or not (o.query or o.after),'INVALID_ARGUMENT','Filters apply to browse.',2)
    if action=='create':
        r.fail(isinstance(o.name,str) and 0<len(o.name.strip())<=128 and isinstance(o.slug,str) and re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}',o.slug) and all(re.fullmatch(UUID,t) for t in o.theme),'INVALID_ARGUMENT','Create requires a valid --name, --slug and optional theme UUIDs.',2)
    if o.alias:r.fail(re.fullmatch(ALIAS,o.alias),'INVALID_ALIAS','Invalid local alias.',2)
    if action in ('show','join','leave','reconcile'):r.fail(o.group_id and re.fullmatch(UUID,o.group_id),'INVALID_GROUP','Use the exact group UUID.',2)
    if action in ('browse','themes','create'):r.fail(o.group_id is None,'INVALID_ARGUMENT','Unexpected group argument.',2)
    with r.locked():
        state=r.read();r.fail(state and state['state']=='active','NOT_ENROLLED','An active local registration is required.')
        host=state['host_id'];r.transport_ready()
        def request(path,body=None,op='',actor='',query=''):
            return r.request(path,host,body,op,actor,query,raw_result=True)
        if action in ('browse','themes','show'):
            query=''
            if action=='browse':
                r.fail(len(o.theme)<=1,'INVALID_ARGUMENT','Browse accepts one theme filter.',2)
                params={k:v for k,v in {'q':o.query,'theme':o.theme[0] if o.theme else None,'after':o.after}.items() if v}
                query=urllib.parse.urlencode(sorted(params.items()),quote_via=urllib.parse.quote,safe='-._~')
            if action=='themes':
                r.fail(not o.query,'INVALID_ARGUMENT','Themes supports only --after.',2)
                query=urllib.parse.urlencode({'after':o.after}) if o.after else ''
            data=request('themes' if action=='themes' else 'groups'+('/'+o.group_id if action=='show' else ''),query=query)
            return 'OK','Group information retrieved.',data
        if action=='reconcile':
            data=request('groups/'+o.group_id+'/route')
            return 'RECONCILED','Current membership and local route reconciled.',routes(r,data,o.alias)
        op=None;path=None
        if action=='resume':
            r.fail(o.group_id and re.fullmatch(r'\d{8}T\d{6}Z\.'+UUID,o.group_id),'INVALID_OPERATION','Use the saved operation ID.',2)
            path=r.directory/('group-'+hashlib.sha256((r.service+o.group_id).encode()).hexdigest()+'.json')
            op=private_json(r,path)
            r.fail(isinstance(op,dict) and op.get('schema_version')==1 and op.get('service')==r.service and op.get('host_id')==host and op.get('key_id')==r.key_id and op.get('operation_id')==o.group_id,'INVALID_OPERATION','No matching saved group operation.')
        else:
            body={};b=None;actor=''
            if action in ('create','join'):
                ref=o.session or state['canonical_session_key'];b=binding(r,ref)
                a=request('actors',{'canonical_session_key':b['canonical_key']},r.http.operation_id()).get('actor')
                r.fail(isinstance(a,dict) and re.fullmatch(UUID,str(a.get('id'))) and a.get('canonical_session_key')==b['canonical_key'] and type(a.get('revision')) is int,'INVALID_RESPONSE','Invalid receiving actor.',5)
                actor=a['id'];body={'canonical_session_key':b['canonical_key'],'actor_revision':a['revision']}
                if action=='create':
                    r.fail(isinstance(o.name,str) and 0<len(o.name.strip())<=128 and isinstance(o.slug,str) and re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}',o.slug),'INVALID_ARGUMENT','Create requires a valid --name and --slug.',2)
                    body.update(name=o.name,slug=o.slug,description=o.description,themeIds=o.theme,joinMode='open')
            op={'schema_version':1,'service':r.service,'host_id':host,'key_id':r.key_id,'operation_id':r.http.operation_id(),
                'action':action,'group_id':o.group_id,'body':body,'binding':b,'actor_id':actor,'alias':o.alias}
            path=r.directory/('group-'+hashlib.sha256((r.service+op['operation_id']).encode()).hexdigest()+'.json');atomic(path,op)
        try:
            b=op['binding']
            if b:check_binding(r,b)
            if 'result' not in op:
                target='groups' if op['action']=='create' else 'groups/'+op['group_id']+'/'+op['action']
                result=request(target,op['body'],op['operation_id'],op['actor_id'])
                r.fail(isinstance(result.get('group_id'),str) and re.fullmatch(UUID,result['group_id']),'INVALID_RESPONSE','Invalid group result.',5)
                op['result']=result;atomic(path,op)
            gid=op['result']['group_id'];data=request('groups/'+gid+'/route')
            if b:check_binding(r,b)
            if op['action']=='leave':r.fail(data.get('membership')=='absent','MEMBERSHIP_CHANGED','Host has rejoined since that leave; local route retained.')
            outcome=routes(r,data,op['alias'],b['canonical_key'] if b else None)
            op['local_result']=outcome;atomic(path,op)
            return 'GROUP_COMPLETE','Server operation and local route reconciled.',dict(outcome,operation_id=op['operation_id'])
        except (r.cli.Failure,OSError,ValueError,KeyError,TypeError) as e:
            code=e.code if isinstance(e,r.cli.Failure) else 'LOCAL_ROUTE_FAILED'
            raise r.cli.Failure(code,'Group operation is incomplete; inspect the saved result and resolve the reported '+code.lower().replace('_',' ')+'.',e.exit_code if isinstance(e,r.cli.Failure) else 3,
                data={'operation_id':op['operation_id'],'server_state':'recorded' if 'result' in op else 'unconfirmed','group_id':op.get('result',{}).get('group_id'),'local_state':'not_reconciled'},
                next_action=('antenna clawreef groups reconcile '+op['result']['group_id'] if code=='STALE_BINDING' and 'result' in op else 'antenna clawreef groups resume '+op['operation_id'])+' --service '+r.service,retryable=code not in ('STALE_BINDING','CAPABILITY_DENIED','HOST_REVOKED','OPERATION_EXPIRED','IDEMPOTENCY_CONFLICT')) from None
