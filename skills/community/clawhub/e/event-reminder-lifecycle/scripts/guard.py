#!/usr/bin/env python3
"""Offline reminder eligibility; never schedules, sends or establishes permission."""
import argparse
from datetime import datetime, timezone
import json
import sys

def need(ok,message):
    if not ok:raise ValueError(message)

def instant(v):
    need(isinstance(v,str),'timestamp string required')
    try:t=datetime.fromisoformat(v.replace('Z','+00:00'))
    except ValueError:raise ValueError('invalid timestamp') from None
    need(t.tzinfo is not None and t.utcoffset() is not None,'explicit UTC offset required')
    return t.astimezone(timezone.utc)

def decision(d):
    need(isinstance(d,dict) and type(d.get('schema_version')) is int and d['schema_version']==1,'schema_version 1 required')
    now,due,cutoff=map(instant,(d.get('now'),d.get('due'),d.get('cutoff')))
    need(due<cutoff,'due must precede cutoff')
    need(d.get('event_status') in ('active','cancelled','closed'),'invalid event_status')
    for k in ('event_revision','job_revision'):
        need(type(d.get(k)) is int and d[k]>=1,'positive integer revisions required')
    for k in ('task_complete','already_sent'):
        need(type(d.get(k)) is bool,k+' boolean required')
    reason='eligible'
    if d['event_status']!='active':reason='event_inactive'
    elif d['event_revision']!=d['job_revision']:reason='superseded'
    elif d['task_complete']:reason='task_complete'
    elif d['already_sent']:reason='already_sent'
    elif now>=cutoff:reason='expired'
    elif now<due:reason='not_due'
    return {'eligible':reason=='eligible','reason':reason,'scope':'local eligibility only, not send authority or concurrency lock'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');a=p.parse_args()
    try:
        with open(a.input,encoding='utf-8') as f:r=decision(json.load(f))
    except (OSError,ValueError,TypeError,KeyError) as e:
        print('Invalid input: '+str(e),file=sys.stderr);return 2
    print(json.dumps(r,indent=2));return 0

if __name__=='__main__':sys.exit(main())
