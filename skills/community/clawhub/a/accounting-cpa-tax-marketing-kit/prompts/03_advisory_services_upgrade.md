# Prompt 3: Advisory Services Upgrade Campaign

## Purpose
Convert tax-prep-only clients ($500/year average) to accounting retainer clients ($500/month average) — the highest LTV upgrade in the professional services portfolio. Off-season (May–September) campaign with full Circular 230 written advice compliance.

## Inputs Required

```
FIRM_NAME: [Your firm name]
CPA_LICENSE: [CPA license #]
CURRENT_CLIENT_SEGMENT: [Individual taxpayers / Small business owners / Both]
ADVISORY_SERVICES: [List: bookkeeping, monthly financial statements, CFO advisory, business formation, payroll, R&D credits, cost segregation, entity structuring, cash flow planning, other]
RETAINER_TIERS: [e.g., Bookkeeping $500/month / Tax+Books $800/month / CFO Advisory $1,500/month]
IDEAL_UPGRADE_CANDIDATE: [e.g., small business owner, $500K-$2M revenue, currently only comes in for annual tax return]
REFERRAL_PARTNER_TARGETS: [e.g., financial advisors, business attorneys, commercial real estate agents, business brokers]
CITY_STATE: [e.g., Las Vegas NV]
```

## The Prompt

```
You are a professional services marketing copywriter with expertise in accounting firm compliance and client value-ladder marketing.

Generate an off-season advisory services upgrade campaign for:

Firm: [FIRM_NAME] | License: [CPA_LICENSE]
Current client segment: [CURRENT_CLIENT_SEGMENT]
Advisory services offered: [ADVISORY_SERVICES]
Retainer pricing: [RETAINER_TIERS]
Ideal upgrade candidate: [IDEAL_UPGRADE_CANDIDATE]
Referral partner targets: [REFERRAL_PARTNER_TARGETS]
Location: [CITY_STATE]

COMPLIANCE REQUIREMENTS:
1. All advisory content: "This is general business and financial information, not advice for your specific situation. Contact us to discuss how these concepts apply to your business."
2. No specific tax savings promises: "businesses in similar situations have found opportunities in [area]" not "we will save you $X"
3. ROI examples: use composite/generalized language — "a client similar to yours" or "businesses with $X revenue commonly find" — never name actual clients
4. LinkedIn articles: must comply with IRS Circular 230 § 10.37 (written advice standards) — general educational content is permitted; specific advice in writing requires engagement letter
5. Referral fee compliance: AICPA § 1.500.001 requires disclosure if you receive compensation for referrals — flag this in referral partner materials
6. "CFO" usage: acceptable as service description; do not claim to be the company's CFO unless actually contracted as fractional CFO
7. CPA_LICENSE # in all materials

Generate:

**1. "Beyond Tax Season" 3-Email Nurture Sequence** (send May, June, July)
Email 1 (May — 1 month after tax season):
Subject (2 A/B options)
Body (200 words): What your tax return revealed about your business + what you could do differently
CTA: Discovery call for advisory services
Compliance footer: CAN-SPAM + "general information, not advice" disclaimer

Email 2 (June):
Subject (2 A/B options)
Body (200 words): Mid-year tax planning window — specific concepts (estimated payments, retirement contributions, entity review) explained generally
CTA: Mid-year review call
Compliance footer

Email 3 (July):
Subject (2 A/B options)
Body (200 words): Q3 planning — what decisions made in August/September have tax consequences (retirement plan setup, capital equipment purchases, etc.)
CTA: Q3 strategy call
Compliance footer

**2. LinkedIn Article Outline**
Title: "5 Tax Moves [IDEAL_UPGRADE_CANDIDATE description] Should Make Before December 31"
Outline: intro hook + 5 sections + conclusion CTA
Each section: explain the concept generally (education) — not how it applies to a specific person
Compliance note at top of article: "This article is general tax education. Consult a qualified tax professional for advice specific to your situation."
~800 words outline (sections are headlines + 2-3 bullet points each)

**3. ROI Case Study Template**
A generalized, Circular 230-compliant case study format using composite language.
Structure:
- Client type: "A [industry] business with approximately $[revenue range] in annual revenue"
- Challenge: what they were experiencing (tax surprises, cash flow issues, etc.)
- Services engaged: which advisory services
- Results: "this type of engagement commonly results in..." — general range, not specific promise
- "Individual results vary based on business structure, industry, and circumstances"
- No client names, no specific identifying details

**4. Referral Partner Pitch (2 versions)**
Version A: Financial Advisor / Wealth Manager
- How accounting + advisory complements wealth management
- Client referral process
- AICPA § 1.500.001 disclosure: "If we formalize a referral arrangement, any compensation must be disclosed to mutual clients" — build this in

Version B: Business Attorney / Commercial Real Estate Agent
- How proactive accounting catches issues attorneys/agents need to address (entity structure, lease vs. buy analysis, due diligence)
- Referral process
- Same AICPA disclosure

Each pitch: 1 email + 1 follow-up + 1-page "how we work together" overview

**5. Advisory Services One-Pager** (PDF-ready copy)
- Headline + 1 paragraph overview
- 3 service tiers from [RETAINER_TIERS] — price anchored, decoy middle tier
- What's included in each tier (bullet points)
- Who it's for (ideal client description)
- How to get started (CTA + scheduling link placeholder)
- Credentials + [CPA_LICENSE] + firm tagline
- Footer: "Fees stated are starting prices; final pricing based on engagement scope. [FIRM_NAME] provides general financial and tax planning services. Advice specific to your situation requires an engagement letter."

**6. Pricing Page Copy** (website section)
- 3 tiers from [RETAINER_TIERS]
- Decoy pricing psychology (make middle tier the "recommended" option visually)
- "Most popular" badge on mid-tier
- What each tier includes (checkmarks)
- FAQ section (3 questions): "What if I only need help at tax time?", "Can I change tiers?", "Do you work with my industry?"
- CTA button copy for each tier

Format all outputs with clear headers. Include a compliance checklist at the end noting all Circular 230 and AICPA standards addressed.
```

## Compliance Notes

- IRS Circular 230 § 10.35-10.37: "Written advice" to clients is regulated. Marketing content is generally not a "covered opinion" but specific written advice in an email to a named client IS regulated. This prompt generates template marketing — not client-specific advice.
- AICPA § 1.500.001 Commissions and Referral Fees: If you pay or receive referral fees, you must disclose this to the referred client in writing. The referral partner pitches in this prompt include this disclosure requirement.
- AICPA § 1.700 Confidential Client Information: Never use client-specific information in marketing without written consent. All case studies use composite/generalized language.
- LinkedIn: Posts that respond to a specific person's tax situation in the comments could cross into Circular 230 written advice territory. Keep responses general or direct to a consultation.
