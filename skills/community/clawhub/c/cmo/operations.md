# Marketing Operations — Budget, Economics, Team, Stack, Agencies

## Budget: Derive, Then Benchmark

Derivation (canonical):

```
Budget = pipeline target × historical $ spend per $ pipeline, summed by channel
```

The pipeline target comes from the pipeline math in `demand.md`. No spend history yet → budget the channel tests with their kill lines (SKILL.md Rule 6) plus one owned-audience investment, and build the ratio within two quarters.

Sanity benchmarks — never the starting point: Gartner's CMO spend survey has ranged roughly 6-11% of company revenue in recent years for established companies; venture-stage SaaS routinely runs far higher because it buys growth ahead of revenue. Quoting either as "the right number" without the derivation is the tell of a template plan.

Portfolio split heuristic: ~70% proven channels / ~20% emerging / ~10% experiments. This axis is orthogonal to brand vs. activation (60/40 average, B2B ~46/54 — canonical in SKILL.md Rule 3): proven and experimental dollars each carry their own brand and activation share.

Separate the budget into three buckets when presenting it: **committed** (people, tools, contracts — cannot be cut this quarter), **working media** (the part that actually buys reach), and **test**. Most "marketing budget" arguments are really about the ratio of committed to working, and nobody notices until it is drawn.

## Defending the Budget in a Cut

When the cut order arrives, bring three scenarios, not one objection: −10%, −25%, −40%, each with the pipeline consequence quantified through the same formula above and a named read date. Cut in this order — experiments, then emerging channels, then frequency on proven channels, then reach; production of new brand assets before distribution of proven ones (`brand.md`). Name what stops entirely rather than thinning everything: a program at 60% of its budget usually produces far less than 60% of its result.

## Unit Economics the CMO Owns

- CAC payback (months) = CAC ÷ (monthly revenue per account × gross margin). Example: CAC $6,000, $500/month account, 80% margin → 6,000 ÷ 400 = 15 months.
- Common SaaS screens: payback under ~12 months is strong; beyond ~24 months is alarming outside enterprise ACVs; LTV:CAC ≥ 3 is the conventional filter. These are screens, not goals — you can pass them by cutting all demand-creation spend and starve next year's 95% (SKILL.md Rule 4).
- Blended CAC (all customers ÷ all spend) vs. paid CAC (paid-sourced only): blended hides paid inefficiency behind word of mouth. Report both; make paid decisions on paid CAC.
- Fully loaded CAC includes salaries, tools, and agency fees — not just media. Reporting media-only CAC to a board that computes it fully loaded is how a credibility problem starts.
- Watch the *direction of the marginal* CAC, not the average: the average stays comfortable long after the next dollar has stopped working (`diagnose.md`).

## Team Structure

| Stage | Team | Rule |
|-------|------|------|
| Seed | One generalist doer + freelancers | Match the hire to your one proven or likeliest channel; do NOT hire a VP to go find the channel |
| Series A | Head of marketing + 2-3 specialists | Specialists in the working motion, not full functional coverage |
| Series B | CMO + managers per function (demand, content, product marketing, ops) | Product marketing is usually the most under-hired function at this stage |
| Series C+ | Full teams per function | Ops/analytics becomes its own discipline |

Interfaces: with **sales** — shared lead definitions (MQL contract in `demand.md`), shared pipeline number, marketing sits in pipeline reviews. With **product** — product marketing owns launches (`launch.md`) and win/loss; feed win/loss into positioning (`positioning.md`) quarterly. With **finance** — one agreed definition of CAC, spend, and pipeline before the board deck, never during it. With **support and success** — they hold the complaint and churn vocabulary that should be shaping the message.

## Hiring Marketers

- Hire for the motion you have proven, not for the org chart you imagine. The most expensive mis-hire in marketing is a senior leader from a company three stages ahead, whose skill is running a machine you do not have yet.
- Work-sample over interview: a written teardown of your funnel, a real brief, or a critique of your positioning tells you more than any competency questionnaire.
- Ask for the *decisions* they made, not the results they were near: "what did you kill and why" separates operators from passengers.
- Generalists find channels; specialists scale them. Sequencing them the other way round burns two quarters.
- Every role needs one number it owns and one interface it maintains. A marketer with no number becomes a service desk.

## Stack

Buy in this order: CRM → analytics → email/automation → attribution and enrichment last. Selection rules:
- Integration with the CRM beats feature lists.
- Total cost includes implementation plus the human who runs it; every tool needs a named owner or it becomes shelfware.
- Tool markets churn — evaluate current options at purchase time instead of trusting any static vendor list.
- Data model before tooling: agree what an account, a lead, and a source *are* before buying anything that will encode the answer.
- Audit annually against usage: seats nobody logs into, overlapping tools bought by two teams, and contracts auto-renewing past their usefulness. Consolidation usually funds the next test budget.
- You own the accounts, pixels, audiences, domains, and creative files — never the agency (`paid.md`).

## Agencies

Use agencies for: specialized skills (paid media at scale, technical SEO audits), spike capacity, testing a channel before hiring for it. Keep in-house: strategy, positioning, daily creative voice, anything requiring tribal knowledge.

Working rules:
- The pitch team is senior; the delivery team often isn't. Bait-and-switch is the norm — name the delivery team in the contract.
- Agencies paid a % of ad spend are structurally incentivized to grow spend, not efficiency; tie fees to pipeline metrics or go flat-fee.
- Agencies run on your briefs; a vague brief buys expensive guessing (use the campaign brief in `demand.md`).
- Quarterly performance review against pre-agreed metrics, with a replacement trigger written down in advance.
- Write the offboarding into the onboarding: account ownership, data export, notice period, and a documented handover. The moment to negotiate an exit is before the relationship needs one.

## The Planning Calendar

| Cadence | Work |
|---------|------|
| Weekly | Operational dashboard, campaign vs. kill lines, lead SLA, pipeline review with sales |
| Monthly | Executive dashboard, spend vs. plan, budget reforecast, experiment log review (`measurement.md`) |
| Quarterly | Brand metrics, MQL definition renegotiation, win/loss synthesis, agency review, channel portfolio rebalance |
| Annually | Positioning revalidation, budget derivation from next year's targets, brand tracking wave, stack audit |

Anchor the annual plan to the company's planning cycle, and write the assumptions down separately from the numbers — next year you will need to know which assumption broke, not just that the number missed.
