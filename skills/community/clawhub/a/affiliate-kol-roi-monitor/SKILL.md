---
name: affiliate-kol-roi-monitor
description: Automate affiliate and KOL reconciliation, attribution, true ROAS, commission math, and renewal strategy. Use when the user has more than ~5 KOL or affiliate partners, needs real ROAS (not vanity clicks), must match orders to creators, settle commissions net of refunds, spot fake or low-quality traffic, or wants influencer performance reports and tiered renewal offers. Also trigger on affiliate payout disputes, UTM vs discount-code attribution, "which creator actually sold," commission spreadsheets, or CAC by creator — even if they only say "clean up our affiliate mess." Do NOT use for generic social media growth tips with no orders or payouts, pure content calendars without performance data, or single one-off creator contracts with no reconciliation need.
compatibility:
  required: []
---

# Affiliate & KOL ROI Monitor

You replace **manual commission runs**, **order-to-creator matching**, and **influencer performance reporting** with a repeatable workflow: **attribution data → net of refunds → profit-aware economics → tiered renewals**.

## Core workflow (always follow in order)

1. **Extract attribution data** — Map each order (or session) to a creator: discount codes, UTM (`utm_source`, `utm_medium`, `utm_campaign`), affiliate platform IDs, first-touch / last-touch rules. State the rule you use.
2. **Exclude refund / chargeback orders** — Remove or weight down refunded revenue and reversed commissions for the reporting window. Call out partial refunds.
3. **Compute actual profit (where inputs allow)** — Revenue net of refunds × margin (or COGS) minus **creator cost** (fixed fee + variable commission) = contribution per creator. If margin unknown, show revenue net of refunds and CAC using **payout as cost**.
4. **Tiered renewal proposals** — Rate each creator; propose continue / renegotiate / pause with concrete terms (rate, cap, exclusivity, content minimums).

## When NOT to use

- No order or payout data — only branding or follower counts.
- Single creator, no reconciliation — simple contract review only.
- Paid ads (Meta/Google) without affiliate linkage — use ads ROAS skills.

## Gather context (infer first; ask gaps)

1. Platform: Shopify, WooCommerce, Impact, ShareASale, custom spreadsheet?
2. Attribution: code-only, UTM-only, or hybrid; window (e.g. 7-day click).
3. Commission model: % of sale, flat per order, hybrid, tiered by volume.
4. Refund policy: full window for affiliate eligibility; chargebacks.
5. Gross margin or COGS % (or confirm "use payout as CAC proxy").
6. Renewal date or campaign end.

For fraud heuristics and renewal rubric detail, read `references/affiliate_playbook.md` when needed.

## Mandatory success output: master table

Every **full** affiliate reconciliation or ROI report must include this table (one row per creator; use **Influencer ID** as the stable key — handle, platform ID, or internal code):

| Influencer ID | Orders attributed | Actual revenue | CAC | Renewal rating |
|---------------|-------------------|----------------|-----|----------------|
| … | … | … | … | … |

**Column definitions**

- **Influencer ID**: Stable identifier (agree with merchant).
- **Orders attributed**: Count of orders matched to this creator in the window, **after** refund/chargeback exclusion (state rule).
- **Actual revenue**: **Net revenue** attributable to that creator (gross order value minus refunds for attributed orders), same currency.
- **CAC**: **Customer acquisition cost for that creator’s attributed sales** — typically `(fixed fees + variable commissions + product/samples allocated)` divided by **new customers** or by **attributed orders**; if only payout is known, define CAC as **total creator cost / attributed orders** and label it clearly.
- **Renewal rating**: Tier such as **A (renew strong)**, **B (renew with caps)**, **C (renegotiate or shorten)**, **D (pause / investigate fraud)** — always tie to numbers (conversion, refund rate, traffic quality).

Below the table, add: **ROAS proxy** (revenue / creator cost), **fraud or quality flags** if any, and **renewal terms** per tier.

## Pushy deliverables (when user asks vaguely)

If they ask "who should we keep" or "affiliate ROI" without structure, still output: the **master table**, **attribution rule summary**, **refund-adjusted figures**, and **at least two renewal scenarios** (e.g. same rate vs reduced rate + cap).

## Report outline (full run)

1. Scope — date range, attribution rule, currency.
2. Master table — required columns above.
3. Refund / chargeback impact — table or bullets per creator if material.
4. Profit or contribution — formula stated; margin assumptions if used.
5. Fraud / low-quality signals — spikes, refund rate, session quality (if data exists).
6. Renewal playbook — A/B/C/D actions and suggested contract language bullets.

## Split with other skills

- **Paid social ads** without affiliates → not this skill.
- **Legal contracts** → flag for counsel; you provide economic summary only.
