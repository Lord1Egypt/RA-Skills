---
name: shopify-store-optimizer
description: Audit Shopify stores end-to-end and produce a prioritized fix list to lift conversion rate, AOV, and SEO traffic. Diagnoses theme speed, product page anatomy, collection structure, cart/checkout friction, app bloat, mobile UX, and pricing/discount strategy. Knows the Shopify-specific levers (sections, metafields, app stack, Shop Pay, Markets, Checkout Extensibility) and the 2026 Online Store 2.0 patterns. Use when asked to audit a Shopify store, improve conversion, increase AOV, fix slow theme, optimize product pages, restructure collections, reduce cart abandonment, plan a redesign, evaluate apps, or prepare for BFCM. Triggers on "shopify audit", "shopify conversion", "shopify speed", "product page", "collection page", "abandoned cart", "AOV", "shopify theme", "shopify apps", "checkout optimization", "BFCM prep".
metadata:
  tags: ["shopify", "ecommerce", "conversion-rate", "cro", "dtc", "store-design", "online-store", "checkout"]
---

# Shopify Store Optimizer

Audit a Shopify store the way a senior CRO consultant would — site-wide pass first to find the biggest leak, then focused product-page surgery, then long-tail SEO and AOV plays. Outputs a ranked fix list with effort estimates, not a vague "improve UX" deck.

## Usage

Use when revenue per visitor is below benchmark, when a store has plateaued, or before a high-stakes period (BFCM, holiday, new product launch).

**Basic invocation:**
> Audit my Shopify store: example-store.myshopify.com
> Why is my conversion rate stuck at 1.2%?
> My product page bounce rate is 70% — diagnose
> Plan my BFCM prep — store is on Dawn theme

**With context:**
> Stack: Dawn 11.0, Klaviyo, Shogun, Loox, Bold Bundles. CR 1.4%, AOV $58, mobile share 78%.
> 6-month-old DTC skincare brand, $8k/mo revenue, plateaued. Want to hit $25k.
> Switching from Plus to Basic to cut cost — what loses functionality?
> Migrating from Magento to Shopify — what to keep, what to redesign.

The agent runs a five-layer audit (storefront speed → IA → PDP → cart/checkout → retention) and produces ranked fixes with expected lift, effort, and Shopify-specific implementation notes.

## How It Works

### Layer 1: Storefront speed and core web vitals

LCP > 2.5s = ranking + conversion penalty. Order of attack:

1. **Theme baseline** — Dawn / Sense / Trade / Pipeline / Symmetry are fast out of the box. Vintage 1.0 themes (Brooklyn, Debut, Boundless) are slow and unmaintained — replatform recommendation.
2. **App audit** — every embedded app injects JS. Run `?debug=true` and Theme Inspector. Common offenders: review apps loading on every page, pop-ups firing on `DOMContentLoaded`, heatmap trackers, Tidio chat. Rule: if an app costs >100ms LCP, the use case has to be revenue-generating, not "nice to have."
3. **Image weight** — hero images >300KB, product images >150KB, lazy-loading missing on below-fold. Tool: Shopify Image Optimizer or Tinify (avoid full third-party CDNs — Shopify CDN is fine).
4. **Liquid loops** — `{% for product in collection.products %}` with deep metafield access at scale = slow. Move to section settings or `{% paginate %}`.
5. **Custom fonts** — limit to 2 weights, use `font-display: swap`, prefer Shopify's font picker (preloaded).

Output: speed-fix list with PageSpeed before/after estimates and effort (XS/S/M/L).

### Layer 2: Information architecture and navigation

A store with 500 SKUs and 4 collections in the menu is leaking traffic. Audit:

- **Collection depth** — every product should be reachable in ≤3 clicks. Use mega menu for stores with >20 collections.
- **Filtering** — Shopify Search & Discovery filters drive AOV; tag products with material, color, size, occasion, price band. Avoid filters with <3 products (causes empty states).
- **Search** — install Shopify Search & Discovery (free) before paying for Boost AI / Searchanise. Synonyms (e.g., "tee" → "t-shirt"), redirects on no-results, and trending queries are table stakes.
- **Breadcrumbs** — must be enabled, structured-data marked, and clickable at every level.
- **Footer** — should hold trust badges, shipping/returns, contact, and a discount-capture (10% off) for first-purchase intent.

### Layer 3: Product page (PDP) anatomy

This is where 60% of conversion lift lives. Audit each section:

| Element | Best practice 2026 |
|---|---|
| Image gallery | 5–8 images, model + flat-lay + scale + detail + lifestyle + UGC. Mobile carousel with thumbnails. |
| Title | Under 60 chars, includes searchable attribute (size, color, use). |
| Price | Include compare-at if discount real, never fake. Bundle/subscription pricing visible. |
| Reviews | Star average + count above the fold. Loox / Judge.me / Yotpo all OK. |
| Variants | Swatches for color, size selector, low-stock urgency only when real. |
| ATC | Sticky on mobile after scroll. Buy Now if Shop Pay enabled (express checkout = +9% CR). |
| Trust badges | Shipping ETA, returns policy, secure checkout. Money-back if applicable. |
| Description | Scannable: bullets for spec, prose for story. Tabs for size guide / care / FAQ. |
| Bundle / cross-sell | Use Shopify Bundles (free) or Bold Bundles. "Frequently bought together" lifts AOV 8–15%. |
| Shipping | Show free-shipping threshold and estimated delivery date dynamically by zip. |

### Layer 4: Cart and checkout

Cart-to-checkout drop is the silent killer. Audit:

- **Cart drawer vs page** — drawer wins for impulse, page for high-consideration. Hybrid (drawer with "view cart" link) is safe.
- **Free shipping bar** — progress indicator from cart subtotal toward threshold ($X away from free shipping). Tools: Free Shipping Bar (free) or built into theme.
- **Discount field placement** — collapsed by default. Expanded fields lift abandonment (people leave to search for codes).
- **Checkout extensibility** — on Plus, use checkout.liquid → Checkout Extensibility migration (deadline expired Aug 2024 — anyone still on legacy is at risk). Build apps, not custom Liquid.
- **Shop Pay** — must be on; one-click checkout converts at 1.91x baseline per Shopify data.
- **Local payment methods** — Klarna / Afterpay / Affirm for AOV >$80; iDEAL / Bancontact for EU; Konbini / PayPay for JP.
- **Address auto-complete** — Shopify ships this; if disabled, re-enable.

### Layer 5: Retention and lifecycle

Acquisition without retention = treadmill. Audit:

- **Email/SMS capture** — entry pop-up (Privy / Klaviyo) with discount; exit-intent on PDP.
- **Klaviyo flows** — Welcome (3-email), Abandoned Cart (3-email + SMS), Browse Abandonment, Post-Purchase, Win-back at 60/90/180 days, Replenishment for consumables.
- **Subscriptions** — for consumables, Recharge / Skio / Shopify Subscriptions. 15–25% discount on subscribe is standard.
- **Loyalty** — Smile.io / Loyalty Lion only justified at >$30k/mo. Below that, simpler discount on second order works.
- **Reviews/UGC loops** — automated request 10–14 days post-delivery; offer points or discount for photo review.

## Audit Outputs

Always returns a ranked fix list:

```markdown
## Audit: example-store.myshopify.com (run 2026-05-02)

### Top 5 fixes (do these this week)
1. **PDP: add review widget above fold** — Effort: S | Lift: +8–12% CR
   - Loox is installed but rendering below description tab. Move to top of PDP, show count + stars.
2. **Cart: enable free-shipping bar** — Effort: XS | Lift: +5–7% AOV
3. **Speed: remove unused Tidio chat on PDP** — Effort: XS | Lift: +0.4s LCP, +2% CR mobile
4. **Checkout: enable Shop Pay** — Effort: XS | Lift: +9% on Shop Pay click-through
5. **Klaviyo: launch 3-email Welcome flow** — Effort: M | Lift: +12% list-attributable revenue

### Medium-term (this month)
6. Add Shopify Bundles for SKU-A → SKU-B FBT — Effort: M | Lift: +10% AOV
7. Restructure collections from 4 → 12 with filterable tags — Effort: M | Lift: SEO + filter conversion
8. Migrate from Vintage Brooklyn theme to Dawn — Effort: L | Lift: speed + maintenance

### Strategic (this quarter)
9. Subscription program for hero SKU — Effort: L | Lift: +18% LTV
10. Move from Basic to Shopify (or back) based on app cost analysis — Effort: M | Lift: cost
```

## Plan-Stage Diagnosis

Match the store stage to the right work:

- **Pre-launch / first 90 days** — Don't optimize; ship paid ads to PDP. Track CR by traffic source. Optimization without traffic = vanity work.
- **$5k–$25k/mo plateau** — PDP + cart drawer surgery. Apps audit. First Klaviyo flows.
- **$25k–$100k/mo** — Bundles + subscriptions. Server-side tracking (GA4 + Meta CAPI). Search & filtering depth.
- **$100k+/mo** — Plus features (B2B, Markets, Checkout Extensibility). Tax automation. Loyalty. Real CRO testing (Optimizely / VWO).

## App Stack Recommendations (2026)

Default stack for under $100k/mo (cost-conscious, all proven):

- **Reviews:** Judge.me ($15/mo) or Loox ($9.99–$34.99/mo)
- **Email/SMS:** Klaviyo (free up to 250 contacts, then $20+/mo)
- **Bundles:** Shopify Bundles (free, Online Store 2.0 themes only)
- **Subscriptions:** Shopify Subscriptions (free, in-house) or Recharge for advanced
- **Search:** Shopify Search & Discovery (free)
- **Loyalty (>$30k/mo only):** Smile.io ($49+/mo)
- **Upsell post-purchase:** ReConvert ($4.99–$24.99/mo) — high ROI, low effort
- **Heatmap:** Microsoft Clarity (free)

Avoid stacking: 3 review apps, 2 popup apps, dueling discount apps. Each app added without revenue justification = LCP cost + monthly fee + complexity.

## Shopify Plus Decision Tree

Plus ($2,300/mo or 0.4% rev) makes sense at:

- Revenue > $1M/yr (cost as % becomes reasonable)
- Need: Wholesale (B2B), Markets+ (multi-currency PDP control), Checkout Extensibility apps, Launchpad for sales, Flow automations
- 15+ stores under one org
- Custom checkout requirements

Don't move to Plus to "look bigger." Move to Plus when you can't ship a deal without it.

## BFCM Prep Playbook

8 weeks out:
- Lock in promo strategy. Site-wide vs collection-specific.
- Test load with WebPageTest + traffic simulation.
- Stage all banners, popups, price changes in a draft theme.
- Email warm-up (send-volume ramp up to avoid spam folder Nov 27).
- Stock and shipping cutoff calendar.

2 weeks out:
- Freeze new features. Bug-fix only.
- Customer support staffing plan.
- Backup theme + database.

Day-of:
- Theme deploy via "Publish" (not edit live).
- Live monitoring: GA4 realtime, Klaviyo deliverability, support inbox SLA.

## Metric Benchmarks (DTC, 2026)

- **Conversion rate:** mobile 1.5–2.5%, desktop 2.5–4%
- **AOV:** apparel $60–90, beauty $50–75, home $80–150, supplements $40–55
- **Bounce on PDP:** <55% healthy, >70% diagnose
- **Add-to-cart rate:** 8–12%
- **Cart-to-checkout:** 35–45%
- **Checkout-to-order:** 75–85% (drops below = friction or trust gap)
- **Returning customer rate:** 25–35% mature brand

If the store is below benchmark on multiple metrics, the diagnosis order is: speed → PDP → cart → checkout → retention.

## Output Format

The agent produces:

1. **Snapshot:** revenue range, CR, AOV, mobile share, theme, app count, plan tier
2. **Top 5 fixes** (week 1) — ranked by ROI, with effort and expected lift
3. **Medium-term roadmap** (month 1) — 5–8 items
4. **Strategic moves** (quarter 1) — 2–3 items
5. **Killed apps / bad spend** — what to remove this week
6. **Tracking gaps** — analytics, attribution, funnel events missing

No filler, no "leverage synergies." Concrete fixes with theme files, app names, and configuration steps.
