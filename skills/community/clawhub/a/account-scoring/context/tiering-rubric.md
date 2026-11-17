---
title: Account tiering rubric
description: What A, B, C and disqualified mean, and what evidence is allowed to decide each one. The tiering agent reads this file on every run.
---

# Account tiering rubric

PLACEHOLDER, and the most important file in this skill. The agent's system
prompt says how to behave; this says what to decide. Put it in the project's
context repo beside the ICP (`icp.md`, the one tam-building reads or wrote).
Edit it there and the next run tiers differently, with no deploy and a git
history of why.

Every tier is decided against the ICP. A tier that cannot name the line it
came from is a guess, and the evaluator fails it.

## Tiers

| Tier           | What it means                                   | The bar                                                                                                                                                  |
| -------------- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `A`            | Work it now                                     | Fits the firmographics AND shows strong evidence of the motion the ICP sells into: the persona employed, or the practice visible in public               |
| `B`            | Worth a sequence, not a rep                     | Fits the firmographics AND shows weaker evidence (a stack, a growth pattern), or fits everything but the persona is inferred rather than observed        |
| `C`            | In the market, not in the motion                | Fits the firmographics and nothing else. No visible technical champion, no automation practice, no signal                                                |
| `disqualified` | Do not spend another credit or another rep-hour | Any disqualifier in the ICP is true, or the sourced record is wrong about the company (dead domain, acquired, headcount off by more than one whole band) |

## Evidence rules

- **Judge on the sourced facts first.** Name, domain, industry, headcount and
  description come with the row. If they settle the tier, settle it and stop.
- **Search only to resolve a specific doubt.** One question, one search: "does
  this company employ a GTM engineer", not "tell me about this company". A
  search that could not change the tier is a step wasted against `maxSteps`.
- **Record where the fact came from.** When a search decided the tier, put the
  page in `tier_evidence_url`. A tier a rep cannot audit is a number they will
  not trust.
- **Never invent a firmographic.** If a fact cannot be found, say the fact is
  absent and tier on what is known. An absent persona is a real `C`, not a
  guessed `B`.

## Ties

- Firmographics fit and the disqualifier is uncertain: tier `C`, and say in the
  rationale what would need to be true for it to be `disqualified`. Sourcing is
  already paid for; the cost of a wrong `disqualified` is a lost account.
- Evidence is strong but the headcount is one band off: tier `B`. Two bands off
  is `disqualified` under the ICP.
