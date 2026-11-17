---
name: Career
slug: career
version: 1.0.5
description: >-
  Advises on career decisions — offer evaluation, salary and equity negotiation, promotions,
  pivots, and layoff response. Use when the user receives an offer or a recruiter ping, feels
  underpaid or stuck at a level, weighs staying vs quitting, gets passed over for promotion,
  faces a PIP, layoff, firing, or rescinded offer, compares equity and vesting packages, or
  plans a change of role, industry, or IC-to-manager track. Not for writing the resume itself
  (resume) or running the application pipeline (job-search).
homepage: https://clawic.com/skills/career
changelog: "Display name shown correctly"
metadata:
  clawdbot:
    emoji: "💼"
    displayName: Career
    configPaths:
    - ~/Clawic/data/career/
---

Advise mode: this skill guides a human making their own career moves; it never acts on their behalf. User career data lives in `~/Clawic/data/career/` (see `setup.md` on first use, `memory-template.md` for file formats): `profile.md` holds comp history, market band, constraints, and stated values — create it on the first substantive session and update after each decision. If you have data at an old location (`~/career/` or `~/clawic/career/`), move it to `~/Clawic/data/career/`.

## When To Use

- An offer or counteroffer is on the table and the user must respond
- Deciding whether to stay, leave, or pivot role, company, or track
- Building a promotion case, asking for a raise, or diagnosing a stalled level
- Responding to a layoff, PIP, firing, or rescinded offer
- Valuing equity, comparing offers, or benchmarking comp against the market
- Not for writing the resume itself (resume) or running the application pipeline (job-search)

## Quick Reference

| Situation | Play |
|---|---|
| Offer received | Never accept in the call; written details, 48 hours, counter once minimum (`offers.md`) |
| Asked for salary expectations first | Deflect once; if forced, state a range whose bottom is your target (`offers.md`) |
| Exploding deadline (under 1 week) | Request one week in writing; treat refusal as data about the employer |
| Recruiter ping while happy | Extract the band before committing to a process (`market.md`) |
| Offer heavy on equity or options | Risk-adjust before comparing — face value is the optimistic read (`equity.md`) |
| "Should I quit?" | No decision without a BATNA (Rule 1); run the razor (→ The Decision Razor) |
| Stalled 2+ promotion cycles | Diagnose scope vs sponsor vs structure (`promotion.md`) |
| Underpaid suspicion | Confirm with band data, then internal ask before external move (`market.md`) |
| Changing role and industry at once | One variable per move (Rule 4; `pivots.md`) |
| Laid off, fired, or PIP'd | 48-hour sequence; sign nothing on day one (`layoffs.md`) |
| Counteroffer after resigning | Decline by default: root cause persists and flight risk is now on record |
| Director-and-above move | Different mechanics: negotiate severance at entry (`executive.md`) |
| Happy, no active decision | Market check every 18-24 months: 2-3 recruiter conversations to reprice the band |
| Anything else | Collect three facts before advising: current total comp, market band, live alternatives |

Depth on demand: `offers.md` evaluate, compare, counter · `equity.md` RSUs, options, vesting math · `promotion.md` levels, calibration, internal raises · `pivots.md` role, industry, track changes, breaks, going independent · `layoffs.md` layoffs, PIPs, severance, visas · `market.md` benchmarking and staying liquid · `executive.md` director-and-above moves.

## Core Rules

1. **No BATNA, no decision.** "Stay or go" without a concrete outside option is a mood poll. Check: can the user name a specific alternative and its comp? If not, the first step is generating options, not deciding.
2. **Counter = 2 × target − offer.** Offer 100k, target 112k, counter 124k: negotiations gravitate toward the midpoint of the two stated numbers, so countering at your target guarantees landing below it.
3. **Switchers outprice stayers.** Atlanta Fed Wage Growth Tracker: job switchers beat stayers by roughly 1-2 percentage points of annual wage growth in most years. This is the base-rate argument behind the 18-24 month market check even when content.
4. **One-variable transitions.** Per move, change role OR industry OR track (IC to manager), not two. Each simultaneous change resets leverage to beginner on that axis; two at once typically costs both comp and title.
5. **Promotion is a lagging indicator.** You get promoted for having already done the next level's job for 6-12 months with witnesses outside your team. If nobody above your manager can describe your work, the packet fails at calibration.
6. **Negotiate the package, not the base.** Typical employer flexibility, most to least: sign-on bonus, equity, start date and vacation, title and review timing, base. Sign-on is a one-time cost to them; moving base reprices their whole band.
7. **Reversibility sets the risk bar.** If a move can be undone within about 12 months (boomerang hire, internal transfer back, contract work), bias toward acting; irreversible moves (relocation with family, visa changes, walking away from a cliff) get the full BATNA-plus-runway treatment.
8. **Resign only on paper.** A verbal offer is a mood; resign only on a written offer with contingencies (background check, references) cleared. A rescind after resignation is a self-inflicted layoff.

## The Decision Razor

Diagnose before prescribing; a bad manager and a bad career have opposite fixes.

- (a) Would a different manager fix this? Internal transfer before quitting (`promotion.md`). (b) Would the same role at a better company fix it? Switch companies, keep the role (Rule 4). (c) Does the work itself drain you even in good weeks, for 3+ months? Pivot, planned as a one-variable move (`pivots.md`).
- Quitting without an offer requires runway of at least 2× realistic search time. Senior searches commonly run 3-6 months, so hold 6-12 months of expenses in cash, not "some savings"; executive searches run longer — scale the same formula (`executive.md`).
- Tenure math: sunk years are not an asset; unvested equity is. Compute the dollar cost of leaving before the next vest date (`equity.md`) and treat only that number as the price of leaving.

## Offer Response In Brief

Full sequence in `offers.md`; the spine:

1. Everything in writing: base, bonus target with payout history, equity grant with vest schedule and cliff, sign-on with clawback terms, refresher policy.
2. Compute annualized total comp yourself; recruiters quote best case.
3. Set target from the market band (`market.md`), never from current comp. "Current plus 15%" is an anchor, not a target.
4. Counter once at 2 × target − offer (Rule 2), justified with one sentence of market data, never personal need.
5. Base capped? Walk the flexibility ladder in Rule 6 order.

Internal negotiation is a different game: performance already known, peer equity beats market rate, and you need a champion in the room, not just a request (`promotion.md`). Never wave an external offer you are unwilling to take.

## Output Gates

Before delivering career advice, check:

- Did I get current total comp, market band, and live alternatives before recommending any number or any stay/quit call?
- Is every counter I proposed computed as 2 × target − offer, not the midpoint of the visible range?
- Did I check unvested equity and cliff dates before endorsing a departure timeline?
- When no live alternative exists, did I recommend generating a BATNA instead of deciding?
- If `visa_dependent` or a non-US `region` applies, did I adjust legal defaults and timelines (`layoffs.md`)?
- Is the recommendation scored against the values in `profile.md`, not against brand prestige?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/career/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| region | US \| EU \| UK \| other | US | Switches employment-law defaults in `layoffs.md`: at-will vs statutory notice, severance norms, non-compete enforceability |
| career_stage | early \| mid \| senior \| executive | mid | Routes director-and-above questions to `executive.md`; scales search-time and runway estimates in The Decision Razor |
| risk_posture | conservative \| moderate \| aggressive | moderate | Conservative doubles runway floors and defaults against irreversible moves (Rule 7); aggressive accepts reversible bets at 1× runway |
| visa_dependent | bool | false | Adds immigration clocks to every timeline: layoff grace periods, job-change risk, start-date and termination-date negotiation |

Preference areas to record as the user reveals them:

- **comp philosophy** — cash vs equity weighting, appetite for private-company paper; affects offer scoring in `offers.md` and equity discounting in `equity.md`
- **constraints** — location and remote requirements, excluded industries, family or caregiving limits; affects option generation before any stay/leave call
- **values ranking** — what "better" means (comp, learning, autonomy, mission, hours), stored ranked in `profile.md`; affects how offers and stay/leave options are scored
- **coaching style** — frameworks only vs drafted word-for-word scripts, blunt vs cushioned delivery; affects the format of every negotiation deliverable

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Accepting on the call | Peak-emotion decision at their anchor | 48 hours and written details, always |
| Naming your number first | Anchors at your guess of their band, usually low | Deflect once; if forced, range with target at the bottom |
| Comparing offers on year-1 base | Bonus reality, vest schedule, and refreshers dominate by year 3 | Normalize to 4-year total value (`offers.md`) |
| Resigning to force a counteroffer | Root cause persists and you are flagged as flight risk | Resign only when ready to leave |
| "I have invested 5 years here" | Sunk cost; tenure is not an asset, unvested equity is | Price only the forward-looking cost of leaving |
| Chasing title over scope | Inflated title with unchanged scope fails the next interview loop | Trade title for scope, budget, or reports |
| Calling a mentor a sponsor | Advice does not move calibration decisions | Verify who speaks for you in the room (`promotion.md`) |
| Negotiating base only | Base is their stickiest number | Sign-on, equity, dates, title first (Rule 6) |
| Interviewing only when desperate | Desperation prices in; the band is stale exactly when you need it | Market check on elapsed time, not unhappiness (`market.md`) |
| Prestige capture | Optimizing for logo approval over fit compounds misery | Score offers against stored profile values, not brand names |

## Where Experts Disagree

- **Passion-first vs skill-first**: both schools hold conditionally. Under about 5 years of experience, skills compound faster than self-knowledge, so bias skill-first (the career-capital position, Newport); with rare skills banked, passion picks between good options.
- **Generalist vs specialist**: specialize while the field expands (early markets pay depth); generalize as it consolidates (mature markets pay range and management).
- **Loyalty premium**: tenure-track systems (government, academia, some East Asian conglomerates) genuinely pay tenure; the switcher math of Rule 3 is calibrated to open-market private sectors and reverses there.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/career (install if the user confirms):
- `job-search` — running the pipeline: applications, company research, interview prep
- `resume` — when the decision is made and materials need targeting
- `negotiate` — negotiation mechanics beyond comp: limits, principals, approvals
- `comp-design` — the employer side: designing base, bonus, and equity mix

## Feedback

- If useful, star it: https://clawic.com/skills/career
- Latest version: https://clawic.com/skills/career

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/career.
