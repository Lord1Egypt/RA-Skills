#!/usr/bin/env python3
"""Local qualification triage. No credentials, telemetry or personal-data transmission."""
import argparse
import concurrent.futures
import html
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def live_check(op):
    try:
        r = subprocess.run(['curl', '--silent', '--show-error', '--location', '--max-time', '12',
                            '--max-filesize', '600000', '--user-agent', 'OpportunityNavigator/1.0 public-page-check',
                            '--write-out', '\n%{http_code}', op['source_url']],
                           capture_output=True, text=True, timeout=15)
        if r.returncode: return 'UNKNOWN'
        body, _, code = r.stdout.rpartition('\n')
        if code in ('404','410'): return 'CLOSED_OR_REMOVED'
        body = html.unescape(body)
        ok = code == '200' and op['public_page_marker'].lower() in body.lower() and op['public_apply_marker'].lower() in body.lower()
        return 'PUBLIC_APPLICATION_INTAKE_VISIBLE' if ok else 'UNKNOWN'
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return 'UNKNOWN'

def classify(op, p, live_status):
    skips, unresolved = [], []
    skills = {s.lower().strip() for s in p.get('skills', [])}
    if p.get('preference') == 'offline':
        skips.append('This catalog contains remote online roles only.')
    if not skills:
        unresolved.append('Main skills are missing.')
    elif not skills.intersection(op['skills_any']):
        skips.append('Listed core skills do not match the supplied profile.')
    hours = p.get('hours_per_week')
    if hours is None:
        unresolved.append('Available weekly hours are missing.')
    elif op['hours_min'] is not None and hours < op['hours_min']:
        skips.append('Available hours are below the advertised weekly commitment.')
    years = p.get('years_experience')
    if op['years_min']:
        if years is None:
            unresolved.append('Relevant professional experience must be confirmed.')
        elif years < op['years_min']:
            skips.append('Experience is below the stated minimum.')
    if op['id'] == 'dataannotation-software':
        unresolved.append('Production or substantial open-source experience requires confirmation.')
    if p.get('english') is not True:
        unresolved.append('Written-English suitability requires confirmation.')
    country = p.get('country')
    if not country:
        unresolved.append('Country is missing.')
    elif op['eligible_countries'] is None:
        unresolved.append('Country/work-authorization eligibility is not established by the public role page.')
    elif country not in op['eligible_countries']:
        skips.append('Country is outside the stated list.')
    if p.get('needs_external_ai') and op['external_ai_permitted'] is not True:
        unresolved.append('Permission to use external AI is unverified; AI evaluation is not permission to outsource work.')
    if live_status == 'CLOSED_OR_REMOVED':
        skips.append('Original page returned a confirmed removal response.')
    elif live_status != 'PUBLIC_APPLICATION_INTAKE_VISIBLE':
        unresolved.append('Current application availability has not been verified.')
    state = 'SKIP' if skips else 'WATCH' if unresolved else 'READY'
    return {'id': op['id'], 'title': op['title'], 'state': state, 'source_url': op['source_url'],
            'pay': op['payment_amount'], 'pay_type': op['payment_type'], 'weekly_commitment': op['weekly_commitment'],
            'reasons': skips + unresolved, 'eligibility': op['eligibility'], 'ai_usage_rules': op['ai_usage_rules'],
            'application_url': op['application_url'], 'deadline': op['deadline'], 'costs': op['costs'],
            'net_income': 'UNKNOWN', 'approval_probability': 'UNKNOWN', 'allocated_paid_task': False,
            'source_status': live_status, 'snapshot_verified_at': op['last_verified']}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--profile', default='-', help='JSON file, or - for stdin')
    ap.add_argument('--live', action='store_true', help='GET only the catalog public pages; never sends profile data')
    args = ap.parse_args()
    try:
        p = json.load(sys.stdin) if args.profile == '-' else json.loads(Path(args.profile).read_text())
        if not isinstance(p, dict): raise ValueError('profile must be an object')
        if not isinstance(p.get('skills', []), list) or not all(isinstance(s, str) for s in p.get('skills', [])):
            raise ValueError('skills must be a list of strings')
        for k in ('hours_per_week', 'years_experience'):
            v=p.get(k)
            if v is not None and (not isinstance(v, (float,int)) or isinstance(v,bool) or v < 0):
                raise ValueError(k + ' must be a nonnegative number')
        ops = json.loads((ROOT/'references/opportunities.json').read_text())['opportunities']
        if args.live:
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
                states=list(ex.map(live_check,ops))
        else:
            states=['HISTORICAL_SNAPSHOT_ONLY']*len(ops)
        rows=[classify(op,p,s) for op,s in zip(ops,states)]
        order={'READY':0,'WATCH':1,'SKIP':2};rows.sort(key=lambda x:order[x['state']])
        result={'checked_at':datetime.now(timezone.utc).isoformat(),'is_test':'caller_must_label_self_tests',
                'mode':'public_page_check' if args.live else 'historical_snapshot',
                'current_verified_matches':sum(r['state']=='READY' for r in rows),
                'allocated_paid_tasks':0,'notice':'Application candidates are not allocated work or confirmed earnings.',
                'next_action':'Review original country eligibility and assessment rules before investing time.',
                'results':rows}
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (ValueError,TypeError,KeyError,OSError) as e:
        print(json.dumps({'error':str(e)}),file=sys.stderr);return 2
    return 0

if __name__=='__main__': sys.exit(main())
