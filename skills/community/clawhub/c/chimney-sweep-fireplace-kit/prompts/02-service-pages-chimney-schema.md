# Prompt 2 — Service Pages + Chimney/Fireplace JSON-LD Schema

**Paid prompt.**

---

## Variables

- `[BUSINESS_NAME]`, `[OWNER_NAME]`, `[CITY_STATE]`, `[ZIP_CODES]`
- `[CCS_NUMBER]` — CSIA Certified Chimney Sweep number or "in training"
- `[NFI_CREDENTIALS]` — NFI Gas Appliance Specialist / Wood Burning Specialist / Pellet Specialist (comma-separated, or "none")
- `[STATE_LICENSE]` — State contractor license number
- `[SERVICES]` — Select all: gas-fireplace | wood-chimney | pellet | dryer-vent | relining | masonry | epa-install | level-ii-prelisting
- `[PHONE]`, `[WEBSITE]`
- `[REVIEW_COUNT]`, `[RATING]`

---

## Prompt

```
You are an expert chimney and fireplace contractor marketing and compliance copywriter. Generate service pages with JSON-LD schema markup for [BUSINESS_NAME] in [CITY_STATE].

CREDENTIALS: CCS [CCS_NUMBER] | NFI: [NFI_CREDENTIALS] | License: [STATE_LICENSE]
SERVICES: [SERVICES]
SERVICE AREA ZIPS: [ZIP_CODES]
REVIEWS: [REVIEW_COUNT] at [RATING] stars

COMPLIANCE RULES — apply to every service page:

1. CSIA CREDENTIAL GATE:
   - CCS number provided: "CSIA Certified Chimney Sweep #[CCS_NUMBER]" in intro paragraph and schema
   - "in training": "trained to CSIA Best Practices guidelines" — PERMANENTLY BLOCK "CSIA Certified," "CCS," "CSIA-certified company"

2. NFPA 211 LEVEL ENFORCEMENT:
   - All inspection references must specify Level I or Level II
   - Level I: routine annual, readily accessible areas only
   - Level II: required for real estate transactions, after operational problems, after system modification, after external event — always use "NFPA 211 Level II" (not "Level 2" or just "Level II inspection")
   - "Chimney inspection" without level specification is PERMANENTLY BLOCKED in service page headers and body

3. UL LISTING NUMBER ACCURACY:
   - Wood/solid-fuel relining: "UL 103-listed stainless steel liner system" (standard) or "UL 103HT-listed liner" (high-temperature coal/solid fuel)
   - Factory-built/zero-clearance fireplace service: "UL 127-listed factory-built fireplace"
   - Gas appliance relining: "UL 1777-listed flexible gas liner system"
   - "UL-listed liner" without the specific listing number is PERMANENTLY BLOCKED

4. EPA PHASE 2 GATE (for any wood stove / insert installation service pages):
   - Include: "All wood stove and fireplace insert installations use EPA Phase 2 certified units only (effective May 15, 2020 under 40 CFR Part 60 Subpart AAA/QQQQ). Verify the EPA Certification Number at epa.gov/burnwise before purchase."
   - "EPA-approved fireplace/stove" is PERMANENTLY BLOCKED
   - Clark County/Southern Nevada: include No-Burn Episode disclosure on all wood-burning pages

5. NFI GAS SCOPE GATE:
   - NFI Gas Appliance Specialist credential: unlock full gas appliance service page (service and maintenance of gas logs, inserts, direct-vent systems)
   - No NFI credential: gas service page limited to "chimney and venting inspection for gas appliances" — do NOT claim gas appliance servicing, pilot or valve work
   - Nevada gas line work (valve replacement, gas pressure testing, new gas piping beyond appliance connection): "Gas line work is performed by our Nevada C-1-licensed plumbing subcontractor" — BLOCK "we handle all gas work" without licensed subcontractor disclosure

6. CREOSOTE GRADE EDUCATION (wood chimney sweep pages):
   - Grade 1: dusty, flaky deposits — swept during routine service
   - Grade 2: tar-like, sticky deposits — must be removed before use; may require chemical treatment
   - Grade 3: glazed, hardened deposits — HIGH FIRE RISK; requires specialized Poultice Creosote Remover or full relining; "do not use" advisory
   - Include grade definitions in wood chimney sweep page; omit from gas-only pages

7. DRYER VENT COMPLIANCE (if dryer-vent in [SERVICES]):
   - Reference NFPA 211 Section 15 and NFPA 54 Chapter 10 for clothes dryer venting
   - "Clean lint trap reduces dryer fire risk" ✓
   - "We clean your entire dryer duct from lint trap to exterior termination" ✓
   - Maximum duct length disclosure: NFPA 54 specifies maximum 25-foot duct run (subtract 5 ft per 90° elbow); flag if client's duct exceeds limits
   - "Dryer vent cleaning eliminates all fire risk" is PERMANENTLY BLOCKED

8. OSHA LADDER SAFETY DISCLOSURE (all service pages):
   - Include in every roof-access service page: "All roof-access inspections are performed with OSHA-compliant ladder systems — our technicians are trained to OSHA 29 CFR 1926.1053 ladder safety standards"

9. FTC 2023 ENDORSEMENT GUIDES:
   - No "5-star review" request language in any service page body or CTA
   - No incentivized review offers

10. JSON-LD SCHEMA (each page):
    - Type: LocalBusiness + HomeAndConstructionBusiness
    - Required fields: name, url, telephone, address, areaServed (ZIP codes), licenseNumber ([STATE_LICENSE])
    - Credential fields: hasCredential with CCS # and NFI credentials
    - Aggregate rating: ratingValue [RATING], reviewCount [REVIEW_COUNT]
    - Service-specific offer catalog per page

GENERATE THESE 7 SERVICE PAGES:

---

### Page 1: Gas Fireplace Service & Tune-Up
(Only if gas-fireplace in [SERVICES])

Title: "Gas Fireplace Service & Tune-Up — [CITY_STATE] | [BUSINESS_NAME]"

Include:
- NFI Gas Appliance Specialist credential (if held) — full gas appliance service scope
- Annual gas fireplace tune-up checklist: burner inspection, pilot assembly, thermocouple/thermopile, igniter, gas valve operation (visual), heat exchanger, venting/flue, glass seal, remote/receiver, blower motor
- Safety check items: CO detector recommendation, carbon monoxide advisory (annual CO detector test required for any home with gas appliances)
- Gas line scope gate: if valve or gas piping work needed, licensed C-1 subcontractor
- NFPA 211 Level I venting inspection included in annual tune-up; Level II if real estate transaction
- Clark County burn advisory NOT applicable (gas appliances exempt from most open burn ordinances)
- OSHA ladder disclosure
- CTA: Annual service plan enrollment + booking URL

JSON-LD schema:
```json
{
  "@context": "https://schema.org",
  "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
  "name": "[BUSINESS_NAME]",
  "url": "[WEBSITE]",
  "telephone": "[PHONE]",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "[CITY_STATE split: city]",
    "addressRegion": "[CITY_STATE split: state]",
    "postalCode": "[PRIMARY_ZIP]"
  },
  "areaServed": [ZIP_CODES — array of ZIP strings],
  "licenseNumber": "[STATE_LICENSE]",
  "hasCredential": [
    {"@type": "EducationalOccupationalCredential", "credentialCategory": "CSIA Certified Chimney Sweep", "identifier": "[CCS_NUMBER]"},
    {"@type": "EducationalOccupationalCredential", "credentialCategory": "NFI Gas Appliance Specialist"}
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "[RATING]",
    "reviewCount": "[REVIEW_COUNT]"
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Gas Fireplace Services",
    "itemListElement": [
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Annual Gas Fireplace Tune-Up"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "NFPA 211 Level I Venting Inspection"}}
    ]
  }
}
```

---

### Page 2: Wood-Burning Chimney Sweep & NFPA Level I Inspection

Title: "Chimney Sweep & NFPA 211 Level I Inspection — [CITY_STATE] | [BUSINESS_NAME]"

Include:
- CSIA CCS credential hook
- Creosote grade table (Grade 1/2/3 definitions, Grade 3 = do not use)
- What's included in sweep + Level I: exterior cap/crown/flashing, smoke chamber, firebox, damper, accessible liner
- What Level I does NOT include: attic/crawl space (that's Level II)
- Clark County No-Burn Episode disclosure for wood-burning content
- OSHA ladder safety disclosure
- Dryer vent upsell mention if applicable
- CTA: Book annual sweep

JSON-LD: same structure as Page 1, offer catalog updated to "Annual Chimney Sweep" and "NFPA 211 Level I Inspection"

---

### Page 3: Chimney Relining — Stainless Steel & Flexible Liner Systems

Title: "Chimney Relining — UL 103-Listed Stainless Steel Liner | [BUSINESS_NAME]"

Include:
- Lead with: "UL 103-listed stainless steel liner systems for wood-burning applications; UL 1777-listed flexible gas liner systems for gas appliance venting — not generic 'stainless liner'"
- Why relining is needed: cracked clay tile, failed mortar joints, oversized flue for appliance BTU load, conversion from wood to gas (requires UL 1777 gas liner)
- Liner sizing: stainless liner must be sized to appliance manufacturer specifications — "6-inch round vs. 8-inch" not interchangeable; oversized liner reduces draft
- Smoke chamber parging: refractory parging above smoke shelf to smooth corbeled smoke chamber (reduces creosote accumulation)
- Lifetime liner warranty: if offered, specify what the warranty covers and excludes
- Before/after: pre-liner inspection finding + liner spec + post-install Level I verification sweep
- OSHA ladder disclosure
- CTA: Free relining assessment + booking URL

JSON-LD: offer catalog — "Chimney Relining (UL 103)", "Chimney Relining (UL 1777)", "Smoke Chamber Parging"

---

### Page 4: Chimney Cap, Crown, and Masonry Repair

Title: "Chimney Cap, Crown & Masonry Repair — [CITY_STATE] | [BUSINESS_NAME]"

Include:
- Chimney cap: stainless steel or galvanized; sized to flue tile dimension; "fits all flue sizes" is blocked — cap must match flue tile I.D. or manufacturer OD measurement
- Chimney crown: reinforced concrete crown (Portland cement + mortar, sloped for drainage); CrownCoat or equivalent elastomeric sealant for crack repair vs. full crown replacement
- Spalling brick: efflorescence, spalling, and mortar joint deterioration — tuckpointing specification (Type N vs. Type S mortar matching original)
- Waterproofing: ChimneySaver or equivalent 100% vapor-permeable water repellent — "waterproofing" that seals off vapor transmission is permanently blocked (causes spalling)
- Photography disclosure: before/after photos provided for every masonry repair job
- OSHA ladder disclosure
- CTA: Free masonry assessment

JSON-LD: offer catalog — "Chimney Cap Installation", "Chimney Crown Repair/Replacement", "Chimney Tuckpointing", "Chimney Waterproofing"

---

### Page 5: Dryer Vent Cleaning
(Only if dryer-vent in [SERVICES])

Title: "Dryer Vent Cleaning — NFPA 211 Section 15 Compliant | [BUSINESS_NAME]"

Include:
- NFPA 211 Section 15 reference: annual dryer vent cleaning recommended for all residential dryers
- NFPA 54 duct length gate: maximum 25-foot duct run before length reduction required for 90° elbows; flag oversized installs
- Scope: lint trap housing → duct run → exterior termination cap; duct material type noted (foil, semi-rigid aluminum, rigid aluminum — foil is permanently blocked as NFPA non-compliant)
- Cleaning method: rotary brush system (not compressed air only)
- Blockage finding: if duct fully blocked or duct run exceeds NFPA limits, written finding provided
- "Dryer vent cleaning eliminates all fire risk" is PERMANENTLY BLOCKED
- CTA: Book dryer vent cleaning (often bundled with chimney sweep)

JSON-LD: offer catalog — "Dryer Vent Cleaning", "Dryer Duct Length Assessment"

---

### Page 6: EPA Phase 2 Wood Stove & Fireplace Insert Installation
(Only if epa-install in [SERVICES])

Title: "EPA Phase 2 Certified Wood Stove & Fireplace Insert Installation | [BUSINESS_NAME]"

Include:
- EPA Phase 2 gate: "We only install EPA Phase 2 certified units manufactured after May 15, 2020 under 40 CFR Part 60 Subpart AAA. Verify the EPA Certification Number at epa.gov/burnwise before purchase."
- "EPA-approved" is PERMANENTLY BLOCKED — use "EPA Phase 2 certified" throughout
- NFI Wood Burning Specialist credential (if held) for appliance selection guidance
- UL 103-listed liner required for all wood stove installations (insert into existing masonry fireplace)
- Clearance requirements: manufacturer-specified clearance to combustibles — "we match clearances to each unit's installation manual"
- Clark County No-Burn Episode disclosure
- Permit disclosure: "Wood stove and fireplace insert installation requires a building permit in Clark County — we handle permit coordination"
- OSHA ladder disclosure
- CTA: Installation consultation + booking URL

JSON-LD: offer catalog — "EPA Phase 2 Wood Stove Installation", "Fireplace Insert Installation"

---

### Page 7: NFPA 211 Level II Pre-Listing Chimney Inspection
(Only if level-ii-prelisting in [SERVICES])

Title: "NFPA 211 Level II Pre-Listing Chimney Inspection — [CITY_STATE] | [BUSINESS_NAME]"

Include:
- NFPA 211 Section 14.2 citation: "Level II inspection required at all changes of occupancy or ownership"
- Scope: all areas accessible by normal means + accessible attic, crawl space, basement areas; includes video scan of liner (if applicable)
- Written report: provided within 24–48 hours of inspection; documents findings by NFPA 211 level and location; grade for all creosote found
- What's in the report: cap condition, crown condition, flashing, firebox, damper, smoke chamber, liner condition, clearances to combustibles
- Why realtors need a CCS credential: "A Level II inspection report carries more weight in a real estate transaction when signed by a CSIA Certified Chimney Sweep — verifiable at csia.org/find-a-sweep"
- How to order: "Realtors: email or call [PHONE] to schedule — digital report delivered for upload to MLS disclosure package"
- OSHA ladder disclosure
- CTA: Schedule Level II + direct realtor contact CTA

JSON-LD: offer catalog — "NFPA 211 Level II Pre-Listing Chimney Inspection", "Chimney Inspection Report (Written)"
```
