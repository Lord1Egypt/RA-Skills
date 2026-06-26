#!/usr/bin/env python3
"""Calendar Optimizer"""
import argparse, csv, re

FLUFF = ['synergy','circle back','paradigm','leverage','moving forward','touch base','proactive','value add','streamline']
DEADLINE_RE = re.compile(r'(monday|tuesday|wednesday|thursday|friday|tomorrow|eod|by (\w+))', re.I)

def optimize(event, time_str):
    text = event.lower()
    fluff_free = ' '.join(w for w in text.split() if w not in FLUFF)
    has_deadline = bool(DEADLINE_RE.search(event + ' ' + time_str))
    return {
        'original': event,
        'time': time_str,
        'clean_topic': fluff_free.strip().title(),
        'actionable': len(fluff_free.strip()) > 10,
        'has_deadline': has_deadline,
        'suggestion': 'Consider declining' if 'sync' in text and len(text) < 30 else 'Review agenda before attending'
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--event', required=True)
    p.add_argument('--time', default='TBD')
    args = p.parse_args()
    r = optimize(args.event, args.time)
    print(f"""
📅 CALENDAR OPTIMIZER
═══════════════════════════════
ORIGINAL: {r['original']}
TIME:     {r['time']}

CLEAN:    {r['clean_topic']}
STATUS:    {'✅ Actionable' if r['actionable'] else '⚠️ Vague'}
DEADLINE: {'✅' if r['has_deadline'] else '❌ Missing'}
TIP:      {r['suggestion']}
""")
if __name__ == '__main__':
    main()
