# Prompt 2 — Service Pages + Compliance + JSON-LD Schema

## Overview
Generates full service page copy for auto detailing, ceramic coating, PPF, mobile, and fleet services — plus AutoRepair and FAQPage JSON-LD structured data for Google rich results. Every claim is calibrated to what the business can legally support.

## Required Inputs
```
Business name: [your business name]
City/state: [city, state]
Address: [full street address]
Phone: [phone number]
Website: [URL]
Years in business: [number]
Google rating: [X.X stars, XXX reviews]
Certifications: [IDA, Gtechniq Authorized Detailer, XPEL Certified Installer, CARPRO, 3M, etc.]
Services to generate pages for: [check all]
  - [ ] Interior detail
  - [ ] Exterior detail / paint decontamination
  - [ ] Ceramic coating
    - Product: [e.g., "Gtechniq Crystal Serum Ultra"]
    - SiO2%: [e.g., "70%"]
    - Manufacturer warranty: [e.g., "9 years with annual inspection" or "not warranted"]
  - [ ] Paint protection film (PPF)
    - Brand: [e.g., "XPEL ULTIMATE PLUS"]
    - Self-healing: [Yes / No]
    - Manufacturer warranty: [e.g., "10 years"]
  - [ ] Window tint
    - Brand: [e.g., "Llumar ATR"]
    - VLT options available: [e.g., "35%, 20%, 5%"]
  - [ ] Mobile / on-site detailing
    - Water source: [customer tap / self-contained tank / reclaim system]
    - Service area radius: [XX miles from city]
  - [ ] Fleet / dealer prep
    - Fleet types served: [dealerships / delivery fleets / property management / hotels]
Paint correction services offered: [1-stage / 2-stage / 3-stage / all / none]
Price range (starting at): [interior from $X / exterior from $X / ceramic from $X / PPF from $X]
Primary differentiator: [compliance-first, licensed IDA, certified installer, fastest turnaround, etc.]
```

## Prompt
```
You are a professional automotive marketing copywriter and SEO specialist. Generate complete service page copy for the detailing business described below, including JSON-LD structured data.

**Business details:**
[PASTE INPUTS HERE]

**For each selected service, generate:**

### [Service Name] Service Page

**Page Title (60 char max):** [Service] in [City] | [Business Name]
**Meta Description (155 char max):** [Service benefit + city + CTA]

**Hero Section (H1 + 2 sentences):**
[Headline that names the service + city. Subhead that names the primary customer pain point solved.]

**Why [Business Name] for [Service] (3 bullet points):**
[Trust signal 1: certification or credential]
[Trust signal 2: specific product or process detail]
[Trust signal 3: guarantee or process that others don't offer]

**What's Included (service deliverables list):**
[Specific steps/items included in service — no vague language like "full clean"]

**Pricing (starting at $X):**
[Price floor only. "Starting at" language. Note that final pricing depends on vehicle size and condition assessment.]

**Our Process (4 steps):**
[Step 1: Inspection + condition assessment]
[Step 2: Preparation / decontamination]
[Step 3: Core service]
[Step 4: Final inspection + delivery]

**Compliance Disclosure (include for: ceramic, PPF, mobile, window tint):**
[Ceramic: product name + SiO2% + manufacturer warranty duration]
[PPF: product name + self-healing confirmation + manufacturer warranty]
[Mobile: water reclaim/containment statement]
[Tint: VLT options + state legal limit note for front windows]

**CTA Section:**
[Book Now button text + form field labels (Name, Phone, Vehicle Year/Make/Model, Service Interest)]

**FAQPage JSON-LD:**
[3-5 FAQs relevant to this service with compliance-accurate answers]

**AutoRepair + LocalBusiness JSON-LD:**
[Full schema with business details, service offered, geo, aggregate rating]

**COMPLIANCE RULES — DO NOT VIOLATE:**

1. **Ceramic coating duration:** Only use the manufacturer's stated warranty period. Examples:
   - Gtechniq Crystal Serum Ultra: "up to 9 years with annual registered installer inspection"
   - CARPRO CQuartz UK 3.0: "up to 3 years"
   - Generic/unbranded: "multi-year protection" — never state a specific year count
   Do NOT write "10-year ceramic coating" without the specific manufacturer warranty citation.

2. **SiO2 concentration:** If SiO2% is provided in inputs, include it. "Our ceramic coating contains X% SiO2" is verifiable and differentiating. Do not invent a percentage.

3. **PPF "self-healing":** Only applies to topcoat-equipped films (XPEL ULTIMATE PLUS, LLumar FormulaOne Ceramic, SunTek CXP, 3M Pro Series). Standard clear PPF without ceramic topcoat does NOT self-heal. Use only if confirmed in inputs.

4. **Paint correction staging:** Always specify:
   - "1-stage paint correction" = removes light swirls and water spots, does not remove deeper scratches
   - "2-stage paint correction" = removes moderate oxidation and swirl marks, significantly reduces deeper scratches
   - "3-stage paint correction" = removes heavy scratches, oxidation, and etching — most extensive correction
   Never promise "swirl-free" in writing — use "significantly reduced" or "minimized."

5. **Window tint VLT limits:** Nevada: front side 35% VLT minimum. California: 70% VLT minimum for front side windows. If generating for multiple states, note the legal limit in the FAQ.

6. **"Guaranteed results":** Replace with "we stand behind our work — if you're not satisfied with [specific outcome], contact us within [X days] for a complimentary re-service assessment."

7. **Mobile water:** For CA, NV, AZ: include "All mobile services use EPA-compliant water containment. Wash water is collected and disposed per [state] stormwater regulations — we never discharge to storm drains."

8. **IDA / certification claims:** "IDA Certified Detailer" only if current IDA certification confirmed in inputs. "Gtechniq Authorized Detailer" only if current authorization confirmed. Do not use certification language without confirmation.

**Output all selected service pages sequentially, each with complete JSON-LD.**
```

## JSON-LD Templates

### AutoRepair + LocalBusiness
```json
{
  "@context": "https://schema.org",
  "@type": ["AutoRepair", "LocalBusiness"],
  "name": "[Business Name]",
  "description": "[One sentence describing services]",
  "url": "[Website URL]",
  "telephone": "[Phone]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[Street]",
    "addressLocality": "[City]",
    "addressRegion": "[State]",
    "postalCode": "[ZIP]"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "[LAT]",
    "longitude": "[LONG]"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "[X.X]",
    "reviewCount": "[XXX]",
    "bestRating": "5"
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Detailing Services",
    "itemListElement": [
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "name": "[Service Name]",
          "description": "[Service description]"
        },
        "priceSpecification": {
          "@type": "PriceSpecification",
          "price": "[starting price]",
          "priceCurrency": "USD",
          "description": "Starting price — final quote based on vehicle size and condition"
        }
      }
    ]
  }
}
```
