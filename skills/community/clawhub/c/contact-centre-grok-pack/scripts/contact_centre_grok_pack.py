#!/usr/bin/env python3
"""Contact Centre Grok Pack: transcript summarisation and routing heuristics."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

DEMO = "Customer says the boiler repair was missed twice, elderly tenant has no heating, asks for urgent callback today."
ROUTES = {
 'council': {'housing repairs':['boiler','heating','repair','tenant','leak'], 'benefits':['benefit','council tax','payment'], 'safeguarding':['elderly','vulnerable','child','risk']},
 'clinic': {'clinical triage':['pain','bleeding','symptom','medication'], 'appointments':['appointment','reschedule','cancel'], 'billing':['invoice','insurance','charge']},
 'support': {'technical support':['error','bug','login','crash'], 'billing':['invoice','payment','refund'], 'customer success':['training','how do i','setup']},
 'sme': {'sales':['quote','pricing','demo'], 'operations':['delivery','order','stock'], 'accounts':['invoice','payment','statement']},
}
NEGATIVE={'angry','upset','frustrated','complaint','missed','failed','urgent','no heating','broken'}
DISTRESS={'distressed','unsafe','vulnerable','elderly','child','emergency','risk','no heating','bleeding'}
POSITIVE={'thanks','great','happy','resolved','appreciate'}

def read_transcript(path):
    if not path: return DEMO
    try:
        text=Path(path).read_text(encoding='utf-8')
    except FileNotFoundError:
        import sys
        print(f"Error: input file '{path}' not found.", file=sys.stderr)
        sys.exit(1)
    try:
        obj=json.loads(text)
        return obj.get('transcript') or obj.get('text') or text
    except json.JSONDecodeError:
        return text

def classify(text, industry, sla_hours):
    low=text.lower(); words=re.findall(r"[a-z0-9']+", low)
    sent='neutral'
    if any(k in low for k in DISTRESS): sent='distressed'
    elif any(k in low for k in NEGATIVE): sent='frustrated'
    elif any(k in low for k in POSITIVE): sent='positive'
    urgency='normal'; reasons=[]
    if any(k in low for k in DISTRESS): urgency='critical'; reasons.append('vulnerability/emergency keyword')
    elif any(k in low for k in ['urgent','today','missed','complaint','blocked']): urgency='high'; reasons.append('time-sensitive or complaint keyword')
    elif sla_hours <= 4: urgency='high'; reasons.append('short SLA target')
    route_scores={}
    for route, kws in ROUTES.get(industry, ROUTES['support']).items():
        route_scores[route]=sum(1 for k in kws if k in low)
    route=max(route_scores, key=route_scores.get) if route_scores else 'general triage'
    if route_scores and route_scores[route]==0: route='general triage'
    summary=' '.join(text.strip().split())[:180]
    if len(text.strip())>180: summary+='...'
    actions=['Log transcript and caller intent', f'Route to {route}', f'Respond within {sla_hours} hours']
    if urgency in ('high','critical'): actions.insert(0,'Escalate for same-day human review')
    return {"summary":summary,"sentiment":sent,"urgency":urgency,"route":route,"actions":actions,"evidence":{"matched_route_scores":route_scores,"reasons":reasons,"word_count":len(words)}}

def main():
    p=argparse.ArgumentParser(description='Summarise and route contact-centre transcripts.')
    p.add_argument('--input'); p.add_argument('--industry', choices=['council','clinic','support','sme'], default='support')
    p.add_argument('--output'); p.add_argument('--sla-hours', type=int, default=24)
    args=p.parse_args(); result=classify(read_transcript(args.input), args.industry, args.sla_hours)
    data=json.dumps(result, indent=2)
    if args.output: Path(args.output).write_text(data+'\n', encoding='utf-8')
    print(data)
if __name__=='__main__': main()
