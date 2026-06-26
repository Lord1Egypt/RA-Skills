---
name: b2b-saas-pricing-coach
description: Coach for B2B SaaS founders on pricing — choosing the value metric (per-seat, per-API-call, per-MAU, per-revenue-processed, per-asset-monitored, per-feature-tier, per-outcome), structuring tiers (Starter / Pro / Business / Enterprise) without trapping yourself, setting headline prices that ladder properly to ACV targets, deciding when to sell free trial vs freemium vs no-free, packaging logic (what's in tier vs add-on vs Enterprise-only), discounting policy + sales-led friction, the contract-period question (monthly vs annual vs multi-year), repricing existing customers without losing them, and re-pricing during inflation / cost shocks. Use when founder says "what should we charge", "pricing v2", "raise prices", "going from PLG to sales-led pricing", "free vs freemium", "annual contract pricing", "SaaS pricing tier strategy", "value metric", "per-seat pricing too low", "enterprise tier needed". Triggers on phrases like "B2B SaaS pricing", "SaaS pricing strategy", "value metric", "per-seat pricing", "usage-based pricing", "freemium vs free trial", "tier packaging", "enterprise pricing", "SaaS price increase", "grandfathering customers", "expansion revenue", "annual contract value", "ACV vs ARR".
---

# b2b-saas-pricing-coach

Coach a B2B SaaS founder through pricing — initial pricing for a new product, repricing for one that's been in market, or restructuring tiers and value metrics that have stopped working. The job is structural, not cosmetic: most pricing failures are about the wrong value metric or wrong tier-packaging, not the wrong dollar amount.

The 2024-2026 B2B SaaS pricing landscape has shifted:
- Per-seat is becoming weaker as a primary value metric (especially for AI-augmented products where one user does the work of many)
- Usage-based pricing has matured (now standard for infrastructure, AI APIs, observability) but is still hard for traditional CRUD apps
- Sales-led + product-led hybrid is the dominant motion (not pure PLG, not pure sales-led)
- Annual prepay norms have weakened; net-30 monthly billing is more common at SMB
- Enterprise tier is required earlier than founders expect (by ~$2-3M ARR, customers ask for it)

This coach walks the founder through diagnostic, value-metric choice, tier design, headline pricing, packaging, sales motion alignment, and ongoing pricing discipline.

## When to engage

Trigger when the founder mentions:
- Initial pricing decisions: "I'm launching, what do I charge", "first three customers", "what's the right per-seat", "how many tiers"
- Repricing: "my prices are too low", "raising prices", "going from $20 to $50", "regret giving customer X a discount"
- Tier restructure: "Starter / Pro / Business" mapping, "what goes in Pro vs Enterprise", "should we have a free tier"
- Value metric: "per-seat doesn't fit my product", "should I switch to usage-based", "per-API-call vs per-customer-record"
- Sales motion mismatch: "PLG isn't converting to paid", "sales reps can't sell at this price", "self-serve cap is $X but enterprise wants $Y"
- Contract period: "monthly vs annual", "multi-year discount", "auto-renew language"
- Discount discipline: "every deal turns into a 30% discount", "VPs are negotiating list price"
- Grandfathering: "raising prices, what about existing customers"
- Specific patterns: freemium-to-paid conversion, expansion revenue ratio, NRR / GRR pricing impact

Do not engage for: B2C / consumer subscription pricing (different dynamics), e-commerce / physical-product pricing, agency / services pricing (use consulting-rate-strategist), or open-source-monetization-only questions (different skill — open-core / OSS pricing has its own playbook).

## Diagnostic sweep

1. **Stage + maturity.**
   - Pre-PMF / first 10 customers: pricing is mostly a learning vehicle, not a revenue optimization. Don't over-engineer.
   - PMF + first $200K-$2M ARR: pricing is a deliberate growth tool. Wrong choices compound.
   - Scaling (>$2M ARR): pricing is now central to NRR, expansion, and unit economics. Repricing is high-leverage but high-risk.

2. **Sales motion.**
   - Pure PLG (self-serve, credit card, no sales team): pricing must be visible, simple, and ladder cleanly with usage growth
   - PLG + sales-assist (self-serve up to a threshold, then sales): pricing must transition cleanly between the two motions; one of the most common breaks
   - Pure sales-led (no public pricing, sales reps quote): pricing logic still must exist internally; "discoverable" pricing through call notes is a leak
   - Channel / partner-sold: list price + discount tiers for channel partners

3. **Customer ICP.**
   - SMB (1-100 employees): low ACV ($300-$5K), volume motion, expansion via seats / usage
   - Mid-market (100-1000): mid ACV ($5K-$50K), procurement involvement, annual contracts standard
   - Enterprise (1000+): high ACV ($50K-$500K+), 90-180 day sales cycles, security/compliance reviews, custom pricing common

4. **Value-creation pattern.**
   - Does the customer value increase with: more users, more API calls, more revenue processed, more assets monitored, more outcomes generated?
   - Is value broadly proportional to one variable? Or is it conditional on multiple variables?
   - This drives the value metric choice.

5. **Cost-to-serve.**
   - Compute / storage / API cost per active customer
   - Support cost per customer
   - Onboarding / implementation cost
   - Cost-to-serve floor must be below price floor by >70% (gross margin > 70% target for healthy SaaS).

6. **Competitive landscape.**
   - Direct competitors' public pricing (use ProductHunt, capterra, G2, public pricing pages, and "pricing" field on changelog announcements)
   - Adjacent-tool replacements (what is the customer using today instead?)
   - Status-quo / DIY cost (often the highest competitor)

7. **Existing customer base (if repricing).**
   - List of all customers, current price, contract end date, expansion / contraction trend
   - Customers paying way under current target, customers paying way over (anchored by anomaly)
   - Cohort by signup date — typically older cohorts paying less (price anchor drift)

## Choosing the value metric

The value metric is THE most consequential pricing decision. Wrong metric = pricing pressure, churn, expansion misalignment for years.

### Per-seat / per-user
- Pros: easy to understand, predictable, sales-friendly
- Cons: weak alignment with value when AI / automation lets one user do more work; ceiling exists at company size; discount pressure on big-team deals
- Right when: collaboration product (Slack, Notion, Figma, Linear), individual workflow product, customer team size grows over time
- Wrong when: AI-augmented (one analyst with your tool replaces 5 analysts without), API-centric, asset-monitoring, transaction processing
- Modern pattern: per-seat as floor + usage component on top

### Per-API-call / per-event / per-token
- Pros: aligns directly with usage; expansion automatic as customer scales
- Cons: customer billing-anxiety, hard to forecast, often gets discounted via committed-spend agreements
- Right when: infrastructure product (Twilio, SendGrid, Stripe), observability (Datadog), AI APIs (OpenAI, Anthropic), search/index
- Wrong when: workflow tools where call volume is decoupled from value
- Modern pattern: usage-based with commitment tiers (commit $X/month, get Y discount)

### Per-customer-record / per-asset / per-monitored-thing
- Pros: aligns with customer business size; expansion as customer grows
- Cons: requires clear definition of "record", customers may delete to manage cost
- Right when: CRM (per-contact), security tools (per-endpoint), ITSM (per-asset), analytics (per-event source)

### Per-revenue-processed / per-transaction-value
- Pros: tied to customer's economic outcome
- Cons: can become very cheap or very expensive based on customer mix; harder for finance to predict
- Right when: payments / fintech / e-commerce platforms / marketplace tools
- Modern pattern: take-rate (1-5%) with cap at high volumes

### Per-outcome / per-result
- Pros: maximum value alignment, hard to compete with
- Cons: hard to define and measure, attribution disputes
- Right when: lead-gen platforms (per-qualified-lead), AI agents (per-task-completed), security (per-prevented-incident — rarely works in practice)
- Modern pattern: outcome-pricing as Enterprise-tier add-on; not the default tier

### Hybrid (most modern B2B SaaS)
- Per-seat + per-usage: collaboration product with API or AI feature
- Per-asset + per-feature-tier: monitoring / security
- Per-customer-record + per-feature-tier: CRM-style
- Hybrid is harder to communicate but more accurate. Start single-axis; layer hybrid only when single-axis is clearly wrong.

### Test the metric
- Could you double a customer's bill while they hold the metric constant and they'd still feel they're getting value? If yes, metric undersells. If no, metric is fair.
- Could you halve the metric and the customer's bill drops without their value-receipt dropping? If yes, metric is over-aligned with value. If no, metric is right.

## Tier design — Starter / Pro / Business / Enterprise

Most B2B SaaS converges on 3-4 tiers. Don't invent a new model.

### Default 4-tier structure
- **Free / Starter**: $0-$50/month per seat (or modest usage allowance). Built for: trying the product, single-user use case, eligible for "credit card swipe" purchase
- **Pro**: $X (3-5x Starter price). Built for: small teams, common features needed
- **Business**: $Y (3-5x Pro). Built for: cross-team usage, integrations, admin controls
- **Enterprise**: "Contact us". Built for: SSO, SOC 2 review, custom DPA, procurement, dedicated CSM

### Tier-jump multiplier
- Default ratio: 3-4x between tiers. Less than 2.5x and customers won't bother upgrading; more than 5x and customers don't upgrade because the gap feels too big.

### What goes in each tier — packaging logic

Pack tiers around personas / job-to-be-done, not feature checklist:
- **Starter**: solo user, basic functionality, no admin
- **Pro**: small team (3-10 people), team admin, basic integrations
- **Business**: cross-team (20-100 people), advanced admin, role-based permissions, API access, advanced integrations, SLA
- **Enterprise**: SSO/SAML, SOC 2 / GDPR documentation, dedicated CSM, custom contract, audit logs, enterprise-only integrations (Workday, ServiceNow, etc.)

### What does NOT go in lower tiers (lock to Enterprise)
- SSO/SAML — Enterprise tier only (industry norm; customers expect this)
- SOC 2 / SOC 2 Type 2 documentation — Enterprise (or Business at minimum)
- Audit logs and security exports — Business or Enterprise
- Dedicated support / CSM — Business or Enterprise
- Service-level agreements — Business or Enterprise

### What should NOT be tier-locked (anti-pattern)
- Basic CRUD operations
- Read-only API
- Single-user features
- Anything that's a "core experience" of the product

If the customer can't experience the core value in Free/Starter, they'll churn before upgrading.

### Add-ons vs tier inclusion
- Add-on when: usage-based component that not all customers need (e.g., extra API calls, extra storage, premium support)
- Add-on when: feature is for a specific persona only (e.g., compliance archive for regulated industries)
- Tier-include when: feature is core to the persona of that tier
- Avoid: making everything an add-on (creates negotiation friction); making nothing an add-on (caps revenue per customer)

## Headline pricing

### Anchor logic
- Find your direct competitor's public price → set your price 0% to +30% above for "premium positioning" or -10% to -30% below for "challenger positioning"
- DO NOT undercut competitor by >40%. Looks weak; doesn't capture price-sensitive segment fully; trains market that you're cheap
- DO NOT exceed competitor by >50% without specific value-claim that justifies it

### Round-number pricing (US/EU B2B)
- $19, $29, $39, $49, $79, $99 for sub-$100 tiers (Starter)
- $99, $149, $199, $249, $299, $499 for Pro
- $499, $799, $999, $1499, $1999 for Business (often "starting at $X" because it's a minimum-seat or minimum-spend tier)
- $X+ for Enterprise (no list price)

### Public vs private pricing
- Public: builds inbound, removes negotiation friction, signals self-serve maturity
- Private (Enterprise): allows custom pricing, higher ACV, prevents anchoring competitors
- Default: public pricing through Business tier; "Contact us" for Enterprise

### "Per seat" vs "starting at"
- Per seat: simple, transparent, but caps total visible price
- Starting at: signals minimum, allows for upsell, but vague
- Default: per-seat with min-seat for higher tiers ("$99/user/month, 5-seat minimum")

## Free vs freemium vs free trial vs no-free

### Free trial (14 / 30 day)
- All features for trial period; revert to paid or expire
- Right when: product value is realized within trial window, sales-assist motion
- Wrong when: product takes >30 days to integrate (data warehouse, security tool)
- Friction: low (credit card sometimes optional)

### Freemium (perpetual free tier)
- Limited free version; paid for power features / scale
- Right when: PLG motion, viral / network features, single-user value present, low cost-to-serve free users
- Wrong when: cost-to-serve free users is high (compute-heavy, support-heavy)
- Friction: very low; sometimes too low (unqualified leads consume support)

### "Free for X" structures
- Free for first X users (then pay), free for first X events (then pay), free for X days (then pay)
- These are usually metered freemium with a clear upgrade trigger; clean if the trigger is reached predictably

### No free (sales-led only)
- Right when: Enterprise-only product, ACV $50K+, multi-month sales cycle
- Wrong when: SMB segment exists and competitors offer free; you'll lose self-serve

### Common mistakes
- Freemium too generous: free tier covers 80% of customer use cases, conversion <2%
- Freemium too restrictive: free users churn before experiencing value
- Free trial too short for integration timeline: customer never gets to value during trial
- Free trial doesn't auto-convert to paid: high churn at end of trial
- No-free with SMB ICP: lose self-serve segment to competitors

## Discounting policy

Most discount discipline failures: every sales rep can give 30%, leadership doesn't know real net price.

### Set the floor
- "Below 80% of list = approval required"
- "Below 60% of list = founder/VP approval required"
- "No discount permanently — only term-extension trades (4% per year of contract)"

### Acceptable discount triggers
- Annual prepay (10-15% off vs monthly)
- Multi-year (additional 5-10% per year of commitment)
- Volume (10%+ off above N seats / $X spend)
- Logo / case-study trade (5-10% in exchange for logo + customer call)
- Strategic deal (case-by-case, founder-approved)

### Unacceptable
- "I'll give you 30% if you close today" (anchors the customer to expect discount renewals)
- "Match competitor" without internal review (often the competitor's quote is bluff)
- Stair-step "list, then 10%, then 20%, then 25%" reveals desperation

### Document every discount
- Reason code: which trigger justified the discount
- Approver: who signed off
- Renewal expectation: does the discount carry to renewal or is it deal-specific?

## Annual vs monthly contracts

### Annual prepay
- Pros: cash up front, lower churn, predictable revenue
- Cons: longer sales cycle (procurement involvement at $5K+), refund pressure
- Discount: 15-25% off monthly equivalent

### Monthly
- Pros: easier first-conversion, faster cash, less procurement
- Cons: higher churn, less revenue predictability, harder forecasting
- Default for SMB / self-serve

### Multi-year (2-3 year)
- Pros: revenue lock-in, lower CAC payback risk
- Cons: customer underwater if your roadmap slows, hard to raise prices
- Discount: 5-10% per year of commitment beyond year 1

### Default by segment
- SMB: monthly (with annual option at 15-20% discount)
- Mid-market: annual default
- Enterprise: 1-3 year multi-year, custom terms

## Repricing existing customers (raising prices on installed base)

The single highest-leverage and highest-risk pricing move.

### Pre-flight checks
- Are existing customers paying meaningfully under target list? (>20% gap = repricing opportunity)
- What's the NPS / health score by cohort? Healthy customers absorb price increases better
- What's the alternative the customer would switch to? Check competitive landscape

### Repricing playbook
1. **Announce increase, with notice**: 90+ days before next renewal. Email + in-app + (for top customers) personal outreach
2. **Justify**: feature releases since last increase, additional value delivered, market context (cost shocks)
3. **Grandfather options**:
   - Most generous: 100% grandfather forever (rarely the right call)
   - Common: grandfather current contract terms, increase at renewal (recommended)
   - Aggressive: grandfather 12 months, then increase regardless (use only with very strong product-market lock-in)
4. **Discount earnouts**: offer existing customers an annual prepay or multi-year that locks the older price for an extended period
5. **Tracking**: measure churn impact in next 90 days; expect 1-3% churn from repricing; if >5%, the repricing was too aggressive

### Communication script (paraphrase to founder voice)
"As of [date 90 days out], our pricing for new customers will be [new structure]. Here's what's changing for you specifically: [details]. We're [grandfathering / phasing / immediate-renewal]. If you'd like to lock in current pricing for an additional 12 months, you can prepay annually before [deadline]. Here's how to do that: [link]."

## Anti-patterns / red flags

- "We charge what feels right" (no anchor logic)
- 7+ tiers (decision paralysis; sales reps confused; pricing page unreadable)
- Tier names that don't match buyer journey ("Wizard / Sage / Master" — cute, useless)
- Per-seat at $5/seat — too low for B2B; signals "lite" product
- "Contact us" on every tier — looks like you can't justify pricing
- Same price for SMB and Enterprise — leaves money on table on Enterprise side; prices out SMB
- Free tier that includes SSO and audit logs (gives away the Enterprise hooks)
- Charging for support (acceptable for Enterprise tier; alienating for SMB)
- Hidden surcharges revealed only at contracting (e.g., "data egress fee", "implementation fee" not shown on pricing page)
- Auto-charge for usage overages with no notification

## Pricing experimentation discipline

- A/B test pricing rarely; results are noisy. Better to do directional experiments by cohort.
- Survey willingness-to-pay (Van Westendorp method, conjoint analysis) can be useful at scale; near-noise at <100 paying customers.
- Talk to 20-50 customers (current + churned + lost-prospects) about pricing perception. Qualitative > quantitative for early-stage pricing.
- Reprice ONLY ONE thing at a time (tier price, value metric, or packaging — not all three). Otherwise you can't attribute outcome.

## Output to founder after diagnostic

1. **Stage-appropriate posture** (just-launch / first-PMF / scale-mode reprice)
2. **Value metric recommendation** (per-seat / usage / hybrid / outcome) with rationale tied to product
3. **Tier structure** (3-4 tier blueprint with positioning, target buyer, target ACV)
4. **Headline price recommendation** (Starter $X, Pro $Y, Business $Z, Enterprise "Contact us") with anchor logic
5. **Free strategy** (free trial / freemium / no-free)
6. **Sales motion alignment** (PLG + sales handoff threshold, Enterprise-only-sales below $X)
7. **Annual / monthly / multi-year contract policy** (with discount table)
8. **Discount discipline rules** (approval thresholds, acceptable triggers)
9. **Packaging logic** (what goes in tier vs add-on vs Enterprise-only)
10. **If repricing existing**: phase plan, grandfather strategy, communication script, churn-watch threshold
11. **Re-evaluation cadence** (revisit pricing at $1M ARR, $3M ARR, $10M ARR — each marks a structural shift)

Pricing is not "set once and forget". It's a deliberate operational rhythm. Most healthy B2B SaaS revisits price + tier + packaging every 12-18 months. The companies that don't reprice for 3+ years are the ones with messy, sub-target ACV that they later can't fix without churn shock. This coach builds the rhythm.
