#!/usr/bin/env python3
"""Encrypted state snapshots and confirmed in-place replacement (no service control)."""
import argparse
import contextlib
from datetime import datetime, timezone
import io
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'lib'))
import antenna_plugin_state as state

WARNING='This will replace Antenna’s configuration and saved state with this backup. Changes made since the backup—including newer inbox records—will be lost. Installed program files and OpenClaw conversation history will not be changed. Continue?'
FORMAT=2
PRODUCER_VERSION='1.6.9'
COMPATIBLE_VERSIONS=('1.6.8', '1.6.9')
TAR_LIMIT=state.MAX_TOTAL+state.MAX_MEMBERS*2048+1024*1024


def terminal():
    try:
        fd=os.open('/dev/tty',os.O_RDWR)
        os.close(fd)
    except OSError:
        raise state.StateError('TERMINAL_REQUIRED','Rerun interactively: enter the backup passphrase directly at the protected terminal, not in chat. --yes and --json do not bypass unlock.') from None


def age(source,target,decrypt=False):
    terminal()
    args=['age','--decrypt' if decrypt else '--passphrase',str(source)]
    # Bound the decrypt stream without trusting tar sizes or retaining passphrases.
    with open(target,'xb') as out:
        os.chmod(target,0o600)
        try: proc=subprocess.Popen(args,stdout=subprocess.PIPE)
        except OSError: raise state.StateError('DEPENDENCY','Install age; no automatic installation is performed.') from None
        try:
            total=0
            while True:
                chunk=proc.stdout.read(65536)
                if not chunk: break
                total+=len(chunk)
                state.need(total<=TAR_LIMIT+1024*1024,'SIZE_LIMIT','Archive exceeds the supported size.')
                out.write(chunk)
            state.need(proc.wait()==0,'UNLOCK_FAILED','Encryption/unlock cancelled or failed; check the passphrase and archive.')
            out.flush();os.fsync(out.fileno())
        finally:
            proc.stdout.close()
            if proc.poll() is None: proc.kill();proc.wait()


def write_archive(path,root,files,refs):
    manifest={'format_version':FORMAT,'producer_version':PRODUCER_VERSION,'state_schema':2,
              'created_at':datetime.now(timezone.utc).isoformat(),'source_root':str(root),
              'files':[{'name':n,'size':len(raw),'sha256':state.digest(raw)} for n,raw in sorted(files.items())],
              'absent':sorted(set(refs)-set(files))}
    with tarfile.open(path,'w',format=tarfile.USTAR_FORMAT) as tar:
        for name,raw in [('manifest.json',state.encode(manifest))]+[('payload/'+n,r) for n,r in sorted(files.items())]:
            item=tarfile.TarInfo(name);item.size=len(raw);item.mode=0o600
            tar.addfile(item,io.BytesIO(raw))
    os.chmod(path,0o600)
    return manifest


def load_archive(path):
    files={}; total=0
    try:
        with tarfile.open(path,'r:') as tar:
            for item in tar:
                state.need(item.isfile() and not item.pax_headers and item.name not in files and
                           len(files)<state.MAX_MEMBERS+1,'INVALID_ARCHIVE','Archive has duplicate, linked or unsupported members.')
                state.relative(item.name)
                state.need(0<=item.size<=state.MAX_FILE,'SIZE_LIMIT','Archive member exceeds limit.')
                total+=item.size
                state.need(total<=state.MAX_TOTAL+1024*1024,'SIZE_LIMIT','Archive exceeds total limit.')
                raw=tar.extractfile(item).read(item.size+1)
                state.need(len(raw)==item.size,'INVALID_ARCHIVE','Truncated archive.')
                files[item.name]=raw
    except (tarfile.TarError,OSError):
        raise state.StateError('INVALID_ARCHIVE','Cannot read the bounded archive.') from None
    state.need('manifest.json' in files,'INVALID_ARCHIVE','Manifest missing.')
    m=state.decode(files.pop('manifest.json'))
    state.need(isinstance(m,dict) and m.get('format_version')==FORMAT and m.get('state_schema')==2 and
               m.get('producer_version') in COMPATIBLE_VERSIONS,'UNSUPPORTED_FORMAT','Unsupported backup format or producer state schema.')
    state.need(isinstance(m.get('source_root'),str) and Path(m['source_root']).is_absolute() and
               str(state.lexical(m['source_root']))==m['source_root'],'INVALID_ARCHIVE','Invalid source metadata.')
    state.need(isinstance(m.get('created_at'),str) and len(m['created_at'])<80 and
               isinstance(m.get('files'),list) and isinstance(m.get('absent'),list),'INVALID_ARCHIVE','Invalid manifest.')
    try: datetime.fromisoformat(m['created_at'])
    except ValueError: raise state.StateError('INVALID_ARCHIVE','Invalid snapshot date.') from None
    payload={}
    for entry in m['files']:
        state.need(isinstance(entry,dict) and set(entry)=={'name','size','sha256'},'INVALID_ARCHIVE','Invalid manifest entry.')
        n=entry['name'];state.relative(n)
        state.need(n not in payload and 'payload/'+n in files,'INVALID_ARCHIVE','Missing or duplicate payload.')
        raw=files.pop('payload/'+n)
        state.need(type(entry['size']) is int and len(raw)==entry['size'] and state.digest(raw)==entry['sha256'],'INVALID_ARCHIVE','Payload digest/size differs.')
        payload[n]=raw
    state.need(not files,'INVALID_ARCHIVE','Unlisted archive members.')
    root=Path(m['source_root'])
    cfg,peers,queue,fingerprints=state.validate_snapshot(root,payload)
    expected=state.expected(root,payload)
    state.need(all(isinstance(n,str) for n in m['absent']) and len(m['absent'])==len(set(m['absent'])) and
               set(m['absent'])==set(expected)-set(payload),'INVALID_ARCHIVE','Absent state inventory differs.')
    state.need(sum(map(len,payload.values()))<=state.MAX_TOTAL,'SIZE_LIMIT','Payload exceeds total limit.')
    return m,payload,fingerprints


def summary(m,fingerprints):
    return {'snapshot_date':m['created_at'],'producer_version':m['producer_version'],
            'files':len(m['files']),'plaintext_bytes':sum(e['size'] for e in m['files']),
            'identity_fingerprints':fingerprints}


def package_target(root):
    state.need(root.is_dir() and root==root.resolve(),'INVALID_TARGET','Select a regular existing Antenna installation directory.')
    for n in ('bin/antenna.sh','lib/session_policy.py','lib/antenna_plugin_state.py','scripts/antenna-backup.py','plugin/recovery-validate.mjs'):
        state.read_file(root/n)
    package=state.decode(state.read_file(root/'plugin/package.json'))
    state.need(package.get('version') in COMPATIBLE_VERSIONS,'INCOMPATIBLE_TARGET','Target must be a compatible v1.6.8 or v1.6.9 companion installation.')
    # Explicitly qualified schema-2 versions only, not arbitrary future packages.
    state.need((root/'lib/antenna_plugin_state.py').read_bytes()==(ROOT/'lib/antenna_plugin_state.py').read_bytes(),
               'INCOMPATIBLE_TARGET','Target must have matching schema-2 recovery validators.')


def prepared(m,files,target):
    data=dict(files);oldroot=Path(m['source_root'])
    cfg=state.decode(data['antenna-config.json']);peers=state.decode(data['antenna-peers.json'])
    remaps=[]
    cfg['install_path']=str(target)
    original=cfg.get('inbox_queue_path','antenna-inbox.json')
    cfg['inbox_queue_path']=state.destination(oldroot,original)
    if original!=cfg['inbox_queue_path']: remaps.append({'field':'inbox_queue_path','to':cfg['inbox_queue_path']})
    for name,p in peers.items():
        for field in state.KEY_FIELDS:
            if field not in p: continue
            original=p[field];p[field]=state.destination(oldroot,original,True,public=field=='signing_public_key_file')
            if original!=p[field]: remaps.append({'peer':name,'field':field,'to':p[field]})
    if cfg.get('log_path') and Path(cfg['log_path']).is_absolute():
        cfg['log_path']='antenna.log';remaps.append({'field':'log_path','to':'antenna.log'})
    data['antenna-config.json']=state.encode(cfg);data['antenna-peers.json']=state.encode(peers)
    plugin=state.decode(data[state.PLUGIN])
    for field,name in state.NATIVE.items():
        if field in plugin:
            plugin[field]=str(target/name)
            remaps.append({'field':field,'to':str(target/name)})
    data[state.PLUGIN]=state.encode(plugin)
    state.validate_snapshot(target,data)
    return data,remaps


def restore_plan(m,files,target):
    package_target(target)
    desired,remaps=prepared(m,files,target)
    refs,current,stamps=state.capture(target,tolerant=True)
    owned={n for n,p in refs.items() if p==target/n and n in current}
    removals=sorted(owned-set(desired))
    # Host config is read locally, not restored from an archive. Replace only
    # Antenna config and disable its entry; preserve all unrelated fields.
    host,_=state.host_config()
    plugin=state.decode(desired.pop(state.PLUGIN))
    operator=host.get('gateway',{}).get('auth',{}).get('token')
    peers=state.decode(desired['antenna-peers.json'])
    self_peer=peers[plugin['receiver']]
    self_token=desired[state.destination(target,self_peer['token_file'],True)].decode().strip()
    state.need(isinstance(operator,str) and operator not in (plugin['bearer'],self_token),
               'OPERATOR_SEPARATION','Resolved operator token must differ from restored Antenna bearer.')
    host['plugins']['entries']['antenna']['config']=plugin
    host['plugins']['entries']['antenna']['enabled']=False
    desired['@host']=state.encode(host)
    targets={n:target/n for n in set(desired)|set(removals) if n!='@host'}
    targets['@host']=state.HOST
    state.need(state.HOST not in [p for n,p in targets.items() if n!='@host'],'PATH_COLLISION','Host overlaps Antenna state.')
    for n,p in targets.items():
        state.safe_path(p,missing=True)
        state.need(n=='@host' or not p.exists() or n in owned,'TARGET_CONFLICT','Restore would overwrite a file outside the current Antenna inventory.')
    prior={n:(state.read_file(p) if p.exists() else None) for n,p in targets.items()}
    plan={'target':str(target),'host':str(state.HOST),'snapshot_date':m['created_at'],
          'replace':sorted(n for n in desired if prior[n] is not None),
          'add':sorted(n for n in desired if prior[n] is None),'remove':removals,
          'remappings':remaps,'preserved_external_files':sorted(str(p) for n,p in refs.items() if p!=target/n and p.exists()),
          'warning':WARNING,'resume':'Plugin is disabled. Restore does not start services or deliver messages. Review settings/holds/replay state and explicitly re-enable after verification; old snapshots can permit duplicates.'}
    return plan,desired,prior,stamps,refs,targets


def atomic(path,raw):
    state.safe_path(path,missing=True)
    path.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='.antenna-write-',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as f: f.write(raw);f.flush();os.fsync(f.fileno())
        os.replace(name,path)
        d=os.open(path.parent,os.O_DIRECTORY)
        try: os.fsync(d)
        finally: os.close(d)
    finally:
        if os.path.exists(name): os.unlink(name)


def replace_state(target,desired,prior,targets=None):
    targets=targets or {n:target/n for n in prior}
    rollback=Path(tempfile.mkdtemp(prefix='.antenna-restore-',dir=target))
    modes={n:(targets[n].stat().st_mode & 0o777) for n,raw in prior.items() if raw is not None}
    try:
        entries=[]
        for i,(n,raw) in enumerate(sorted(prior.items())):
            backup=str(i) if raw is not None else None
            if raw is not None: atomic(rollback/backup,raw)
            entries.append({'path':str(targets[n]),'backup':backup,'mode':modes.get(n)})
        atomic(rollback/'rollback.json',state.encode({'target':str(target),'files':entries}))
        atomic(rollback/'README.txt',b'Restore was interrupted. Keep dispatch stopped. rollback.json maps absolute target paths to private numbered copies; null means absent before restore. Restore those copies with the recorded permission modes or remove those newly added files only. Do not resume until the covered state is consistent.\n')
    except BaseException:
        shutil.rmtree(rollback)
        raise
    print('Temporary rollback: '+str(rollback),file=sys.stderr,flush=True)
    try:
        for n in sorted(prior):
            if n in desired: atomic(targets[n],desired[n])
            elif targets[n].exists(): targets[n].unlink()
        for n in prior:
            state.need((not targets[n].exists()) if n not in desired else state.read_file(targets[n])==desired[n],
                       'VERIFY_FAILED','Replacement verification failed.')
    except BaseException:
        try:
            for n,raw in prior.items():
                if raw is None:
                    if targets[n].exists(): targets[n].unlink()
                else:
                    atomic(targets[n],raw);os.chmod(targets[n],modes[n])
            for n,raw in prior.items():
                state.need(not targets[n].exists() if raw is None else state.read_file(targets[n])==raw)
        except BaseException:
            raise state.StateError('ROLLBACK_REQUIRED','Restore incomplete. Keep dispatch stopped; recover displaced state using '+str(rollback/'rollback.json')) from None
        shutil.rmtree(rollback)
        raise state.StateError('RESTORE_FAILED','Restore failed; original covered state was restored.') from None
    shutil.rmtree(rollback)


def emit(value,json_mode,stream=sys.stdout):
    if json_mode: print(json.dumps(value,ensure_ascii=True),file=stream)
    else:
        for k,v in value.items():
            if k in ('schema_version','ok'): continue
            print(k.replace('_',' ').capitalize()+': '+json.dumps(v,ensure_ascii=True),file=stream)


def main(argv=None):
    parser=argparse.ArgumentParser(prog='antenna backup',description='Encrypted Antenna state backup and in-place restore. If you lose the passphrase, you cannot recover this backup. Enter it directly at age’s protected terminal prompt, not in chat. No unattended unlock.')
    sub=parser.add_subparsers(dest='action',required=True)
    create=sub.add_parser('create');create.add_argument('--output',required=True)
    for name in ('inspect','verify','restore'):
        p=sub.add_parser(name);p.add_argument('archive');p.add_argument('--json',action='store_true')
        if name=='restore':
            p.add_argument('--to',default=str(ROOT));p.add_argument('--apply',action='store_true');p.add_argument('--yes',action='store_true')
    create.add_argument('--json',action='store_true')
    for command_parser in sub.choices.values():
        command_parser.add_argument('--host',default=os.environ.get('OPENCLAW_CONFIG_PATH',str(Path.home()/'.openclaw/openclaw.json')))
    a=parser.parse_args(argv)
    if a.action=='restore': state.need(not a.yes or a.apply,'USAGE','--yes requires --apply.')
    state.HOST=state.lexical(a.host)
    if a.action in ('create','restore'):
        package_target(Path(a.to) if a.action=='restore' else ROOT)
    terminal()
    with tempfile.TemporaryDirectory(prefix='antenna-backup-') as temp:
        temp=Path(temp)
        if a.action=='create':
            output=state.lexical(a.output)
            state.need(not output.exists() and not output.is_symlink(),'OUTPUT_EXISTS','Choose a new backup filename; existing output is never overwritten.')
            state.safe_path(output,missing=True)
            state.need(output.parent.is_dir(),'OUTPUT_PATH','Create the output directory first.')
            state.quiescent()
            refs,_,_,queue=state.inventory(ROOT)
            state.need(output not in refs.values() and not any(state.within(output,ROOT/f) for f in ('secrets','keys','state','.clawreef')),
                       'OUTPUT_CONFLICT','Store the archive outside operational state paths.')
            with state.locks(ROOT,[refs[queue]]):
                first=state.capture(ROOT)
                write_archive(temp/'snapshot.tar',ROOT,first[1],first[0])
                state.need(state.capture(ROOT)==first,'STATE_CHANGED','State changed during capture; stop all writers and retry.')
                state.quiescent()
            print('If you lose the passphrase, you cannot recover this backup. Verification requires opening the encrypted archive again.',file=sys.stderr)
            age(temp/'snapshot.tar',temp/'archive.age')
            age(temp/'archive.age',temp/'verified.tar',True)
            m,files,fps=load_archive(temp/'verified.tar')
            state.need(files==first[1],'VERIFY_FAILED','Created archive differs from captured state.')
            # Exclusive publication on destination filesystem, fsync then link.
            fd,name=tempfile.mkstemp(prefix='.antenna-backup-',dir=output.parent)
            try:
                with os.fdopen(fd,'wb') as f,open(temp/'archive.age','rb') as src:
                    shutil.copyfileobj(src,f);f.flush();os.fsync(f.fileno())
                os.link(name,output)
            finally: os.unlink(name)
            emit({'schema_version':1,'ok':True,'code':'BACKUP_VERIFIED','output':str(output),**summary(m,fps)},a.json)
        else:
            archive=state.lexical(a.archive);state.safe_path(archive,private=True,limit=TAR_LIMIT+1024*1024)
            age(archive,temp/'snapshot.tar',True)
            m,files,fps=load_archive(temp/'snapshot.tar')
            if a.action!='restore':
                emit({'schema_version':1,'ok':True,'code':'ARCHIVE_VERIFIED',**summary(m,fps)},a.json);return
            target=state.lexical(a.to)
            original=restore_plan(m,files,target)
            emit({'schema_version':1,'ok':True,'code':'RESTORE_PREVIEW',**original[0],'identity_fingerprints':fps},a.json,sys.stderr if a.apply else sys.stdout)
            if not a.apply: return
            if not a.yes:
                with open('/dev/tty','w') as tty:
                    tty.write(WARNING+' [y/N] ');tty.flush()
                with open('/dev/tty','r') as tty:
                    state.need(tty.readline().strip().lower() in ('y','yes'),'CANCELLED','Restore cancelled; no state replaced.')
            state.quiescent()
            paths=[p for n,p in original[4].items() if n.endswith('.json')]
            with state.locks(target,paths):
                state.need(restore_plan(m,files,target)==original,'STATE_CHANGED','Target changed after preview; rerun restore.')
                state.quiescent()
                replace_state(target,original[1],original[2],original[5])
            emit({'schema_version':1,'ok':True,'code':'RESTORED','target':str(target),'resume':original[0]['resume']},a.json)


if __name__=='__main__':
    os.umask(0o077)
    signal.signal(signal.SIGTERM,lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    try: main()
    except (state.StateError,OSError,ValueError,KeyError,TypeError,KeyboardInterrupt) as exc:
        value={'schema_version':1,'ok':False,'code':getattr(exc,'code','OPERATION_FAILED'),
               'message':str(exc) if isinstance(exc,state.StateError) else 'Operation failed or interrupted; no success claimed. Check permissions, format and dependencies.'}
        emit(value,'--json' in sys.argv,sys.stderr);sys.exit(2 if value['code']=='USAGE' else 1)
