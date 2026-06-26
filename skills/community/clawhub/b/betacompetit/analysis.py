#!/usr/bin/env python3
import argparse
def main():
    p = argparse.ArgumentParser()
    p.add_argument('--competitors', required=True)
    p.add_argument('--us', required=True)
    args = p.parse_args()
    comps = [c.strip() for c in args.competitors.split(',')]
    print(f"""🔬 COMPETITOR ANALYSIS: {args.us}
{'='*60}

## COMPETITORS
""")
    for c in comps:
        print(f"- {c}")
    print(f"""
## COMPARISON TABLE
| Feature | {args.us} | {' | '.join(comps)} |
|---------|----------|{'-|' * len(comps)}-----|
| Price | $$ | $$$$ | $ |
| UX | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Support | 24/7 | Business hours | Email only |

## SWOT: {args.us}
| Strengths | Weaknesses |
| {args.us} is faster | Less known |
| Better pricing | Fewer features |

| Opportunities | Threats |
| Growing market | Big player copying |

## RECOMMENDATIONS
1. Differentiate on: Speed + Support
2. Match: Features X and Y
3. Dominate: Niche segment
""")
if __name__ == '__main__':
    main()
