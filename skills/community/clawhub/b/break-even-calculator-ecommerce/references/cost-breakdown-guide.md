# Ecommerce Cost Breakdown Guide

A comprehensive taxonomy of costs to include in break-even analysis. Use this to ensure no cost line is missed.

---

## Variable Costs (scale with units sold)

### Product costs
- COGS / unit cost (manufacturing or wholesale)
- Landed cost (COGS + freight to warehouse + duties/tariffs)
- Quality inspection / testing per unit

### Fulfillment costs
- Pick, pack, and ship labor per order
- Packaging materials (box, filler, tape, inserts)
- Outbound shipping to customer
- Shipping insurance (if offered)

### Transaction costs
- Payment processing (Stripe 2.9% + $0.30, PayPal 3.49% + $0.49)
- Platform/marketplace fees (Amazon 15%, Etsy 6.5%, eBay ~13%)
- Shopify transaction fee (if not using Shopify Payments)
- Currency conversion fees (cross-border)

### Return & refund costs
- Return shipping (if seller-paid)
- Restocking / inspection labor
- Product loss (items that can't be resold)
- Refund processing fees (some processors don't refund their fee)
- Customer service time per return

### Marketing costs (per-unit allocation)
- Cost per acquisition (CPA) from paid ads
- Influencer/affiliate commission per sale
- Coupon/discount cost per unit

---

## Fixed Costs (don't change with volume — in the short term)

### Operations
- Warehouse rent / 3PL monthly minimum
- Full-time staff salaries
- Equipment depreciation
- Insurance (liability, inventory, business)

### Technology
- Ecommerce platform subscription (Shopify, BigCommerce)
- Email/SMS platform (Klaviyo, Attentive)
- Analytics/reporting tools
- ERP / inventory management software
- Domain, hosting, CDN

### Marketing (fixed portion)
- Creative production (photo, video)
- Agency retainers
- Brand/PR costs
- Content creation tools

### Administrative
- Accounting / bookkeeping
- Legal / compliance
- Business licenses
- Loan payments / interest

---

## Semi-Variable Costs (step functions)

These are fixed within a range but jump at thresholds:

| Cost | Fixed within | Jumps when |
|---|---|---|
| Warehouse staff | Up to X orders/day | Need extra shift |
| 3PL storage fees | First X pallets | Exceed tier |
| Customer service | Up to X tickets/day | Need extra agent |
| Shipping rates | Carrier tier | Volume crosses tier bracket |

---

## Platform-Specific Fee Quick Reference

| Platform | Referral/Commission | Payment Processing | Other |
|---|---|---|---|
| Amazon FBA | 8–15% (category) | Included | FBA fees ($3–8/unit) |
| Amazon FBM | 8–15% (category) | Included | Shipping by seller |
| Shopify | 0% | 2.9% + $0.30 | Monthly plan $39–399 |
| Etsy | 6.5% transaction | 3% + $0.25 | $0.20 listing fee |
| eBay | ~13% final value | Included | Store subscription |
| Walmart | 6–15% (category) | Included | No monthly fee |
| TikTok Shop | 5% (+ 1% TTS fee) | Included | Varies by region |

---

## Cost Confidence Levels

When building break-even models, tag every input:

| Level | Symbol | Meaning | Example |
|---|---|---|---|
| Confirmed | ✅ | From actual invoices or reports | Last month's COGS from supplier invoice |
| Estimated | ⚠️ | Based on quotes or comparable data | Shipping estimate from rate calculator |
| Assumed | ❓ | Industry benchmark or guess | Return rate from category average |
