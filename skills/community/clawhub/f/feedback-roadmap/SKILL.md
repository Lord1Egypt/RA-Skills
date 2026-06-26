---
name: feedback-roadmap
description: Convert customer feedback, review themes, and complaint clusters into product improvement priorities with clear rationale and urgency ranking.
---

# Feedback Roadmap

This skill turns scattered ecommerce customer feedback — reviews, post-purchase surveys, support transcripts, return-reason codes, and social DMs — into a single prioritized improvement roadmap. The output is a ranked list of changes with frequency and severity evidence, a transparent priority score, a suggested owner, and a one-line rationale each. Use it when you have a pile of qualitative signal and need to decide *what to fix first* without it becoming a loudest-voice argument.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
| --- | --- | --- | --- |
| Signal sources to include | 4+ independent sources (reviews, surveys, support, returns, social) cross-checked against each other | 2-3 sources covering both happy and unhappy paths | A single channel (e.g. only 5-star reviews or only the loudest tickets) |
| Clustering granularity | Themes map to one actionable owner + decision; 8-20 clusters for a mid-size store | A handful of broad buckets with sub-tags noted | One mega-bucket ("UX is bad") or 80 hyper-specific clusters nobody can act on |
| Prioritization framework | RICE or weighted impact/effort/urgency with documented weights | ICE or a clean Impact/Effort 2x2 | Gut-feel ordering with no recorded scores |
| Urgency scoring | Tied to objective triggers (revenue at risk, safety, churn, legal, seasonal deadline) | Relative high/med/low agreed by 2+ stakeholders | "Everything is urgent" or urgency = whoever complained loudest |
| Owner assignment | Named person/team who controls the fix, accepts the item, has capacity | A function (e.g. "Merch") with a follow-up to name a person | Unassigned, or "everyone," or assigned to a team that can't actually ship it |
| Evidence threshold | Quantified frequency + severity + at least 2 verbatim quotes per theme | Frequency count + one quote | "Customers hate this" with no count and no quote |
| Severity rubric | Blocker / Major / Minor / Cosmetic applied consistently with a written rubric | Severity tagged but rubric loosely applied | Severity = personal annoyance level |
| Review cadence | Refreshed on a fixed cadence (e.g. monthly) with deltas vs last cycle tracked | Refreshed each planning cycle | One-and-done; never revisited |
| Sample-size handling | Small clusters flagged as "monitor," not ranked as facts | Note added when n is low | Acting on n=2 as if it were a trend |

## Solves

- **Feedback graveyard**: hundreds of reviews, tickets, and survey rows that nobody reads or acts on because there's no synthesis layer.
- **Loudest-voice bias**: a single angry customer or one viral DM driving roadmap decisions while a quiet, high-frequency friction point goes unfixed.
- **Severity blindness**: treating a cosmetic typo complaint and a checkout-blocking bug as the same "1 mention."
- **No shared prioritization logic**: every planning meeting re-litigates priorities from scratch because there's no recorded scoring.
- **Orphaned action items**: improvements that everyone agrees on but nobody owns, so they never ship.
- **Symptom chasing**: fixing the thing customers named ("the button") instead of the root cause ("sizing chart is wrong, so people return and then complain about checkout").
- **Stale roadmaps**: a priority list built once in Q1 that no longer matches what customers are saying in Q3.

## Workflow

1. **Collect & normalize signals.** Pull raw feedback from every available channel: reviews (on-site + marketplace), post-purchase NPS/CSAT survey free-text, support chat/email transcripts, return-reason codes, cancellation reasons, and social DMs/comments. Normalize into one table with columns: `source`, `date`, `verbatim`, `product/category`, `customer_value` (e.g. LTV tier or order value), and `raw_tag`. De-duplicate the same customer raising the same issue across channels so you don't double-count.

2. **Cluster into themes.** Group normalized rows into actionable themes using a consistent tagging taxonomy (see `references/feedback-clustering-guide.md`). Each theme should map to a single decision and owner. Separate symptom from root cause — "checkout is slow" and "PayPal button missing" may be the same root cause or two different ones; tag accordingly.

3. **Quantify frequency & severity.** For each theme, count distinct mentions (not raw rows) and assign a severity using a written rubric: Blocker (prevents purchase/use, safety, legal), Major (significant friction or churn driver), Minor (annoyance, workaround exists), Cosmetic (polish). Weight mentions by source reliability and customer value where it matters — a blocker reported by 12 high-LTV customers outranks a cosmetic gripe from 40 one-time buyers.

4. **Score priority (impact / effort / urgency).** Apply a single documented framework — RICE, ICE, or weighted impact/effort/urgency (see `references/prioritization-frameworks.md`). Estimate each factor from the data, not vibes: reach from mention frequency and traffic, impact from severity and revenue at risk, effort from engineering/ops sizing, urgency from objective triggers (seasonal deadlines, escalating trend, legal/safety). Show the math so the ranking is auditable.

5. **Assign owners & rationale.** Give every ranked item a named owner or team that actually controls the fix and has the capacity to take it. Write a one-line rationale that ties the score to evidence ("Ranked #1: 47 mentions, Major severity, ~$18k/mo returns attributable; low effort config change"). The owner should be able to read the row and start work.

6. **Build the roadmap doc.** Assemble the deliverable using `references/output-template.md`: exec summary, signal-source inventory, theme cluster table, prioritized roadmap table, and a parking-lot/monitor section for low-confidence or low-priority items. Keep verbatim quotes attached so stakeholders feel the customer pain, not just the number.

7. **Set review cadence.** Decide how often the roadmap refreshes (monthly is typical for an active store; quarterly minimum). On each refresh, recompute scores, track deltas vs last cycle, promote items out of the monitor list when they cross the evidence threshold, and close out shipped items with a note on whether the underlying complaints dropped.

## Example 1

**Store:** *Lumen & Loft*, a mid-size DTC home-lighting brand. ~9,000 orders/quarter, AOV $140. Pulled feedback from on-site reviews (Q1), post-purchase CSAT free-text, Gorgias support tickets, and return-reason codes.

**Normalized & clustered themes (distinct mentions, 90-day window):**

| Theme | Mentions | Severity | Notes |
| --- | --- | --- | --- |
| Bulbs not included / "needs separate bulb" surprise | 61 | Major | Top return reason; PDP doesn't state bulb type/inclusion clearly |
| Dimmer compatibility unclear | 38 | Major | Customers buy, then find their dimmer flickers |
| Shipping damage (glass shades) | 29 | Blocker | Arrives broken; immediate refund/replace cost |
| Assembly instructions confusing | 22 | Minor | Workaround exists (YouTube), but adds friction |
| Color temperature looks "yellower" than photos | 17 | Minor | Expectation mismatch on PDP imagery |
| Wishlist/save-for-later missing | 9 | Cosmetic | Nice-to-have, low signal |

**Scoring with RICE** (Reach = est. customers affected/quarter; Impact 0.25-3; Confidence 0-1; Effort in person-weeks). Score = Reach × Impact × Confidence ÷ Effort.

| Item | Reach | Impact | Conf | Effort | RICE |
| --- | --- | --- | --- | --- | --- |
| Add bulb-inclusion + bulb-type module to PDP | 1,400 | 2 | 0.9 | 1 | (1400×2×0.9)/1 = **2,520** |
| Dimmer compatibility checker on PDP | 900 | 2 | 0.8 | 3 | (900×2×0.8)/3 = **480** |
| Upgrade glass-shade packaging | 600 | 3 | 0.9 | 2 | (600×3×0.9)/2 = **810** |
| Rewrite + illustrate assembly guide | 500 | 1 | 0.8 | 2 | (500×1×0.8)/2 = **200** |
| Add accurate color-temp swatches to PDP | 400 | 1 | 0.7 | 1 | (400×1×0.7)/1 = **280** |
| Wishlist feature | 300 | 0.5 | 0.6 | 4 | (300×0.5×0.6)/4 = **22.5** |

**Resulting ranked roadmap:**

| Rank | Item | Score | Owner | Rationale |
| --- | --- | --- | --- | --- |
| 1 | PDP bulb-inclusion module | 2,520 | Merch / PDP team | Highest reach, low effort, directly cuts the #1 return reason |
| 2 | Glass-shade packaging upgrade | 810 | Ops / Fulfillment | Blocker severity; broken arrivals are pure refund cost |
| 3 | Dimmer compatibility checker | 480 | Product/Eng | High-friction pre-purchase confusion; medium effort |
| 4 | Color-temp swatches | 280 | Merch / Photo | Cheap expectation-setting fix; reduces "looks wrong" returns |
| 5 | Assembly guide rewrite | 200 | CX / Content | Real but lower-impact; workaround exists |

Wishlist drops to the **monitor** list (n=9, low score). Note the bulb-inclusion fix and color-temp swatches together attack the return-rate problem from two angles.

## Example 2

**Store:** *PaceForge*, a running-apparel store. ~25,000 orders/quarter, AOV $65. Sources: Trustpilot + on-site reviews, NPS survey free-text, Instagram DMs, and return-reason codes. Here we use **weighted impact/effort/urgency** because a seasonal deadline (spring marathon season) makes urgency a first-class factor.

Weights agreed by team: **Impact 50%, Urgency 30%, Effort 20% (inverted — low effort scores high).** Each factor scored 1-5. Score = (Impact×0.5) + (Urgency×0.3) + (EffortInverse×0.2), all on a 5-point scale.

**Clustered themes (distinct mentions, 90-day):**

| Theme | Mentions | Severity |
| --- | --- | --- |
| Sizing runs small / inconsistent across styles | 188 | Major |
| Returns label costs $7 (customer-paid) frustration | 74 | Major |
| Out-of-stock on popular sizes during launches | 53 | Major |
| Sweat-wicking claim doesn't match experience | 31 | Minor |
| Checkout rejects some Apple Pay cards | 19 | Blocker |
| App push notifications too frequent | 14 | Cosmetic |

**Scoring (5-point factors; EffortInv = 6 − effort):**

| Item | Impact | Urgency | Effort | EffortInv | Weighted Score |
| --- | --- | --- | --- | --- | --- |
| Per-style size guide + "true to size" review tags | 5 | 4 | 3 | 3 | (5×.5)+(4×.3)+(3×.2)=**4.3** |
| Fix Apple Pay card rejection | 4 | 5 | 2 | 4 | (4×.5)+(5×.3)+(4×.2)=**4.3** |
| Free returns for loyalty members | 4 | 4 | 4 | 2 | (4×.5)+(4×.3)+(2×.2)=**3.6** |
| Size-level back-in-stock alerts | 4 | 5 | 4 | 2 | (4×.5)+(5×.3)+(2×.2)=**3.9** |
| Clarify sweat-wicking copy + add tech spec | 2 | 2 | 2 | 4 | (2×.5)+(2×.3)+(4×.2)=**2.4** |
| Notification frequency controls | 2 | 1 | 3 | 3 | (2×.5)+(1×.3)+(3×.2)=**1.9** |

**Resulting ranked roadmap** (tie at 4.3 broken by severity — Apple Pay is a Blocker):

| Rank | Item | Score | Owner | Rationale |
| --- | --- | --- | --- | --- |
| 1 | Fix Apple Pay card rejection | 4.3 | Eng / Payments | Blocker losing orders silently; max urgency before marathon-season traffic |
| 2 | Per-style size guide + fit tags | 4.3 | Merch + CX | 188 mentions, top return driver; urgent before peak; medium effort |
| 3 | Size-level back-in-stock alerts | 3.9 | Eng / Growth | Captures demand lost at launch; high urgency for spring drops |
| 4 | Free returns for loyalty members | 3.6 | Finance + CX | Real frustration but cost/effort high; pilot to one tier first |
| 5 | Sweat-wicking copy fix | 2.4 | Content | Low-cost expectation fix; do opportunistically |

Notification controls go to the **monitor** list. Note the Apple Pay item had only 19 mentions but ranks #1 — severity and urgency, not raw count, carried it. This is exactly why frequency alone is a weak prioritizer.

## Common Mistakes

1. **Counting raw rows instead of distinct issues.** One customer emailing three times about the same broken shade is one issue, not three. *Fix:* de-dup by customer + theme before counting.
2. **Ranking on frequency alone.** A blocker with 19 mentions can outrank a cosmetic gripe with 188 (see Example 2). *Fix:* always combine frequency with severity and urgency.
3. **Ignoring the silent majority.** Reviews and tickets over-represent extremes. *Fix:* pull from neutral channels too (surveys to all buyers, return codes from everyone) and note channel bias.
4. **Mega-buckets.** "Improve UX" can't be owned or shipped. *Fix:* split until each theme maps to one decision and one owner.
5. **Fixing symptoms, not root causes.** Customers complain about "checkout," but the root cause is a confusing size chart driving returns and rage. *Fix:* trace each theme to a root cause before scoring.
6. **Effort estimated by the wrong people.** PMs guessing eng effort produces fantasy scores. *Fix:* get effort sizing from the team that would build it.
7. **Unowned items.** A ranked list with no owners is a wish list. *Fix:* assign a named owner who controls the fix and has capacity before publishing.
8. **Treating small samples as trends.** Acting on n=2 because it was vivid. *Fix:* set an evidence threshold; park low-n items in "monitor."
9. **Hidden weights / unaudited scores.** "Trust me, this is #1." *Fix:* record the formula, factors, and inputs so anyone can recompute.
10. **One-and-done.** Building the roadmap once and never refreshing as feedback shifts. *Fix:* set a cadence and track deltas each cycle.
11. **Dropping the verbatims.** A spreadsheet of numbers loses the human pain and stakeholder buy-in. *Fix:* keep 2+ representative quotes per theme.
12. **Mixing pre-purchase and post-purchase signal without labeling.** "Confusing" at the PDP vs "confusing" in assembly need different owners. *Fix:* tag the customer journey stage.

## Resources

- `references/output-template.md` — Fill-in template for the finished roadmap: exec summary, signal inventory, theme cluster table, prioritized roadmap table, and parking-lot/monitor section.
- `references/prioritization-frameworks.md` — Formulas, numeric examples, and when-to-use guidance for RICE, ICE, Impact/Effort 2x2, weighted urgency scoring, and a Kano must-have/delighter lens.
- `references/feedback-clustering-guide.md` — How to normalize and cluster raw feedback: de-duping, tagging taxonomy, symptom vs root cause, source/value weighting, severity rubric, and small-sample handling.
- `assets/quality-checklist.md` — A pre-publish checklist across signal coverage, clustering, quantification, prioritization rigor, evidence, ownership, clarity, and cadence.
