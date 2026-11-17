# Technical Debt Management

## What Counts as Debt

Debt is an **intentional trade-off**: shipping faster now with known shortcuts. Fowler's quadrant separates the cases — deliberate-prudent ("ship now, we know the cost") is strategy; deliberate-reckless ("no time for design") is malpractice; inadvertent debt is a learning artifact, not a moral failure.

**Not debt** (different fixes apply):
- Bugs — just fix them
- Bad code from inexperience — training problem
- Yesterday's patterns aging — evolution; only debt if it blocks work today

**Is debt:** skipped tests to hit a deadline, hardcoded config awaiting parameterization, known performance deferrals, the monolith you've outgrown.

## Hotspot Rule (the highest-leverage idea in this file)

**Debt in code you never touch costs nothing. Never pay it down.**

Prioritize by `churn × complexity` (Tornhill's hotspot analysis): rank files by commit frequency, weight by complexity. The intersection — complex AND frequently changed — is where debt charges interest daily. A horrifying module with 2 commits a year is a museum piece; leave it.

Cheap approximation without tooling: `git log` file-frequency for the last 6 months × your team's "which files do you dread" answer. They converge.

## Debt Registry

| Item | Type | Hotspot? | Interest | Payoff estimate |
|------|------|----------|----------|-----------------|
| Auth service coupling | Architecture | Yes — touched weekly | Growing | 2 sprints |
| Missing API tests | Testing | Yes | Stable | 1 sprint |
| Legacy payment code | Code | No — frozen | None | Don't |

**Interest = how fast it worsens.** Growing (every feature adds coupling) = schedule now. Stable = when convenient. None (cold code) = never.

## The 20% Rule — Canonical Definition

Default **20% of sprint capacity** to maintenance, debt paydown, and developer experience. Scale 10-30%:
- Young codebase, pre-PMF: ~10% — the code may not live long enough to collect interest
- Normal operation: 20%
- Legacy-heavy, post-acquisition, or after a year of "we'll fix it later": ~30% until hotspots cool

Worked example: 10 engineers × 20% = 2 FTE-equivalents of debt work per sprint, as a standing lane. **Reality check:** if debt items are the first cut every sprint, the budget isn't real — the fix is making it a lane with its own owner, not renegotiating each planning.

## Refactor With Features

Bundle paydown into feature work touching the same area: feature touches auth → improve auth tests; new endpoint → clean adjacent code. Why: pure refactor sprints lose business support in one quarter; bundled improvements are invisible and therefore unkillable. This also self-enforces the hotspot rule — you only clean what you touch.

## Rewrites

Almost never (Spolsky's "Things You Should Never Do" — the Netscape rewrite handed the market to IE). Consider only when ALL hold:
- The old system architecturally cannot support a requirement the business has committed to
- Strangler-fig extraction (→ `architecture.md`) was evaluated and genuinely can't work
- Someone on the team has survived a rewrite before

Plan for 2-3× the estimate while maintaining both systems and shipping near-zero features. If the CEO hasn't explicitly accepted that feature freeze, the rewrite is not approved — it's just unstarted.

## Communicating Debt to Business

Never "we have technical debt" — that's engineering vocabulary asking for charity. State it as an investment case:

> "Checkout changes now take 3 weeks instead of 1. Two sprints of paydown returns us to 1 week — that's every future checkout feature landing 2 weeks sooner."

Frame as: velocity delta (before/after, in weeks) · risk (outage, security exposure) · concrete investment with concrete return. If you can't quantify the velocity delta even roughly, you're guessing too — measure cycle time on that area first.
