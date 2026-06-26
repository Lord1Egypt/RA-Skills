#!/usr/bin/env python3
"""BS Detector — extracts real points from verbose text"""
import argparse, re

FLUFF = [
    'synergy', 'leverage', 'paradigm', 'value-add', 'circle back',
    'touch base', 'moving forward', 'at the end of the day',
    'it goes without saying', 'needless to say', 'honestly',
    'basically', 'literally', 'actually', 'very', 'really',
    'in terms of', 'at this point in time', 'going forward',
    'proactive', 'robust', 'streamline', 'optimize'
]

def detect_bs(text):
    text_lower = text.lower()
    fluff_count = sum(1 for f in FLUFF if f in text_lower)
    fluff_pct = fluff_count / (len(text.split()) / 10)

    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    longest = max(sentences, key=len) if sentences else text[:100]

    words = text.split()
    has_numbers = any(c.isdigit() for c in text)
    has_deadline = any(w in text_lower for w in ['deadline', 'by friday', 'by monday', 'eod', 'due', 'tomorrow'])

    real_point = longest if len(longest) > 30 else text[:150]

    verdict = "LOTS OF BS" if fluff_pct > 2 else "SOME FLUFF" if fluff_pct > 0.5 else "CLEAN"
    return {
        'verdict': verdict,
        'real_point': real_point.strip(),
        'fluff_pct': round(fluff_pct, 1),
        'sentences': len(sentences),
        'has_numbers': has_numbers,
        'has_deadline': has_deadline
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--text', default=None)
    p.add_argument('--input', default=None)
    args = p.parse_args()

    if args.input:
        with open(args.input) as f:
            text = f.read()
    else:
        text = args.text or input("Paste text: ")

    result = detect_bs(text)
    print(f"""
🔍 BS DETECTOR RESULT
═══════════════════════════════
VERDICT: {result['verdict']} ({result['fluff_pct']} fluff density)

💡 THE REAL POINT:
{result['real_point'][:200]}

📊 Message stats:
   Sentences: {result['sentences']}
   Has numbers: {'✓' if result['has_numbers'] else '✗'}
   Has deadline: {'✓' if result['has_deadline'] else '✗'}
═══════════════════════════════
""")

if __name__ == '__main__':
    main()
