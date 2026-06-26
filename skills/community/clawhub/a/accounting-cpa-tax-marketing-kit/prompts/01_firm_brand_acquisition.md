# Prompt 1: Firm Brand & Client Acquisition System

## Purpose
Build compliant foundational marketing assets for your accounting firm. All outputs enforce IRS Circular 230 advertising standards, AICPA Code § 1.400 (no false/misleading claims), state CPA board disclosure requirements (credential # in ads), and FTC rules (no outcome guarantees).

## Inputs Required

Fill in each field before running:

```
FIRM_NAME: [Your firm's full legal name]
CPA_LICENSE: [State CPA license # — e.g., NV-CPA-20019-4721]
PTIN: [IRS Preparer Tax Identification Number — e.g., P01234567, or NONE if not applicable]
EA_NUMBER: [Enrolled Agent enrollment card number, or NONE if not applicable]
SERVICES: [Check all that apply: individual tax prep / small business tax / corporate tax / bookkeeping / payroll / audit / CFO advisory / IRS representation / nonprofit / estate/trust]
YEARS_IN_PRACTICE: [Number]
SPECIALIZATIONS: [e.g., real estate investors, medical professionals, Spanish-speaking clients, back taxes, ITIN filers]
TARGET_CLIENT: [Individual taxpayers / small business owners / both]
CITY_STATE: [e.g., Las Vegas NV]
PRICE_RANGE: [e.g., "starting at $195 for individual returns" or "contact for pricing"]
```

## The Prompt

```
You are a professional services marketing copywriter with expertise in IRS Circular 230, AICPA Code of Professional Conduct, and FTC advertising compliance for accounting firms.

Generate a complete brand and client acquisition marketing package for:

Firm: [FIRM_NAME]
CPA License: [CPA_LICENSE]
PTIN: [PTIN]
EA Number: [EA_NUMBER]
Services: [SERVICES]
Years in practice: [YEARS_IN_PRACTICE]
Specializations: [SPECIALIZATIONS]
Target clients: [TARGET_CLIENT]
Location: [CITY_STATE]
Pricing: [PRICE_RANGE]

COMPLIANCE RULES (enforce in every output):
1. Include CPA license # [CPA_LICENSE] in every ad and official copy
2. Include PTIN [PTIN] wherever required (paid preparer advertising)
3. NO outcome guarantees: never use "guaranteed," "maximum refund," "biggest refund," "you'll get money back," or any specific savings promise
4. ALL savings/results claims must include: "Based on similar situations; actual results vary depending on your tax circumstances"
5. NO "we'll save you" language — only "may help reduce," "clients in similar situations have," "potential opportunities include"
6. NO unsolicited claim that you can reduce a specific person's taxes without a consultation
7. Credentials must be accurately stated: CPA = Certified Public Accountant; EA = Enrolled Agent (licensed by the IRS)
8. LinkedIn posts must be educational/thought leadership, not promotional offers
9. "Certified" may only appear in "Certified Public Accountant" — never as a standalone claim

Generate:

**1. Google Business Profile Description (750 characters max)**
Keyword-rich, benefit-focused, no outcome guarantees, CPA license # included.

**2. Website Headline + 3 Sub-Headlines**
Headline: under 10 words, benefit-driven, no guarantee language
Sub-headlines: address the 3 biggest client pain points

**3. Google Search RSA — Tax Season Variant**
15 headlines (30 characters max each) + 4 descriptions (90 characters max each)
Include: credential # in 1-2 headlines, price signal if applicable, location signal, urgency without fake deadlines

**4. Google Search RSA — Year-Round Advisory Variant**
15 headlines (30 characters max each) + 4 descriptions (90 characters max each)
Focus on bookkeeping, advisory, peace of mind — not tax deadlines

**5. Facebook/Instagram Ad Creative Set (3 ads)**
Ad 1: Tax season urgency (deadline-based, not fake scarcity)
Ad 2: Referral/social proof angle (no client names without consent; use "clients like you" framing)
Ad 3: Advisory services upgrade angle ("beyond tax season")
Each ad: headline (40 chars) + primary text (125 chars) + description (30 chars) + CTA + compliance footer

**6. Email Subject Line Bank**
Tax season (10 subject lines) — escalating urgency Jan 15 through Apr 1
Advisory/year-round (5 subject lines) — off-season nurture

**7. LinkedIn Post Set (3 posts)**
Post 1: Educational — common tax mistake your target client makes (general info, not advice)
Post 2: Thought leadership — one tax planning concept relevant to your specialization
Post 3: Community/credibility — practice milestone, community involvement, or professional development
All posts: end with "This is general tax information, not advice for your specific situation. Consult a qualified tax professional."

**8. "Why Choose Us" Website Section**
4-5 bullet points + 1 paragraph. Credentials prominently displayed. Benefits-focused. No outcome guarantees. Compliance footer included.

Format all outputs with clear headers. Flag any state-specific disclosure requirements for [CITY_STATE] in a compliance notes section at the end.
```

## Example Output Preview

See `/examples/accounting_example.md` for complete output using Clark County Tax & Accounting (Las Vegas NV).

## Compliance Notes

- This prompt enforces AICPA Code § 1.400.001 (false/misleading advertising prohibition)
- State CPA board rules: most states require CPA firm license # in ALL advertising — this prompt enforces it
- IRS Circular 230 § 10.30 covers standards for written communication with clients; marketing is not "covered opinion" territory but must not contain false statements
- FTC Act § 5: "guaranteed maximum refund" has been cited in FTC actions against tax preparers
- Nevada-specific: NAC 628.230 requires Nevada CPA certificate number in advertising
