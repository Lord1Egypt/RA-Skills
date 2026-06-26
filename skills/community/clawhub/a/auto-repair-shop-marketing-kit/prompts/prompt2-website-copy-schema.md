# Prompt 2: Website Copy + Compliance Review + Schema (PAID)

## Instructions

Use after completing Prompt 1. Requires your exact credentials, warranty policy, and state for compliant disclosure language.

---

## The Prompt

You are an expert automotive service marketing copywriter and compliance specialist. Generate complete, publish-ready website copy for the following auto repair shop. Apply all compliance rules listed below — every page must include the correct disclosure language for the shop's state.

**Shop Information:**
- Shop name: [NAME]
- City, State: [CITY, STATE]
- Services offered (list all): [FULL SERVICE LIST]
- ASE credentials (exact): [EXACT CREDENTIALS]
- EPA Section 608 certification: [Universal / Type I-III / specify which techs]
- Shop certifications: [NAPA AutoCare / AAA / CarFax / iATN / ASE Blue Seal / other]
- State license number: [LICENSE #]
- Years in business: [YEARS]
- Number of bays: [BAYS]
- Labor rate: [$/hour]
- Parts policy: [OEM only / OEM + OE-quality aftermarket / all quality tiers offered — customer chooses]
- Warranty policy: [Full details: duration, mileage, who provides, what's covered, exclusions]
- Owner name (for About page): [NAME]
- Website URL: [URL or "not yet built"]

**Generate the following:**

1. **Homepage**
   - H1 headline + subheadline
   - Trust bar (5 trust signals with icons suggested)
   - Hero section body copy (100 words)
   - Services overview section (3 featured services with 40-word descriptions each)
   - "Why Choose Us" section (5 differentiators, compliance-accurate)
   - CTA section (appointment booking or call)

2. **Service Pages** (one per major service offered — 300-400 words each):
   - General Repair
   - Brake Service (include: DOT compliance, brake fluid standards)
   - AC & Heating (include: EPA 608 disclosure, refrigerant types — R-134a and/or R-1234yf)
   - Tire & Alignment (include: UTQG rating explanation, speed rating basics)
   - Oil Change (include: viscosity grade accuracy, OEM interval disclaimer)
   - Diagnostics (include: no "free diagnosis" unless genuinely free — FTC rule)
   - Collision/Body Repair (if applicable: insurance supplement process, OEM vs LKQ vs aftermarket parts for collision)
   Each service page includes: FAQPage JSON-LD schema (3-5 questions)

3. **About Page**
   - Shop history narrative
   - Technician credentials section (exact ASE credential language only)
   - Community involvement section (if any details provided)
   - Shop certifications section with explanation of what each means to customers

4. **Warranty Policy Page** (Magnuson-Moss compliant)
   - Full vs. Limited warranty designation (MUST specify which)
   - What's covered (parts, labor, or both)
   - What's excluded (misuse, modifications, normal wear)
   - Duration and mileage cap
   - Who performs warranty repairs (this shop only, or NAPA/AAA nationwide network)
   - How to claim warranty service
   - Dispute resolution process

5. **OEM vs Aftermarket Parts Policy Page**
   - Explain difference between OEM, OE-quality aftermarket, and remanufactured
   - Explain how parts choice affects warranty
   - Insurance-required OEM parts note (for collision shops)
   - Customer choice policy (if applicable)

6. **State-Required Estimate/Repair Order Disclosure Page**
   [Generate based on state provided]:
   - CA: BAR repair order requirements, display of customer rights sign, written authorization threshold
   - TX: DMV Rule 84 estimate requirements, itemized invoice requirement, storage fee disclosure
   - NV: DMV estimate rules, written authorization for cost overruns, customer rights
   - FL: DHSMV estimate requirements, lien rights disclosure
   - Other: "Contact us for our written estimate policy — we always get your authorization before starting work"

7. **JSON-LD Structured Data** (paste into site `<head>`):
```json
{
  "@context": "https://schema.org",
  "@type": ["LocalBusiness", "AutoRepair"],
  "name": "[SHOP NAME]",
  "description": "[GENERATED DESCRIPTION]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[ADDRESS]",
    "addressLocality": "[CITY]",
    "addressRegion": "[STATE]",
    "postalCode": "[ZIP]"
  },
  "telephone": "[PHONE]",
  "url": "[URL]",
  "openingHours": "[HOURS]",
  "priceRange": "$$",
  "hasCredential": [
    "[ASE CREDENTIAL 1]",
    "[EPA 608 CERTIFICATION]",
    "[SHOP AFFILIATION]"
  ],
  "areaServed": {
    "@type": "GeoCircle",
    "geoMidpoint": {
      "@type": "GeoCoordinates",
      "latitude": "[LAT]",
      "longitude": "[LONG]"
    },
    "geoRadius": "15"
  }
}
```

**COMPLIANCE RULES:**

**ASE Credentials:**
- List only exact credentials confirmed — never say "master technician" unless A1-A8 + L1 confirmed
- "ASE Blue Seal of Excellence" = 75%+ of technicians hold ASE credentials — verify before using
- Use "certified" not "licensed" for ASE (it's a certification program, not a state license)

**EPA Section 608:**
- Required by law for anyone who purchases, recovers, or charges refrigerant
- "EPA Section 608 Universal certified" covers all refrigerant types (Type I, II, III)
- For shops handling only R-1234yf (newer vehicles), note SAEJ2843 certification requirement
- NEVER imply this is optional or that the shop can do AC work without it

**Parts Accuracy:**
- "OEM" = Original Equipment Manufacturer (made by or for the vehicle manufacturer)
- "OE-quality aftermarket" = third-party part meeting OEM specifications — do NOT call this "OEM"
- "Remanufactured" = used core rebuilt to spec — different from "rebuilt" (which has no standard)
- For collision work: state whether shop uses LKQ (like kind and quality), aftermarket, or OEM

**Oil Change:**
- Do not specify viscosity grades unless shop confirms they use correct grade per OEM specs
- "Manufacturer-recommended interval" is safe; do not override OEM interval with shop preference
- "Synthetic" vs "conventional" vs "high mileage" must match what's actually used

**Diagnostics:**
- "Free diagnostic" = must be genuinely free; if shop charges a diagnostic fee that's applied toward repair, say that explicitly
- "We'll waive the diagnostic fee if you proceed with the repair" is accurate and legal; "free diagnostic" when there's a charge is an FTC deception
