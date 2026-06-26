# Prompt 3 — Website Content + JSON-LD Schema

Generate SEO-optimized service pages with technically accurate auto glass and ADAS language, structured data markup, and meta tags. All outputs pass AGSC, ADAS, OEM, deductible, and FTC compliance gates.

---

## Input Fields

```
[All fields from Prompt 1, plus:]

Services to build pages for [check all]:
  [ ] Windshield replacement
  [ ] Chip & crack repair
  [ ] Side & rear glass replacement
  [ ] ADAS recalibration
  [ ] Mobile auto glass service
  [ ] Fleet glass services
  [ ] RV / commercial vehicle glass

Glass brands/products stocked (be specific: Pilkington NSF P-1, AGC OEM Line, Lynx, PGW Aurora, other):
Calibration equipment used (if ADAS offered): Autel ADAS Pro / Launch X-431 ADAS Pro+ / Bosch DAS 3000 / OEM scan tool / Other:
Team credentials/certifications (AGSC, ASE, I-CAR, other):
Years in business:
Number of locations:
Google rating + review count (for schema):
Owner/manager name (for LocalBusiness schema):
```

---

## Compliance Gates (All Prompt 1 gates apply, plus:)

**Technical Accuracy — Glass Construction:**
- Windshield = laminated safety glass (two glass layers bonded with PVB — polyvinyl butyral — interlayer). Must not shatter on impact. DOT-required.
- Side/rear glass = tempered glass (single layer, heat-treated to shatter into small granular pieces on impact). Different installation — no adhesive, gasket/channel system.
- Never conflate laminated and tempered in technical descriptions.
- Acoustic interlayer (SoundShield, Acoustic PVB) = legitimate feature for OEM-spec vehicles; don't claim on standard aftermarket glass.
- Tinted glass (factory-installed shade band, privacy glass) ≠ aftermarket tint film.

**ADAS Technical Accuracy:**
- Camera mounts to windshield bracket — windshield replacement disturbs camera position by millimeters = sufficient to throw calibration.
- Static recalibration: vehicle parked, targets placed at OEM-specified distances and heights in controlled environment. Not all shops have space to do this correctly.
- Dynamic recalibration: vehicle driven at specified speed (usually 25-45 mph) for 20+ minutes on certain road type, scan tool connected. Not suitable for all vehicles.
- Some vehicles require both static + dynamic (Mercedes, BMW, some Ford).
- Skill does NOT claim shop can calibrate makes/models they haven't documented capability for.

**Safe Drive-Away Time:**
- Technically: "Minimum Drive-Away Time" (MDAT) per AGSC Standard 150, dependent on adhesive, primer, temperature, humidity.
- Common MDMATs: Sika Tack Ultra Fast: 30 min @ 68°F+; Dow Betaseal Express: 60 min; generic urethane: 1+ hour; some OEM adhesive systems: 8 hours.
- Never state specific drive-away time without knowing the adhesive used and environmental conditions.
- Web page language: "Drive-away time varies by adhesive and temperature — our AGSC-certified technicians will tell you exactly when it's safe." [Only if AGSC-certified; else remove "AGSC-certified"]

---

## Output

### 1. Windshield Replacement Service Page (700-900 words)

**Meta Title (55-60 chars):** Windshield Replacement [City], NV | [Shop Name]
**Meta Description (150-160 chars):** Windshield replacement in [City] from [Shop Name]. AGSC-certified installation. Insurance billing direct. ADAS recalibration available. Call [phone] — same day.

**H1:** Windshield Replacement in [City], Nevada

**Intro (100-150 words):**
[Shop Name] provides windshield replacement for all makes and models in [City] and surrounding [service area cities]. We use [glass sourcing framing per Gate 5], perform AGSC-certified installation [if applicable], and bill your insurance directly — handling the paperwork so you don't have to. If your vehicle has a camera mounted to the windshield for lane departure or collision warning systems, we offer ADAS recalibration to ensure those systems work correctly after installation [if applicable].

**H2: What to Expect During Your Windshield Replacement**
Step-by-step process: 1) Inspection and measurement; 2) Old windshield removal (trim/molding preserved where possible); 3) Frame cleaning and primer application; 4) Adhesive application (AGSC Standard 150-compliant urethane); 5) New glass positioning and cure; 6) ADAS recalibration if equipped [if applicable]; 7) Drive-away time review with technician.
[Technical note: PVB interlayer, laminated construction, DOT-required specs explained simply]

**H2: Does Your Insurance Cover Windshield Replacement?**
[Generate honest insurance framing — most comprehensive policies include glass; deductible varies by policy; chip repair often zero deductible; "check your policy" qualifier always present; deductible waiver HARD BLOCKED]

**H2: OEM vs. Aftermarket Glass — What We Stock**
[Generate based on glass sourcing gate input — truthful claim only]

**H2: ADAS Recalibration After Windshield Replacement** [if shop offers]
[Explain which vehicles need it, what static/dynamic means, how long it takes, why skipping it is a safety risk — educational framing, not fear-based]

**H2: Service Area**
[List cities; JSON-LD geo radius anchor]

**H2: Frequently Asked Questions**
[See Prompt 1 FAQ structure; include 5 Q for this page]

**CTA:** Get a Free Quote | Call [Phone] | [Online booking link if applicable]

**NSCB License disclosure:** [Shop Name] is a Nevada State Contractors Board licensed glass and glazing contractor. License #[NSCB-number].

---

### 2. Chip & Crack Repair Page (600-700 words)

**Meta Title:** Windshield Chip Repair [City] | [Shop Name] — Fast & Affordable
**Meta Description:** Chip smaller than a quarter? [Shop Name] repairs windshield chips in [City] in under 30 minutes. Often covered by insurance at no deductible. Call [phone].

**H1:** Windshield Chip & Crack Repair in [City]

**Key content blocks:**
- What's repairable vs. what requires replacement (size thresholds, location, depth)
- How chip repair works (resin injection process — technically accurate)
- Insurance coverage for chip repair (most comprehensive = no deductible for chip repair — "most" qualifier + check your policy)
- Why timing matters (temperature, UV exposure, pressure accelerate cracking)
- Limitations: chip in driver's line of sight, deep impact through both glass layers, crack longer than 6 inches → replacement recommended
- FAQ: 5 questions specific to chip repair

**Compliance notes:** No "100% invisible repair" — resin fill is visible on close inspection in some cases; "significantly reduced visibility of the chip" is accurate. No "guaranteed" outcomes without basis.

---

### 3. ADAS Recalibration Page [include only if shop offers] (700-900 words)

**Meta Title:** ADAS Recalibration [City] | After Windshield Replacement | [Shop Name]
**Meta Description:** ADAS camera recalibration after windshield replacement in [City]. Static and dynamic recalibration for Toyota, Honda, Subaru, Tesla, Ford + more. Call [phone].

**H1:** ADAS Recalibration After Windshield Replacement in [City]

**Content blocks:**
- What ADAS is (forward collision warning, lane departure, auto emergency braking, adaptive cruise — camera-dependent)
- Why windshield replacement disrupts calibration (millimeter-level position change = system error)
- Which vehicles are affected (list major systems: Subaru EyeSight, Toyota Pre-Collision, Honda Sensing, Mazda 360°, Ford Co-Pilot360, GM Super Cruise, Volvo IntelliSafe, Tesla Autopilot — with disclosure: "this list grows with model years; ask us about your specific vehicle")
- Static recalibration explained (controlled environment, targets, equipment: [list shop's equipment])
- Dynamic recalibration explained (drive cycle, scan tool, road conditions required)
- NHTSA documentation reference: "The National Highway Traffic Safety Administration has flagged improperly calibrated ADAS as a contributing factor in crashes"
- What to ask any glass shop: "Do you offer ADAS recalibration? What equipment do you use? Do you provide a post-calibration report?"
- [Shop Name]'s calibration process and documentation

**Compliance:** No "guaranteed 100% accurate calibration" without post-calibration verification data. "Certified recalibration" requires documented equipment + trained technician. Use "professional" or "equipment-verified" if certification not held.

---

### 4. Fleet Services Landing Page (500-700 words)

**Meta Title:** Fleet Glass Service [City] | [Shop Name] — Commercial & Fleet Accounts
**Meta Description:** Fleet windshield replacement and chip repair in [City]. Mobile service available. Fleet account pricing. ADAS recalibration for ADAS-equipped vehicles. Call [phone].

**H1:** Fleet Auto Glass Service in [City] — Commercial Accounts Welcome

**Content blocks:**
- Who we serve: rental agencies, delivery fleets, rideshare partners, municipal/government fleets, auto dealer service departments
- Services: mobile glass for at-your-location service; bulk account pricing; scheduled fleet audits; ADAS recalibration for equipped vehicles
- Why fleet managers choose us: one point of contact, direct billing, documentation for fleet records, AGSC-certified installation on every vehicle [if applicable]
- Process: fleet account setup, intake form, scheduling preferences, billing/invoicing options
- CTA: "Set up your fleet account — call [phone] or email [email]"

---

### 5. Full FAQ Page (15 Questions)

Generate answers to:
1. Do you use OEM glass? [sourcing gate]
2. What's the difference between OEM and aftermarket glass?
3. Will my insurance cover my windshield replacement?
4. Can you waive my deductible? [NRS 686A.2825 gate — explain law, offer billing assistance]
5. How long will it take?
6. When can I drive after my windshield is replaced? [AGSC/MDAT gate]
7. Do I need ADAS recalibration? [vehicle-based; ADAS gate]
8. What's the difference between static and dynamic ADAS recalibration?
9. Can you repair my chip or do I need a replacement?
10. Do you come to me? [mobile service gate]
11. What's your service area?
12. Is your work warrantied?
13. Do you work with my insurance company?
14. How does the insurance claim process work?
15. Are you licensed in Nevada? [NSCB gate — license number disclosed]

---

### 6. JSON-LD Schema Block

```json
{
  "@context": "https://schema.org",
  "@type": "AutoRepair",
  "name": "[Shop Name]",
  "image": "[logo URL]",
  "url": "[website URL]",
  "telephone": "[phone]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[street]",
    "addressLocality": "[city]",
    "addressRegion": "NV",
    "postalCode": "[zip]",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "[lat]",
    "longitude": "[long]"
  },
  "openingHoursSpecification": "[generate from hours input]",
  "priceRange": "$$",
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Auto Glass Services",
    "itemListElement": [
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Windshield Replacement"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Windshield Chip Repair"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "ADAS Recalibration"}}
    ]
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "[rating]",
    "reviewCount": "[count]"
  },
  "areaServed": [
    "[city 1]", "[city 2]", "[city 3]"
  ],
  "sameAs": [
    "[Google Business Profile URL]",
    "[Yelp URL]",
    "[Facebook URL]"
  ]
}
```

**Compliance note:** aggregateRating only included if real rating/count provided. Do not fabricate or estimate. No "bestRating: 10" without valid review scale.
