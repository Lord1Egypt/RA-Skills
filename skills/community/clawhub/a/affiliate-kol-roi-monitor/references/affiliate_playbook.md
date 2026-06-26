# Affiliate & KOL ROI playbook

Load when `affiliate-kol-roi-monitor` needs depth. Use by section.

---

## 1. Attribution extraction

| Source | Pros | Cons |
|--------|------|------|
| Unique discount code | High confidence | Code sharing, leakage |
| UTM (source/medium/campaign) | Scalable | Stripping, multi-touch ambiguity |
| Affiliate network click ID | Contractual | Platform fees, latency |
| Custom link shortener + redirect | Control | Same as UTM if params dropped |

**Rule of thumb**: one **primary** rule per report (e.g. last-touch code within 30 days); document conflicts (code + UTM both present).

---

## 2. Refunds and commissions

- Match **refund date** to **original order**; exclude or claw back attributed revenue.
- **Partial refunds**: attribute proportional revenue reduction.
- **Chargebacks**: treat like refunds for ROI; flag for renewal.
- If commission already paid on refunded orders, show **net commission owed** or **clawback line**.

---

## 3. CAC and ROAS (creator economics)

- **Creator cost** = fixed (fee, retainer, gifted product at cost) + variable (% of net sales, per-order bounties).
- **CAC (per attributed order)** = creator cost / orders attributed (label if repeat customers included).
- **CAC (per new customer)** = creator cost / new customers from creator (needs customer ID dedup).
- **ROAS (creator)** = actual revenue / creator cost (state if revenue is net of refunds).

---

## 4. Fake or low-quality traffic (heuristics)

Not proof of fraud — use for **investigation** and **D-tier renewal**.

| Signal | What to check |
|--------|----------------|
| High clicks, near-zero orders | Landing mismatch, bot traffic, incentive fraud |
| Extreme refund rate vs store avg | Misleading promo, wrong audience |
| Single geo spike with no brand fit | Purchased traffic |
| All orders same SKU / same time | Stacking or self-dealing |
| Session duration near zero, 100% bounce | Bot or junk placements |

Recommend: compare each creator’s **conversion rate**, **AOV**, **refund rate** to **store baseline**.

---

## 5. Renewal rating rubric (align to master table)

| Rating | Criteria (example) | Action |
|--------|----------------------|--------|
| A | ROAS above target, refund at or below baseline, clean traffic | Renew; optional volume bonus |
| B | Positive but thin margin or volatile | Renew with monthly cap or tiered % |
| C | Break-even or refund elevated | Short extension; stricter code; audit placement |
| D | Negative contribution or fraud signals | Pause; reconcile clawbacks; require disclosure |

---

## 6. Tiered renewal proposals (output ideas)

- **Volume tier**: e.g. 10% → 12% above $X net sales/month.
- **Cap**: max payout per month to limit risk on new creators.
- **Exclusivity window**: competitor clause in exchange for higher %.
- **Content minimums**: posts/stories per month with trackable links.
