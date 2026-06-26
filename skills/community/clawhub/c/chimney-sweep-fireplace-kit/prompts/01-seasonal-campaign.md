# Prompt 1 — Seasonal Campaign + Real Estate Inspection Funnel

**Free prompt.**

---

## Variables

- `[BUSINESS_NAME]`, `[OWNER_NAME]`, `[CITY_STATE]`
- `[CCS_NUMBER]` — CSIA Certified Chimney Sweep number (e.g., CCS-2847) or "in training"
- `[NFI_CREDENTIAL]` — NFI Gas Appliance Specialist / Wood Burning Specialist / Pellet Specialist (or "none")
- `[SERVICES]` — comma-separated: gas-fireplace, wood-chimney, pellet, dryer-vent, relining, masonry, epa-install
- `[REVIEW_COUNT]` and `[RATING]` — e.g., "87 Google reviews, 4.9 stars"
- `[PHONE]` and `[BOOKING_URL]`

---

## Prompt

```
You are an expert chimney sweep and fireplace contractor marketing copywriter. Generate a fall chimney safety campaign for [BUSINESS_NAME] in [CITY_STATE].

CREDENTIALS:
- CSIA: [CCS_NUMBER] (use "CCS in training" track if "in training")
- NFI: [NFI_CREDENTIAL]
- Reviews: [REVIEW_COUNT], [RATING]

COMPLIANCE RULES — apply to every output:

1. CSIA CERTIFICATION GATE:
   - If CCS number provided: use "CSIA Certified Chimney Sweep #[CCS_NUMBER]" — link csia.org/find-a-sweep
   - If "in training": use "trained to CSIA Best Practices guidelines" — NEVER use "CSIA Certified," "CCS," or "CSIA-certified company"
   - "Our company is CSIA certified" is PERMANENTLY BLOCKED regardless of credential status

2. NFPA 211 LEVEL SPECIFICATION:
   - Annual sweep/inspection = "NFPA 211 Level I inspection"
   - Real estate referral context = "NFPA 211 Level II pre-listing inspection" (this exact phrase)
   - Generic "chimney inspection" without the level is permanently blocked in realtor-facing copy
   - Level II trigger reminder: required for all real estate transactions, after any operational problem, after system modification, after external event (earthquake, adjacent fire)

3. CLARK COUNTY BURN ADVISORY (Southern Nevada only — include if [CITY_STATE] is Las Vegas/Henderson/North Las Vegas/Clark County area):
   - "Wood-burning fireplace use may be restricted during Clark County Air Quality Management Division No-Burn Episodes. Check airnow.gov or nvdetr.org before each use."
   - Include in all wood-burning fireplace content; omit from gas-only service content

4. NFI GAS SCOPE:
   - If NFI Gas Appliance Specialist: use "NFI Gas Appliance Specialist — authorized to service and maintain gas logs, inserts, and direct-vent systems to manufacturer specifications"
   - If no NFI credential: limit gas fireplace content to "chimney and venting inspection for gas appliances" — do NOT claim gas appliance servicing

5. EPA PHASE 2 (only if "epa-install" in [SERVICES]):
   - Include: "We only install EPA Phase 2 certified units. Verify certification at epa.gov/burnwise before purchase."
   - "EPA-approved fireplace" is PERMANENTLY BLOCKED — use "EPA Phase 2 certified"

6. FTC REVIEW LANGUAGE:
   - "Please give us 5 stars" is PERMANENTLY BLOCKED
   - Compliant: "If you were satisfied, an honest Google review helps other homeowners find reliable chimney professionals"

GENERATE ALL OF THE FOLLOWING:

### Output A: Fall Chimney Safety Email Sequence (3 emails)

EMAIL 1 — Subject: "Your fireplace may not be safe to light this season" (early October)
- Hook: NFPA statistic — chimney fires account for X% of home heating fires (cite NFPA report)
- Introduce free NFPA 211 Level I visual inspection offer
- Credential: [CCS_NUMBER] / NFI credential
- CTA: Book inspection at [BOOKING_URL]
- 250–300 words; no spam trigger words

EMAIL 2 — Subject: "Spots filling fast — free chimney check before the cold hits" (mid-October)
- Social proof: [REVIEW_COUNT] reviews / [RATING] stars
- Creosote grade education: Grade 1 (dusty/flaky — routine sweep), Grade 2 (tar-like — removal required before use), Grade 3 (glazed — high fire risk; requires specialized treatment or relining)
- Clark County burn advisory reminder if applicable
- CTA: Limited spots, book now
- 200–250 words

EMAIL 3 — Subject: "Last call — winter booking slots" (late October)
- Urgency: typical lead time / schedule note
- Feature relevant service from [SERVICES]
- CTA: Final push with phone and booking URL
- 150–200 words

---

### Output B: Free NFPA Level I Inspection Offer — Landing Page Section

Landing page hero section for "Free NFPA 211 Level I Visual Inspection" lead generation offer.

Include:
- Headline: [BUSINESS_NAME] — CSIA / NFI credential hook
- What's included in a Level I inspection (per NFPA 211: exterior, interior accessible areas, connection)
- What Level I does NOT cover (attic/crawl space — that's Level II; clarify the distinction)
- When Level II is needed: real estate transfer, after any operational problem
- Creosote grade finding: what they'll receive after inspection
- Trust signals: [REVIEW_COUNT] reviews, credential #, OSHA ladder safety disclosure
- CTA: Phone + booking URL
- 300–350 words

---

### Output C: Google My Business Post Series (4 posts)

POST 1 — October: "Fall chimney sweep season open" (seasonal awareness, NFPA Level I hook)
POST 2 — November: "Before you light that first fire" (creosote grade + safety check CTA)
POST 3 — December: "NFPA Level II inspection — required for all real estate closings" (realtor referral angle)
POST 4 — January: "Midseason safety check" (if you haven't had your annual sweep yet)

Each post: 150–200 words, compliant credential language, no star-rating requests in post body

---

### Output D: NFPA 211 Level II Realtor Referral Introduction Letter

Letter from [OWNER_NAME] to a real estate agent introducing the NFPA 211 Level II pre-listing inspection service.

Include:
- Opening: NFPA 211 Section 14.2 — Level II is required at every change of occupancy/ownership
- What differentiates a Level II from a "basic chimney inspection" (scope, documentation, written report)
- Why realtors need a credentialed CCS for Level II (liability, report defensibility)
- Service: written Level II inspection report, 24–48 hr turnaround, digital delivery
- Credential: [CCS_NUMBER]
- Offer: free Level II inspection for the agent's own home as a trust-building introduction
- CTA: Phone + booking URL
- Professional letterhead format
- 350–400 words
```
