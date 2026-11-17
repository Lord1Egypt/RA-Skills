"""Local, bounded Antenna state inventory. No gateway calls or repairs.

Backup and readiness share session-policy validation with Doctor. Paths from an
archive are never used as unrestricted restore destinations.
"""
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import stat
import subprocess

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'lib'))
import session_policy as policy
MAX_FILE = 128 * 1024 * 1024
MAX_TOTAL = 512 * 1024 * 1024
MAX_MEMBERS = 10000
FIXED = ('antenna-config.json', 'antenna-peers.json', 'antenna-lists.json',
         'antenna-public-groups.json', 'antenna-ratelimit.json', 'state/antenna-replay.json',
         'secrets/antenna-exchange.agekey', 'secrets/antenna-exchange.agepub')
KEY_FIELDS = ('token_file', 'peer_secret_file', 'signing_private_key_file', 'signing_public_key_file')
PROTECTED = {'bin','lib','scripts','tests','references','agent','agent-runtime','.git',
             'secrets','keys','.clawreef','state'}


class StateError(ValueError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def need(ok, code='INVALID_STATE', message='State validation failed; inspect local configuration with Doctor.'):
    if not ok:
        raise StateError(code, message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def decode(raw):
    try:
        return policy.decode(raw)
    except (ValueError, UnicodeError):
        raise StateError('INVALID_JSON', 'Invalid or duplicate JSON fields; contents withheld.') from None


def encode(data):
    return (json.dumps(data, ensure_ascii=True, indent=2) + '\n').encode()


def lexical(path):
    return Path(os.path.abspath(path))


def safe_path(path, missing=False, private=False, limit=None):
    """Reject links/special files and unsafe parents, including absent targets."""
    path = lexical(path)
    sealed = False
    for parent in reversed(path.parents):
        try:
            st = parent.lstat()
        except FileNotFoundError:
            continue
        # Root-owned sticky /tmp is safe for a private child; other writable
        # ancestors are not. This is not a hostile same-user guarantee.
        need(stat.S_ISDIR(st.st_mode) and not parent.is_symlink() and
             st.st_uid in (0, os.getuid()) and
             (sealed or not st.st_mode & 0o022 or (st.st_uid == 0 and st.st_mode & stat.S_ISVTX)),
             'UNSAFE_PATH', 'Unsafe ancestor; no files changed.')
        sealed = sealed or (st.st_uid == os.getuid() and not st.st_mode & 0o077)
    try:
        st = path.lstat()
    except FileNotFoundError:
        need(missing, 'MISSING_STATE', 'Required state file is missing.')
        return None
    need(stat.S_ISREG(st.st_mode) and st.st_uid == os.getuid() and st.st_nlink == 1 and
         (not st.st_mode & 0o077 if private else (sealed or not st.st_mode & 0o022)),
         'UNSAFE_PATH', 'State must be an owned regular file with safe permissions and no links.')
    need(st.st_size <= (MAX_FILE if limit is None else limit), 'SIZE_LIMIT', 'State exceeds the per-file size limit.')
    return st


def identity(st):
    return (st.st_dev,st.st_ino,st.st_mode,st.st_uid,st.st_gid,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns)


def read_file(path, private=False):
    before = safe_path(path, private=private)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as f:
        need(identity(os.fstat(f.fileno())) == identity(before), 'STATE_CHANGED', 'State changed during inspection.')
        raw = f.read(MAX_FILE + 1)
        after = os.fstat(f.fileno())
    need(len(raw) <= MAX_FILE and identity(before) == identity(after) and identity(Path(path).lstat()) == identity(after),
         'STATE_CHANGED', 'State changed during inspection.')
    return raw


def relative(name):
    need(isinstance(name, str) and len(name) <= 1024 and not any(ord(c)<32 or ord(c)==127 for c in name), 'UNSAFE_PATH', 'Invalid state path.')
    p = Path(name)
    need(name and not p.is_absolute() and p.as_posix() == name and '..' not in p.parts and '.' not in p.parts,
         'UNSAFE_PATH', 'Invalid relative state path.')
    return p


def within(path, root):
    try: path.relative_to(root);return True
    except ValueError:return False


def source_path(root, value):
    need(isinstance(value, str) and value and not value.startswith(('${', 'secret:', 'env:')), 'UNSUPPORTED_REFERENCE', 'Unsupported file reference; values withheld.')
    p = Path(value)
    need('..' not in p.parts, 'UNSAFE_PATH', 'Parent traversal in file reference is unsupported.')
    if not p.is_absolute(): relative(value)
    return lexical(p if p.is_absolute() else root / p)


def destination(root, value, credential=False, public=False):
    p = source_path(root, value)
    try: name = p.relative_to(root).as_posix()
    except ValueError:
        # Never trust archived external locations as write authority.
        if credential and public: return 'keys/'+digest(str(p).encode())+'.ed25519.pem'
        return ('secrets/restored-' + digest(str(p).encode()) if credential else 'antenna-inbox.json')
    rel = relative(name)
    if credential:
        need(len(rel.parts) == 2 and rel.parts[0] in ('secrets','keys'), 'UNSUPPORTED_REFERENCE', 'Internal credentials must be in Antenna secrets/ or keys/.')
    else:
        need(rel.parts[0] not in PROTECTED and not rel.parts[0].startswith('.') and
             (name == 'antenna-inbox.json' or (name not in FIXED and rel.suffix == '.json' and
              not name.endswith('.example.json'))), 'UNSAFE_PATH', 'Inbox conflicts with protected files.')
    return name


def config_valid(config):
    try:
        policy.validate(config)
        for field in ('local_agent_id','relay_agent_id'):
            value=config.get(field,'antenna' if field=='relay_agent_id' else 'agent')
            need(isinstance(value,str) and re.fullmatch(r'[A-Za-z0-9_-]+',value))
        for field in ('max_message_length','log_max_size_bytes'):
            if field in config: need(type(config[field]) is int and config[field] > 0)
        security = config.get('security', {})
        need(isinstance(security,dict))
        for key, maximum in (('max_message_age_seconds',3600),('max_future_skew_seconds',300)):
            if key in security: need(type(security[key]) is int and 0 <= security[key] <= maximum)
    except (ValueError, TypeError, KeyError, AttributeError):
        raise StateError('INVALID_CONFIG','Configuration/session policy is invalid; values withheld.') from None


def references(root, config, peers):
    refs = {'antenna-config.json': root/'antenna-config.json', 'antenna-peers.json': root/'antenna-peers.json'}
    queue = destination(root, config.get('inbox_queue_path','antenna-inbox.json'))
    refs[queue] = source_path(root, config.get('inbox_queue_path','antenna-inbox.json'))
    for peer in peers.values():
        need(isinstance(peer,dict))
        for field in KEY_FIELDS:
            if field not in peer: continue
            name = destination(root,peer[field],True,public=field=='signing_public_key_file')
            path = source_path(root,peer[field])
            need(name not in refs or refs[name] == path, 'PATH_COLLISION','State roles collide.')
            refs[name] = path
    for name in FIXED:
        need(name not in refs or refs[name] == root/name, 'PATH_COLLISION','State roles collide.')
        refs[name] = root/name
    return refs,queue


def owned_name(name):
    p=relative(name)
    if len(p.parts)!=2: return False
    folder,base=p.parts
    if folder=='state': return base=='antenna-replay.json'
    if folder=='.clawreef': return bool(re.fullmatch(r'[0-9a-f]{64}\.json',base))
    if folder=='keys': return bool(re.fullmatch(r'[0-9a-f]{64}\.ed25519\.pem',base))
    if folder=='secrets': return bool(re.fullmatch(r'(antenna-signing-(private|public)\.pem|antenna-exchange\.(agekey|agepub)|antenna-peer-[A-Za-z0-9_.-]+\.secret|hooks_token_[A-Za-z0-9_.-]+|restored-[0-9a-f]{64})',base))
    return False


def inventory(root, tolerant=False):
    root=lexical(root)
    try: config=decode(read_file(root/'antenna-config.json'))
    except (StateError,OSError):
        if not tolerant: raise
        config={}
    try: peers=decode(read_file(root/'antenna-peers.json'))
    except (StateError,OSError):
        if not tolerant: raise
        peers={}
    if not isinstance(config,dict):
        need(tolerant);config={}
    if not isinstance(peers,dict):
        need(tolerant);peers={}
    try:
        refs,queue=references(root,config,peers)
    except (StateError,TypeError,AttributeError):
        if not tolerant: raise
        # Damaged reference fields cannot authorize arbitrary current-file deletion.
        refs,queue=references(root,{}, {})
    for folder in ('secrets','keys','state','.clawreef'):
        d=root/folder
        if not d.exists() and not d.is_symlink(): continue
        st=d.lstat()
        need(stat.S_ISDIR(st.st_mode) and st.st_uid==os.getuid() and not st.st_mode&0o022,'UNSAFE_PATH','Unsafe state directory.')
        for p in d.iterdir():
            name=p.relative_to(root).as_posix()
            if p.name.endswith('.lock') or p.name=='.lock': continue
            need(name in refs or owned_name(name),'UNKNOWN_STATE','Unrecognized operational file; inventory cannot safely include or remove it.')
            refs[name]=p
    need(len(refs)<=MAX_MEMBERS,'SIZE_LIMIT','Too many state files.')
    return refs,config,peers,queue


def command(args, raw=None):
    try:
        p=subprocess.run(args,input=raw,capture_output=True,timeout=10)
        need(p.returncode==0,'INVALID_KEY','Key validation failed; values withheld.')
        return p.stdout
    except (OSError,subprocess.TimeoutExpired):
        raise StateError('DEPENDENCY','Required local key validator unavailable.') from None


def validate_snapshot(root, files):
    config=decode(files['antenna-config.json']);peers=decode(files['antenna-peers.json'])
    config_valid(config)
    need(isinstance(config.get('install_path'),str) and lexical(config['install_path'])==root,
         'INSTALL_PATH_MISMATCH','Snapshot install_path does not match its source installation.')
    need(isinstance(peers,dict) and sum(isinstance(p,dict) and p.get('self') is True for p in peers.values())==1)
    refs,queue=references(root,config,peers)
    required={'antenna-config.json','antenna-peers.json'}
    fingerprints={}
    for name,p in peers.items():
        need(isinstance(name,str) and re.fullmatch(r'[A-Za-z0-9_.-]+',name) and isinstance(p,dict))
        need(isinstance(p.get('url'),str) and p['url'].startswith(('http://','https://')))
        mode=p.get('auth_mode','unpaired' if p.get('self') else None);need(mode in ('ed25519-v1','plaintext-legacy','unpaired'))
        need(mode!='unpaired' or p.get('self') is True)
        fields=['token_file']+(['signing_public_key_file'] if mode=='ed25519-v1' else ['peer_secret_file'])
        if p.get('self') and mode=='ed25519-v1': fields+=['signing_private_key_file']
        for field in fields: need(field in p)
        for field in KEY_FIELDS:
            if field not in p: continue
            logical=destination(root,p[field],True,public=field=='signing_public_key_file');required.add(logical)
            need(logical in files and files[logical], 'MISSING_CREDENTIAL','Referenced credential is missing.')
        if mode=='ed25519-v1':
            pub=files[destination(root,p['signing_public_key_file'],True,public=True)]
            der=command(['openssl','pkey','-pubin','-outform','DER'],pub)
            need(der.startswith(bytes.fromhex('302a300506032b6570032100')) and len(der)==44,'INVALID_KEY','Expected Ed25519 public key.')
            fingerprints[name]='ed25519-sha256:'+digest(der)
            if p.get('self'):
                private=files[destination(root,p['signing_private_key_file'],True)]
                need(command(['openssl','pkey','-passin','pass:','-pubout','-outform','DER'],private)==der,'INVALID_KEY','Signing key pair differs.')
        if 'peer_secret_file' in p:
            need(re.fullmatch(rb'[0-9a-f]{64}\s*',files[destination(root,p['peer_secret_file'],True)]),'INVALID_KEY','Invalid peer secret.')
    exchange='secrets/antenna-exchange.'
    if exchange+'agekey' in files or exchange+'agepub' in files:
        need(exchange+'agekey' in files and exchange+'agepub' in files,'INVALID_KEY','Incomplete exchange identity.')
        pub=command(['age-keygen','-y'],files[exchange+'agekey']).strip()
        need(pub==files[exchange+'agepub'].strip(),'INVALID_KEY','Exchange key pair differs.')
        self_peer=next(p for p in peers.values() if p.get('self'))
        need(self_peer.get('exchange_public_key',pub.decode())==pub.decode(),'INVALID_KEY','Exchange pin differs.')
    else:
        need(not any(p.get('exchange_public_key') for p in peers.values()),'MISSING_CREDENTIAL','Exchange identity files missing.')
    if queue in files:
        try:
            items=policy.validate_queue(decode(files[queue]))
            need(all(i.get('status') in ('pending','approved','denied','delivered','failed') for i in items))
        except (ValueError,TypeError,KeyError): raise StateError('INVALID_INBOX','Inbox schema invalid.') from None
    for name,raw in files.items():
        need(name in refs or owned_name(name),'UNKNOWN_STATE','Archive contains an unknown state role.')
        if name=='state/antenna-replay.json':
            v=decode(raw);need(isinstance(v,dict) and set(v)=={'entries'} and isinstance(v['entries'],list))
            for e in v['entries']:
                need(isinstance(e,dict) and set(e)=={'id','peer','seen'} and isinstance(e['peer'],str) and
                     isinstance(e['id'],str) and re.fullmatch(r'[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}',e['id']) and type(e['seen']) is int and e['seen']>=0)
        elif name=='antenna-ratelimit.json':
            v=decode(raw);need(isinstance(v,dict) and all(isinstance(a,list) and all(type(n) is int and n>=0 for n in a) for a in v.values()))
        elif name in ('antenna-lists.json','antenna-public-groups.json'):
            v=decode(raw);need(isinstance(v,dict))
            for k,e in v.items():
                need(isinstance(k,str) and bool(k))
                if name=='antenna-lists.json': need(isinstance(e,list) and all(isinstance(i,dict) and isinstance(i.get('peer'),str) for i in e))
                else: need(isinstance(e,dict) and all(isinstance(e.get(f),str) for f in ('group_id','name','relay_peer')))
        elif name.startswith('.clawreef/'):
            v=decode(raw);need(isinstance(v,dict) and v.get('schema_version')==1 and v.get('state') in ('pending','active') and
                isinstance(v.get('service_origin'),str) and digest(v['service_origin'].encode())+'.json'==Path(name).name and
                v.get('peer_name') in fingerprints and v.get('key_id')==fingerprints[v['peer_name']] and
                isinstance(v.get('host_id'),str) and re.fullmatch(r'[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}',v['host_id']))
    need(required<=files.keys(),'MISSING_STATE','Required archive state missing.')
    return config,peers,queue,fingerprints


def capture(root, tolerant=False):
    refs,config,peers,queue=inventory(root,tolerant)
    files={}; stamps={}; total=0
    for name,path in refs.items():
        info=safe_path(path,missing=True,private=(name.startswith('.clawreef/') or (name.startswith('secrets/') and not name.endswith(('.agepub','public.pem')))))
        stamps[str(path)]=None if info is None else (info.st_ino,info.st_size,info.st_mtime_ns,info.st_ctime_ns)
        if info is not None:
            total+=info.st_size
            need(total<=MAX_TOTAL,'SIZE_LIMIT','State exceeds total archive limit.')
            files[name]=read_file(path)
    need(sum(map(len,files.values()))<=MAX_TOTAL,'SIZE_LIMIT','State exceeds total archive limit.')
    if not tolerant: validate_snapshot(root,files)
    return refs,files,stamps


def quiescent():
    """Conservative Linux local process check; never contacts/stops a gateway."""
    need(Path('/proc').is_dir(),'GATEWAY_UNKNOWN','Cannot establish stopped gateway; Linux /proc is required.')
    try:
        for p in Path('/proc').iterdir():
            if not p.name.isdigit() or int(p.name)==os.getpid(): continue
            try:
                raw=(p/'cmdline').read_bytes().replace(b'\x00',b' ')
                comm=(p/'comm').read_text().strip()
            except FileNotFoundError: continue
            need(not (comm.startswith('openclaw-gatewa') or raw.startswith(b'openclaw-gateway') or
                re.search(rb'(?:^|/)(?:openclaw|openclaw\.mjs|entry\.js|index\.js) +gateway(?: |$)',raw) or
                re.search(rb'/antenna-(?:relay|inbox|send|msg|peers|exchange|setup|upgrade|uninstall|pair|list-send|public-group)(?:-[a-z]+)?\.sh(?: |$)',raw)),
                'GATEWAY_RUNNING','Stop the local OpenClaw gateway and Antenna writers before capture/replacement; no service was stopped.')
    except PermissionError:
        raise StateError('GATEWAY_UNKNOWN','Cannot inspect local processes; gateway state is unknown.') from None


@contextlib.contextmanager
def locks(root, paths):
    # Nonblocking means an inbox drain holding queue then config cannot deadlock
    # with capture. Offline operators must also stop old/non-cooperating writers.
    names={root/'antenna-backup.lock',root/'antenna-config.json.lock',root/'antenna-ratelimit.json.lock',root/'state/antenna-replay.json.lock'}
    names.update(Path(str(p)+'.lock') for p in paths)
    if (root/'.clawreef').exists(): names.add(root/'.clawreef/.lock')
    with contextlib.ExitStack() as stack:
        for p in sorted(names,key=str):
            safe_path(p,missing=True)
            p.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
            fd=os.open(p,os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW|os.O_NONBLOCK,0o600)
            stack.callback(os.close,fd)
            need(os.fstat(fd).st_nlink==1 and os.fstat(fd).st_uid==os.getuid(),'UNSAFE_PATH','Unsafe operation lock.')
            try: fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError: raise StateError('BUSY','State writer is active; retry after stopping Antenna activity.') from None
        yield
