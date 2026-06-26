# Prompt 3 — Reputation Engine + B2B Referral System

**Paid prompt.**

---

## Variables

- `[BUSINESS_NAME]`, `[OWNER_NAME]`, `[TECHNICIAN_NAME]`
- `[CITY_STATE]`
- `[CCS_NUMBER]` — CSIA CCS number or "in training"
- `[NFI_CREDENTIALS]` — or "none"
- `[PHONE]`, `[GOOGLE_REVIEW_URL]`, `[WEBSITE]`
- `[REVIEW_COUNT]`, `[RATING]`

---

## Prompt

```
You are an expert chimney sweep and fireplace contractor marketing copywriter. Generate a complete reputation engine and B2B referral system for [BUSINESS_NAME] in [CITY_STATE].

CREDENTIALS: CCS [CCS_NUMBER] | NFI: [NFI_CREDENTIALS]
REVIEWS: [REVIEW_COUNT] at [RATING]

COMPLIANCE RULES:

1. FTC 2023 ENDORSEMENT GUIDES (16 CFR Part 255 — all review sequences):
   - "Please leave us a 5-star review" is PERMANENTLY BLOCKED — soliciting a specific star rating violates FTC 2023 Guides
   - "Leave a review and get 10% off" is PERMANENTLY BLOCKED — incentivized reviews require disclosure or constitute deceptive practice
   - Review requests must not suppress negative reviews (routing unhappy customers away from public review)
   - Compliant language: "If you were satisfied with our service, an honest Google review helps other homeowners find reliable chimney professionals — we appreciate whatever you're willing to share"
   - Satisfaction check gate: sequence must include a genuine satisfaction check BEFORE the public review ask — prevents capturing complaints publicly while harvesting only positive reviews (FTC enforcement risk)

2. NFPA 211 LEVEL SPECIFICATION (all realtor/home inspector letters):
   - "NFPA 211 Level II pre-listing inspection" (exact phrase) in all real estate referral materials
   - "Chimney inspection" or "pre-listing inspection" without the Level II specification is PERMANENTLY BLOCKED

3. CSIA CREDENTIAL ACCURACY:
   - CCS number provided: "CSIA Certified Chimney Sweep #[CCS_NUMBER]" + csia.org/find-a-sweep
   - "in training": "trained to CSIA Best Practices guidelines" — no CCS language

GENERATE ALL OF THE FOLLOWING:

---

### Output A: Post-Service Review Request Sequence (3-touch, FTC 2023-compliant)

TOUCH 1 — Text message (same day, within 2 hours of job completion):
- Satisfaction check: "Hi [Customer name], this is [TECHNICIAN_NAME] from [BUSINESS_NAME] — how did everything go today? Any concerns I can address before I leave the area?"
- If positive response → Touch 2 (review ask)
- If negative or no response → internal alert only; no public review push
- 50–75 words

TOUCH 2 — Email (24 hours after job, sent to satisfied customers only):
Subject: "Thanks for trusting [BUSINESS_NAME] with your chimney"
- Personalized: technician name, service performed, date
- NFPA education hook: "Your chimney is now set for another season. One reminder: NFPA 211 recommends an annual inspection — we'll reach out next fall."
- Compliant review ask: [GOOGLE_REVIEW_URL]
- "No star rating request in ask — honest review language only"
- 150–200 words

TOUCH 3 — Handwritten card (mailed within 72 hours):
- "Thank you for choosing [BUSINESS_NAME]" — brief, personal
- Technician signed (facsimile signature acceptable)
- Include business card with CCS # and NFI credentials
- No review ask language on card (FTC-safe; review ask already done digitally)
- 50–75 words

---

### Output B: NFPA 211 Level II Realtor Referral Letter

From [OWNER_NAME], [BUSINESS_NAME] → Real estate agent

Include:
- Opening: NFPA 211 Section 14.2 — Level II is required at all real estate transactions involving a change of occupancy/ownership; this is a code requirement, not a upsell
- Level II scope distinction: what realtors DON'T get from a basic chimney cleaning service (no attic/crawl access, no written report, no NFPA level classification)
- What a CCS-signed Level II report includes: written findings, liner condition, creosote grade, all NFPA-specified components, digital delivery for MLS disclosure
- Credential hook: "CSIA Certified Chimney Sweep #[CCS_NUMBER] — fewer than 1,800 active CCS professionals nationwide; verifiable at csia.org/find-a-sweep"
- Turnaround: 24–48 hours, digital delivery
- Offer: complimentary Level II inspection of the agent's own home as an introduction
- CTA: [PHONE] + [WEBSITE]
- 400–450 words; professional letterhead format

---

### Output C: Home Inspector Referral Letter

From [OWNER_NAME] → Licensed home inspector

Include:
- Opening: home inspectors find chimney issues but typically disclaim specialty evaluation — "the inspector notes 'recommend chimney inspection by a licensed chimney professional' — that's where we come in"
- NFPA 211 Level II scope: inspectors writing "Level II recommended" need a CCS who can actually deliver it with a written report
- Co-marketing angle: "We'll include your name and contact on our post-inspection follow-up materials if you prefer reciprocal referrals"
- Turnaround, digital report, credential
- CTA: [PHONE]
- 300–350 words; professional format

---

### Output D: Real Estate Transaction Coordinator Letter

From [OWNER_NAME] → TC at a real estate brokerage or TC firm

Include:
- TC-specific angle: TCs need fast turnaround and reliable delivery for MLS disclosure deadlines
- 24-hour scheduling, 48-hour written report delivery
- E-sign compatible PDF report format for e-disclosure packages
- "Call to action for TCs: add [BUSINESS_NAME] to your preferred vendor list"
- Credential + turnaround + CTA
- 250–300 words

---

### Output E: Property Manager Annual Inspection Program Letter

From [OWNER_NAME] → Property management company

Include:
- Value prop: annual NFPA 211 Level I inspection program for rental properties with gas fireplaces or wood-burning fireplaces
- Liability angle: documented annual inspection creates paper trail for insurance claims and tenant disputes
- Volume discount structure: suggest 3-tier (1–5 units / 6–20 units / 21+ units)
- Annual inspection report for each unit: tenant-safe, property manager copy, digital archive
- Credential + CTA
- 300–350 words

---

### Output F: HOA Preferred Vendor Application Cover Letter

From [OWNER_NAME] → HOA board or property management firm managing an HOA

Include:
- NFPA 211 annual inspection angle: HOA-mandated annual chimney inspection for townhome/condo units with fireplaces
- Credential: CCS # + NFI + OSHA ladder safety disclosure
- Insurance: note that a credentialed sweep carries general liability and workers' comp (prevents HOA subrogation claims)
- Volume inspection program: annual sweep day for all fireplace units (scheduling efficiency for HOA)
- 300–350 words
```
