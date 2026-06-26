#!/usr/bin/env python3
"""Content Writer — AI-powered article generator"""
import argparse

def outline(topic, content_type, words):
    return f"""OUTLINE: {content_type.upper()} ON "{topic}" ({words} words)
═══════════════════════════════════════

1. HOOK (opening 50 words)
   - Start with a bold claim or surprising statistic
   - Connect to reader's pain point

2. CONTEXT (150 words)
   - Explain why this topic matters NOW
   - Set the stakes

3. MAIN BODY ({words-300} words)
   - Point 1: [Key insight + evidence]
   - Point 2: [Supporting data or case study]
   - Point 3: [Practical takeaways]

4. CALL TO ACTION (50 words)
   - What should reader do next?
   - Link to your product/service (optional)

═══════════════════════════════════════
Estimated reading time: {words//200} min
"""
def main():
    p = argparse.ArgumentParser()
    p.add_argument('--topic', required=True)
    p.add_argument('--type', default='blog', choices=['blog','doc','thread','whitepaper'])
    p.add_argument('--length', type=int, default=800)
    args = p.parse_args()
    print(outline(args.topic, args.type, args.length))

if __name__ == '__main__':
    main()
