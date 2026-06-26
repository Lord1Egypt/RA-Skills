# Feedback Clustering Guide

Raw feedback is noisy, duplicated, and mixes symptoms with causes. This guide turns it into clean, weighted, actionable themes before you score anything. Garbage clusters produce garbage rankings.

---

## 1. Normalize first

Get every channel into one table with the same shape:

| Column | Example | Why it matters |
| --- | --- | --- |
| `source` | reviews / survey / support / returns / social | Lets you weight by reliability and spot channel bias |
| `date` | 2026-05-12 | Trend detection and recency |
| `verbatim` | "shade arrived shattered" | Keep the real words for quotes |
| `product` / `category` | Glass pendant / Lighting | Routes to the right owner |
| `journey_stage` | pre-purchase / checkout / delivery / use | "Confusing" means different things at different stages |
| `customer_value` | LTV tier or order value | Weighting (see §4) |
| `raw_tag` | bulb-not-included | First-pass label before clustering |

Strip noise: shipping carriers you don't control, off-topic praise, spam. Note what you removed so coverage stays honest.

---

## 2. De-duping

Count **distinct issues**, not raw rows.

- **Same customer, same issue, multiple channels:** one customer who left a review *and* opened a ticket about the broken shade = **1 mention**. Match on customer ID / email / order number.
- **Same customer, repeat contacts:** three follow-up emails on one problem = 1 mention.
- **Boilerplate / templated text:** copy-paste return reasons or canned survey prompts — count the underlying issue once per customer, not once per occurrence.
- **Bots and incentivized reviews:** flag and exclude obvious review-incentive language and duplicate near-identical text.

A good rule: **one customer can contribute at most one mention per theme.** This single rule prevents the loudest customer from inflating a theme.

---

## 3. Tagging taxonomy

Build a shallow, consistent two-level taxonomy. Level 1 = area (owner-aligned); Level 2 = specific issue.

```
Product Quality
  ├─ defect-on-arrival
  ├─ durability
  └─ material-mismatch
Sizing & Fit
  ├─ runs-small
  ├─ inconsistent-across-styles
  └─ size-chart-wrong
PDP / Information
  ├─ missing-spec (e.g. bulb not included)
  ├─ misleading-imagery
  └─ compatibility-unclear
Checkout & Payment
  ├─ payment-method-fails
  ├─ promo-code-broken
  └─ slow/erroring
Fulfillment & Returns
  ├─ shipping-damage
  ├─ slow-shipping
  ├─ return-cost
  └─ wrong-item
Post-purchase / Use
  ├─ assembly-confusing
  └─ instructions-missing
```

Rules:
- **Each theme maps to one owner and one decision.** If a tag would route to two teams, split it.
- **8-20 active themes** for a mid-size store. Fewer = mega-buckets; many more = unactionable fragmentation.
- **Lock the taxonomy** for a cycle so counts are comparable; add new tags deliberately and note them in the changelog.

---

## 4. Weighting by source reliability and customer value

Not all mentions are equal. Apply weights *transparently* — show both raw count and weighted count.

**Source reliability** (how representative / actionable):

| Source | Reliability | Note |
| --- | --- | --- |
| Return-reason codes | High | Backed by money and action, not just opinion |
| Post-purchase survey | High | Sent to all buyers; less self-selection |
| Support tickets | Medium-high | Real problems, but skews to friction |
| On-site / marketplace reviews | Medium | Skews to extremes (5★ and 1★) |
| Social DMs / comments | Low-medium | Loudest-voice, hard to verify |

**Customer value:** weight a Blocker from high-LTV / high-AOV customers more heavily — losing them costs more. A practical approach: multiply mention count by a value factor (e.g. VIP ×1.5, standard ×1.0) only for severity-driven decisions, and always disclose the multiplier. Don't over-engineer; weighting matters most when raw counts are close.

---

## 5. Symptom vs root cause

Customers describe **symptoms**; you must score **root causes**, or you'll fix the wrong thing.

- "Checkout is broken" (symptom) → the real cause might be a failing Apple Pay token, a broken promo field, or a slow third-party script. Each has a different owner.
- "I returned it, the site is confusing" (symptom) → root cause is often an inaccurate size chart, not the return UX.
- Technique: for each cluster, ask **"why did the customer end up saying this?"** until you reach something a team can actually change. Tag the cluster by root cause, but keep symptom verbatims for quotes.
- When one root cause spawns several symptom themes, merge them under the cause and note the combined evidence — this often surfaces a higher-priority item than any single symptom suggested.

---

## 6. Severity rubric

Apply consistently. Severity, not frequency, often decides rank.

| Severity | Definition | Examples |
| --- | --- | --- |
| **Blocker** | Prevents purchase or use; safety, legal, or guaranteed loss | Checkout fails, item arrives broken/unusable, safety hazard |
| **Major** | Significant friction or a clear churn/return driver; workaround is costly | Sizing runs small, key spec missing from PDP, paid-return frustration |
| **Minor** | Annoyance; a workaround exists | Assembly guide unclear, copy slightly off |
| **Cosmetic** | Polish; low or no functional impact | UI nit, notification frequency, wording preference |

Tie-break rule for scoring: when two items score equally, the higher severity wins (see SKILL.md Example 2, where a Blocker broke a tie).

---

## 7. Handling small-sample noise

Vivid anecdotes feel like trends but aren't.

- **Set an evidence threshold** before ranking (e.g. minimum 5-10 distinct mentions to enter the scored roadmap; lower for Blockers, since one verified safety/checkout failure is enough).
- **Park, don't rank, low-n items.** Put them in the monitor list with a promotion trigger ("re-evaluate if mentions exceed 10 next cycle").
- **Watch the trend, not just the level.** A theme rising from 3 → 9 → 18 across cycles deserves attention even before it's huge; a flat n=4 probably doesn't.
- **Beware recency/seasonality spikes.** A burst after one bad shipment isn't a structural problem — check whether it persists.
- **Never present n=2 as a fact.** Label sample size whenever it's thin so readers calibrate trust.
