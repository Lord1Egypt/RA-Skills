# Prompt 2: Service Pages + JSON-LD Schema

**Skill:** Appliance Repair Marketing Kit  
**Prompt:** 2 of 4  
**Tier:** Paid

---

## Instructions

Copy the prompt below into Claude (any version). Fill in every `[BRACKET]` field before submitting.

---

## The Prompt

```
You are an SEO copywriter specializing in local home services businesses.

Generate 5 SEO-optimized service pages + JSON-LD schema for this appliance repair business:

BUSINESS INFO:
- Business name: [BUSINESS NAME]
- City/State: [CITY, STATE]
- Service area: [LIST ALL CITIES/ZIPS SERVED]
- Brands serviced: [LIST BRANDS]
- Authorized service center: [YES/NO — which brands if yes]
- OEM parts: [YES (genuine OEM sourced) / NO (quality aftermarket) / MIXED]
- EPA 608 certified: [YES/NO]
- Repair warranty: [e.g., 90-day parts & labor]
- Years in business: [NUMBER]
- Pricing model: [flat-rate / diagnostic fee + parts / hourly]
- Diagnostic fee: [AMOUNT or "waived with repair"]
- Phone: [PHONE]
- Website: [URL]

GENERATE 5 SERVICE PAGES:

PAGE 1: Washer Repair [City]
PAGE 2: Dryer Repair [City]
PAGE 3: Refrigerator Repair [City]
PAGE 4: Dishwasher Repair [City]
PAGE 5: Oven & Range Repair [City]

FOR EACH PAGE, GENERATE:

1. SEO TITLE TAG (60 chars max): include appliance type + city + brand hint
2. META DESCRIPTION (155 chars max): problem + solution + CTA
3. H1 HEADING: appliance type + city + key brand(s)
4. INTRO PARAGRAPH (100 words): common failure symptoms, fast diagnosis angle, response time
5. COMMON PROBLEMS SECTION (H2 + 4-5 bullet points): brand-specific failures for top 2-3 brands
6. WHY CHOOSE US SECTION (H2 + 3 bullets): OEM parts claim, warranty, authorization status
7. SERVICE AREA SECTION (H2): city + neighboring cities natural language (no keyword stuffing)
8. FAQ SECTION (H2 + 3 Q&As): repair cost range, same-day availability, warranty question
9. CTA SECTION: phone number + booking link + urgency statement

JSON-LD SCHEMA FOR EACH PAGE:
- @type: LocalBusiness + Service
- ServiceType: [appliance type] repair
- AreaServed: all cities listed
- PriceRange: based on pricing model
- AggregateRating: placeholder (★★★★★ with note to update with real data)
- hasOfferCatalog: list services covered

COMPLIANCE RULES (mandatory):
1. OEM PARTS: 
   - If OEM = YES: "genuine OEM parts sourced directly from [Brand]" is allowed
   - If OEM = NO: use "quality replacement parts" — never "OEM" or "genuine" 
   - If MIXED: "OEM parts available; quality aftermarket used when OEM unavailable" 
2. AUTHORIZED SERVICE:
   - Only use "authorized service center" if authorized = YES for that brand
   - Unapproved: "factory-trained technicians specializing in [Brand]" is acceptable
3. EPA 608:
   - Refrigerator page: if EPA 608 = YES, state "EPA 608-certified technicians for refrigerant handling"
   - If EPA 608 = NO: remove all refrigerant-related service claims from fridge page
4. WARRANTY CLAIMS: only guarantee stated repair warranty — no "lifetime guarantee" language
5. PRICING: if flat-rate, can state price ranges; if diagnostic fee, always note waiver policy
6. BRAND TRADEMARKS: use brand names for identification only, not to imply affiliation
   - Acceptable: "we repair GE appliances" / "specializing in Whirlpool repairs"
   - Not acceptable: "GE Authorized" unless authorization confirmed

Output all 5 pages + JSON-LD. Use markdown headers. No commentary outside the page content.
```

---

## What You Get

- 5 complete service pages (~600-900 words each)
- JSON-LD schema for all 5 pages
- Brand-specific failure symptoms (converts visitors who searched by symptom)
- OEM parts compliance language pre-built
- FAQ schema for rich snippets

## Pro Tip

The refrigerator page will be your top traffic driver — people search "refrigerator repair [city]" at emergency frequency. The brand-specific failure sections (LG linear compressor, Samsung ice maker, Whirlpool water inlet valve) are what separates your pages from generic competitors and earns featured snippets.
