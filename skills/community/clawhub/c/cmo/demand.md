# Demand Generation

## Pipeline Math (canonical)

```
Leads needed = new revenue target ÷ ACV ÷ win rate ÷ lead→opp rate
```

Worked example: $2M new ARR at $25k ACV → 80 deals. At 20% win rate → 400 opportunities. At 10% lead→opp → 4,000 qualified leads ≈ 333/month. If current volume is 100/month, the plan must name what closes the 3.3× gap — a channel, a conversion rate, or ACV — not "more content."

- Use your own trailing 2-4 quarters of funnel rates; industry benchmarks are sanity checks only.
- No history yet → run the math twice with a pessimistic/optimistic pair, never one guess.
- Pipeline coverage target = 1 ÷ win rate. The folkloric "3× coverage" assumes ~33% win rate; applying it with a 15% win rate under-builds pipeline by roughly half.
- Run the math *backwards* too: at your current lead volume and rates, what revenue does the plan actually produce? The gap between that number and the target is the honest ask for budget or headcount.
- Lag matters more than volume: if the sales cycle is 90 days, leads generated in the last month of the quarter cannot close in it. Build the plan on cohorts by creation date, not on the quarter's total.

## Demand Capture vs. Demand Creation

| | Capture | Creation |
|---|---------|----------|
| Reaches | The ~5% in-market now (95:5 → SKILL.md Rule 4) | The 95% who will buy later |
| Channels | Paid search, review sites, retargeting, comparison SEO | Social, podcasts, events, brand, teaching content |
| Feedback loop | Days-weeks, attributable | Months-quarters, mostly unattributable |
| Failure mode | Saturates: spend rises, conversions plateau, CPCs climb | Declared "not working" and cut right before it compounds |

If paid search spend rises while conversions plateau, you have saturated existing demand — the incremental dollar belongs in creation, not in higher bids.

Ceiling check before funding capture: category search volume × realistic click share × conversion rate sets the maximum pipeline capture can ever produce. If that ceiling is below the target, no bid strategy closes the gap and the plan needs creation, outbound, or a new segment.

## Channel Selection

Bullseye (SKILL.md Rule 5): list channels where the ICP demonstrably is, run ~3 cheapest tests in parallel with written kill lines (Rule 6), commit to the winner.

| Channel | Best for | Time to signal | Watch for |
|---------|----------|----------------|-----------|
| Paid search | Provable existing demand, high intent | Days-weeks | Branded-term spend inflating ROAS (`paid.md`) |
| Paid social | Creative-led creation, retargeting | Weeks | Fatigue: frequency up + CTR down → rotate creative |
| SEO/content | Compounding capture and creation | Months, not weeks | Traffic to pages no buyer reads (`content.md`) |
| Outbound with marketing air cover | High ACV, definable account list | Weeks-months | Cold volume without warm-up burns deliverability |
| Events and field | Enterprise trust, few large deals | Months | Counting badge scans as leads (`b2b.md`) |
| Partnerships and integrations | Borrowed trust and distribution | Months | Roadmap dependence on the partner |
| Review sites and marketplaces | Late-stage capture, comparison shoppers | Weeks | Pay-to-play placement rented, not owned |
| Community and creators | Trust at low CPM in narrow niches | Months | Norms punish extraction; contribute before linking |
| Referral programs | Cheap expansion of an existing base | Weeks after critical mass | Rewarding referrers who would have referred anyway |

Default: if search demand for your category exists, start with capture (paid search + bottom-funnel SEO). New category with no search demand → creation only, and budget a longer runway.

**Finding the shortlist, cheaply**: ask the last 20 customers where they learned about the category (not about you); look at where competitors spend consistently for more than two quarters (persistence implies it works); check which communities the ICP posts in unprompted; count the channels your team can actually staff. Anything that survives all four is a test candidate.

## Offers, Not Just Channels

The offer usually moves conversion more than the channel does. Ranked by intent captured:

| Offer | Intent | Use when |
|-------|--------|----------|
| Demo / talk to sales | Highest | ACV justifies a human; buyer expects a conversation |
| Free trial or free tier | High | Product demonstrates value inside days without help (`product-led.md`) |
| Assessment, audit, calculator | Medium-high | Buyer suspects a problem but cannot size it |
| Webinar or workshop | Medium | Complex product, committee purchase |
| Template, tool, original research | Low-medium | Building a list in the 95%; expect nurture, not a call |
| Newsletter subscription | Low, but durable | Owned-audience compounding (Rule 7) |

Rule: never route a low-intent offer straight to a salesperson. A person who downloaded a template is curious, not buying — an SDR call converts curiosity into an unsubscribe.

## Lead Scoring and Routing

Two axes only — fit (ICP match: size, industry, role) and intent (behavior: demo request, pricing views, repeated returns):

| | High intent | Low intent |
|---|-------------|------------|
| **High fit** | Route to sales inside the SLA — response speed is conversion | Nurture + targeted outbound |
| **Low fit** | Self-serve path or polite deflect; don't burn AE time | Suppress; mailing them buys spam complaints |

Default at low volume: skip the point model — a human eyeballing every signup beats a premature scoring system, and teaches you the fit signals you will later automate.

Response speed is the highest-leverage operational variable in the whole funnel: inbound demo requests decay fast, so measure median time-to-first-touch weekly and treat a regression as an incident, not a report line.

The MQL definition is a written contract with sales, with example leads attached, renegotiated quarterly. If sales routinely ignores MQLs, the definition or the trust is broken — fix the definition before demanding follow-up.

**Two-way SLA, written**: marketing commits to volume, fit criteria, and enrichment completeness; sales commits to a touch window, a minimum number of attempts, and a disposition reason on every rejected lead. Without the disposition reason, no diagnosis is possible next quarter (`diagnose.md`).

## The Demand Waterfall

Model the funnel with stage-to-stage conversion *and* stage duration, both from your own data:

```
Visitors → Leads → MQL → SQL/Accepted → Opportunity → Closed-won
```

- Every stage needs one owner and one entry definition. Two teams disagreeing about where "opportunity" starts is the source of most forecast fights.
- Track by creation cohort, not by close date, or improvements look like regressions for one full sales cycle.
- Report the stage that constrains the whole chain. Optimizing a 60% stage while a 3% stage sits upstream is arithmetic malpractice.

## Campaign Brief (copyable)

```
Objective: [one measurable pipeline goal]
Audience: [segment + why now]
Message: [the one claim, with proof point]
Offer: [what the audience gets, and its intent level]
Channels: [where, and the owned-asset side effect — Rule 7]
Kill line: [budget cap / minimum result / decision date]
Success metrics: [primary = pipeline; secondary]
Owner + review date: [name, date]
```

## Referral and Word of Mouth

The cheapest channel is the one already running unmeasured. Instrument it before incentivizing it: add the self-reported source field (`measurement.md`), then ask happy customers directly at the moment of value, not on a schedule. Incentives change the mix — cash rewards attract referrers whose referrals convert worse; give the reward to the *recipient* (a discount or extended trial) to keep the recommendation credible. Never gate a referral program behind an account requirement the referrer's friend does not have yet.

## Review Sites and Marketplaces

For most B2B categories, review sites are late-funnel capture at high intent and rented placement at high cost. Rules: earn the reviews before buying the placement (a category presence with three reviews converts worse than no presence); ask for reviews at a value moment via a neutral link, never with a script or a reward that violates the site's terms (`compliance.md`); and treat the comparison pages the site ranks for as competitors to your own comparison pages (`content.md`).
