#!/usr/bin/env python3
"""Generate safe browser-agent workflow templates."""
from __future__ import annotations
import argparse, json
from pathlib import Path

DEFAULT_STEPS={
 'form-filling':['Open portal login page','Navigate to target form','Extract required fields','Fill draft values','Pause for human review','Submit after approval','Capture confirmation reference'],
 'case-routing':['Open case queue','Filter unassigned cases','Read case detail','Classify intent and urgency','Assign queue suggestion','Pause for supervisor review','Apply routing label'],
 'portal-operation':['Open target portal','Search target record','Validate identity/context','Prepare requested action','Capture before-state','Request approval','Execute action','Capture after-state'],
 'research-capture':['Open source page','Capture title/date/source URL','Extract relevant facts','Store snapshot/hash','Summarise changes','Emit evidence bundle'],
}

def load_steps(path, use_case):
    if path:
        try:
            return json.loads(Path(path).read_text(encoding='utf-8'))
        except json.JSONDecodeError as e:
            import sys
            print(f"Error: steps file '{path}' contains invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)
    return [{'name':s,'tool':'browser','approval':('review' in s.lower() or 'submit' in s.lower() or 'execute' in s.lower())} for s in DEFAULT_STEPS.get(use_case, DEFAULT_STEPS['portal-operation'])]

def build(args):
    steps=load_steps(args.steps, args.use_case)
    strict=args.approval_threshold
    gates=[]
    for i,s in enumerate(steps,1):
        name=s.get('name', str(s)) if isinstance(s, dict) else str(s)
        risky=any(w in name.lower() for w in ['submit','execute','apply','send','delete','payment','approval'])
        if risky or strict=='high' or (strict=='normal' and i==len(steps)):
            gates.append({'before_step':i,'gate':'human_approval','reason':name})
    return {
      'workflow': {'use_case':args.use_case,'portal':args.portal,'objective':f'Safe {args.use_case} workflow for {args.portal}'},
      'steps':steps,
      'approval_gates':gates,
      'evidence_required':['source URL','before/after screenshots for state changes','timestamped action log','confirmation/reference ID when available'],
      'error_handling':['Stop on login/auth failure','Do not retry irreversible actions automatically','Emit partial results if source blocks automation','Escalate ambiguous fields to a human'],
      'handoff_schema':{'case_id':'string','summary':'string','recommended_action':'string','evidence_urls':['string'],'approval_status':'pending|approved|rejected'}
    }

def markdown(doc):
    lines=[f"# {doc['workflow']['objective']}","",f"Portal: {doc['workflow']['portal']}","","## Steps"]
    for i,s in enumerate(doc['steps'],1): lines.append(f"{i}. {s.get('name', s) if isinstance(s, dict) else s}")
    lines += ["","## Approval Gates"] + [f"- Before step {g['before_step']}: {g['reason']}" for g in doc['approval_gates']]
    lines += ["","## Evidence Required"] + [f"- {e}" for e in doc['evidence_required']]
    lines += ["","## Error Handling"] + [f"- {e}" for e in doc['error_handling']]
    lines += ["","## Handoff Schema","```json",json.dumps(doc['handoff_schema'], indent=2),"```",""]
    return '\n'.join(lines)

def main():
    p=argparse.ArgumentParser(description='Generate browser-agent workflow templates.')
    p.add_argument('--use-case', choices=list(DEFAULT_STEPS), default='portal-operation'); p.add_argument('--portal', default='government service portal')
    p.add_argument('--steps'); p.add_argument('--output'); p.add_argument('--json', action='store_true'); p.add_argument('--approval-threshold', choices=['low','normal','high'], default='normal')
    args=p.parse_args(); doc=build(args); out=json.dumps(doc, indent=2) if args.json else markdown(doc)
    if args.output:
        out_path = Path(args.output); out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out+'\n', encoding='utf-8')
    print(out)
if __name__=='__main__': main()
