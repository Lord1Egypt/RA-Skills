# Competitor offer and price-power playbook

Load when `competitor-offer-monitor` needs extra depth. Use by section; no need to read end-to-end every invocation.

---

## 1. What to monitor (signals)

| Signal type | Examples | Notes |
|-------------|----------|-------|
| List & promo price | Sitewide %, category sales, clearance | Capture **start/end**, **exclusions**, **stacking** (code + sale) |
| Cart & checkout | Free gift at $X, BOGO, tiered discount | Often beats small list cuts for perceived value |
| Shipping & service | Free expedited, extended returns, warranty | Can offset nominal price gap |
| Marketplace | Amazon Buy Box, coupons on PDP | May diverge from DTC; check **your** channel rules |
| Ads & PLAs | "Up to X% off" in copy, aggressive Shopping bids | Click volume up but CVR down → possible **price expectation** mismatch |
| Email & social | Teaser calendars, influencer codes | Early warning before site changes |

Document **source** (screenshot date, newsletter, third-party tracker) so the team can agree on facts.

---

## 2. Aligning competitor moves with your metrics

1. **Same clock** — store timezone vs ad platform reporting; note day-boundary effects.
2. **Same definition** — session CVR vs user CVR; include / exclude bounces if comparing weeks.
3. **Lag** — paid traffic may react within hours; organic + email can lag 24–72h.
4. **Mix** — a spike in cheap prospecting traffic depresses CVR without any competitor move; segment **brand vs non-brand**, **device**, **geo**.
5. **Overlapping promos** — your own email blast or influencer post can confound; mark on the timeline.

**Strong inference** needs at least one of: geographic holdout, category where only one competitor competes, or external price tracker timestamp matching the inflection.

---

## 3. Hypotheses besides "they cut price"

| Alternative cause | Quick checks |
|-------------------|--------------|
| Creative fatigue | New vs old ad CTR/CVR; refresh date |
| Landing mismatch | PDP speed, OOS, broken variant selector |
| Policy / UX | Returns text change, duty messaging, payment method removed |
| Seasonality | YoY same week, category index |
| Search intent shift | Branded impression share, new SERP features |

Keep these in parallel with competitor tracking so you do not over-index on price.

---

## 4. Response levers (prefer value before blind list cuts)

| Lever | When it fits | Risk |
|-------|----------------|------|
| **Targeted match** | Hero SKU in head-to-head comparison shopping | Trains price sensitivity on that SKU |
| **Bundle / kit value** | You can add perceived value without matching line price | Operations complexity |
| **Loyalty / email-only** | Protects public list price; rewards committed buyers | Segment fairness perception |
| **Financing / BNPL** | Similar monthly payment vs rival lump sum | Fee drag |
| **Shipping / returns upgrade** | Competitor weak on service | Cost per order |
| **Warranty or authenticity** | Commodity category with trust issues | Must be true and provable |
| **Limited window** | Match **duration** bounded; avoids permanent reset | Clear end date + comms |

Avoid sitewide list cuts as the default first move unless data shows broad comparison behavior.

---

## 5. Price match policy design (operational)

- **Eligibility**: same SKU / variant / condition; in-stock; public price (not opaque B2B quotes).
- **Proof**: screenshot rules; competitor URL; exclude marketplace third-party sellers if policy says so.
- **Channel**: DTC only vs retail partners; MAP implications.
- **Stacking**: whether match combines with your other codes.
- **Caps**: max discount % or dollar cap per order.
- **Audit**: who approves exceptions; log for margin review.

Phrase customer-facing copy to emphasize **fairness and confidence**, not desperation.

---

## 6. Governance and kill switches

- **Contribution margin floor** per SKU or category — automated or manual check before enabling match.
- **Inventory** — do not match into stockouts or long backorders.
- **Partner conflict** — retail partners undercut; coordinate or isolate promos.
- **Exit criteria** — e.g. revert after N days, or when competitor ends promo, or when your CVR recovers to baseline in holdout geo.

---

## 7. Measurement after a response

| Metric | Why |
|--------|-----|
| CVR by traffic segment | See if match fixed the right funnel |
| AOV / margin $ | Promo may recover conversion but hurt profit |
| Repeat purchase rate | Training customers to wait for sales |
| Competitor reaction | Escalation dynamics |

Review on a fixed cadence (e.g. 3 / 7 / 14 days) with a written decision to extend, tweak, or end.
