---
name: ecommerce-revenue-pack
description: Automates the four highest-ROI intelligence tasks for e-commerce sellers — competitor price monitoring, product research, profit margin analysis, and abandoned cart recovery copy. Built for Shopify, Amazon FBA, and direct-to-consumer brands.
version: 1.0.0
tags:
  - ecommerce
  - shopify
  - amazon
  - pricing
  - product-research
  - profit
  - automation
---

# E-commerce Revenue Pack

A complete intelligence and automation suite for online sellers.
Covers the four workflows that directly impact margin and revenue.

## When to use this skill

Use this skill when the user asks about any of the following:
- Monitoring competitor prices and detecting price changes
- Researching new products to add or test
- Calculating true profit margins including all fees and COGS
- Writing abandoned cart recovery email/SMS sequences
- Analyzing Amazon reviews for product improvement insights
- Finding suppliers or evaluating product viability

---

## Workflow 1: Competitor Price Monitor

Track competitor pricing and surface opportunities to win or protect margin.

### What to research per competitor
- Current price for specified products
- Whether they're running sales or promotions
- Their shipping offer (free shipping threshold, speed)
- Review count and rating trends
- Stock availability signals (low stock = price increase incoming?)

### Output format
```
COMPETITOR PRICE REPORT
Product: [name/ASIN/URL]
Your price: $XX.XX
Date: [YYYY-MM-DD]

COMPETITOR SNAPSHOT
[Competitor 1]
- Price: $XX.XX (▲ up $X from last check / ▼ down $X / — unchanged)
- Shipping: [free over $X / flat $X / Prime]
- Stock: [in stock / low stock / out of stock]
- Rating: X.X (XXX reviews)

PRICE POSITION
- You are: [cheapest / mid-range / most expensive] of X competitors
- Recommended action: [hold / test lower / increase — with reasoning]

OPPORTUNITIES
- [Competitor X is out of stock — opportunity to capture their traffic]
- [Competitor Y just raised prices — you have a window to win on value]
```

### Instructions for the agent
1. Ask for: your product name/URL, your current price, and up to 5 competitor URLs or ASINs
2. Use web search to pull current pricing and availability for each
3. Generate the report
4. Set a reminder cadence if the user wants regular monitoring

---

## Workflow 2: Product Research Engine

Evaluate whether a product is worth adding to your store or catalog.

### Research checklist for each product
- Search volume signals (is anyone looking for this?)
- Competition density (how many sellers? how entrenched?)
- Price range and margin potential
- Amazon Best Seller Rank (BSR) if applicable
- Review sentiment — what do customers love/hate about existing products?
- Seasonality signals
- Supplier availability and MOQ estimates

### Scoring output (1–10 per category)
```
PRODUCT RESEARCH REPORT
Product: [name]
Date: [YYYY-MM-DD]

OPPORTUNITY SCORE

Demand:          X/10  [evidence]
Competition:     X/10  [evidence — 10 = low competition]
Margin potential: X/10  [evidence]
Differentiation: X/10  [how easy to stand out]

OVERALL: XX/40

VERDICT: [Strong opportunity / Proceed with caution / Avoid]

WHAT THE 1-STAR REVIEWS SAY (your product improvement roadmap)
- [Pain point 1]
- [Pain point 2]
- [Pain point 3]

YOUR DIFFERENTIATION ANGLE
[Specific suggestion for how to enter this market differently]

SUGGESTED STARTING PRICE: $XX–$XX
ESTIMATED MARGIN AT THAT PRICE: XX%
```

### Instructions for the agent
1. Ask for the product name, category, and target platform (Shopify/Amazon/both)
2. Ask for their rough target price point
3. Research using web search
4. Generate the report with a clear verdict

---

## Workflow 3: Profit Margin Calculator

Calculate true net margin accounting for every cost layer.

### Cost inputs to collect
- Product cost (COGS)
- Shipping to warehouse
- Amazon FBA fees OR Shopify payment fees (2.9% + 30¢)
- Advertising spend per unit (if known)
- Return rate estimate
- Platform referral fee (Amazon: 8–15% by category)
- Packaging cost

### Output format
```
MARGIN ANALYSIS
Product: [name]
Selling price: $XX.XX

COST BREAKDOWN
- Product cost:         $X.XX
- Inbound shipping:     $X.XX
- Platform fee:         $X.XX (X%)
- FBA / fulfillment:    $X.XX
- Advertising (est):    $X.XX
- Returns provision:    $X.XX (X% rate)
- Packaging:            $X.XX
─────────────────────────────
TOTAL COSTS:            $XX.XX

GROSS PROFIT:           $X.XX
NET MARGIN:             XX%

BREAK-EVEN PRICE:       $XX.XX
MINIMUM VIABLE PRICE:   $XX.XX (at 20% margin)

VERDICT: [Healthy / Thin — watch ad spend / Unsustainable at this price]
```

### Instructions for the agent
1. Ask for all cost inputs (offer defaults if user is unsure)
2. Calculate and generate the report
3. Run 3 scenarios: current price, 10% higher, 10% lower
4. Recommend the optimal price point

---

## Workflow 4: Abandoned Cart Recovery Sequences

Write high-converting email and SMS sequences for abandoned carts.

### The 3-message sequence
- **Message 1 (1 hour after abandon):** Gentle reminder, no discount
- **Message 2 (24 hours later):** Social proof + address objections
- **Message 3 (72 hours later):** Final nudge + small incentive if appropriate

### Rules
- Message 1 never leads with a discount — trains customers to abandon for deals
- Message 2 should address the most common purchase objection for that product type
- Message 3 discount should be modest (5–10%) and framed as time-limited
- SMS messages: under 160 characters
- Email subject lines: create urgency without being fake

### Output per sequence
- 3 emails (subject line + body)
- 3 SMS messages (under 160 chars each)
- Recommended send times

### Instructions for the agent
1. Ask for: product name, price, and the main customer objection (price / shipping / trust / unsure)
2. Ask for brand tone (casual / professional / fun)
3. Generate full email + SMS sequence
4. Generate 3 subject line variants for each email

---

## Output and file management
- Save to ~/Documents/drew2_workspace/output/[store-name]/
- Subdirectories: competitor-reports/, product-research/, margins/, cart-recovery/
- Name files: YYYY-MM-DD-type.md
- Confirm before writing
