#!/usr/bin/env python3
import argparse
def main():
    p = argparse.ArgumentParser()
    p.add_argument('--brand', required=True)
    p.add_argument('--personality', default='bold,smart')
    args = p.parse_args()
    traits = [t.strip() for t in args.personality.split(',')]
    print(f"""🎨 BRAND VOICE: {args.brand}
{'='*60}

## BRAND PERSONALITY
""")
    for t in traits:
        print(f"- {t.upper()}")
    print(f"""
## TONE GUIDE
| Situation | Do | Don't |
|-----------|-----|-------|
| Marketing | Confident, clear | Jargon, vague |
| Support | Empathetic, helpful | Dismissive, technical |
| Social | Engaging, brief | Salesy, long |

## VOCABULARY
Use: {traits[0].title()}, innovative, proven, results
Avoid: Maybe, possibly, try, hope

## SAMPLE CONTENT
"{args.brand} — because {traits[0]} beats {traits[1] if len(traits)>1 else 'uncertainty'}."
""")
if __name__ == '__main__':
    main()
