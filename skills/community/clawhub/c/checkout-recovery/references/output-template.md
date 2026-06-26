# Output Template — Checkout Recovery Audit

Use this template to structure every checkout recovery audit output. Complete all three sections; a partial output that omits the Recovery Roadmap is not actionable.

---

## [Store Name] — Checkout Recovery Audit

**Audit date:** [Date]
**Platform(s):** [List of selling platforms]
**Target markets:** [List]
**Baseline checkout completion rate:** [%] over [time period]
**Platform benchmark:** [%] (note platform and vertical)
**Gap vs. benchmark:** [+ or - %]

---

## Section 1 — Payment Coverage Gap Report

| Market | Supported Payment Methods | Missing Key Methods | Estimated Buyer Coverage Gap |
|---|---|---|---|
| [Market] | [List what's currently supported] | [List what's missing for this market] | [Estimated % of buyers who cannot pay] |

**Coverage gap assessment:**
- [Market]: [2-sentence assessment of how significant the gap is and whether it explains part of the checkout completion shortfall]

---

## Section 2 — Friction Audit

Rate each item: **Critical** (fix within 1 week) / **High** (fix within 2–4 weeks) / **Medium** (fix within 4–8 weeks) / **Low** (monitor)

| Issue | Severity | Finding |
|---|---|---|
| Payment method coverage | [Severity] | [Specific finding for this store] |
| Error message copy | [Severity] | [What error messages currently show; what's missing] |
| Guest checkout availability | [Severity] | [Whether account creation is forced before payment] |
| Mobile checkout quality | [Severity] | [Assessment based on platform/description provided] |
| Shipping cost visibility | [Severity] | [When shipping costs are revealed in the flow] |
| Trust signals | [Severity] | [SSL, logos, guarantees near pay button] |
| Checkout step count | [Severity] | [Number of steps; presence of progress indicator] |
| Recovery sequence timing | [Severity] | [First recovery touch timing vs. 1-hour best practice] |
| Recovery sequence coverage | [Severity] | [Channels used; sequence length vs. 3-touch best practice] |
| Recovery copy quality | [Severity] | [Whether product is referenced; whether checkout link is direct] |

---

## Section 3 — Recovery Roadmap

List 4–6 prioritized fixes ordered by expected impact. For each:

**Fix 1 — [Title]** (Priority: Critical/High/Medium)
- **What to do**: [Specific action step]
- **Implementation**: [How to do it — platform setting, app, provider, or copy change]
- **Copy template** (if applicable):
  > [Paste the suggested copy here — error message rewrite, recovery email subject line, or CTA text]
- **Expected impact**: [Conservative estimate of how this fix affects completion rate]
- **Timeline**: [Estimated implementation time]

**Fix 2 — [Title]** (Priority: [Level])
- [Same format]

**Fix 3 — [Title]** (Priority: [Level])
- [Same format]

**Fix 4 — [Title]** (Priority: [Level])
- [Same format]

---

## Retry Sequence Template (if current recovery is absent or weak)

Use this template to build a 3-touch abandoned checkout sequence:

**Touch 1 — Soft reminder** (Send: 1 hour after abandonment)
- Subject: "Still thinking about [Product Name]?"
- Body: Remind the buyer what they left behind. Include product image + name + price. Direct "Complete Your Order" CTA linking to the exact checkout URL. No discount yet.

**Touch 2 — Social proof** (Send: 24 hours after abandonment)
- Subject: "[Product Name] — [X] customers love it"
- Body: Include a relevant customer review or rating for the specific product. Reiterate the direct checkout link. Still no discount (unless your policy allows it at this stage).

**Touch 3 — Final nudge with optional incentive** (Send: 72 hours after abandonment)
- Subject: "Last chance — your cart expires soon"
- Body: Create mild urgency (truthful only — do not fake scarcity). If your policy allows a recovery incentive, this is the appropriate touch to include a small discount code (e.g., 5–10% off). Direct checkout link.

---

## Disclaimer

This audit is based on the checkout flow, payment configuration, and metrics you described. Recommendations reflect documented ecommerce conversion best practices. Actual improvement results depend on your specific platform, traffic quality, product category, and market conditions.
