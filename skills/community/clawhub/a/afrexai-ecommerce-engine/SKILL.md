# Ecommerce Operations Engine

Complete system for launching, optimizing, and scaling ecommerce businesses — from product selection through multi-channel operations and profitability management. Works for DTC brands, marketplace sellers, and hybrid operations.

---

## Phase 1: Business Foundation & Product Strategy

### Ecommerce Business Brief

```yaml
business_brief:
  brand_name: ""
  stage: "idea | launch | growth | scale"
  model: "DTC | marketplace | hybrid | dropship | wholesale"
  channels: []  # shopify, amazon, ebay, etsy, walmart, tiktok-shop
  category: ""
  target_customer: ""
  avg_order_value_target: "$"
  monthly_revenue_target: "$"
  current_monthly_revenue: "$"
  biggest_challenge: ""
  competitive_advantage: ""
```

### Product Selection Scorecard (0-100)

Score each product candidate across 5 dimensions:

| Dimension | Weight | Score 1-5 | Criteria |
|-----------|--------|-----------|----------|
| **Demand** | 25% | _ | Search volume >1K/mo, trending up, not seasonal-only |
| **Margin** | 25% | _ | >60% gross margin after ALL costs (COGS+shipping+fees+returns) |
| **Competition** | 20% | _ | <50 direct competitors, no dominant brand >40% share |
| **Logistics** | 15% | _ | <2lb, non-fragile, no hazmat, easy to ship and store |
| **Moat** | 15% | _ | Brandable, can differentiate, not easily commoditized |

**Score = Σ(weight × score × 4) → scale to 100**

- **80+**: Strong candidate — proceed to sourcing
- **60-79**: Viable with differentiation strategy
- **40-59**: Risky — needs unique angle or pass
- **<40**: Kill — move to next candidate

### Product Research Process

1. **Demand validation**: Search volume (Google Trends, Keyword Planner), Amazon BSR rank, social mention volume
2. **Competition mapping**: Count page-1 sellers, check review counts (>500 reviews = entrenched), brand registry presence
3. **Margin calculation**: Get 3 supplier quotes, calculate landed cost + all fees (see Unit Economics below)
4. **Trend direction**: Google Trends 12-month slope, seasonal patterns, category growth rate
5. **Kill criteria**: If margin <40% after all costs, if top 3 sellers have >10K reviews each, if product is restricted/gated

### Sourcing Decision Tree

```
Need product sourced?
├── Volume <100 units/month → Domestic wholesale or print-on-demand
├── Volume 100-1000 → Alibaba verified suppliers (Gold+ status, Trade Assurance)
├── Volume 1000+ → Direct factory (attend Canton Fair or hire sourcing agent)
└── Digital product → No sourcing needed (courses, templates, software)

For physical products ALWAYS:
1. Order 3-5 samples from different suppliers
2. Test quality, packaging, shipping time
3. Negotiate MOQ down for first order (mention "trial order, larger orders planned")
4. Get product liability insurance before selling
```

---

## Phase 2: Unit Economics & Pricing

### Complete Cost Stack (calculate for EVERY SKU)

```yaml
unit_economics:
  sku: ""
  selling_price: 0.00
  
  # Cost of Goods
  product_cost: 0.00        # Per unit from supplier
  shipping_to_warehouse: 0.00  # Freight / unit
  packaging: 0.00           # Box, inserts, tape
  labeling: 0.00            # FNSKU, barcodes
  landed_cost: 0.00         # Sum of above
  
  # Platform Fees (calculate per channel)
  referral_fee: 0.00        # Amazon: 8-45% by category
  fba_fee: 0.00             # Or 3PL pick/pack
  payment_processing: 0.00  # Stripe 2.9%+30¢, PayPal 3.49%+49¢
  subscription_fee_per_unit: 0.00  # Shopify plan / units
  
  # Fulfillment
  shipping_to_customer: 0.00
  packaging_materials: 0.00
  
  # Variable Costs
  return_rate: 0.00         # % (fashion 20-30%, electronics 5-10%)
  return_cost_per_unit: 0.00  # Return shipping + restock + lost inventory
  advertising_cost_per_unit: 0.00  # Total ad spend / units sold (target: <15% of revenue)
  
  # Calculated
  total_cost_per_unit: 0.00
  gross_profit: 0.00
  gross_margin_pct: 0.00    # TARGET: >60% for DTC, >30% for marketplace
  contribution_margin: 0.00  # After variable costs
  break_even_units: 0       # Fixed costs / contribution margin
```

### Pricing Strategy by Channel

| Channel | Pricing Rule | Fee Structure | Margin Target |
|---------|-------------|---------------|---------------|
| **Own store (Shopify)** | Full price, brand premium | 2.9% + 30¢ payment | >65% |
| **Amazon** | Competitive, Buy Box eligible | 15% referral + FBA | >30% |
| **eBay** | 5-10% below Amazon | 13% final value | >25% |
| **Walmart** | Match or beat Amazon | 6-20% referral | >30% |
| **Etsy** | Premium (handmade perception) | 6.5% transaction + 3% payment | >50% |
| **TikTok Shop** | Impulse price (<$50) | 5% + 1.8% payment | >40% |

### Pricing Psychology Toolkit

1. **Charm pricing**: $47 not $50, $97 not $100 (9% higher conversion)
2. **Anchor pricing**: Show "Compare at $X" with 30-50% perceived discount
3. **Bundle pricing**: 2-pack at 15% discount increases AOV 25-40%
4. **Free shipping threshold**: Set at 30% above current AOV (e.g., AOV $35 → free ship at $45)
5. **Subscription discount**: 10-15% off for recurring (increases LTV 2-3x)
6. **Decoy pricing**: 3 options where middle is the target (small $19, medium $29, large $32)

---

## Phase 3: Store Setup & Optimization

### Shopify Store Launch Checklist

```
[ ] Domain purchased and connected (use .com, avoid hyphens)
[ ] SSL certificate active (automatic with Shopify)
[ ] Theme selected and customized (Dawn for speed, or premium for $)
[ ] Logo and brand assets uploaded
[ ] Navigation structured (max 7 top-level items)
[ ] Homepage: hero image + value prop + 3 trust badges + featured products + social proof
[ ] Product pages optimized (see Product Page template below)
[ ] Collection pages with filters
[ ] About page (brand story, team, mission)
[ ] Contact page with form + email + phone
[ ] FAQ page (reduces support tickets 30-40%)
[ ] Shipping policy page
[ ] Return policy page (generous = higher conversion)
[ ] Privacy policy + Terms of Service (auto-generated + reviewed)
[ ] Payment gateways configured (Shop Pay + PayPal + Apple Pay + Google Pay)
[ ] Tax settings configured (use automated tax with Avalara)
[ ] Shipping zones and rates configured
[ ] Email flows set up (see Email Automation section)
[ ] Google Analytics 4 installed
[ ] Facebook Pixel installed
[ ] Conversion tracking verified (test purchase)
[ ] Mobile experience tested (60%+ of traffic is mobile)
[ ] Page speed score >70 on Google PageSpeed Insights
[ ] 404 page customized with search + popular products
```

### Product Page Template (High-Converting)

```
ABOVE THE FOLD:
├── Product images (7+ images: hero, lifestyle, detail, scale, packaging, infographic, video)
├── Product title (benefit-driven, include primary keyword)
├── Star rating + review count (social proof)
├── Price (with compare-at if applicable)
├── Key benefits (3-4 bullet points with icons)
├── Variant selector (color, size with guide link)
├── Add to Cart button (high contrast, sticky on mobile)
├── Trust badges (secure checkout, free shipping, guarantee)
└── Urgency element (stock count or shipping deadline — only if real)

BELOW THE FOLD:
├── Detailed description (features → benefits → use cases)
├── Size/spec chart
├── Comparison table vs competitors (or vs previous version)
├── Social proof section (UGC photos, testimonials, press mentions)
├── FAQ accordion (5-8 product-specific questions)
├── Reviews section (with photo reviews highlighted)
├── Related products / "Frequently bought together"
└── Sticky ATC bar on scroll (mobile)
```

### Amazon Listing Optimization

**Title Formula** (200 chars max, front-load keywords):
`[Brand] [Primary Keyword] - [Key Benefit] [Material/Size] [Secondary Keyword] for [Use Case]`

**Bullet Points** (5 bullets, each 200-250 chars):
1. PRIMARY BENEFIT — Lead with the #1 reason people buy
2. KEY FEATURE — What makes this different
3. USE CASE — Help buyer visualize using it
4. QUALITY/MATERIAL — Build trust
5. GUARANTEE — Risk reversal ("100% satisfaction or your money back")

**Backend Keywords** (250 bytes):
- No commas needed (space-separated)
- No brand names (yours or competitors — TOS violation)
- Include misspellings, synonyms, Spanish translations
- No duplicates of title/bullet words

**A+ Content** (if brand registered):
- Comparison chart module (yours vs generic)
- Rich image + text modules telling brand story
- Cross-sell module linking to other products

---

## Phase 4: Traffic & Customer Acquisition

### Channel Strategy by Stage

| Stage | Primary Channels | Budget Allocation | Focus |
|-------|-----------------|-------------------|-------|
| **Launch (0-$10K/mo)** | Organic social, influencer seeding, Amazon PPC | 80% paid, 20% organic | Validate product-market fit |
| **Growth ($10K-$100K/mo)** | Meta Ads, Google Ads, Amazon PPC, email | 60% paid, 25% email, 15% organic | Scale profitable channels |
| **Scale ($100K+/mo)** | All channels + wholesale + retail | 40% paid, 30% email/SMS, 20% organic, 10% new | Diversify, reduce CAC |

### Paid Acquisition Framework

**Meta Ads (Facebook/Instagram)**:
```yaml
campaign_structure:
  testing:
    budget: "$20-50/day per ad set"
    objective: "Purchase"
    targeting: "Broad or 1 interest stack"
    creative: "3-5 creatives per ad set"
    kill_criteria: "No purchase after 2x AOV spend"
    
  scaling:
    method: "Duplicate winning ad sets at 20% budget increase"
    frequency: "Every 3-4 days if ROAS holds"
    ceiling: "When CPM rises >20% or ROAS drops below target"
    
  creative_types_ranked:
    1: "UGC video testimonial (best performer for most DTC)"
    2: "Before/after or problem/solution"
    3: "Founder story / behind the scenes"
    4: "Product demo / unboxing"
    5: "Static image with bold text overlay"
    
  metrics_targets:
    ctr: ">1.5% (link clicks)"
    cpc: "<$2 for <$50 AOV, <$5 for >$50 AOV"
    roas: ">3x for <$50 AOV, >2x for >$100 AOV"
    frequency: "<3 in 7 days"
```

**Google Ads**:
```yaml
campaign_priority:
  1: "Brand search (capture branded traffic, ROAS 10x+)"
  2: "Shopping campaigns (product feed optimization critical)"
  3: "Non-brand search (high-intent keywords)"
  4: "Performance Max (let Google optimize across surfaces)"
  5: "YouTube (top-of-funnel, retargeting)"

shopping_feed_optimization:
  - Title: include primary keyword + brand + key attribute
  - Description: benefit-rich, keyword-natural
  - Images: white background, high-res, no text overlay
  - Product type: use detailed taxonomy
  - GTIN/UPC: always include (improves visibility)
  - Custom labels: margin tier, bestseller, seasonal
```

**Amazon PPC**:
```yaml
campaign_structure:
  auto_campaign:
    purpose: "Keyword discovery"
    bid: "Start at $0.50-0.75, adjust weekly"
    negatives: "Add irrelevant terms weekly"
    
  manual_exact:
    purpose: "Scale proven keywords"
    source: "Graduate from auto campaign (>3 orders)"
    bid: "Aggressive — these are proven converters"
    
  manual_phrase:
    purpose: "Capture long-tail variations"
    bid: "Moderate"
    
  sponsored_brands:
    purpose: "Brand awareness + cross-sell"
    when: "After 10+ reviews and brand registered"
    
  targets:
    acos: "<30% for growth, <20% for profit"
    tacos: "<12% of total revenue"
```

### Organic Acquisition

**SEO for Ecommerce**:
- Blog targeting "best [product] for [use case]" keywords
- Category page optimization (unique descriptions, not just product grid)
- Product schema markup (rich snippets in search)
- Build topical authority: 10+ articles per product category
- Target featured snippets with comparison tables and lists

**Social Commerce**:
- Instagram: 4-7 posts/week (Reels prioritized), shoppable tags
- TikTok: 1-3 videos/day (volume > polish), TikTok Shop linked
- Pinterest: Pin every product, SEO-rich descriptions (evergreen traffic)
- YouTube: Product reviews, how-tos, unboxings (long-tail search)

---

## Phase 5: Email & SMS Automation

### Email Flow Architecture (Non-Negotiable)

```yaml
flow_1_welcome:
  trigger: "Email signup"
  emails:
    - delay: "immediate"
      content: "Welcome + discount code + brand story"
    - delay: "+1 day"
      content: "Best sellers + social proof"
    - delay: "+3 days"
      content: "Founder story + UGC"
    - delay: "+5 days"
      content: "Discount reminder (expiring)"
  expected_revenue: "20-30% of email revenue"

flow_2_abandoned_cart:
  trigger: "Cart abandoned"
  emails:
    - delay: "+1 hour"
      content: "Forgot something? (product image, no discount)"
    - delay: "+24 hours"
      content: "Social proof + FAQ (overcome objections)"
    - delay: "+48 hours"
      content: "Last chance + 10% discount or free shipping"
  expected_recovery: "5-15% of abandoned carts"

flow_3_browse_abandonment:
  trigger: "Viewed product, no add-to-cart"
  emails:
    - delay: "+2 hours"
      content: "Still looking? (product + similar items)"
    - delay: "+24 hours"
      content: "Reviews for that product"
  expected_conversion: "1-3%"

flow_4_post_purchase:
  trigger: "Order placed"
  emails:
    - delay: "immediate"
      content: "Order confirmation + what to expect"
    - delay: "+3 days"
      content: "Shipping update + how to use product (if applicable)"
    - delay: "+7 days (after delivery)"
      content: "How's your [product]? (review request)"
    - delay: "+14 days"
      content: "Cross-sell complementary products"
    - delay: "+30 days"
      content: "Replenishment reminder (if consumable) or VIP program invite"

flow_5_winback:
  trigger: "No purchase in 60 days"
  emails:
    - delay: "immediate"
      content: "We miss you + what's new"
    - delay: "+7 days"
      content: "Exclusive comeback offer (15-20% off)"
    - delay: "+14 days"
      content: "Last chance before we stop emailing"
  after_flow: "If no purchase, move to sunset segment (reduce frequency)"

flow_6_vip:
  trigger: "3+ orders OR top 10% by spend"
  emails:
    - content: "Early access to new products"
    - content: "Exclusive VIP-only discounts"
    - content: "Birthday/anniversary rewards"
    - content: "Referral program with premium incentives"
```

### SMS Strategy (Complement, Don't Duplicate)

- **Use for**: Flash sales, back-in-stock, shipping updates, abandoned cart (2nd touch)
- **Don't use for**: Brand storytelling, long content, cold outreach
- **Frequency**: Max 4-6 SMS/month (fatigue kills fast)
- **Timing**: 10am-8pm local time only
- **Format**: Short (<160 chars), clear CTA, always include opt-out

### Email Health Metrics

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Open rate | >25% | 15-25% | <15% |
| Click rate | >3% | 1.5-3% | <1.5% |
| Unsubscribe | <0.3% | 0.3-0.5% | >0.5% |
| Revenue per email | >$0.10 | $0.05-0.10 | <$0.05 |
| List growth | >5%/mo | 2-5%/mo | <2%/mo |

---

## Phase 6: Conversion Rate Optimization

### CRO Prioritization Framework

Score each test idea:

| Factor | Score 1-5 | Description |
|--------|-----------|-------------|
| **Traffic** | _ | How much traffic hits this page? (5 = homepage, 1 = obscure page) |
| **Impact** | _ | How much will conversion improve? (5 = fundamental change, 1 = minor tweak) |
| **Ease** | _ | How easy to implement? (5 = copy change, 1 = full redesign) |
| **Confidence** | _ | How sure are we this will work? (5 = proven elsewhere, 1 = gut feeling) |

**Priority Score = Traffic × Impact × Ease × Confidence** → Test highest scores first

### High-Impact CRO Quick Wins

1. **Add trust badges near ATC button** (+5-15% conversion)
2. **Show shipping cost/timeline on product page** (reduces cart abandonment 18%)
3. **Add "Frequently bought together" section** (+10-30% AOV)
4. **Simplify checkout to single page** (+20-35% checkout completion)
5. **Add guest checkout option** (+45% for new customers)
6. **Show stock scarcity** (only if real — "Only 3 left" +7%)
7. **Add payment logos below ATC** (+5% perceived security)
8. **Product video** (+80% time on page, +64-85% purchase likelihood)
9. **Live chat / chatbot** (+12-20% conversion on high-consideration products)
10. **Exit-intent popup with offer** (+3-5% of bouncing visitors)

### Ecommerce Conversion Benchmarks

| Metric | Poor | Average | Good | Excellent |
|--------|------|---------|------|-----------|
| **Site conversion** | <1% | 1-2% | 2-3.5% | >3.5% |
| **Add-to-cart rate** | <5% | 5-8% | 8-12% | >12% |
| **Cart-to-purchase** | <30% | 30-50% | 50-65% | >65% |
| **Email signup rate** | <1% | 1-3% | 3-5% | >5% |
| **Return rate** | >25% | 15-25% | 8-15% | <8% |
| **Repeat purchase** | <15% | 15-25% | 25-40% | >40% |

---

## Phase 7: Inventory & Fulfillment

### Fulfillment Model Decision

```
Sales volume?
├── <50 orders/month → Self-fulfill (garage/spare room)
├── 50-500 orders/month → 3PL or FBA
│   ├── Selling on Amazon? → FBA (Buy Box advantage)
│   └── DTC primarily? → 3PL (ShipBob, ShipMonk, Deliverr)
├── 500-5000 orders/month → Hybrid FBA + 3PL
└── 5000+ orders/month → Dedicated 3PL + FBA + own warehouse evaluation
```

### Inventory Management Rules

1. **Reorder point** = (Average daily sales × Lead time in days) + Safety stock
2. **Safety stock** = Average daily sales × Safety days (start with 14 days)
3. **Never go below 14 days stock** — stockouts kill Amazon ranking and ad momentum
4. **Track inventory velocity weekly** — days of supply for each SKU
5. **ABC classification**:
   - A items (top 20% of SKUs, 80% of revenue): Daily monitoring, never stockout
   - B items (next 30%): Weekly monitoring
   - C items (bottom 50%): Monthly review, consider cutting slow movers

### Dead Stock Protocol

| Days Without Sale | Action |
|-------------------|--------|
| 60 days | Flag for review — check listing quality, pricing |
| 90 days | Run clearance promotion (30-50% off) or bundle with A items |
| 120 days | Liquidate at cost (Amazon Outlet, B-stock marketplaces) |
| 180 days | Donate (get tax write-off) or dispose — storage costs exceed value |

---

## Phase 8: Customer Experience & Retention

### Customer Service Standards

| Channel | Response Time Target | Resolution Target |
|---------|---------------------|-------------------|
| Live chat | <2 minutes | Same session |
| Email/ticket | <4 hours (business) | <24 hours |
| Social DM | <1 hour | <4 hours |
| Phone | <30 seconds | Same call |
| Amazon messages | <12 hours (24h max or ODR hit) | <24 hours |

### Return Policy Framework

**Generous returns = higher conversion + higher LTV**:
- 30-day minimum (60-90 preferred for DTC)
- Free return shipping for defective/wrong items
- Customer-paid returns for "changed mind" (provide label at cost)
- Instant refund on receipt (or keep-the-item for <$15 items — cheaper than return processing)
- Track return reasons → feed into product improvement

### Loyalty & Repeat Purchase System

```yaml
loyalty_program:
  type: "points | tiered | VIP | subscription"
  
  points_program:
    earn: "1 point per $1 spent"
    bonus: "200 points on signup, 100 on review, 500 on referral"
    redeem: "100 points = $1 off"
    expire: "Never (or 12 months with notice)"
    
  tier_program:
    bronze: "0-$200/year → 1x points"
    silver: "$200-500/year → 1.5x points + free shipping"
    gold: "$500+/year → 2x points + early access + free shipping"
    
  referral:
    give: "$15 off first order"
    get: "$15 credit after friend's first purchase"
    target: "3% of customers refer (good), 5%+ (excellent)"
```

### Key Retention Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| **Repeat purchase rate** | Returning customers / total customers | >25% |
| **Purchase frequency** | Total orders / unique customers (12 mo) | >2x/year |
| **Customer lifetime value** | AOV × Purchase frequency × Lifespan | >3x CAC |
| **Net Promoter Score** | % Promoters (9-10) minus % Detractors (0-6) | >50 |
| **Churn rate** | Customers lost / starting customers (period) | <5%/month |

---

## Phase 9: Analytics & Reporting

### Weekly Ecommerce Dashboard

```yaml
weekly_dashboard:
  date_range: ""
  
  revenue:
    total_revenue: "$"
    vs_last_week: "+/- %"
    vs_same_week_last_year: "+/- %"
    orders: 0
    aov: "$"
    units_sold: 0
    
  traffic:
    sessions: 0
    unique_visitors: 0
    top_sources:
      - source: ""
        sessions: 0
        conversion_rate: "%"
        revenue: "$"
    
  conversion:
    site_conversion_rate: "%"
    add_to_cart_rate: "%"
    cart_to_purchase_rate: "%"
    
  acquisition:
    total_ad_spend: "$"
    roas: "x"
    cac: "$"
    new_vs_returning: "% / %"
    email_revenue: "$"
    email_pct_of_total: "%"
    
  product_performance:
    top_5_by_revenue: []
    top_5_by_units: []
    bottom_5_by_revenue: []
    return_rate_by_sku: []
    
  inventory:
    days_of_supply_avg: 0
    stockout_skus: []
    overstock_skus: []
    
  customer:
    new_customers: 0
    repeat_customers: 0
    repeat_rate: "%"
    avg_reviews_received: 0
    csat_or_nps: 0
    
  action_items:
    - item: ""
      owner: ""
      deadline: ""
```

### Monthly P&L Template

```
Revenue
  Gross sales                    $______
  - Discounts                    $______
  - Returns/refunds              $______
  = Net Revenue                  $______

Cost of Goods Sold
  Product cost                   $______
  Shipping to warehouse          $______
  Packaging                      $______
  = Total COGS                   $______

= Gross Profit                   $______ (target: >60% DTC, >30% marketplace)

Operating Expenses
  Advertising                    $______ (target: <25% of revenue)
  Platform fees                  $______
  Software/tools                 $______
  Fulfillment/3PL                $______
  Customer service               $______
  Returns processing             $______
  = Total OpEx                   $______

= Net Operating Profit           $______ (target: >15%)

Cash Flow Note
  Inventory investment           $______
  Accounts payable               $______
  Cash on hand                   $______
  Runway (months)                ______
```

---

## Phase 10: Scaling & Multi-Channel

### Multi-Channel Expansion Sequence

```
1. Start on ONE channel — master it (profitable, repeatable)
2. Add channel #2 only when channel #1 is profitable at scale
3. Never launch >1 new channel simultaneously

Recommended sequence for most brands:
  DTC-first: Shopify → Amazon → Google Shopping → Walmart → TikTok Shop → Wholesale
  Marketplace-first: Amazon → Shopify (DTC) → Walmart → eBay → TikTok Shop
  Handmade/Niche: Etsy → Shopify → Amazon Handmade → Wholesale → Faire
```

### Channel Integration Rules

1. **Unified inventory**: Single source of truth prevents overselling (use Sellbrite, Linnworks, or ChannelAdvisor)
2. **Consistent pricing**: MAP (minimum advertised price) policy if you wholesale
3. **Channel-specific listings**: Don't copy-paste — optimize for each platform's algorithm
4. **Separate P&L per channel**: Know which channels are actually profitable
5. **Brand consistency**: Same imagery, voice, and quality across all touchpoints

### Scaling Levers (in order of impact)

1. **Increase AOV**: Bundles, upsells, cross-sells, free shipping threshold
2. **Increase conversion rate**: CRO testing, better creative, social proof
3. **Increase traffic**: Scale winning ad channels, launch new channels, SEO
4. **Increase repeat rate**: Email/SMS automation, loyalty program, subscription
5. **Expand catalog**: New products in same category (lower risk), adjacent categories
6. **International**: Start with Canada/UK (English-speaking), then EU, then APAC

### International Expansion Checklist

```
[ ] Market research: demand exists for product category
[ ] Regulatory check: certifications, restricted ingredients, labeling requirements
[ ] Tax registration: VAT/GST in target country
[ ] Logistics: FBA international, local 3PL, or cross-border shipping
[ ] Localized listings: native language, local measurements, local price points
[ ] Customer service: support in local language and timezone
[ ] Payment methods: local preferences (iDEAL in NL, Klarna in DE, PIX in BR)
[ ] Returns: local return address or keep-the-item policy for international
```

---

## Phase 11: Risk Management & Compliance

### Platform Risk Mitigation

| Risk | Prevention | Recovery |
|------|-----------|----------|
| **Amazon suspension** | ODR <1%, no TOS violations, respond to claims in 24h | Appeal with plan of action (root cause, actions taken, preventive measures) |
| **Ad account ban** | No misleading claims, diversify creative, follow platform policies | Appeal + diversify to other channels immediately |
| **Supplier failure** | Dual-source critical SKUs, maintain 30-day safety stock | Activate backup supplier, raise prices temporarily if needed |
| **Chargebacks** | Clear billing descriptor, easy returns, fraud detection | Dispute with evidence, implement fraud filters (Signifyd, NoFraud) |
| **IP complaint** | Verify product is not infringing, document supply chain | Respond to complaint, get authorization letter from brand, or delist |

### Legal & Compliance Checklist

```
[ ] Business entity formed (LLC or Corp)
[ ] Sales tax registered in nexus states (economic nexus thresholds vary)
[ ] Product liability insurance ($1M minimum)
[ ] Proper labeling (country of origin, materials, care instructions)
[ ] FDA compliance (if food, supplements, cosmetics)
[ ] CPSC compliance (if children's products)
[ ] California Prop 65 warning (if applicable)
[ ] GDPR/CCPA privacy compliance (cookie consent, data handling)
[ ] Terms of service and return policy published
[ ] Trademark filed for brand name and logo
```

### Fraud Prevention Rules

1. **Address mismatch**: Billing ≠ shipping on high-value orders → verify before shipping
2. **Velocity check**: Multiple orders from same IP/email in short time → hold for review
3. **International high-risk**: First-time buyer, high-value, expedited shipping → verify
4. **Gift card abuse**: Large gift card purchases → limit per transaction
5. **Tool recommendation**: Shopify Fraud Analysis (built-in) + Signifyd or NoFraud for scaling

---

## 100-Point Ecommerce Health Rubric

| Dimension | Weight | Score 0-10 | Key Indicators |
|-----------|--------|------------|----------------|
| **Product-Market Fit** | 15% | _ | Repeat purchase >25%, organic reviews growing, NPS >40 |
| **Unit Economics** | 15% | _ | Gross margin >50%, LTV:CAC >3:1, positive contribution margin |
| **Traffic & Acquisition** | 15% | _ | Diversified sources (no channel >50%), CAC trending down, ROAS >3x |
| **Conversion** | 10% | _ | Site CVR >2%, cart completion >50%, improving MoM |
| **Operations** | 10% | _ | No stockouts on A items, shipping <2 days, return rate <15% |
| **Customer Experience** | 10% | _ | Response time <4h, CSAT >4.5/5, churn <5%/mo |
| **Email/Retention** | 10% | _ | Email >25% of revenue, flows automated, list growing >5%/mo |
| **Financial Health** | 10% | _ | Net profit >15%, positive cash flow, >3mo runway |
| **Brand & Moat** | 5% | _ | Trademark filed, brand search growing, differentiated positioning |

**Score = Σ(weight × score × 10)**

- **85+**: Category leader — optimize and scale
- **70-84**: Strong foundation — fix gaps and accelerate
- **50-69**: Work in progress — prioritize unit economics and conversion
- **<50**: Fundamentals broken — fix before spending on growth

---

## Edge Cases & Advanced Patterns

### Seasonal Business Management
- Build 60% of annual inventory 3 months before peak
- Ramp ad spend 6 weeks before peak, scale 2x during
- Plan post-season clearance (30% discount) to avoid dead stock carrying costs
- Maintain skeleton operations in off-season (keep email list warm, SEO content)

### Subscription / Replenishment Model
- Offer 10-15% discount vs one-time (3x LTV improvement typical)
- Default to the most common replenishment cycle (auto-selected)
- Allow easy skip/pause (reduces cancellations 40%)
- Surprise & delight: occasional free sample or upgrade in box

### Wholesale / B2B Channel
- Minimum order: 12-24 units (or $250+)
- Wholesale pricing: 50% off retail (your margin should still be >30% at wholesale)
- Terms: Net 30 for established retailers, prepay for new accounts
- Use Faire, Abound, or direct sales for distribution

### Dropshipping Specific
- Margin must be >40% (lower volume = need higher margin per unit)
- Test with 3-5 products, kill non-performers in 14 days
- Shipping time >10 days = customer complaint magnet → use domestic suppliers or agents with US/EU warehouses
- Brand the experience (custom packaging, inserts) even if dropshipping

### Marketplace-to-Brand Transition
1. Build email list from marketplace customers (insert cards in packaging with QR to website)
2. Launch Shopify store with same products at same or slightly higher prices
3. Drive repeat purchasers to DTC with exclusive offers
4. Gradually shift ad spend: marketplace PPC → DTC paid social
5. Goal: 50%+ revenue from owned channels within 18 months

---

## Natural Language Commands

| Command | What It Does |
|---------|-------------|
| "Evaluate this product idea" | Run Product Selection Scorecard |
| "Calculate my unit economics" | Build complete cost stack with margin analysis |
| "Optimize my product listing" | Review and improve title, bullets, images, keywords |
| "Build my email flows" | Design complete automation architecture |
| "Review my ad performance" | Analyze ROAS, CAC, creative performance |
| "Run a CRO audit" | Score current site and prioritize tests |
| "Check my inventory health" | Analyze days of supply, stockouts, dead stock |
| "Build my weekly dashboard" | Generate weekly ecommerce report |
| "Plan my channel expansion" | Recommend next channel with launch checklist |
| "Calculate my P&L" | Generate monthly profit and loss statement |
| "Audit my compliance" | Run legal and platform compliance checklist |
| "Score my ecommerce health" | Run 100-point rubric with recommendations |
