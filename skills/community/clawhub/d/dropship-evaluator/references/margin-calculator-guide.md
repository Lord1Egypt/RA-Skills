# Margin Calculator Guide

A complete walkthrough for building accurate margin models before launching a dropshipping product.

## The Core Formula

Most dropshippers calculate gross margin. That's wrong. You need **net margin after acquisition cost** because ads are a cost of sale, not optional overhead.

```
Net Margin = Selling Price − COGS − Shipping − Platform Fees − Payment Fees − Return Cost − CPA
```

**Target thresholds**:
- Net margin ≥25%: Excellent — significant room for scaling and optimization
- Net margin 15–24%: Acceptable — viable but requires careful CPA management
- Net margin 10–14%: Risky — any CPA increase or return spike wipes profit
- Net margin <10%: Reject or reprice — not worth the operational risk

---

## Line-by-Line Breakdown

### 1. Cost of Goods Sold (COGS)

The price the supplier charges per unit, including any product customization fees.

**Watch out for**:
- COGS that increases after your first 10–20 orders ("sample pricing" bait-and-switch)
- FX conversion costs if paying in USD from a non-USD bank
- Import/customs duties for your target market (especially post-Brexit UK, EU VAT)

**Example**: Posture corrector from CJ = $6.20/unit

---

### 2. Shipping Cost to End Customer

The cost your supplier charges to ship the product to your customer. Not your free shipping threshold — the actual cost paid to the carrier.

**Key shipping methods comparison**:

| Method | Typical Cost (China → US) | Transit Time | Reliability |
|---|---|---|---|
| ePacket | $2–5 | 15–30 days | Medium |
| YunExpress | $3–7 | 12–20 days | Medium-High |
| 4PX | $4–8 | 10–18 days | High |
| DHL eCommerce | $5–10 | 8–15 days | High |
| DHL Express | $12–20 | 3–5 days | Very High |

**Never model using the cheapest shipping available**. Model using the method your supplier actually defaults to.

---

### 3. Platform and App Fees

| Cost | Typical Rate |
|---|---|
| Shopify Basic plan (per order) | ~$0.50–1.00 amortized |
| Shopify transaction fee (if not Shopify Payments) | 2% |
| DSers / AutoDS / Zendrop subscription | $0.20–0.60/order amortized |
| Currency conversion (Shopify Payments international) | 1.5% |

**Pro tip**: Calculate monthly app costs divided by expected monthly orders. A $50/month app on 100 orders = $0.50/order. Factor this in.

---

### 4. Payment Processing Fees

| Processor | Rate |
|---|---|
| Shopify Payments (US) | 2.9% + $0.30 |
| PayPal | 3.49% + $0.49 |
| Stripe | 2.9% + $0.30 |
| Afterpay / Klarna | 5–6% + $0.30 |

**Model rule**: Use 3.2% + $0.30 as a safe blended estimate. If you're selling at $29.99, that's approximately $1.26/order.

---

### 5. Return Rate Cost

Returns don't just mean refunding the product cost — they include:
- Refund of full product price (or partial depending on policy)
- Return shipping (if you offer it)
- Product restocking loss (most returned items from international dropshipping are not restocked)
- Customer support time cost

**Return rate benchmarks by category**:

| Category | Typical Return Rate |
|---|---|
| Home & garden | 2–5% |
| Fitness / wellness | 4–7% |
| Electronics / gadgets | 6–10% |
| Clothing / accessories | 8–15% |
| Beauty / cosmetics | 5–10% |

**How to model**: (Return rate %) × (Selling price) = Return cost per average order

Example: 5% return rate on $34.99 product = $1.75/order cost

---

### 6. Customer Acquisition Cost (CPA)

Your CPA (cost per acquisition) is what you pay in ads to get one paying customer. This is the biggest swing factor in your margin model.

**How to estimate CPA before launch**:
1. Research competitor CPAs using tools like Minea, AdSpy, or seller interviews in dropship communities
2. Use category benchmarks: Home goods $8–15, Fitness $10–20, Fashion $12–25, Electronics $15–30
3. Set a "max CPA" where you break even and plan campaigns not to exceed it

**Build your margin model at 3 CPA scenarios**:

| Scenario | CPA | Net Margin |
|---|---|---|
| Optimistic | | |
| Realistic | | |
| Pessimistic | | |

Only launch if even the pessimistic scenario is cash-flow neutral.

---

## Full Worked Example

**Product**: Lumbar Support Pillow (for office chairs)  
**Selling price**: $39.99  
**Target market**: United States

| Line Item | Amount | Notes |
|---|---|---|
| COGS | $7.50 | CJ supplier |
| Shipping (4PX to US) | $5.20 | 10–16 day transit |
| Shopify + apps | $0.80 | Amortized |
| Payment processing | $1.46 | 3.2% + $0.30 |
| Return cost (4%) | $1.60 | $39.99 × 4% |
| **Total before ads** | **$16.56** | |
| **Gross margin** | **$23.43** | *58.6%* |
| CPA (optimistic) | $12.00 | |
| CPA (realistic) | $16.00 | |
| CPA (pessimistic) | $20.00 | |
| **Net margin (optimistic)** | **$11.43** | *28.6%* ✅ |
| **Net margin (realistic)** | **$7.43** | *18.6%* ⚠️ |
| **Net margin (pessimistic)** | **$3.43** | *8.6%* ❌ |

**Conclusion**: This product works at realistic CPA if we can keep CPAs ≤$16. Pessimistic scenario barely breaks even. Set max CPA rule at $18 in ad campaigns.

---

## Common Margin Mistakes

1. **Not including CPA** — "We'll figure out the ads later" is how you discover your winning product loses money
2. **Using COGS without FX buffer** — AliExpress prices fluctuate; build in 5–10% buffer
3. **Ignoring return rates** — beauty and fitness products have high returns; not modeling this kills you
4. **Single-scenario modeling** — only model the optimistic case
5. **Forgetting Shopify app costs** — $200/month in apps on 50 orders/month = $4/order hidden cost
