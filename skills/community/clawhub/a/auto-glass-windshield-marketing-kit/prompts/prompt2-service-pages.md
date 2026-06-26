# Prompt 2 — Service Pages + ADAS Compliance + JSON-LD Schema

## Instructions

Fill in the variables below, then paste this entire prompt into Claude (claude.ai) or any capable AI model.

---

## PROMPT

You are an SEO copywriter and schema markup specialist for local auto glass businesses. Generate service page content and structured data using only the information provided. Follow all compliance rules — never add claims the shop did not confirm.

**Shop details:**
- Shop name: [SHOP_NAME]
- Address: [STREET], [CITY], [STATE] [ZIP]
- Phone: [PHONE]
- Website: [URL or "not provided"]
- AGRSS certified: [YES/NO — include cert number if available: e.g., AGRSS #NV-2024-1142]
- NWRA member: [YES/NO]
- Services offered (check all that apply): [WINDSHIELD REPLACEMENT / ROCK CHIP REPAIR / SIDE & REAR GLASS / SUNROOF & MOONROOF / HEAVY EQUIPMENT GLASS]
- OEM glass tier: [OEM-ONLY / OEM + OEE / AFTERMARKET-ONLY / OEM + AFTERMARKET]
- ADAS recalibration: [IN-HOUSE STATIC / IN-HOUSE DYNAMIC / IN-HOUSE BOTH / DEALERSHIP REFERRAL / NONE]
- Insurance carriers billed directly: [LIST or "NONE"]
- Warranty: [e.g., "lifetime warranty on installation workmanship", "1-year parts and labor", "NONE"]
- Mobile service: [YES — radius: [X] miles / NO]
- Hours: [e.g., "Mon-Fri 8AM-5PM, Sat 9AM-3PM, closed Sunday"]
- Google Business Profile URL: [URL or "not provided"]

**Compliance rules:**
1. AGRSS claims only if AGRSS = YES; include cert number if provided.
2. OEM glass only referenced if OEM tier includes OEM. "OEE" always explained as "Original Equipment Equivalent (same factory specification, independently manufactured)." Aftermarket never called "OEM quality."
3. ADAS recalibration section is MANDATORY regardless of in-house capability — if DEALERSHIP REFERRAL, include "We coordinate recalibration with a certified dealer service center at no scheduling hassle to you." If NONE, include "Note: If your vehicle has ADAS features, recalibration at a certified dealer or calibration center is required after windshield replacement — we will inform you of this requirement before beginning work."
4. Chip repair size limits always stated: "We repair chips up to 1 inch (25mm) in diameter and cracks up to 3 inches (75mm) in length that are not in the driver's primary view field and not within 2 inches of the glass edge."
5. Warranty: "installation workmanship" only — never "lifetime warranty on the glass" unless manufacturer-backed program confirmed.
6. Insurance copy: "most customers pay $0" only if carriers listed AND "(subject to your deductible)" immediately follows.

**Generate:**

**1. Windshield Replacement Service Page (400–500 words)**
Structure:
- H1: [Shop Name] Windshield Replacement — [City, State]
- Opening paragraph: core value prop, insurance, OEM/ADAS
- H2: Why Choose [Shop Name] for Windshield Replacement?
- Bullet list: 4–6 differentiators (gated on confirmed facts)
- H2: What to Expect: Our Windshield Replacement Process
- 4-step process (intake → glass selection → installation → ADAS recalibration/verification)
- H2: ADAS Recalibration After Windshield Replacement
- [Use ADAS compliance section — see rule 3]
- H2: Insurance Direct Billing (only if carriers listed)
- Closing paragraph + CTA

**2. Rock Chip Repair Service Page (300–400 words)**
Structure:
- H1: Rock Chip & Windshield Crack Repair — [City, State]
- Opening: repair vs. replace decision
- H2: When Can a Chip Be Repaired? (include AGRSS size limits)
- H2: Our Repair Process
- H2: When Replacement Is Required
- Closing + CTA

**3. ADAS Recalibration Explainer Section (200–250 words)**
Standalone section usable on any page or as a dedicated FAQ entry:
- What ADAS is and why it matters
- Static vs. dynamic calibration explanation (if in-house both or dynamic)
- Which vehicles require it (camera-based systems: Toyota Safety Sense, Honda Sensing, Subaru EyeSight, Volvo Pilot Assist, GM Super Cruise, Ford Co-Pilot360, Hyundai SmartSense)
- Your shop's capability (in-house or coordinated referral)
- Liability note: "Driving a vehicle with an uncalibrated ADAS camera can result in system malfunction and is a safety risk."

**4. Google Business Profile Description (750 characters max)**
Include: services, AGRSS status, OEM glass, ADAS capability, insurance billing, location.

**5. JSON-LD LocalBusiness Schema**
```json
{
  "@context": "https://schema.org",
  "@type": "AutoRepair",
  "name": "[SHOP_NAME]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[STREET]",
    "addressLocality": "[CITY]",
    "addressRegion": "[STATE]",
    "postalCode": "[ZIP]"
  },
  "telephone": "[PHONE]",
  "openingHours": "[HOURS IN SCHEMA FORMAT]",
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Auto Glass Services",
    "itemListElement": [LIST CONFIRMED SERVICES]
  }
}
```
Complete the schema with all confirmed fields. Do not add fields not provided.
