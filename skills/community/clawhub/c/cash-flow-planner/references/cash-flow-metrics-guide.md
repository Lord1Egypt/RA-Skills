# Cash Flow Metrics Guide for Ecommerce

This guide covers the core metrics that determine your cash health, how to calculate them, and what they mean for your business. These metrics are the diagnostic tools for understanding how long your cash stays invested in inventory and operations before it returns to your bank account.

---

## Core Cash Metrics

### 1. Cash Conversion Cycle (CCC)

**What it measures:** The number of days between when you pay suppliers and when you collect cash from customers. It's the length of time your working capital is tied up in inventory and receivables.

**Formula:**
```
CCC = Days Inventory Outstanding (DIO) + Days Sales Outstanding (DSO) − Days Payable Outstanding (DPO)
```

**Why it matters:** A 30-day CCC means you need to fund 30 days of operations, COGS, and marketing simultaneously. A 60-day CCC means you need twice the working capital. Reducing CCC by 10 days frees up significant cash.

**Ecommerce example:**
- A supplement brand with DIO of 28 days (inventory sits 4 weeks before sale), DSO of 2 days (Stripe settlement), and DPO of 30 days (Net 30 supplier terms)
- CCC = 28 + 2 − 30 = 0 days
- Interpretation: Perfect alignment. You collect cash from customers before you pay suppliers.

**Another example (less favorable):**
- An apparel brand with DIO of 50 days (longer inventory turn for seasonal products), DSO of 3 days, and DPO of 30 days
- CCC = 50 + 3 − 30 = 23 days
- Interpretation: You need to fund 23 days of operations and COGS out of pocket. At $50k weekly spend (COGS + operating expenses), that's roughly $160k of working capital tied up in this cycle.

**Target range for ecommerce:** 0−30 days is healthy. Above 45 days signals that you're tying up excess capital and should negotiate longer payables or accelerate inventory turns.

---

### 2. Days Inventory Outstanding (DIO)

**What it measures:** The average number of days inventory sits before it's sold.

**Formula:**
```
DIO = (Average Inventory Balance / COGS per Day) × 365

Or: DIO = 365 / Inventory Turnover Ratio
Where: Inventory Turnover = Annual COGS / Average Inventory
```

**Why it matters:** Every day inventory sits in a warehouse is a day your cash is locked up. A 28-day DIO is better than a 60-day DIO because you recover that cash faster.

**Ecommerce calculation example:**
- A brand has $200k inventory on average
- Annual COGS is $3.6M ($300k per month)
- DIO = ($200k / ($3.6M / 365)) = ($200k / $9.86k per day) = 20.3 days

**Alternative approach (turnover-based):**
- Inventory Turnover = $3.6M COGS / $200k average inventory = 18 turns per year
- DIO = 365 / 18 = 20.3 days

**What to track:**
- DIO by category: If apparel sits 45 days but supplements sit 20 days, focus on accelerating apparel (or reallocate capital to supplements).
- DIO trend: Is it improving (faster turns) or degrading (inventory stalling)? A 5-day increase is a red flag that demand is weakening or assortment is stale.

**Target range:** 14−35 days for health ecommerce brands (weekly or bi-weekly inventory turns). Above 45 days signals overstock risk or slow-moving inventory.

---

### 3. Days Sales Outstanding (DSO)

**What it measures:** The average number of days between when you make a sale and when you actually receive cash in your bank account.

**Formula:**
```
DSO = (Average Accounts Receivable / Daily Revenue) × 365

Or for ecommerce: DSO = Payment Processing Delay (days) + Refund Processing Delay (days)
```

**Why it matters:** Most direct-to-consumer ecommerce has a DSO of 2−5 days because payment processors settle funds quickly. B2B or wholesale has DSO of 30−60+ days. For cash forecasting, DSO is one of the biggest factors—a 1-day change in settlement timing can swing your weekly cash by 10−20%.

**Ecommerce calculation by processor:**

| Processor | Settlement Window | Typical Hold | Effective DSO |
|-----------|-------------------|--------------|---------------|
| Stripe (connected account) | 2-3 business days | 0% | 2-3 days |
| Shopify Payments | 1-3 business days | 0% | 1-3 days |
| PayPal (standard) | 1 business day | 10-15% held for 21 days | 3-5 days (blended) |
| Amazon Pay | Same as Amazon account | Varies | 3-7 days |
| Square | 1 business day | 0% (established account) | 1 day |

**Example:**
- A brand processes $100k weekly revenue: $60k on Stripe (2-day settlement), $30k on PayPal (1 day settlement + 10% hold for 21 days), $10k COD.
- Stripe cash received: $60k on day 2
- PayPal cash received: $27k on day 1, $3k held until day 21
- COD cash: $10k on delivery (assume day 3)
- Weighted average DSO: roughly 3 days
- But the hold complicates things: in week 1, you're short $3k of the PayPal hold until week 4.

**What to track:**
- DSO by payment method: Identify which processors are slowest and quantify the cash impact.
- Hold policies: PayPal, Stripe, and Square may increase holds for new accounts or high-risk categories (supplements, beauty). Monitor hold percentages and duration.
- Refund processing: If you have 10% refund rate and refunds take 5-7 days to settle, your net DSO is slightly longer.

**Target range:** 2−5 days for health ecommerce (assuming Stripe/Shopify Payments or equivalent). Above 5 days signals processor holds or slow payment methods dominating the mix.

---

### 4. Days Payable Outstanding (DPO)

**What it measures:** The average number of days between when you receive inventory from a supplier and when you pay the invoice.

**Formula:**
```
DPO = (Average Accounts Payable / Daily COGS) × 365
```

**Why it matters:** Longer DPO means you hold suppliers' cash longer, reducing your working capital need. A supplier offering Net 60 instead of Net 30 doubles your DPO, cutting your working capital requirement in half (all else equal).

**Ecommerce example:**
- A brand has $150k of supplier payables on average
- Daily COGS is $10k ($3.65M annual COGS / 365 days)
- DPO = ($150k / $10k) = 15 days

Wait, that's low—usually supplier terms are Net 30, which should be 30 DPO. Why is this only 15? **Most likely answer:** The brand is paying faster than terms require, or they have a mix of terms (some Net 15, some Net 60). If you're consistently paying early, you're leaving working capital on the table.

**Supplier term leverage matrix:**

| Annual COGS Volume | Typical DPO Achievable |
|---|---|
| < $500k | Net 15-20 days (limited leverage) |
| $500k - $2M | Net 30 days (standard) |
| $2M - $10M | Net 45 days (negotiable with key suppliers) |
| > $10M | Net 60-90 days (with largest suppliers) |

**Action:** If your brand does $3M annual COGS but your DPO is only 20 days, you have negotiation room. Talk to your top 2-3 suppliers and request Net 45. Most established brands have a mix: largest suppliers on Net 60, mid-tier on Net 45, smaller suppliers on Net 30.

**What to track:**
- DPO by supplier: Are you negotiating terms effectively? Where can you push for Net 45 or Net 60?
- DPO trend: Is it shrinking? That signals suppliers are tightening terms (often a sign of cash stress in your industry).
- Payment practice: Are you taking full advantage of terms, or paying early? If you're paying Net 30 invoices in 15 days, ask your suppliers for early payment discounts (2/10 Net 30) and only take if the discount (2%) beats your cost of capital.

**Target range:** 30−45 days for established ecommerce brands. Below 20 days signals weak negotiation or tight supplier relationships.

---

## Cash Buffer Benchmarks

### Minimum vs. Ideal vs. Excessive

**Minimum Cash Buffer:** 4−6 weeks of operating expenses
- Definition: Operating expenses = payroll + platform fees + overhead + marketing spend (not COGS, which is funded by payables)
- When to use: Tight cash situation, mature business with predictable cash flow, strong credit access
- Example: $40k/week operating expenses → $160−240k minimum buffer
- Risk: Tight. One bad week and you're scrambling.

**Ideal Cash Buffer:** 8−12 weeks of operating expenses
- When to use: Standard for growing DTC brands, especially those with seasonal demand or growth objectives
- Example: $40k/week operating expenses → $320−480k ideal buffer
- Trade-off: You're holding more cash than necessary for operations, but you have optionality for inventory buys, tax payments, or downside protection.

**Excessive Cash Buffer:** > 16 weeks of operating expenses
- When to use: Post-acquisition, conservative founder, or misunderstanding of cash requirements
- Risk: You're leaving money on the table that could be deployed in inventory, acquisition, or growth.
- Example: If you have $800k cash and only need $320−480k for operations, you should redeploy $300−500k.

**Formula to calculate your target buffer:**
```
Buffer Target = (Weekly Operating Expenses) × (Weeks to Cover)
```

**Operating Expenses Calculation for Ecommerce:**
```
Weekly Operating Expenses = (Monthly Payroll + Monthly Overhead + Monthly Platform Fees + Monthly Ad Spend) / 4.33

EXCLUDE from this: COGS (covered by payables), customer refunds (covered by returns reserve), capital purchases (separate from working capital)
```

**Example:**
- Monthly payroll: $60k
- Monthly platform fees (Shopify, tools): $5k
- Monthly overhead (rent, utilities, etc.): $8k
- Monthly paid media: $80k
- **Total monthly operating expenses: $153k**
- **Weekly operating expenses: $153k / 4.33 = $35.3k**
- **Ideal buffer (10 weeks): $35.3k × 10 = $353k**

---

## Ecommerce-Specific Cash Drains

Beyond the core metrics, ecommerce businesses face unique cash drains that must be modeled separately:

### 1. Inventory Pre-buys

**The problem:** You buy inventory weeks or months before selling it. A Q4 holiday season might require an August inventory purchase (4 months before peak sales), locking up cash for that entire period.

**Cash impact:**
- August buy: $200k inventory purchase on Net 30 terms = $200k cash outflow in September
- Revenue impact: September revenue $50k (slow summer month)
- **Cash gap:** You've spent $200k, but only collected $50k—a $150k hole to fund

**Mitigation:**
- Negotiate extended terms: Net 60 or Net 90 instead of Net 30 delays the cash outflow
- Revenue-based financing: Borrow $200k, repay 8% of monthly revenue starting when seasonal revenue hits
- Pre-orders: Start taking pre-orders in June; collect cash before inventory arrives

### 2. Paid Media Float

**The problem:** You spend cash on ads today, but customers convert and settle over days or weeks. Plus, not every dollar spent converts immediately.

**Cash impact:**
- Monday: Spend $10k on Facebook ads
- Spend $10k on Google ads
- Wednesday: Collect $3k from Monday's conversions
- Friday: Collect $4k from Tuesday-Wednesday's conversions
- **Cash outflow:** $20k
- **Cash inflow:** ~$10-12k (assuming 50-60% of ad spend converts, with 2-day settlement lag)
- **Float:** You're funding $8-10k of working capital in ads.

**At scale:** If you spend $100k/week on ads and the revenue settles over 3-5 days, you're funding $150−250k of working capital in the ad float alone.

**Mitigation:**
- Optimize CAC and ROAS: Better unit economics mean faster payback on ad spend
- Seasonal spend: Pull back ads during low-demand periods to reduce float
- Financing: Include ad float in your working capital calculation when applying for credit lines

### 3. Platform Fee Delays

**The problem:** Shopify, payment processors, and third-party apps deduct fees, often 2-3 days after settlement, creating a timing gap.

**Cash impact:**
- Stripe processes $100k revenue, deposits $97.1k (after 2.9% fee)
- Shopify bills $5k monthly platform fee on the 1st of the month
- You need to account for both outflows separately and time-shifted

**Typical fee structure:**
- Shopify: 2.9% + 30¢ on credit card transactions (billed monthly)
- Stripe: 2.9% + 30¢ (deducted at settlement)
- PayPal: 2.2% + 30¢ (deducted at settlement, plus holds)
- Shopify apps: $30−500/month additional (Klaviyo, Gorgias, etc.)

**At $200k monthly revenue:**
- Stripe/Shopify fees: roughly $7−8k/month
- App fees: $2−5k/month
- **Total fees: $10−13k/month** (5-6.5% of revenue)

**Mitigation:**
- Forecast platform fees explicitly (don't assume all revenue becomes cash)
- Negotiate lower rates: Stripe and Shopify offer discounts at $100k+ monthly volume
- Choose high-margin categories: Fees are a fixed percentage, so higher gross margin products absorb fees better

### 4. Return Reserves & Chargebacks

**The problem:** You collect revenue, but some is refunded or disputed. Refunds often come from operating profit or buffer, creating a cash drain.

**Cash impact:**
- Ecommerce average return rate: 10-20% (apparel, beauty) to 5-10% (supplements, consumables)
- Refund processing: 5-7 days (Stripe holds refunds in reserve before settling)
- Chargebacks: 1-3% of volume (customers dispute charges); recover disputed amount takes 30-90 days

**Example:**
- $100k weekly revenue with 10% return rate and 3% chargeback rate
- Refunds: $10k (5-7 days out)
- Chargebacks: $3k (30-90 days out, with risk of permanent loss)
- **Cash drain:** $13k/week that must come from buffer or payables

**Mitigation:**
- Hold a reserve: Set aside 3-5% of weekly revenue in a returns reserve (separate from operating cash)
- Improve return rate: Better product descriptions, size guides, and quality reduce returns
- Manage chargebacks: Excellent customer service, clear billing descriptors, and fraud prevention lower chargeback rates

---

## Payment Processing Timelines

**Critical for accurate DSO calculation:**

### Stripe / Shopify Payments
- Settlement: 2-3 business days
- Fee: 2.9% + 30¢
- Hold on new accounts: up to 7-10 days (released after 100+ transactions or 14 days, whichever is first)
- Hold on high-risk merchants: up to 21 days (supplements, beauty, CBD, gambling) or hold percentage (e.g., 10% held for 21 days)

**Example timeline:**
- Monday 9am: Customer charges $100
- Wednesday 2pm: Stripe deposits $97.07 ($100 − 2.9% fee − 30¢)
- Total time to cash: ~2.5 business days

### PayPal
- Settlement: 1 business day for connected account, 3-5 days for standard account
- Fee: 2.2% + 30¢ (plus higher for cross-border)
- Hold: 10-15% held for 21 days on all accounts (strict requirement)
- Reserve: Additional 5-10% held on high-risk categories (supplements, gambling, digital goods)

**Example timeline:**
- Monday 9am: Customer pays $100
- Tuesday 2pm: PayPal deposits $87.5 ($100 − 2.2% fee − 30¢ − 10% hold)
- Friday: Additional $10 released (if no disputes)
- Over 21 days: Remaining $10 released (if no chargebacks)
- Total time to full cash: 21 days (with hold), vs. 1 day for settlement

**Impact on forecast:** At $100k weekly revenue (50% PayPal), you're holding $5k in escrow for 21 days. That's working capital that never hits your bank account for 3 weeks.

### Amazon Payments / Amazon Business
- Settlement: 1-2 business days (slower than Stripe)
- Fee: 2.9% (marketplace) to 3.5-8% (A2X charges for added services)
- Hold: None for established accounts; 14-day hold for Amazon Business
- Reserve: Amazon holds 5-10% for 90 days on high-volume FBA sellers

**Example:**
- Monday: Customer buys via Amazon
- Tuesday-Wednesday: Amazon deposits (2% fee deducted)
- Friday: Amazon can halt deposits for chargebacks, returns, or disputes

### International / Cross-border
- Settlement: 3-7 business days
- Fees: 3.5-4.5% (higher due to currency conversion, fraud risk)
- Holds: 10-30% held for 30-90 days
- Currency conversion: FX risk if you're collecting in USD but paying suppliers in other currencies

---

## Seasonal Cash Planning

### Q4 / Holiday Season Inventory Timing

**The challenge:** Q4 accounts for 20-40% of annual revenue for most ecommerce brands. Customers shop from October-December, but inventory must be in-stock by September or earlier.

**Typical timeline:**

| Month | Action | Cash Impact | Notes |
|-------|--------|-------------|-------|
| June | Q4 planning begins | Planning only | Forecast demand, identify SKUs |
| July | Pre-order launches (optional) | +$50−100k cash (collected early) | Reduces financing need |
| August | Inventory purchase order issued | −$150−300k (payment due Sept-Oct) | Large COGS payable due |
| September | Inventory arrives; payment due | −$150−300k cash outflow | Largest cash drain month |
| October | Sales begin to ramp | +$100−150k revenue | Partial payback |
| November | Peak season (BFCM, Thanksgiving) | +$200−400k revenue | Cash inflection point |
| December | Holiday shopping peaks | +$200−400k revenue | Biggest revenue month |
| January | Post-holiday returns; clearance | +$50−100k revenue (but high returns) | Returns drain, inventory burn |

**Cash requirement calculation:**
- Q4 forecast revenue: $1M (Oct-Dec)
- Average DIO: 35 days
- Average COGS: 60% ($600k for Q4)
- Payables terms: Net 45 (pay in October for August/September buy)
- **Working capital locked up:** $600k × (35 days / 30 days) ≈ $700k
- **Less DPO benefit:** $600k × (45 days / 30 days) ≈ $900k of coverage
- **Net need:** Small for a mature brand with extended terms

For a brand **without** extended terms (Net 30):
- **Working capital needed:** $700k − $600k = $100k (still manageable, but tight)

For a brand **without any payables stretch** (cash on delivery):
- **Working capital needed:** $700k (all inventory must be self-funded or financed)

**Mitigation strategies:**
1. Negotiate Net 45-60 with suppliers by June (before buying season)
2. Secure RBF facility by July ($200−500k) to pre-fund inventory
3. Launch pre-orders in July to collect customer cash early
4. Reduce non-core SKUs in Q4 to focus capital on proven winners
5. Plan inventory burn rate: Sell 70% of Q4 inventory by end-December; rest by January 31 (avoid overstocking)

---

## Gross Margin Floor for Cash Health

**Rule of thumb:** A gross margin below 40% signals cash risk for most ecommerce models.

**Why:**
- Gross margin = Revenue − COGS (all other expenses come from GM)
- A 40% GM means 40% of revenue is left to cover payroll, overhead, platform fees, marketing, returns, and working capital
- At 40% margin, a $1M annual revenue business has $400k for all operating expenses and working capital

**Margin floor by category:**

| Category | Healthy GM | Caution Zone | Danger Zone |
|----------|-----------|-------------|-----------|
| Supplements / Consumables | 50-70% | 40-50% | < 40% |
| Beauty / Skincare | 60-75% | 45-60% | < 45% |
| Apparel | 50-65% | 40-50% | < 40% |
| Home Goods | 45-60% | 35-45% | < 35% |
| Electronics | 25-40% | 15-25% | < 15% |

**Cash impact of low margin:**
- At 60% GM: $100k revenue → $60k available for all expenses + growth
- At 40% GM: $100k revenue → $40k available (33% reduction in cash available)
- At 35% GM: $100k revenue → $35k available + struggling to cover payroll + minimal buffer

**Action:** If your brand's gross margin is below 40%, focus on: (1) raising product prices, (2) reducing COGS through supplier negotiation or higher volumes, or (3) shifting product mix to higher-margin SKUs. Don't grow revenue if margin is eroding—it makes cash problems worse.

---

## Inventory Financing Options

### 1. Revenue-Based Financing (RBF)

**Structure:** Borrow capital, repay a percentage of monthly revenue (typically 6-12%) until principal + interest is repaid (usually capped at 1.5-2x the borrowed amount).

**Cost example:**
- Borrow: $200k
- Repayment: 8% of monthly revenue
- At $100k/month revenue: Pay $8k/month (repay $200k in 25 months)
- Total cost: $8k × 25 = $200k (ROI implicit in 8% rate)

**Pros:**
- No equity dilution
- No personal guarantee (usually)
- Fast approval (1-2 weeks)
- Flexible repayment (ties to revenue, not fixed schedule)

**Cons:**
- Higher effective cost (8% of revenue = ~80% APR if revenue is $100k/month)
- Reduces cash flow during revenue peaks
- Lender takes a small percentage of revenue indefinitely (until repaid)

**Best for:** Seasonal inventory builds (Q4), rapid growth phases, bridging known liquidity gaps.

**Providers:** Clearco, Pipe, Uncapped, Rapid Finance, others.

### 2. Supplier Terms (Net 30/45/60)

**Structure:** Pay suppliers 30, 45, or 60 days after receiving inventory.

**Cost:** Free, if you don't take early payment discounts (e.g., "2/10 Net 30" means 2% discount if you pay in 10 days, otherwise pay full amount by day 30).

**Pros:**
- No interest or fees (it's free working capital)
- Relationship-based (no external lender required)
- Scale as business grows (suppliers often extend terms with volume)

**Cons:**
- Requires existing supplier relationship and payment history
- Difficult to negotiate for new vendors or small orders
- Supplier may tighten terms if cash flow deteriorates industry-wide

**Best for:** Ongoing operations, maintaining leverage with key suppliers.

**Negotiation timeline:**
- Month 1-2: Establish relationship, pay on time (Net 30)
- Month 3-6: Hit $50k+ order volume, ask for Net 45
- Month 6-12: Hit $100k+ quarterly volume, request Net 60 with top suppliers
- Year 2+: Negotiate tiered terms (largest supplier Net 60, mid-tier Net 45, new suppliers Net 30)

### 3. Inventory Line of Credit (Inventory LOC)

**Structure:** Bank or lender provides a credit line secured by inventory (typically 40-60% of inventory value).

**Example:**
- Inventory value: $300k
- LOC available: 50% = $150k
- Interest rate: 8-12% APR
- Repay as inventory sells (with periodic draws/repayments)

**Cost:**
- Interest on drawn amount (e.g., $150k drawn at 10% APR = $1.25k/month interest)
- Annual line fee (0.5-1% of available credit)

**Pros:**
- Fixed interest rate (predictable cost)
- Flexible draw/repay based on inventory sales
- Often covers large inventory buys without revenue-sharing

**Cons:**
- Requires strong personal credit and business financials
- Personal guarantee typical
- Slower approval (2-4 weeks)
- Secured by inventory (lender has claims on assets)

**Best for:** Established businesses with stable cash flow, ready to formalize financing.

**Providers:** Banks (Wells Fargo, Chase, Biz2Credit), specialized lenders (Stripe Capital, Square Capital, Lendio).

### 4. Purchase Order (PO) Financing

**Structure:** Lender pays supplier on your behalf, you repay lender when customers pay you.

**Example:**
- You win a $100k customer order (or place a $100k supplier PO for Q4 inventory)
- PO lender pays supplier $100k immediately
- You sell inventory and collect $100k from customers
- You repay lender $100k + 2-5% fee = $102-105k

**Cost:** 2-5% fee on PO value (on top of your supplier's price).

**Pros:**
- Covers 100% of inventory cost (no collateral required)
- Fast funding (1-2 weeks if supplier is approved)
- Works for large, specific orders

**Cons:**
- Lender must approve supplier (and your customer/forecast)
- Higher cost than bank lines
- Typically limited to $50k+ orders

**Best for:** Seasonal builds, large customer orders, growth without credit history.

**Providers:** Biz2Credit, CAN Capital, Flexible Fulfillment, others.

---

## Early Warning Signals: When to Act

### 1. Declining Cash Conversion Cycle
**Signal:** Your CCC increases from 20 days to 30-35 days over 2-3 months.
**Root cause:** Inventory turns are slowing (DIO rising) or you've shortened payables (DPO falling).
**Action:** Investigate which component changed. If DIO is rising, address slow-moving inventory (run sales, change marketing, discontinue SKU). If DPO is falling, renegotiate terms with suppliers.

### 2. Rising Days Inventory Outstanding
**Signal:** DIO increases by 5+ days vs. rolling 12-week average.
**Root cause:** Inventory not selling (demand weakness), overstock, or new SKU underperformance.
**Action:** (1) Audit inventory by SKU age and velocity. (2) Mark down slow-moving inventory (better to convert to cash at 70% margin than sit as dead inventory). (3) Pause reorders of underperforming SKUs. (4) Shift marketing spend to high-turning products.

### 3. Payables Stretching Beyond Negotiated Terms
**Signal:** You're paying Net 30 invoices on day 40-50 regularly.
**Root cause:** Unplanned cash shortage or supplier tolerance.
**Action:** **Do not let this become normal.** Supplier relationships depend on reliability. If you can't pay on terms, proactively contact suppliers and renegotiate before you miss a payment. Missing payments tanks your leverage for future negotiations.

### 4. Cash Conversion Cycle Approaching or Exceeding 60 Days
**Signal:** CCC = 60+ days.
**Root cause:** Inventory turns are slow (45+ days), customer cash settlement is delayed, or supplier terms are short (DPO < 20).
**Action:** This is a liquidity crisis waiting to happen. You need working capital of 60+ days of combined spend (COGS + operating expenses). Model your financing need now, before you're desperate.

### 5. Payment Processor Holds Increasing
**Signal:** Stripe, PayPal, or other processor suddenly increases holds or reduces settlement speed.
**Root cause:** Industry perception of risk (e.g., FDA warning for supplements), chargeback spike, or fraud on your account.
**Action:** (1) Investigate cause immediately. (2) Request hold removal by providing compliance/legal documentation. (3) Consider backup payment processor (reduce concentration risk). (4) Model impact on DSO (hold could increase DSO by 2-3 weeks).

### 6. Supplier Tightening Terms
**Signal:** Your supplier moves from Net 30 to Net 15 or Net 0 (COD), or reduces order size limits.
**Root cause:** You may have missed a payment or been slow; industry-wide cash tightness; or supplier's own cash pressure.
**Action:** (1) Contact supplier immediately to understand issue. (2) Prioritize payment to rebuild relationship. (3) Find backup suppliers before relationship breaks. (4) Reduce reliance on single supplier.

### 7. Ad Spend ROI Declining while CAC Rising
**Signal:** CAC increases from $15 to $25, or ROAS drops from 3.5 to 2.5.
**Root cause:** Market saturation, iOS tracking changes, or increased competition.
**Action:** This hits cash hard because ad spend floats working capital. (1) Slow ad spend growth. (2) Tighten unit economics (improve conversion rate, increase AOV, reduce returns). (3) Shift to lower-cost acquisition channels (email, organic). (4) Model impact on working capital (lower ROAS = higher ad float = less cash available).

---

## Cash Metrics Dashboard Template

Track these metrics weekly to keep your finger on the pulse:

| Metric | Target | Actual (This Week) | Trend (4-Week Avg) | Action if Off |
|--------|--------|---|---|---|
| Cash Balance | $350k+ | $[amount] | $[amount] | [Action] |
| CCC | < 30 days | [#] days | [#] days | [Action] |
| DIO | < 35 days | [#] days | [#] days | [Action] |
| DPO | ≥ 30 days | [#] days | [#] days | [Action] |
| DSO | < 5 days | [#] days | [#] days | [Action] |
| Gross Margin % | > 50% | [%] | [%] | [Action] |
| Inventory Turnover | > 4x/year | [#] x | [#] x | [Action] |
| Ad Spend as % of Revenue | < 30% | [%] | [%] | [Action] |
| CAC | < $15 | $[amount] | $[amount] | [Action] |
| ROAS | > 3.0 | [ratio] | [ratio] | [Action] |

Update this dashboard every Monday morning. Any metric trending in the wrong direction for 2+ weeks is a yellow flag; 3+ weeks is a red flag requiring immediate action.
