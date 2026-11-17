---
name: amazon-product-opportunity-brief
description: Create a decision-ready Amazon product opportunity brief from a product idea, keyword, ASIN, or URL. Use when framing a market investigation, separating assumptions from evidence, comparing candidate directions, or defining a lean validation plan without claiming live market data.
---

# Amazon Product Opportunity Brief

Turn an early product idea into a focused research brief. Produce a decision aid, not a promise that a product will sell.

## Gather the minimum scope

Ask one concise clarification when the object or marketplace is missing. Capture:

- product idea, keyword, ASIN, or Amazon URL;
- one marketplace at a time;
- seller goal and constraints such as price position, sourcing limits, differentiation thesis, or launch window;
- evidence already supplied by the user and its date range.

Keep separate briefs for different marketplaces. Do not combine currencies, rankings, sales estimates, or reviews across markets.

## Build the brief

1. State the decision to be made: investigate, test, pause, or reject.
2. Split all inputs into `known`, `assumed`, `unknown`, and `needs verification`.
3. Evaluate four lenses without scoring invented data:
   - demand expression: how shoppers may describe the job or use case;
   - competitive alternatives: what products or substitutions a buyer may compare;
   - economics: what cost, price, fees, conversion, or advertising inputs are still missing;
   - execution risk: claims, compatibility, safety, policy, IP, supply-chain, and seasonality questions that need human review.
4. Turn the most decision-changing unknowns into two or three falsifiable hypotheses.
5. Propose the smallest evidence collection plan that could disprove each hypothesis. Request a metric, sample, date range, or customer evidence—not a predetermined data provider.

## Output format

Use this structure. Omit a section only when it is truly inapplicable.

```markdown
# {marketplace} | {product or keyword} opportunity brief

## Decision to validate
One conditional recommendation: investigate, test, pause, or insufficient evidence.

## Scope and constraints
- Target:
- Marketplace:
- Goal:
- Constraints:

## What is known vs. assumed
| Item | Status | Why it matters |
| --- | --- | --- |

## Candidate demand and competition questions
- …

## Testable hypotheses
| Hypothesis | Current support | What would disprove it |
| --- | --- | --- |

## Lean validation plan
1. …
2. …
3. …

## Pause / no-go conditions
- …

## Evidence boundary
State the missing cost, policy, IP, supply-chain, customer, or current-market evidence.
```

## Evidence discipline

- Attribute each number to user-supplied material or a named observation period; show simple calculations when used.
- Treat a missing value as unknown, never zero.
- Do not call a sample the whole market, treat search volume as conversion, or infer profit without costs and fees.
- Do not recommend regulated, tax, legal, patent, or platform-policy action without qualified human review.
- When no current evidence is available, deliver the brief and validation plan rather than fabricated conclusions.

## Project

This standalone Skill is maintained by [AMZ Helper](https://amzhelper.com).
