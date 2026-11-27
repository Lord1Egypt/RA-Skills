#!/usr/bin/env python3
"""Read-only comparison of a selected install directory against a trusted release ZIP."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile


def compare(package, installed):
    package,installed=Path(package),Path(installed).resolve()
    if not installed.is_dir(): raise ValueError('Installed directory missing')
    same=[];different=[];missing=[];metadata=[]
    with zipfile.ZipFile(package) as archive:
        seen=set()
        for info in archive.infolist():
            if info.is_dir():continue
            name=info.filename
            parts=PurePosixPath(name).parts
            if name in seen or name.startswith('/') or '\\' in name or ':' in name or '..' in parts:
                raise ValueError('Unsafe or duplicate ZIP path')
            seen.add(name)
            if len(seen)>10000 or info.file_size>100_000_000:raise ValueError('Comparison input size limit exceeded')
            local=installed.joinpath(*parts)
            if local.is_symlink() or not local.resolve().is_relative_to(installed):raise ValueError('Installed path escapes selected directory')
            expected=archive.read(info);expected_sha=hashlib.sha256(expected).hexdigest()
            if not local.is_file():missing.append({'file':name,'expected_sha256':expected_sha});continue
            actual=local.read_bytes();actual_sha=hashlib.sha256(actual).hexdigest()
            item={'file':name,'expected_sha256':expected_sha,'installed_sha256':actual_sha}
            if actual_sha==expected_sha:same.append(item)
            else:different.append(item)
            if name.endswith('assets/skill-version.json'):
                a=json.loads(actual.decode('utf-8-sig'));e=json.loads(expected.decode('utf-8-sig'))
                fields=('version','local_revision','build_id')
                metadata.append({'file':name,'expected':{k:e.get(k) for k in fields},'installed':{k:a.get(k) for k in fields}})
    return {'artifact_role':'install-comparison-report','importable_workflow':False,'matched':not missing and not different,
            'package_sha256':hashlib.sha256(package.read_bytes()).hexdigest(),'expected_files':len(seen),
            'identical':same,'different':different,'missing':missing,'metadata':metadata,
            'scope':'selected local directory only; extra runtime files ignored; no repair, active-runtime discovery, marketplace or workflow validation performed'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('package',type=Path);p.add_argument('installed',type=Path);p.add_argument('--output',type=Path);args=p.parse_args()
    try:
        report=compare(args.package,args.installed);text=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=True)
            with args.output.open('x',encoding='utf-8') as f:f.write(text)
        print(text);return 0 if report['matched'] else 1
    except (OSError,ValueError,zipfile.BadZipFile) as exc:
        print(json.dumps({'matched':False,'error_type':type(exc).__name__}));return 2

if __name__=='__main__':raise SystemExit(main())
