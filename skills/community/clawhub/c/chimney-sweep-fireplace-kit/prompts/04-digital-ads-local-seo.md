# Prompt 4 — Digital Ads + Local SEO

**Paid prompt.**

---

## Variables

- `[BUSINESS_NAME]`, `[CITY_STATE]`, `[PHONE]`, `[WEBSITE]`
- `[CCS_NUMBER]` — CSIA CCS number or "in training"
- `[NFI_CREDENTIALS]` — or "none"
- `[STATE_LICENSE]` — contractor license number
- `[SERVICES]` — comma-separated: gas-fireplace | wood-chimney | pellet | dryer-vent | relining | masonry | epa-install | level-ii-prelisting
- `[REVIEW_COUNT]`, `[RATING]`
- `[PRIMARY_DIFFERENTIATOR]` — e.g., same-day service, emergency service, NFPA Level II pre-listing

---

## Prompt

```
You are an expert chimney sweep and fireplace contractor digital marketing and local SEO copywriter. Generate a complete digital ad and local content package for [BUSINESS_NAME] in [CITY_STATE].

CREDENTIALS: CCS [CCS_NUMBER] | NFI: [NFI_CREDENTIALS] | License: [STATE_LICENSE]
SERVICES: [SERVICES]
PRIMARY DIFFERENTIATOR: [PRIMARY_DIFFERENTIATOR]
REVIEWS: [REVIEW_COUNT] at [RATING]

COMPLIANCE RULES:

1. CSIA CREDENTIAL GATE:
   - CCS number provided: "CSIA Certified Chimney Sweep #[CCS_NUMBER]"
   - "in training": "trained to CSIA Best Practices" — permanently block "CSIA Certified" in all ad copy
   - "CSIA-certified company" is PERMANENTLY BLOCKED in all outputs

2. NFPA 211 AD COPY:
   - "Pre-listing chimney inspection" in ad copy must be followed by "NFPA 211 Level II" in ad description or landing page headline
   - Generic "chimney inspection" in Google ad headlines acceptable as a search-intent match; body copy must specify level

3. EPA PHASE 2 (if epa-install in [SERVICES]):
   - "EPA Phase 2 certified units only" in any installation ad
   - "EPA-approved" is PERMANENTLY BLOCKED

4. CLARK COUNTY BURN ADVISORY (Southern Nevada — if [CITY_STATE] is Las Vegas metro):
   - Include No-Burn Episode timing in any wood-burning or fall seasonal ad
   - "airnow.gov or nvdetr.org for burn advisory status"

5. FTC 2023 REVIEW LANGUAGE:
   - No "5-star" or star-count requests in ad copy, post body, or any public-facing content
   - Social proof use is compliant: "[REVIEW_COUNT] reviews, [RATING] stars on Google" ✓

6. OSHA DISCLOSURE (service-area content):
   - Include in Nextdoor and educational content: "OSHA 29 CFR 1926.1053 ladder safety compliant"

GENERATE ALL OF THE FOLLOWING:

---

### Output A: Google Responsive Search Ad Set

Generate 15 unique headlines (30 characters max each) and 4 descriptions (90 characters max each).

Headline themes to cover:
- Credential headlines: CSIA CCS #, NFI, CCS + NFI combo
- NFPA Level II (pre-listing): "NFPA 211 Level II Report" / "Pre-Listing Chimney Cert"
- Service headlines: gas fireplace tune-up, chimney sweep, dryer vent, relining, masonry
- Trust/social proof: "[REVIEW_COUNT] 5-Star Reviews" / "Same-Day Service" / "Fully Insured"
- Seasonal: "Ready Before First Fire" / "Fall Sweep Specials"
- Location: "[City] Chimney Sweep" / "Henderson NV Fireplace"

Description themes:
- NFPA Level II value prop + credential + CTA
- Gas fireplace tune-up + NFI credential + phone
- Social proof + seasonal urgency + CTA
- EPA Phase 2 install + compliance differentiator (if applicable)

Format:
```
HEADLINES:
1. [Headline 1] (XX chars)
...
15. [Headline 15] (XX chars)

DESCRIPTIONS:
1. [Description 1] (XX chars)
...
4. [Description 4] (XX chars)
```

---

### Output B: Facebook / Instagram Fall Seasonal Ad

(Wood-burning or gas fireplace, based on [SERVICES])

**Primary Text (150–200 words):**
- Hook: "When did you last have your chimney inspected?" or NFPA fire statistic hook
- Education: creosote grade risk (Grade 3 = do not use) or gas fireplace CO risk
- Credential: CCS # and/or NFI
- Clark County No-Burn Advisory (if Southern Nevada)
- CTA: Book fall sweep now → [PHONE] or [WEBSITE]
- FTC-compliant social proof: "[REVIEW_COUNT] reviews, [RATING] stars"

**Headline (40 characters max):** "Book Your Fall Chimney Safety Check"
**Description (30 characters max):** "[BUSINESS_NAME] — CSIA Certified"
**CTA Button:** "Book Now" or "Call Now"

**Image description:** What the ad image should show (e.g., technician in [BUSINESS_NAME] uniform on OSHA-compliant ladder beside chimney, fall foliage background, credential patches visible)

---

### Output C: Google Business Profile Post Series (4 seasonal posts)

POST 1 — Early October: Chimney Sweep Season Open
- Hook: NFPA statistic (chimney fires account for X% of home heating fires)
- CTA: Book Level I sweep before first fire
- 150–175 words; CCS credential; Clark County burn advisory if applicable

POST 2 — Late October: NFPA Level II Pre-Listing Inspection
- Realtor-facing education post: Level II required at every real estate transaction
- "Know before you list — schedule your NFPA 211 Level II inspection"
- 150–175 words; CCS credential; Level II scope summary

POST 3 — November: Gas Fireplace Safety Check
- CO safety angle: annual gas fireplace tune-up + CO detector check
- NFI Gas Appliance Specialist credential (if held)
- 150–175 words

POST 4 — January: Midseason Chimney Safety Reminder
- "If you haven't had your annual sweep yet, we still have spots"
- Creosote Grade 3 risk hook
- 125–150 words

---

### Output D: Nextdoor Neighborhood Post — Chimney Safety Education

Organic, non-salesy Nextdoor post for a homeowner-facing community.

- Title: "Before you light your fireplace this fall — a few things to know [CITY_STATE]"
- Content: NFPA 211 Level I/II education (not a sales pitch); creosote grade 3 risk; carbon monoxide CO risk for gas fireplaces; Clark County burn advisory (if applicable)
- Gentle credential mention: "CSIA Certified Chimney Sweep based in [CITY_STATE] — happy to answer questions"
- No direct booking CTA in main post; respond to comments
- 200–250 words; educational tone

---

### Output E: Home Warranty Company Partner Letter

From [OWNER_NAME] → Home warranty company (American Home Shield, Choice Home Warranty, etc.)

- Angle: become a credentialed in-network chimney and fireplace service provider
- Volume play: warranty company dispatches hundreds of chimney-related claims per year in the metro area
- What the CCS + NFI credentials mean for warranty claim approvals: written inspection report, NFPA-level classification, UL listing documentation for liner claims
- Turnaround: same-day dispatch availability for warranty escalations
- CTA: preferred vendor application + [PHONE]
- 300–350 words

---

### Output F: HOA Newsletter Feature Article — Chimney Safety Education

Educational, non-promotional article for submission to an HOA newsletter.

- Title: "Fireplace Safety for [Community Name] Homeowners — What You Need to Know"
- Content: NFPA 211 annual inspection recommendation; creosote grades; CO safety for gas fireplaces; Clark County No-Burn advisory (if Southern Nevada); EPA Phase 2 for wood stove inserts
- Author byline: "[OWNER_NAME], CSIA Certified Chimney Sweep #[CCS_NUMBER], [BUSINESS_NAME]"
- Ends with: "Questions? I'm happy to answer for [Community Name] residents" — no booking CTA
- 400–450 words; educational tone, homeowner-accessible language
```
