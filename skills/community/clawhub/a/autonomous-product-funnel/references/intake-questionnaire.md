# Intake Questionnaire

Use this reference to build the single initial intake. The source is written in English, but ask it in the user's active conversation language.

Do not mechanically ask every question if the answer is already known. Prefill known values from conversation, files, repository, URLs, and connected services. Clearly show detected values so the user can correct them.

Keep provider names, IDs, event names, technical fields, and environment variable names unchanged.

## Tiering

Ask in two layers so the intake does not overwhelm the user.

**Required (always ask unless detected):** sections 1, 2, 3, 6, 11, 16, 17, 30, 31, 32, 34.

**Conditional (ask only when the answer changes the build):** 4, 5, 7, 8, 9, 10, 12, 13, 14, 15, 18 to 29, 33. Skip a section when the funnel goal makes it irrelevant (for example, shipping for a lead funnel) or when everything in it was detected. Collapse skipped sections to one line: `Defaulted by JEV`.

## 1. Project objective

- Product/project name
- Brand name
- Primary funnel goal: paid order, lead, booking, subscription, pre-order, other
- Final conversion definition
- Launch date or campaign deadline
- Seasonal or evergreen
- Expected traffic sources
- Primary business metric: conversion rate, ROAS, CPA/CAC, revenue, AOV, leads, JEV
- Any hard KPI floor/ceiling

## 2. Product identity and source material

- Product name
- Product URLs: manufacturer, Amazon, Alibaba, current store, marketplace, competitor
- Product images: hero, white background, packaging, dimensions, variants, lifestyle, UGC
- Product videos
- Product description/specification
- Exact box contents
- Dimensions and weight
- Material
- SKU
- Variants/options
- Manufacturer/brand relationship
- Existing product data file or feed
- Existing product page that must be preserved or migrated

## 3. Product economics

- Unit purchase/manufacturing cost
- Packaging cost
- Average shipping/fulfillment cost
- Payment processing cost if known
- Other variable cost
- Current retail price
- Minimum allowed selling price
- Minimum gross margin
- Target AOV
- Target CPA/CAC
- Target ROAS
- Current inventory
- Inventory source of truth
- Restock lead time
- Backorder allowed or not

Use `UNKNOWN` when data is unavailable. Do not invent margin-critical values.

## 4. Product truth, compliance, and claims

- Intended user age
- Seller-provided age recommendation
- Safety warnings
- Certifications and evidence files
- Supported marketing claims
- Prohibited claims
- Regulated categories involved: children, toys, medical, health, food, supplements, cosmetics, batteries, electrical, adult, other
- Instructions/manuals
- Test reports
- Warranty information
- Known limitations or defects that must be disclosed

Never ask the user to claim a certification without evidence.

## 5. Market and customer-facing language

- Launch country/region
- Allowed sales regions
- Excluded regions
- Currency
- Default storefront language
- Additional storefront languages
- Localization URL strategy if relevant
- Known primary buyer
- Known end user
- Main use cases
- Known objections
- Cultural or market constraints
- Tone requirements

If target customer, positioning, or objections are unknown, allow `JEV`.

## 6. Offer authority

Ask whether JEV may decide each item:

- final product positioning
- primary customer segment
- selling price within supplied constraints
- quantity tiers
- bundles
- order bumps
- upsells/downsell
- free-shipping threshold
- discount structure
- coupon availability
- CTA wording
- urgency framing based on real facts

Also collect:

- real MSRP/compare-at price if one exists
- any MAP or pricing policy
- promotion deadline if real
- whether live inventory may be displayed

## 7. Brand and creative

- Logo and brand files
- Brand guideline
- Brand colors
- Fonts
- Current website
- Social accounts
- Brand voice
- Visual references the user likes
- Visual styles to avoid
- Permission to create supporting AI-generated visuals
- Whether generated visuals may depict the actual product
- Rules for preserving product appearance, packaging, quantity, color, and scale
- Legally reusable reviews/testimonials and sources
- UGC permissions

## 8. Competitors and references

- Known competitor URLs
- Marketplace competitor listings
- Reference funnels or landing pages
- Known differentiators
- Competitive tactics to avoid
- Brands or stores that define the desired quality bar

## 9. Funnel shape

- New standalone funnel or existing site integration
- Whether a traditional cart must be preserved
- Whether direct landing -> checkout is allowed
- Need for email capture
- Need for subscription
- Need for upsell/downsell
- Need for post-purchase offer
- Need for abandoned checkout recovery
- Need for waitlist/pre-order
- Need for FAQ
- Need for reviews section
- Need for live chat/support entry point

## 10. Existing repository and engineering environment

- Repository URL/workspace
- Whether the agent has repository access
- Default branch
- Permission to create branch
- Permission to commit
- Permission to push
- Permission to merge
- Permission to modify production branch
- Current framework
- Package manager
- Runtime
- Database
- CMS
- Ecommerce platform
- Existing order system
- Existing analytics abstraction
- Existing test commands
- Existing CI/CD
- Existing secret-management pattern

If no repository exists:

- permission for JEV to select the stack
- preferred/forbidden technologies
- permission to install packages
- permission to create database/schema
- permission to run migrations
- permission to add server/API endpoints

## 11. Payment gateway

- Provider: Stripe, Shopify Payments, Klarna, PayPal, Adyen, Mollie, WooPayments, other, JEV
- Account already exists
- KYC completed
- Live payments enabled
- Agent/connector access available
- Permission to create payment products/prices
- Permission to create/modify webhooks
- Secret storage location or env variable names only
- Required payment methods: card, Apple Pay, Google Pay, Klarna, PayPal, Swish, other
- Capture mode
- Permission to create test orders
- Permission to issue test refunds
- Permission to enable or deploy live mode
- Existing webhook endpoints
- Existing tax integration

Never request a raw secret in chat.

## 12. Tax and VAT

- Legal seller country
- VAT registration status
- VAT number if appropriate for public/legal configuration
- Prices VAT inclusive or exclusive
- Tax calculation source
- OSS/IOSS status where relevant
- Special tax rates or exemptions
- Existing tax service/provider

## 13. Shipping and fulfillment

- Ship-from location
- Shipping provider(s)
- Allowed shipping regions
- Shipping rates
- Free-shipping rule
- Delivery estimate
- Shipping API availability
- Address validation requirement
- Tracking number integration requirement
- Fulfillment destination: email, ecommerce platform, ERP, WMS, API, database, manual export
- Inventory deduction behavior
- Partial shipment/backorder behavior

## 14. Returns, cancellation, refunds

- Existing returns policy URL
- Return period
- Return shipping responsibility
- Damaged-item policy
- Refund workflow
- Cancellation policy
- Warranty process
- Any legally reviewed policy text

If policy is unknown, record `POLICY_REQUIRED`; do not fabricate legal terms.

## 15. Seller identity and legal site data

- Legal company name
- Organization/company number
- VAT number
- Business address
- Support email
- Support phone if published
- Privacy contact
- Existing terms URL
- Existing privacy URL
- Existing shipping policy URL
- Existing returns URL
- Cookie policy URL

## 16. Domain and DNS

- Final domain
- Root/www/subdomain/path preference
- Registrar
- DNS provider
- Agent DNS access available
- Permission to add/modify A, AAAA, CNAME, TXT, MX-related verification records where appropriate
- Permission to configure www redirect
- Permission to configure SSL
- Permission to configure redirects
- Protected DNS records that must not change
- Existing email DNS records that must be preserved

## 17. Deployment

- Hosting/deployment provider
- Existing project/account
- Agent access available
- Production project name
- Staging environment
- Permission to deploy preview/staging
- Permission to deploy production
- Permission to modify environment variables
- Secret store
- CDN
- SSL setup
- Rollback mechanism
- Production health-check URL if one exists

## 18. OpenAI Ads measurement

- ChatGPT/OpenAI Ads in scope: yes, no, future
- Ads Manager account exists
- Agent has Ads Manager access
- Ad account ID if available
- Existing conversion data source / Pixel
- Pixel ID if available
- Setup mode: Measurement Pixel, CAPI, Pixel+CAPI, JEV
- Permission to create conversion data source
- Permission to configure conversion events
- CAPI secret env/secret-manager reference, never raw secret
- Browser measurement allowed
- Server-side CAPI allowed
- User matching allowed under current consent/privacy policy
- Attribution context handling, including `oppref`
- Existing consent gating
- Primary purchase conversion boundary

Default when supported and authorized: Pixel + CAPI with documented deduplication.

## 19. Meta/Facebook measurement

- Meta Business account/workspace
- Agent access
- Pixel ID
- Existing CAPI
- CAPI secret env/secret-manager reference
- Permission to create/modify events
- Permission to send server-side Purchase
- Domain verification status
- Test Events access
- Existing event mapping
- Existing consent gating

Default when supported and authorized: Pixel + CAPI for purchase-critical funnels.

## 20. Google Search Console

- Existing property
- Property type: Domain or URL-prefix
- Property URL/domain
- Agent access
- DNS TXT permission for verification
- Existing sitemap
- Permission to create/modify sitemap.xml
- Permission to create/modify robots.txt
- Permission to create canonical tags
- Permission to add structured data

Treat Search Console as search/indexing infrastructure, not conversion analytics.

## 21. GA4 and Google Tag Manager

- Existing GA4 property
- GA4 Property ID
- Measurement ID
- GTM in use
- GTM Container ID
- Agent access
- Permission to implement ecommerce events
- Existing data layer
- Existing consent mode
- Permission to modify tags/triggers/variables
- Need for DebugView verification

Default ecommerce event coverage where applicable:

- view_item
- add_to_cart
- begin_checkout
- purchase

## 22. Google Ads

- Google Ads in scope
- Account ID
- Conversion ID
- Conversion Label
- Enhanced Conversions desired
- GA4 linked
- Merchant Center involved
- Agent access
- Permission to modify conversion actions

## 23. Other measurement

Collect only what is in scope:

- TikTok Pixel / Events API
- Reddit Pixel
- Pinterest
- Snapchat
- Microsoft Ads
- LinkedIn Insight Tag
- Clarity
- Hotjar
- PostHog
- Plausible
- other

For each: ID, access, server/browser mode, secret reference, consent requirements, and permission to modify.

## 24. Consent and privacy

- CMP provider
- Consent regions
- Existing cookie policy
- Whether advertising cookies may run before consent
- Consent-state storage
- Google Consent Mode requirement
- Existing opt-out mechanism
- Existing privacy constraints on user matching
- Data-retention requirements if known

Use conservative defaults when policy is unclear and do not bypass an existing consent system.

## 25. Transactional email

- Provider
- Agent access
- From email
- From name
- Support email
- SPF/DKIM status
- Permission to send test email
- Required messages: order confirmation, payment failed, shipping, refund, abandoned checkout, other
- Existing templates
- Existing email event/webhook system

## 26. Order management

- Order system of record
- Order ID rules
- Guest checkout allowed
- Customer accounts required
- Admin dashboard required
- Inventory deduction required
- External webhooks required
- CRM/ERP/WMS integrations
- Paid-order fulfillment trigger
- Refund/cancel status mapping

## 27. SEO and discoverability

- Primary keyword if known
- Existing SEO strategy
- Permission for JEV to perform keyword research
- Product structured data required
- Organization/website structured data required
- Open Graph metadata required
- Social share image required
- Existing canonical strategy
- Existing redirect rules
- International hreflang requirement

## 28. Creative and marketing authority

Ask for Yes/No/JEV authority on:

- headline
- positioning
- target customer
- CTA
- page sections
- product description
- FAQ
- bundle structure
- SEO copy
- mobile layout
- visual hierarchy
- A/B-test-ready variant hooks

## 29. Technical authority

Ask for Yes/No/JEV authority on:

- architecture
- components
- dependencies
- database schema
- API routes
- analytics abstraction
- payment architecture
- image optimization
- accessibility fixes
- performance fixes
- refactoring existing code
- test coverage additions

## 30. Production authority

Ask for explicit permission on:

- commit code
- push code
- merge branch
- run DB migrations
- create payment products/prices
- create/modify payment webhooks
- deploy staging
- deploy production
- modify DNS
- add DNS verification TXT
- create analytics properties/events
- configure OpenAI Ads measurement
- configure Meta Pixel/CAPI
- configure GA4/GTM/Google Ads
- send test email
- create test payment
- refund test payment
- enable live payment mode

If permission is denied or missing, complete the surrounding implementation and report the blocked final action.

## 31. Spending authority

- Permission to create new paid-service charges
- Maximum authorized amount
- Permission to purchase a domain
- Permission to start paid advertising
- Maximum ad spend if allowed

Default: no new paid services, domain purchase, or ad spend unless explicitly authorized.

## 32. Known human-only actions

Ask the user to list known blockers such as:

- KYC
- bank verification
- 2FA/passkey/device approval
- CAPTCHA
- legal terms acceptance
- domain ownership approval
- Meta/Google/OpenAI business verification
- credential creation
- registrar approval
- app-store/account-owner approval

Use `NONE` when none are known.

## 33. Final deliverables

Confirm whether the user expects:

- live production URL
- staging URL
- repository changes
- commit hash
- deployment record
- funnel architecture summary
- JEV decision log
- tracking matrix
- payment verification report
- SEO/indexing status
- QA report
- exact manual action list

## 34. Execution consent

End intake with one explicit authorization statement, translated into the user's language:

"After I submit this intake, JEV may make routine decisions within the authority and constraints above. The agent may continue through research, strategy, copy, implementation, payment, tracking, deployment, and QA without asking for ordinary approvals. If an external human-only action is unavailable, complete all surrounding work and list the exact remaining action in the final handoff."

Collect:

- Agree: Yes/No
- Start execution immediately after submission: Yes/No
