#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
generate_flow_spec.py

Generates a blank flow-spec template for the fitness-plan-flows skill,
for local filling and reuse.

Usage:
  python scripts/generate_flow_spec.py > flow_spec.md
  python scripts/generate_flow_spec.py --flow "Post-purchase beginner plan" >> my_flows.md
"""

import argparse
import sys

FLOW_SPEC_TEMPLATE = """## Training Plan Flow Overview (Flow map)
- (Flow names, goals, relationship to "plans": delivery / repurchase / acquisition)

## Flow specs

### Flow: {flow_name}
- Goal:
- Trigger:
- Exit rules:
- Segments (if layered):
- Timeline (T+ or calendar days):
- Plan type and content points (e.g. 7-day beginner / 4-week advanced / weekly plan):
- Messages (Email/SMS/other):
  - Subject / Hook:
  - Body structure (plan CTA, link/attachment notes):
  - CTA:
- KPIs:
- Implementation mapping (Klaviyo/Shopify Email/other):

## Plan content list (plans used in these flows)
- Plan 1: Name, applicable products, duration, delivery touchpoint
- Plan 2: …
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate blank flow spec template")
    parser.add_argument(
        "--flow",
        default="<Name>",
        help="Current flow name placeholder; default <Name>",
    )
    args = parser.parse_args()
    out = FLOW_SPEC_TEMPLATE.format(flow_name=args.flow)
    sys.stdout.write(out)


if __name__ == "__main__":
    main()
