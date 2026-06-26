# Prompt 2: Service Pages + Compliance + JSON-LD Schema (PAID)

## Instructions

Copy this prompt into Claude. Fill in the `[BRACKETS]`. Generates your main cleaning page, 3 specialty pages, FAQ schema, and LocalBusiness JSON-LD.

---

## The Prompt

```
You are an SEO copywriter and local business schema specialist. Generate service page copy and structured data for a cleaning business.

BUSINESS DETAILS:
- Business name: [NAME]
- City + service area (list all zip codes or neighborhoods): [CITY, STATE — list neighborhoods/zips]
- Services offered: [check all: residential maid, deep cleaning, move-in/move-out, vacation rental turnover, commercial/office, post-construction, hoarding/estate cleanout]
- Products used: [brand names if EPA Safer Choice certified, or "professional-grade" if not certified]
- Equipment: [e.g., HEPA vacuums, steam cleaners, microfiber systems — or "standard"]
- Staff type: [W-2 employees / independent contractors / mixed — be accurate for IRS language]
- Bonding & insurance: [GL amount, bonding amount, workers' comp yes/no]
- Certifications: [ARCSI, ISSA CIMS, EPA Safer Choice, EcoLogo, BBB, IICRC for specialty — or "none"]
- Average pricing: [e.g., $120–$160 for standard 2BR/2BA, $200–$280 deep clean]
- Booking method: [phone, online, app — include URL if online]
- Service area radius: [e.g., 20-mile radius from Henderson, NV 89002]
- Years in business: [X years]
- Review count & rating: [e.g., 4.9★ 287 Google reviews]

COMPLIANCE RULES — FOLLOW EXACTLY:
1. "Hospital-grade disinfectant" requires EPA Registration Number confirmation — use "professional-grade disinfectant" if EPA Reg. No. unknown
2. "Chemical-free" prohibited unless ALL products are water/steam-only — use "low-chemical" or "EPA Safer Choice certified" instead
3. "Eco-friendly" requires named certification (EPA Safer Choice, Green Seal, EcoLogo) — or use "plant-based formulas"
4. Move-out cleaning: NEVER promise "get your deposit back" — use "meet your landlord's cleaning standards" or "cleaning standard that helps satisfy move-out inspection"
5. Staff language: use "cleaning professionals" or "cleaning team" — avoid "employees" and "contractors" in marketing copy (IRS classification issue); state factual type in FAQ only
6. "Licensed" claim: only include if your state requires a cleaning license (California HIC, some states for commercial only) — most states do NOT require a residential cleaning license; use "bonded & insured" instead
7. Satisfaction guarantee: must specify what the remedy is (re-clean, refund, credit) — not "100% satisfaction, period"
8. Schema markup: price range must use format "@type": "PriceSpecification"

GENERATE:

**SECTION 1: MAIN CLEANING SERVICES PAGE**
- Title tag (55–60 chars): [Business Name] + primary keyword + city
- Meta description (150–160 chars): include primary keyword, city, 1 trust signal
- H1: primary keyword phrase + city (under 65 chars)
- Introduction (150 words): what you do, who you serve, trust signals
- Services overview (4–6 cards with icon suggestion, 50-word description each)
- Why choose us (4 bullet points with proof — no unverifiable claims)
- Satisfaction guarantee section (state exact re-clean policy)
- CTA section (phone + booking URL)
- Internal linking suggestions (5 pages to link to)

**SECTION 2: THREE SPECIALTY PAGES** (300–400 words each)
Page A: Move-In / Move-Out Cleaning
Page B: Deep Cleaning Service
Page C: Vacation Rental / Airbnb Turnover Cleaning

For each:
- Title tag + meta description
- H1 + intro paragraph
- What's included (checklist format)
- How it works (3-step process)
- Pricing note (range, not exact — link to quote form)
- FAQ (3 questions + answers)
- CTA

**SECTION 3: FAQ SECTION** (for main page)
Generate 12 Q&As covering:
1. How do you price a cleaning?
2. Are your cleaners employees or contractors?
3. What cleaning products do you use?
4. Are you bonded and insured?
5. Do I need to be home during the cleaning?
6. How do I prepare for my first cleaning?
7. What if something gets broken?
8. Do you bring your own supplies and equipment?
9. How often should I schedule cleaning?
10. Do you offer move-out cleaning?
11. Can I request the same cleaner every time?
12. What areas do you serve?

**SECTION 4: JSON-LD SCHEMA**
Generate complete LocalBusiness + CleaningService schema:
- @context, @type: ["LocalBusiness", "HomeAndConstructionBusiness"]
- name, url, telephone, address (PostalAddress)
- geo (latitude/longitude for city center)
- openingHoursSpecification (Mon–Sat 8AM–6PM typical)
- priceRange (use "$" to "$$$")
- aggregateRating (from input data)
- hasOfferCatalog with 4 service types
- areaServed (list neighborhoods/zips)
- sameAs (placeholder for Google Maps, Yelp, Facebook URLs)

Output the JSON-LD in a complete <script type="application/ld+json"> block.
```

---

## Example Input

```
Business: Desert Sparkle Cleaning | Henderson, NV
Service area: Henderson (89002, 89014, 89015, 89052, 89074), Green Valley Ranch, Anthem, Whitney Ranch, Seven Hills, Inspirada
Services: residential maid, deep cleaning, move-in/move-out, Airbnb/VRBO turnover, small office cleaning
Products: Mrs. Meyer's (EPA Safer Choice), Seventh Generation (EPA Safer Choice), Method (EPA Safer Choice), microfiber systems, HEPA vacuums
Staff: W-2 employees (6 full-time)
Insurance: $1M GL (Travelers #NV-GL-2024-44821), $10K bonding (Hartford), workers' comp (Nevada)
Certifications: ARCSI member, BBB Accredited (A+ rating), EPA Safer Choice certified products
Pricing: $130–$180 standard 2BR/2BA | $220–$300 deep clean | $95–$145 Airbnb turnover
Booking: online at desertsparkle.com/book | phone (702) 555-0183
Radius: 20 miles from Henderson, NV 89002
Years: 8 years (founded 2018)
Reviews: 4.9★ 312 Google reviews
```
