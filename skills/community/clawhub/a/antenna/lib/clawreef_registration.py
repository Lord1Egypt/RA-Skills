"""Protected enrollment and non-secret registration recovery for Antenna CLI.

No browser credentials, reusable enrollment secrets, transport changes or key
rotation. The user supplies a one-use code via a hidden prompt or protected stdin.
"""
import contextlib
import fcntl
import getpass
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

UUID=r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

class Registration:
    def __init__(self, cli, service, local):
        self.cli,self.service=cli,service
        self.policy,self.config,self.peer,self.host,self.candidates=local
        self.directory=cli.ROOT/'.clawreef'
        self.path=self.directory/(hashlib.sha256(service.encode()).hexdigest()+'.json')
        self.key_id='ed25519-'+cli.fingerprint(self.peer)
        import clawreef_http
        self.http = clawreef_http

    def fail(self,condition,code,message,exit_code=3,**kw):
        self.cli.fail(condition,code,message,exit_code,**kw)

    def safe_directory(self,create=False):
        if not self.directory.exists() and not self.directory.is_symlink():
            if not create:return False
            self.directory.mkdir(mode=0o700)
        info=self.directory.lstat()
        self.fail(stat.S_ISDIR(info.st_mode) and info.st_uid==os.getuid() and not info.st_mode&0o077,
                  'UNSAFE_LOCAL_STATE','Registration directory must be private and owned by this user.')
        return True

    @contextlib.contextmanager
    def locked(self):
        self.safe_directory(True)
        fd=os.open(self.directory/'.lock',os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW|os.O_NONBLOCK,0o600)
        try:
            info=os.fstat(fd)
            self.fail(stat.S_ISREG(info.st_mode) and info.st_uid==os.getuid() and not info.st_mode&0o077,
                      'UNSAFE_LOCAL_STATE','Unsafe registration lock.')
            fcntl.flock(fd,fcntl.LOCK_EX)
            yield
        finally:os.close(fd)

    def read(self,allow_key_change=False):
        if not self.safe_directory():return None
        try:fd=os.open(self.path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
        except FileNotFoundError:return None
        try:
            info=os.fstat(fd)
            self.fail(stat.S_ISREG(info.st_mode) and info.st_uid==os.getuid() and not info.st_mode&0o077 and info.st_size<=16384,
                      'UNSAFE_LOCAL_STATE','Unsafe registration file.')
            with os.fdopen(fd,'r') as f:fd=None;data=json.load(f)
            self.fail(isinstance(data,dict) and data.get('schema_version')==1 and data.get('service_origin')==self.service and data.get('peer_name')==self.host
                and (allow_key_change or data.get('key_id')==self.key_id) and re.fullmatch(UUID,str(data.get('host_id')))
                and data.get('state') in ('pending','active'), 'STALE_LOCAL_BINDING','Local registration does not match this host/key/service.')
            return data
        finally:
            if fd is not None:os.close(fd)

    def write(self,data):
        # No code, private key, hooks token or other reusable credential belongs here.
        fd,name=tempfile.mkstemp(prefix='.registration-',dir=self.directory)
        try:
            with os.fdopen(fd,'w') as f:
                json.dump(data,f);f.flush();os.fsync(f.fileno())
            os.replace(name,self.path)
            d=os.open(self.directory,os.O_DIRECTORY);os.fsync(d);os.close(d)
        finally:
            if os.path.exists(name):os.unlink(name)

    def context(self,reference=None):
        if reference is None:
            self.fail(len(self.candidates)==1,'SESSION_SELECTION_REQUIRED','Select a receiving conversation with --session.',6)
            reference=self.candidates[0]
        try: _,_,binding=self.policy.resolve(self.config,reference)
        except (ValueError,KeyError,TypeError,OSError):
            raise self.cli.Failure('INVALID_SESSION_CONTEXT','Cannot resolve the selected conversation.',6) from None
        key=binding['canonical_key']
        self.fail(key in self.candidates,'INVALID_SESSION_CONTEXT','Select an existing allowed conversation, not a relay session.',6)
        return key

    def service_peer(self,p):
        return str(p.get('url',p.get('endpoint',''))).rstrip('/') in tuple(self.service+x for x in ('','/registry','/api','/registry/api'))

    def transport_ready(self):
        # Read-only check, no repair, credential copying, peer replacement or sends.
        peers=json.loads((self.cli.ROOT/'antenna-peers.json').read_text())
        matches=[p for p in peers.values() if isinstance(p,dict) and not p.get('self') and
                 self.service_peer(p)]
        self.fail(len(matches)==1 and matches[0].get('auth_mode')=='ed25519-v1',
                  'PAIRING_REQUIRED','Pair this host with the selected ClawReef service first.')
        p=matches[0]
        for field in ('token_file','signing_public_key_file'):
            value=p.get(field)
            self.fail(isinstance(value,str) and bool(value),'PAIRING_REQUIRED','ClawReef peer credentials are incomplete.')
            path=Path(value);path=path if path.is_absolute() else self.cli.ROOT/path
            self.fail(path.is_file() and path.stat().st_size>0,'PAIRING_REQUIRED','ClawReef peer credentials are unavailable.')

    def request(self,operation,host_id,body=None,operation_id='',actor_id='',query='',raw_result=False):
        path=self.cli.CONTRACT['api_base']+'/'+operation
        raw=b'' if body is None else json.dumps(body,ensure_ascii=True,separators=(',',':')).encode()
        fields=dict(audience=self.service,method='GET' if body is None else 'POST',path=path,query=query,host_id=host_id,
            actor_id=actor_id,key_id=self.key_id,timestamp=self.http.timestamp(),nonce=self.http.nonce(),
            idempotency_key=operation_id,body_sha256=hashlib.sha256(raw).hexdigest())
        key=self.peer.get('signing_private_key_file')
        self.fail(isinstance(key,str) and bool(key),'SIGNING_KEY_REQUIRED','A protected existing host signing key is required.')
        key=Path(key);key=key if key.is_absolute() else self.cli.ROOT/key
        try:sig=self.http.sign(fields,key,self.key_id)
        except self.http.SigningError:
            raise self.cli.Failure('SIGNING_KEY_REQUIRED','Unable to use the reviewed protected signing key.',3) from None
        headers=self.http.headers(fields,sig);headers['Accept']='application/json'
        if body is not None:headers['Content-Type']='application/json'
        req=urllib.request.Request(self.service+path+('?'+query if query else ''),data=raw if body is not None else None,method=fields['method'],headers=headers)
        opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),self.cli.NoRedirect())
        try:
            try:response=opener.open(req,timeout=15)
            except urllib.error.HTTPError as e:response=e
            with response:
                status=response.status;result_raw=response.read(65537)
            self.fail(len(result_raw)<=65536,'INVALID_RESPONSE','Service response exceeds the supported size.',5)
            try:result=json.loads(result_raw)
            except (ValueError,UnicodeError):raise self.cli.Failure('INVALID_RESPONSE','Expected a supported service response.',5) from None
            self.fail(isinstance(result,dict) and result.get('schema_version')==1 and type(result.get('ok')) is bool,
                      'INVALID_RESPONSE','Expected a supported service response.',5)
            if not (status==200 and result['ok']):
                allowed={'REPORT_NOT_FOUND','REPORT_ALREADY_OPEN','REPORT_CONFLICT','REPORT_CLOSED','REPORT_RATE_LIMIT','INVALID_REPORT_TEXT','MEMBERSHIP_REQUIRED','NOT_ENROLLED','HOST_REVOKED','SIGNATURE_INVALID','SIGNATURE_EXPIRED','CAPABILITY_DENIED',
                    'INVALID_ENROLLMENT_CODE','GRANT_EXPIRED','GRANT_USED','GRANT_CANCELLED','REPLAY_REJECTED',
                    'INVALID_QUERY','INVALID_PATH','INVALID_GET','STALE_BINDING','DESTINATION_CONFLICT','GROUP_NOT_FOUND','SLUG_EXISTS','INVALID_GROUP_FIELDS','INVALID_THEMES','ACTOR_REQUIRED','REVIEW_CHANGED','IDEMPOTENCY_CONFLICT','OPERATION_EXPIRED','PAIRING_REQUIRED','OPERATION_IN_PROGRESS'}
                code=result.get('code');code=code if code in allowed else 'SERVICE_ERROR'
                raise self.cli.Failure(code,code.replace('_',' ').capitalize()+'.',4 if status==403 else 5 if status>=500 else 3,
                    retryable=status in (429,502,503,504))
            if raw_result:
                data=result.get('data')
                self.fail(isinstance(data,dict) and self.relay_matches(data.get('relay')),'INVALID_RESPONSE','Service relay identity does not match local pairing.',5)
                return {k:v for k,v in data.items() if k!='relay'}
            return self.valid_response(result.get('data'),host_id)
        except (urllib.error.URLError,TimeoutError,OSError):
            raise self.cli.Failure('NETWORK_ERROR','Enrollment state may require recovery; retry the same operation or use enroll --recover.',5,retryable=True) from None

    def valid_response(self,data,host_id):
        self.fail(isinstance(data,dict) and data.get('host_id')==host_id and data.get('key_id')==self.key_id
            and data.get('peer_name')==self.host and data.get('state')=='active' and type(data.get('revision')) is int,
            'INVALID_RESPONSE','Service identity does not match this host.',5)
        caps=data.get('capabilities')
        self.fail(isinstance(caps,dict) and set(caps)=={'groups.join','groups.post','groups.create'} and
            all(v in ('allow','deny') for v in caps.values()),'INVALID_RESPONSE','Invalid host permissions.',5)
        actors=data.get('actors',[data.get('actor')])
        self.fail(isinstance(actors,list) and len(actors)<=1000,'INVALID_RESPONSE','Invalid conversation bindings.',5)
        safe=[]
        for a in actors:
            if a is None:continue
            self.fail(isinstance(a,dict) and re.fullmatch(UUID,str(a.get('id'))) and type(a.get('revision')) is int
                and isinstance(a.get('canonical_session_key'),str),'INVALID_RESPONSE','Invalid conversation binding.',5)
            safe.append({k:a[k] for k in ('id','canonical_session_key','revision')})
        relay_match=self.relay_matches(data.get('relay'))
        return {'host_id':host_id,'peer_name':self.host,'key_id':self.key_id,'state':'active','revision':data['revision'],
                'capabilities':caps,'actors':safe,'authority_scope':'host','remote_checked':True,'local_relay_key_matches':relay_match}

    def relay_matches(self,relay):
        self.fail(isinstance(relay,dict) and isinstance(relay.get('peer_name'),str) and
            re.fullmatch(r'ed25519-sha256:[0-9a-f]{64}',str(relay.get('signing_key_id'))),
            'INVALID_RESPONSE','Invalid service relay identity.',5)
        relay_match=False
        peers=json.loads((self.cli.ROOT/'antenna-peers.json').read_text())
        remote=peers.get(relay['peer_name'],{})
        if isinstance(remote,dict) and remote.get('auth_mode')=='ed25519-v1' and isinstance(remote.get('signing_public_key_file'),str):
            path=Path(remote['signing_public_key_file']);path=path if path.is_absolute() else self.cli.ROOT/path
            try:
                public=subprocess.run(['openssl','pkey','-pubin','-in',str(path),'-outform','DER'],capture_output=True,timeout=10)
                relay_match=(public.returncode==0 and 'ed25519-sha256:'+hashlib.sha256(public.stdout).hexdigest()==relay['signing_key_id'])
            except (OSError,subprocess.TimeoutExpired):pass
        return relay_match

    def status(self,opts):
        state=self.read()
        self.fail(state is not None,'NOT_ENROLLED','No local enrollment for this service.',3)
        if opts.local_only:
            return 'LOCAL_STATE','Local registration only; remote permissions are not verified.',{
                'host_id':state['host_id'],'state':state['state'],'service_origin':self.service,'remote_checked':False}
        return 'OK','Current host permissions verified.',self.request(opts.command,state['host_id'])

    def enroll(self,opts):
        self.transport_ready()
        with self.locked():
            state=self.read(allow_key_change=not opts.recover)
            if opts.recover:
                self.fail(state is not None,'NOT_ENROLLED','No interrupted registration is available to recover.')
                key=self.context(state['canonical_session_key'])
                result=self.request('status',state['host_id'])
            else:
                key=self.context(opts.session)
                if opts.code_stdin:
                    code=sys.stdin.readline(257).strip()
                else:
                    self.fail(not opts.json and sys.stdin.isatty(),'PROTECTED_CODE_REQUIRED','Use --code-stdin with protected input in non-interactive mode.',2)
                    code=getpass.getpass('One-use ClawReef setup code: ').strip()
                match=re.fullmatch(r'cr1\.('+UUID+r')\.('+UUID+r')\.([A-Za-z0-9_-]{43})',code)
                self.fail(match,'INVALID_ENROLLMENT_CODE','Invalid enrollment code.')
                host_id,grant_id=match.group(1,2)
                self.fail(state is None or state['host_id']==host_id,'STALE_LOCAL_BINDING','Another Registry host is already bound locally.')
                operation_id=state['operation_id'] if state and state.get('grant_id')==grant_id else self.http.operation_id()
                self.fail(not state or state.get('grant_id')!=grant_id or state['canonical_session_key']==key,
                          'STALE_LOCAL_BINDING','Retry must use the original canonical conversation.')
                state={'schema_version':1,'service_origin':self.service,'peer_name':self.host,'host_id':host_id,'key_id':self.key_id,
                    'state':'pending','grant_id':grant_id,'operation_id':operation_id,'canonical_session_key':key}
                self.write(state)
                endpoint=str(self.peer.get('url',self.peer.get('endpoint',''))).rstrip('/')
                self.fail(bool(endpoint),'INVALID_LOCAL_STATE','Local self endpoint is missing.')
                result=self.request('enrollments/redeem',host_id,{'code':code,'canonical_session_key':key,
                    'peer_name':self.host,'endpoint':endpoint},operation_id)
            self.fail(result['local_relay_key_matches'],'PAIRING_REQUIRED','The locally pinned ClawReef relay key does not match. Enrollment may be recorded; fix pairing then use enroll --recover.')
            matches=[a for a in result['actors'] if a['canonical_session_key']==key]
            self.fail(len(matches)==1,'STALE_BINDING','Service has no unique matching canonical conversation.',6)
            # Resolve again after network work. Alias movement cannot redirect it.
            self.context(key)
            state.update(state='active',actor_id=matches[0]['id'],actor_revision=matches[0]['revision'])
            self.write(state)
            return 'ENROLLED','Host enrolled; standing permissions verified.',result
