# Abandonment and checkout friction playbook

Load when the `abandoned-checkout-monitor` skill needs extra detail. Use by scenario; no need to read end-to-end every time.

---

## 1. Funnel nodes and typical events (alignment)

| Node | Meaning | Typical signals |
|------|---------|-----------------|
| Add to cart | Add to cart | Add count, add rate |
| Cart view | Cart page | Cart PV, time on page |
| Begin checkout | Start checkout | Checkout clicks |
| Contact / shipping | Shipping / contact | Field errors, drop at ZIP/phone |
| Shipping method | Choose delivery | Spike after shipping total shown |
| Payment | Choose pay method | Back after card/wallet |
| Pay submit | Submit payment | Gateway errors, 3DS failure |
| Purchase | Success | Versus begin-checkout = checkout conversion |

**Checkout conversion** is often defined as: `completed purchase sessions / begin-checkout sessions` (or orders per visit — align with the merchant).

---

## 2. Abnormal friction (by symptom)

| Symptom | Suspect first | How to validate |
|---------|---------------|-----------------|
| Big drop after shipping step | Shipping shock, late disclosure, regional surcharges | Drop-off by region; A/B earlier shipping quote |
| Clustered exit on payment | Gateway, 3DS, card-only vs local wallets | Payment logs, decline codes |
| High-AOV add-to-cart, no pay | Trust, installments, returns clarity | Heatmaps / session replay; trust badges, BNPL |
| One country much worse | Duties copy, delivery SLA, payment mix | Funnel by country + local payment methods |
| Mobile much worse | Form friction, keyboard overlap, redirects | Conversion by device |

---

## 3. Checkout UI friction scan

- **Step count**: single page or sensible merge; progress clarity.
- **Guest checkout**: forced account creation churn.
- **Fields**: too many required; ZIP/phone validation too strict.
- **Shipping**: visible in cart or early checkout; free-shipping threshold readable.
- **Trust**: security badges, returns policy link, support entry.
- **Mobile**: tap targets, autofill, error placement.
- **Discount code**: hard to find → users leave to hunt codes.

---

## 4. Payment gateway troubleshooting (generic)

1. **Reproduce**: same browser / incognito, different cards, amounts.
2. **Environment**: sandbox keys on live by mistake; webhooks returning 200.
3. **Logs**: platform payment logs + gateway dashboard declines / error codes.
4. **3DS / SCA**: EU etc.; bank-side declines.
5. **Currency / decimals**: matches store; zero-amount test if allowed.
6. **Region**: country IP blocked by risk; CDN/firewall blocking callbacks.
7. **Plugin/theme**: new payment app or theme update.

(You may name Shopify / Woo admin paths in the answer so merchants can click through.)

---

## 5. Three-email recovery logic

| # | Timing (indicative) | Goal | Focus |
|---|---------------------|------|--------|
| 1 | 1–4h | Remind + help | Cart link, support, common blockers (shipping / pay) |
| 2 | 24–48h | Remove friction | Free-shipping code / small discount if policy allows, FAQ, BNPL |
| 3 | 72h+ | Last chance | Stock / SLA, human help, unsubscribe |

At least **two subject-line A/B variants** per email; short body, single CTA, mobile-readable.

---

## 6. A/B copy angles (for the master table)

- Free shipping: "You're $X from free shipping" vs "Orders over $X ship free"
- Trust: "Secure checkout" vs "Join N happy customers"
- Urgency: "Your cart is saved" vs "Popular items selling fast"
- Help: "Payment issues?" vs "We'll help you finish checkout"
