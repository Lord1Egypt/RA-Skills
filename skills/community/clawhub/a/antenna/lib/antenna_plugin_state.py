"""v1.6.8 recovery inventory; shared host config is never an archive payload."""
from antenna_state import *
import antenna_state as base
import tempfile
HOST=None
PLUGIN='plugin-config.json'
NATIVE={'inboxFile':'state/plugin-inbox.json','replayFile':'state/plugin-replay.json','rulesetFile':'state/plugin-ruleset.json'}


def host_config():
    need(HOST is not None,'HOST_REQUIRED','Supply --host with the local OpenClaw JSON configuration.')
    raw=read_file(HOST,private=True);h=decode(raw)
    need(isinstance(h,dict) and '$include' not in h,'UNSUPPORTED_HOST','Use a resolved local JSON host configuration; includes are unsupported.')
    c=h.get('plugins',{}).get('entries',{}).get('antenna',{}).get('config')
    need(isinstance(c,dict),'INVALID_HOST','Antenna plugin configuration is required; host settings are not repaired.')
    return h,c


def references(root,config,peers,plugin=None):
    refs,queue=base.references(root,config,peers)
    if plugin is not None:
        for field,name in NATIVE.items():
            if field in plugin:
                p=source_path(root,plugin[field])
                need(p.is_absolute() and p not in refs.values() and p!=HOST,'PATH_COLLISION','Plugin state overlaps another role.')
                need(not within(p,root) or p==root/name or (p.relative_to(root).parts[0] not in base.PROTECTED and p.suffix=='.json'),'UNSAFE_PATH','Plugin state must not overlap program or credential directories.')
                need(p not in [refs[n] for n in NATIVE.values() if n in refs],'PATH_COLLISION','Native state paths collide.')
                refs[name]=p
    return refs,queue


def inventory(root,tolerant=False):
    root=lexical(root);_,plugin=host_config()
    config=decode(read_file(root/'antenna-config.json'));peers=decode(read_file(root/'antenna-peers.json'))
    need(config.get('transport_profile')=='antenna-plugin-v2','INCOMPATIBLE_TARGET','v1.6.8 plugin transport is required; use v1.6.7 for legacy recovery.')
    refs,queue=references(root,config,peers,plugin)
    for folder in ('secrets','keys','state','.clawreef'):
        d=root/folder
        if not d.exists(): continue
        st=d.lstat();need(stat.S_ISDIR(st.st_mode) and st.st_uid==os.getuid() and not st.st_mode&0o022,'UNSAFE_PATH','Unsafe state directory.')
        for p in d.iterdir():
            n=p.relative_to(root).as_posix()
            if p.name.endswith('.lock') or p.name=='.lock': continue
            if p.name=='antenna-scan-slots':
                st=p.lstat();need(stat.S_ISDIR(st.st_mode) and not st.st_mode&0o077,'UNSAFE_PATH','Unsafe scan slot directory.')
                need(all(re.fullmatch(r'(dumb|smart)-[01]',q.name) and safe_path(q,private=True) for q in p.iterdir()),'UNKNOWN_STATE','Unknown scan slot state.')
                continue
            # Contact import uses randomly named token and pin files.
            known=base.owned_name(n) or bool(re.fullmatch(r'secrets/plugin-[0-9a-f-]{36}\.(token|pem)',n))
            need(p in refs.values() or known,'UNKNOWN_STATE','Unrecognized operational state; no partial backup.')
            if p not in refs.values(): refs[n]=p
    need(HOST not in refs.values(),'PATH_COLLISION','Shared host configuration cannot be a companion state reference.')
    need(len(set(refs.values()))==len(refs),'PATH_COLLISION','State roles share a file.')
    need(len(refs)<=MAX_MEMBERS,'SIZE_LIMIT','Too many state files.')
    return refs,config,peers,queue


def validate_snapshot(root,files):
    c=decode(files[PLUGIN]);cfg=decode(files['antenna-config.json']);peers=decode(files['antenna-peers.json'])
    need(cfg.get('transport_profile')=='antenna-plugin-v2','UNSUPPORTED_FORMAT','Legacy recovery is not supported by v1.6.8.')
    need(isinstance(c,dict) and c.get('schemaVersion')==2,'INVALID_PLUGIN','Unsupported plugin configuration.')
    # Reuse exact runtime config/inbox/rules validators in an inert temporary view.
    with tempfile.TemporaryDirectory(prefix='antenna-validate-') as temp:
        temp=Path(temp)
        for n in [PLUGIN,*NATIVE.values()]:
            if n in files:
                p=temp/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(files[n])
        command(['node',str(ROOT/'plugin/recovery-validate.mjs'),str(temp)])
    native=set(NATIVE.values())|{PLUGIN}
    companion={n:r for n,r in files.items() if n not in native}
    # Retained companion identity/session policy validators remain shared with migration.
    extra={n:r for n,r in companion.items() if re.fullmatch(r'secrets/plugin-[0-9a-f-]{36}\.(token|pem)',n)}
    refs,queue=base.references(root,cfg,peers)
    core={n:r for n,r in companion.items() if n not in extra or n in refs}
    result=base.validate_snapshot(root,core)
    need(c['receiver'] in peers and peers[c['receiver']].get('self') is True,'INVALID_PLUGIN','Plugin receiver differs from companion identity.')
    references(root,cfg,peers,c)
    if 'state/plugin-replay.json' in files:
        v=decode(files['state/plugin-replay.json']);need(isinstance(v,dict) and set(v)=={'entries'} and isinstance(v['entries'],list))
        for e in v['entries']:
            need(isinstance(e,dict) and set(e)=={'id','peer','seen'} and isinstance(e['peer'],str) and bool(e['peer']) and isinstance(e['id'],str) and re.fullmatch(r'[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}',e['id']) and type(e['seen']) is int and e['seen']>=0)
    need(set(files)<=set(refs)|native|set(extra)|{n for n in files if base.owned_name(n)},'UNKNOWN_STATE','Unknown state role.')
    need('rulesetFile' not in c or NATIVE['rulesetFile'] in files,'MISSING_STATE','Custom ruleset missing.')
    return result


def capture(root,tolerant=False):
    refs,config,peers,queue=inventory(root,tolerant)
    h,c=host_config();files={PLUGIN:encode(c)};stamps={str(HOST):identity(safe_path(HOST,private=True))};total=0
    for n,p in refs.items():
        st=safe_path(p,missing=True,private=n.startswith(('secrets/','.clawreef/')))
        stamps[str(p)]=identity(st) if st else None
        if st:
            total+=st.st_size;need(total<=MAX_TOTAL,'SIZE_LIMIT','State exceeds archive limit.');files[n]=read_file(p)
    if not tolerant: validate_snapshot(root,files)
    # Synthetic plugin config has no standalone current file.
    return refs,files,stamps


def expected(root,files):
    cfg=decode(files['antenna-config.json']);peers=decode(files['antenna-peers.json']);c=decode(files[PLUGIN])
    refs,_=references(root,cfg,peers,c)
    return set(refs)|{PLUGIN}


@contextlib.contextmanager
def locks(root,paths):
    _,c=host_config();inbox=Path(c['inboxFile']);lock=Path(str(inbox)+'.lock')
    # Runtime inbox uses mkdir, replay uses flock. Do not substitute one for the other.
    lock.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    safe_path(inbox,missing=True)
    try: lock.mkdir(mode=0o700)
    except FileExistsError: raise StateError('BUSY','Plugin inbox writer or stale lock present; inspect while stopped.') from None
    try:
        with base.locks(root,[p for p in paths if p!=inbox]+[Path(c['replayFile']),HOST]): yield
    finally: lock.rmdir()


def quiescent():
    base.quiescent()
    for p in Path('/proc').iterdir():
        if not p.name.isdigit() or int(p.name)==os.getpid():continue
        try: raw=(p/'cmdline').read_bytes().replace(b'\0',b' ')
        except FileNotFoundError:continue
        need(not re.search(rb'/plugin/(?:cli|pairing|legacy-migration)\.mjs(?: |$)',raw),'GATEWAY_RUNNING','Stop plugin CLI writers before recovery.')
