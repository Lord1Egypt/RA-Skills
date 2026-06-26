# Audience Builder Quality Checklist

Use this checklist to verify every audience architecture before launch. Each item should be confirmed or explicitly marked as not applicable.

## Customer Segmentation (9 items)

- [ ] Customer file exported with email, phone, name, and purchase history
- [ ] Tier 1 (High-LTV Repeaters) defined: 3+ orders OR top 20% revenue, <20% returns
- [ ] Tier 1 count is between 1,000–5,000 (or documented reason for deviation)
- [ ] Tier 2 (Recent Single) defined: 1 order in 90d, AOV above median
- [ ] Tier 3 (Lapsed) defined: last order 180+ days ago
- [ ] Tier 4 (Discount-Only) defined and EXCLUDED from all lookalike seeds
- [ ] Gift purchasers identified and excluded from seeds (or documented decision to include)
- [ ] High-return customers (>50% return rate) excluded from seeds
- [ ] Segments include count, AOV, repeat rate, and top product categories

## Prospecting Audiences (10 items)

- [ ] Meta: LAL 1% from Tier 1 seed created
- [ ] Meta: LAL 3% from Tier 1 seed created for expansion
- [ ] Meta: Interest stack uses AND logic (not OR) with 3–5 related interests
- [ ] Meta: Broad/Advantage+ ad set included for comparison
- [ ] TikTok: Custom audience LAL created from Tier 1
- [ ] TikTok: VSA and PSA audiences are in SEPARATE campaigns
- [ ] TikTok: Smart+ campaign included for comparison test
- [ ] Google: Customer Match uploaded with Tier 1 + Tier 2
- [ ] Google: PMax campaign has audience signals configured (not just auto-targeting)
- [ ] Google: In-market segments selected and aligned with product categories

## Retargeting Funnel (8 items)

- [ ] Hot segment defined: 0–7d ATC and checkout abandoners
- [ ] Warm segment defined: 7–30d product viewers (2x+) and ad engagers
- [ ] Cool segment defined: 30–90d site visitors and email subscribers
- [ ] Lapsed segment defined: 90–180d past purchasers
- [ ] Each segment has assigned creative type (dynamic / collection / brand story)
- [ ] Offer escalation ladder defined (no offer → free shipping → discount)
- [ ] Platform roles assigned for retargeting (which platform handles which signals)
- [ ] Retargeting budget allocated by segment (hot gets highest CPM tolerance)

## Exclusion Logic (7 items)

- [ ] Prospecting excludes all purchasers (lifetime)
- [ ] Prospecting excludes all ATC (30 days)
- [ ] Prospecting excludes all retargeting audiences
- [ ] Warm retargeting excludes purchasers (30 days) and hot audiences
- [ ] Hot retargeting excludes recent purchasers (7 days)
- [ ] Cross-platform suppression method defined (CDP / manual CSV / API)
- [ ] Exclusion matrix documented showing which audiences exclude which

## Budget Allocation (6 items)

- [ ] Budget split by funnel stage matches brand phase (scaling/stable/efficiency)
- [ ] Cold prospecting is not more than 65% of total (unless brand new)
- [ ] Retargeting (warm + hot) has at least 20% of total budget
- [ ] Incrementality holdout budget allocated (recommended 5–10% of retargeting)
- [ ] Daily budgets per platform per campaign documented
- [ ] Expected CPM ranges documented per audience

## Frequency Management (5 items)

- [ ] Prospecting frequency cap set: 2–3 impressions/user/week
- [ ] Warm retargeting frequency cap set: 4–5 impressions/user/week
- [ ] Hot retargeting frequency cap set: 6–7 impressions/user/week
- [ ] Cross-platform total frequency considered (<10 combined impressions/week)
- [ ] Frequency monitoring set up in each platform's dashboard

## Measurement Framework (5 items)

- [ ] Primary KPI defined per funnel stage (CPA / ROAS / CVR / reactivation rate)
- [ ] Fatigue signals defined: frequency >8/wk + CTR decline >30% + CPM increase >25%
- [ ] Refresh triggers: audience paused and rebuilt when 2 of 3 fatigue signals hit
- [ ] Incrementality test designed with holdout group and measurement period
- [ ] Attribution windows documented per platform with overlap acknowledgment

## Refresh Schedule (4 items)

- [ ] Customer file re-export: monthly
- [ ] Retargeting seeds refresh: weekly
- [ ] Lookalike seeds refresh: monthly with full rebuild quarterly
- [ ] Architecture review cadence set: quarterly or after significant performance shift

## Launch Readiness (6 items)

- [ ] All audiences created in platform ad managers (not just planned)
- [ ] Customer Match lists uploaded and match rates verified
- [ ] Pixel/tag events firing correctly on all platforms
- [ ] Creative assets assigned per funnel stage per platform
- [ ] Campaign naming convention applied for clear reporting
- [ ] Week 1–8 implementation timeline documented with owners

---

**Total: 60 items**

Pass threshold: all items checked or explicitly marked N/A with documented reasoning.
