# Diagnose — Symptom to Cause Before Spending

Work symptom-first. Each chain is ordered by probability, and every step is a check against data that already exists — not an opinion. Most "marketing isn't working" verdicts are a single funnel stage moving, and the stage everyone argues about is rarely the one that moved.

## The Universal First Three

1. **Reconcile the funnel.** Pull the last 4-8 quarters: visitors → leads → opportunities → wins → ACV. Find the stage whose *rate* changed, not the stage with the ugliest absolute number.
2. **Read 20 closed-lost reasons and 20 closed-won "why us", verbatim.** Message drift, a new competitor, and pricing objections appear here one to two quarters before they appear in a dashboard.
3. **Separate volume from rate.** Volume fell = supply/channel problem. Rate fell = fit, message, or product problem. Both fell at once, sharply, on one date = suspect instrumentation before strategy (`measurement.md`).

## Pipeline Is Down

1. **Tracking break.** A UTM change, a consent-banner rollout, a domain migration, or an ad-blocker shift zeroes a channel with no error anywhere in the dashboard. Test: does total session count reconcile with server logs or CRM-created records?
2. **Comparison base.** Compare to the same quarter last year, not to last quarter — most B2B calendars have a structural Q1 and Q3 dip.
3. **One channel or all of them?** One channel = auction price, algorithm change, or creative fatigue (`paid.md`). All channels = demand, positioning, or a category shift.
4. **Category demand itself.** Brand search volume and share of search are the leading indicators (Les Binet's share-of-search work: share of search tends to move ahead of share of market). Falling category search = a demand-creation problem; no campaign fixes it inside a quarter.
5. **Sales-side illusions.** Fewer reps, a longer cycle, or a stage-definition change reclassifies opportunities and makes marketing look responsible for an accounting change. Check headcount and stage definitions as of the same date.
6. **Only now** rebuild the plan — with the pipeline math (SKILL.md Rule 1) using this quarter's rates, not last year's.

## CAC Is Climbing

Chain, in order: saturation → creative fatigue → audience exhaustion → landing conversion decay → mix shift → margin change misread as CAC.

| Signal | Reading |
|--------|---------|
| Spend up, conversions flat, CPC/CPM up | Saturation of existing demand — the incremental dollar belongs in creation (`demand.md`) |
| Frequency up, CTR down, CPM stable | Creative fatigue — rotate creative before touching bids (`paid.md`) |
| CTR stable, conversion rate down | Page, offer, or audience quality — not the channel |
| Paid CAC up, blended CAC flat | Word of mouth is subsidizing paid; the channel is worse than the blended dashboard says (`operations.md`) |
| CAC up, ACV up proportionally | Not a problem — check CAC payback, which may have improved |

Test order: hold spend flat for one full cycle and re-read CAC; rotate creative; then run a geo holdout on the largest line (`measurement.md`).

## Traffic Up, Revenue Flat

1. **Funnel-stage mismatch**: the traffic is top-funnel and the site has no bottom-funnel pages to catch it (`content.md`, BOFU-first order).
2. **Wrong audience**: check whether new subscribers and signups match the ICP fields, not just the total. Traffic growth with zero ICP-match growth is writing for the wrong reader.
3. **Intent mismatch**: ranking for informational queries in a category where buyers search for comparisons and pricing.
4. **Conversion path**: is there a single click from the winning page to a next step? Most content programs never add one.
5. **Attribution blindness**: revenue may be arriving self-reported as "found you on Google" and being credited to direct (`measurement.md`).

## Sales Rejects the Leads

1. Pull 20 rejected leads and classify each: wrong fit, wrong timing, or duplicate/junk. The distribution names the fix.
2. Mostly wrong fit → the scoring model or the targeting is wrong (`demand.md`, fit × intent).
3. Mostly wrong timing → these are nurture, not rejects; the routing rule is wrong, not the lead.
4. Mostly junk → form quality, incentive-driven gated content, or bot traffic; add enrichment before routing.
5. Sales rejects everything, uniformly → this is a trust problem, not a lead problem. Renegotiate the MQL definition with example leads attached, and put a two-way SLA in writing.

## A Channel Plateaued

Check saturation before concluding failure: has spend at the current CAC been held flat for two full sales cycles? A channel with rising CAC and flat volume is saturated; a channel with flat CAC and flat volume is *capacity limited* — usually by creative volume, budget pacing, or the size of the addressable audience. Saturated → move the marginal dollar to a new test (Bullseye, SKILL.md Rule 5). Capacity limited → the fix is inside the channel, not a new one.

## The Launch Landed Flat

1. Was the audience there? Owned list size × open rate × click rate sets a ceiling no press hit can rescue.
2. Was it a launch or an announcement? A feature the ICP never asked for gets attention proportional to its relevance.
3. Was there a next step? Launches without a demo path, trial, or price convert curiosity into nothing.
4. Was it Tier-1 spend on a Tier-3 event? (`launch.md`)
5. Post-mortem within two weeks, while the data and the memories are both fresh.

## Brand Spend Is Under Attack

The attack always arrives as "we can't attribute it". Answer in this order: (a) show the metric brand is accountable for — prompted/unprompted awareness, share of search, direct and branded search volume, win rate against the named competitor; (b) show the window — brand compounds past six months, activation decays in weeks (Binet & Field); (c) offer the falsifiable test instead of the argument — a regional holdout with a pre-registered read date (`measurement.md`). Never defend brand spend with impressions.

## Email or Lifecycle Revenue Dropped

Inbox placement first, always: a deliverability collapse looks exactly like disinterest in the dashboard. Check the spam-complaint rate (keep it under 0.10%; 0.30% is the level major mailbox providers treat as unacceptable for bulk senders), authentication status (SPF, DKIM, DMARC), and whether a list import or a new sending domain preceded the drop (`lifecycle.md`). Only after placement is clean, look at content, cadence, and offer.

## Nobody Understands What We Do

Run the swap test (SKILL.md Rule 2) and the five-second test with five people in the ICP who have never seen the site: what does it do, who is it for, what does it replace? If two of three answers are wrong, it is positioning, not copy (`positioning.md`). Copy edits on broken positioning produce a nicer sentence that still fails.

## When You Are Truly Stuck

Talk to five customers who bought in the last 90 days and five who evaluated and chose otherwise. Ask what they were doing before, what triggered the search, who else they looked at, and what almost stopped them. Ten conversations reliably out-diagnose a quarter of dashboard archaeology — and the words they use become the next headline.
