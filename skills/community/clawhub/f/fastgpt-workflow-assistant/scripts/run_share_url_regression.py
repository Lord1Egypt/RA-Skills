#!/usr/bin/env python3
"""Reuse an evidenced local instance protocol for share-URL tests. Default: dry run, no requests."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlsplit
from prepare_share_window_test import inspect_target


def registry_path(explicit=None):
    return Path(explicit or os.environ.get('FASTGPT_SHARE_REGISTRY') or (Path.home()/'.config/fastgpt-workflow-assistant/share-instances.json'))


def canonical_origin(url):
    p=urlsplit(url)
    if p.scheme not in ('http','https') or not p.hostname or p.username is not None or p.password is not None:
        raise ValueError('Invalid HTTP origin')
    port=p.port
    if port is not None and not 1 <= port <= 65535:
        raise ValueError('Invalid port')
    host=p.hostname.lower()
    if ':' in host: host='['+host+']'
    suffix='' if port is None or (p.scheme=='https' and port==443) or (p.scheme=='http' and port==80) else ':'+str(port)
    return p.scheme.lower()+'://'+host+suffix


def plan(page_url, registry=None):
    target=inspect_target(page_url)
    origin=canonical_origin(page_url)
    path=registry_path(registry)
    base={'artifact_role':'share-url-test-plan','importable_workflow':False,'page_url':page_url,'share_id':target['share_id'],
          'origin':origin,'registry_file':str(path),'network_called':False,'current_protocol_verified':False}
    if not path.is_file():
        return dict(base,status='protocol_evidence_missing',next_step='inspect_existing_local_test_records_before_http_discovery')
    raw=path.read_bytes();data=json.loads(raw.decode('utf-8-sig'))
    entries=[x for x in data.get('instances',[]) if canonical_origin(x['origin'])==origin]
    if len(entries)>1: raise ValueError('Ambiguous instance profile')
    if not entries:
        return dict(base,status='unknown_instance',next_step='confirm_this_instance_protocol_do_not_apply_other_hosts')
    entry=entries[0];evidence=entry.get('evidence',{})
    if entry.get('protocol')!='fastgpt-share-sse' or entry.get('mode')!='share-only':
        raise ValueError('Unsupported instance protocol; explicit adapter needed')
    endpoint=entry.get('endpoint_path','')
    if not endpoint.startswith('/') or endpoint.startswith('//') or any(x in endpoint for x in ['?', '#', '\\']) or endpoint.strip()!=endpoint:
        raise ValueError('Expected evidenced same-origin API path')
    if not evidence.get('verified_on') or not evidence.get('kind') or not evidence.get('source_file') or not evidence.get('source_sha256'):
        raise ValueError('Instance profile lacks historical evidence')
    return dict(base,status='known_protocol_smoke_required',endpoint=origin+endpoint,share_only=True,app_id=None,
                historical_evidence=evidence,registry_sha256=hashlib.sha256(raw).hexdigest(),
                next_step='one_case_smoke_then_requested_regression_no_browser_or_packet_capture')


def command_for(test_plan,cases,results,gap=3.0,timeout=90.0):
    if test_plan.get('status')!='known_protocol_smoke_required':
        raise ValueError('No evidenced protocol for this instance')
    if gap < 3: raise ValueError('Regression gap must be at least 3 seconds')
    if timeout <= 0: raise ValueError('Positive timeout required')
    return [sys.executable,str(Path(__file__).with_name('run_share_api_regression.py')),str(cases),str(results),
            '--url',test_plan['endpoint'],'--share-only','--share-id',test_plan['share_id'],
            '--gap-seconds',str(gap),'--timeout-seconds',str(timeout)]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('page_url');parser.add_argument('cases',type=Path);parser.add_argument('results',type=Path)
    parser.add_argument('--registry',type=Path);parser.add_argument('--execute',action='store_true',help='Explicitly execute already-authorized test; otherwise print plan only')
    parser.add_argument('--gap-seconds',type=float,default=3);parser.add_argument('--timeout-seconds',type=float,default=90)
    args=parser.parse_args()
    try:
        p=plan(args.page_url,args.registry)
        if p['status']!='known_protocol_smoke_required':
            print(json.dumps(p,ensure_ascii=False,indent=2));return 2
        from run_share_api_regression import load_cases
        cases=load_cases(args.cases)
        p['case_count']=len(cases);p['command']=command_for(p,args.cases,args.results,args.gap_seconds,args.timeout_seconds)
        if not args.execute:
            p['execution']='dry_run_not_tested';print(json.dumps(p,ensure_ascii=False,indent=2));return 0
        if args.results.exists(): raise FileExistsError('Preserve existing test results; choose a new path')
        args.results.parent.mkdir(parents=True,exist_ok=True)
        # The existing runner owns SSE parsing, single-concurrency, isolation, evidence and assertions.
        result=subprocess.run(p['command'])
        return result.returncode
    except (ValueError,TypeError,KeyError,OSError) as exc:
        print(json.dumps({'status':'error','error_type':type(exc).__name__}));return 1

if __name__=='__main__':raise SystemExit(main())
