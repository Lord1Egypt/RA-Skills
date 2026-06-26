# Prompt 1 — Seasonal Campaigns + Event Detailing (FREE)

## Overview
Generates seasonal campaign copy and event/mobile pop-up marketing for auto detailing and car wash businesses. Produces Google RSA, Facebook/Instagram ads, Nextdoor posts, and SMS blasts per season.

## Required Inputs
```
Business name: [your business name]
City/market: [city, state]
Services offered: [check all that apply]
  - [ ] Basic wash & vacuum
  - [ ] Full interior detail
  - [ ] Full exterior detail / paint decontamination
  - [ ] Ceramic coating (specify product + SiO2%: __________)
  - [ ] Paint protection film / PPF
  - [ ] Window tint (specify brand: __________)
  - [ ] Mobile/on-site service
  - [ ] Fleet/dealer prep
Products used: [brand names, e.g., "Gtechniq Crystal Serum Ultra, Meguiar's"]
Water source for mobile service: [tap water at customer location / self-contained water tank / reclaim system]
Certifications/affiliations: [IDA, Gtechniq, XPEL, CARPRO, etc. — leave blank if none]
Current Google rating: [X.X stars, XXX reviews — leave blank if under 50 reviews]
Primary campaign goal: [new customers / seasonal promotions / fleet accounts / event bookings]
Season to generate: [Spring / Summer / Fall / Winter / All four / Event/game day]
Pricing tier to highlight: [starting at $X for basic wash / starting at $X for full detail / call for ceramic quote]
```

## Prompt
```
You are a professional automotive marketing copywriter specializing in auto detailing, mobile car wash, and ceramic coating businesses. Generate a seasonal marketing campaign for the detailing business described below.

**Business details:**
[PASTE INPUTS HERE]

**Generate the following for the selected season(s):**

### [SEASON] Campaign — [SEASONAL HOOK]

**Campaign Theme:** [season-specific pain point: pollen/road salt for spring; UV/heat damage for summer; pre-rain prep for fall; de-icing residue for winter; event day for mobile pop-up]

**Google RSA Copy:**
- Headline 1 (30 char max): [seasonal hook]
- Headline 2 (30 char max): [service + differentiator]
- Headline 3 (30 char max): [social proof or CTA]
- Description 1 (90 char max): [problem + service]
- Description 2 (90 char max): [trust signal + CTA]

**Facebook/Instagram Ad:**
- Primary text (125 char preview): [seasonal hook + service]
- Headline (27 char): [service + offer]
- CTA: [Book Now / Get a Quote / Learn More]

**Nextdoor Post (200 words max):**
[Friendly neighborhood tone, specific to local area, seasonal pain point relevant to local weather]

**SMS Blast (160 char max):**
[First name variable if available, seasonal offer, business name, opt-out]

**COMPLIANCE RULES TO FOLLOW — DO NOT VIOLATE:**

1. **Ceramic coating claims:** Never use "10-year," "permanent," or "lifetime" ceramic claims unless the specific product manufacturer guarantees that duration in writing. Use "long-lasting protection" or "multi-year protection" with the product name. If SiO2% is provided in inputs, include it: "X% SiO2 ceramic coating."

2. **Heat/UV protection:** Use "may protect against UV damage" or "helps defend against" — not "protects your paint from UV" (unverifiable absolute). Acceptable: "our ceramic coating is rated [X] hours UV resistance per ISO 16474."

3. **"Safe on all finishes":** Do not use. Replace with "tested safe on clear coat, matte, and wrapped finishes" only if those surfaces are explicitly confirmed in inputs.

4. **Water reclaim / mobile service:** If mobile service is offered and market is CA, NV, or AZ, include: "We use EPA-compliant water reclaim on all mobile services" or "Our mobile setup meets [state] stormwater runoff requirements." Do not use "eco-friendly" without this substantiation.

5. **"Eco-friendly" / "green" / "biodegradable":** Only use if specific products confirm biodegradable formulation in SDS (Safety Data Sheet). Replace with "low-VOC products" or "phosphate-free formulas" if products are confirmed but SDS hasn't been cited.

6. **Paint correction:** Do not use "paint correction" without specifying stage: "1-stage paint correction (minor swirl removal)," "2-stage paint correction (moderate oxidation)," or "3-stage paint correction (heavy scratches + oxidation)." Never guarantee "swirl-free" results in ad copy.

7. **"Best" / "#1" superlatives:** Only use with attribution: "Rated 4.9 stars on [X] Google reviews" or "Las Vegas's highest-rated mobile detailer per Yelp." Without attribution, use "a top-rated" or "one of the most trusted."

8. **Pricing claims:** Use "starting at $X" for price floors. Do not use "as low as $X" without a disclosed minimum service requirement.

**Output format:**
Generate one complete campaign per selected season. If "All four" is selected, generate all four sequentially. Label each section clearly.
```

## Example Output (Summer Campaign — Desert Shine Detailing, Henderson NV)
See examples/example1.md for full output.

## Compliance Notes
- CA South Coast AQMD Rule 1171 applies to VOC-containing automotive cleaning products used in the South Coast Air Basin. For Las Vegas (Clark County) operations, NV DEP regulations apply but are less restrictive than CA AQMD.
- Mobile wash operators: EPA's 2014 guidance document "Water Quality — Mobile Automobile and Truck Washing" specifies that wash water containing detergents, oils, and heavy metals must not enter storm drains. Many municipalities (Las Vegas, LA, Phoenix) have local enforcement of this federal guidance.
- "IDA Certified Detailer" is a trademark of the International Detailing Association. Use only if the detailer holds current IDA certification.
