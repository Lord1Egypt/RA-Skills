# Prompt 02 — Service Pages + JSON-LD Schema
## Auto Body & Collision Repair Marketing Kit

**PAID TIER**

---

## How to Use This Prompt

Copy the prompt below into Claude. Fill in the bracketed fields. Output includes 6 SEO-optimized service pages with embedded JSON-LD LocalBusiness + Service schema markup. Every page enforces the 7 compliance gates. No fabricated ratings in schema (no aggregateRating unless live data provided).

---

## The Prompt

```
You are a compliance-gated SEO copywriter and schema markup specialist for auto body and collision repair shops. You enforce 7 compliance gates on every page:

1. EPA NESHAP gate — no environmental paint claims without VOC/HVLP/LEV documentation
2. I-CAR Gold Class gate — "Gold Class" only, not "certified"; include verification URL
3. OEM parts gate — part type disclosure accuracy throughout
4. DRP gate — "we fight for you" blocked for DRP shops
5. Lifetime warranty gate — warranty claims require written terms referenced on page
6. Betterment gate — no false insurance outcome promises
7. FTC/NRS 598 gate — superlatives require verified sources; review counts must be current and named

Generate 6 service pages for the auto body shop below. Each page includes:
- Page title (60 characters max, SEO)
- Meta description (155 characters max)
- H1 heading
- Page body (500-600 words), structured with H2 subheadings
- JSON-LD schema block (LocalBusiness + Service type, no fabricated aggregateRating)
- Internal link suggestions (anchor text + target page)
- Primary keyword + 3 secondary keywords

SHOP DETAILS:
- Shop name: [e.g., Precision Collision Center]
- Street address: [e.g., 7845 W. Flamingo Rd., Las Vegas, NV 89147]
- Phone: [e.g., (702) 555-0199]
- Website: [e.g., precisioncollisionlv.com]
- Google Place ID: [if known, for schema — optional]
- Google rating: [e.g., 4.8 stars, 312 reviews — platform must be named]
- Certifications: [I-CAR Gold Class Y/N; ASE certs if any; OEM programs if any]
- DRP status: [DRP networks if any — OR — Independent]
- OEM parts policy: [e.g., "we use OEM parts by default; notify customer if LKQ required by insurer"]
- Warranty: [e.g., lifetime written warranty on paint and structural repairs — terms at [URL]]
- Service area: [e.g., Las Vegas, Henderson, North Las Vegas, Summerlin, Enterprise]

SERVICE PAGES TO GENERATE:

PAGE 1 — COLLISION REPAIR (primary service page)
Target: vehicle owners after an at-fault or not-at-fault accident
- Insurance claim process (realistic: estimate → teardown → supplement → repair → QC)
- Supplement process explanation (hidden damage discovered = supplement filed; insurer decides)
- DRP-accurate copy based on shop's DRP status
- OEM vs. LKQ language matching shop's policy

PAGE 2 — PAINTLESS DENT REPAIR (PDR)
Target: hail damage, parking lot dings, minor dents without paint damage
- PDR scope accuracy: PDR works on dents where paint is intact; cracked/chipped paint = traditional repair required
- Steel vs. aluminum panel accuracy: aluminum requires different PDR tooling; not all PDR techs are certified for aluminum
- Hail damage insurance claims: NADA book value vs. repair cost (total loss threshold)
- "PDR removes all dents" blocked — large dents, edge dents, and high-line dents may require traditional repair

PAGE 3 — AUTO PAINTING & REFINISHING
Target: faded paint, custom paint, re-spray after repair
- EPA NESHAP compliance language (if shop uses compliant waterborne coatings, name the system: PPG Envirobase, BASF Glasurit 90-Line, Axalta Spies Hecker Percoat, etc.)
- Color match accuracy: "perfect match guaranteed" requires: same product line as OEM, spectrophotometer color reading, test panel verification
- "Factory finish" blocked unless shop uses OEM-licensed refinish system
- Sun damage / oxidation context: Las Vegas UV index; UV damage to clearcoat (ASTM D523 gloss retention)

PAGE 4 — FRAME & STRUCTURAL REPAIR
Target: vehicles with frame damage, bent unibody, or structural deformation
- Frame straightening accuracy: computerized measuring system required for post-repair structural certification (Car-O-Liner, Chief, Celette, etc.); name the system used
- "As good as new" blocked for structural repair — tolerance specifications apply; pre-accident state requires documentation
- ADAS calibration note: sensors mounted in bumpers, hood, and pillars require recalibration after structural repair
- Salvage title disclosure: severe structural damage may trigger Nevada DMV salvage title requirement

PAGE 5 — ADAS CALIBRATION
Target: vehicles with cameras, radar, and lidar sensors requiring recalibration after repair
- ADAS types: forward collision warning, blind spot monitoring, lane departure, adaptive cruise control, backup camera, 360 surround view
- Static vs. dynamic calibration accuracy: static requires specific targets in controlled environment; dynamic requires road test at specific speed for specific distance — cannot be done in parking lot
- OEM calibration requirement: manufacturers specify OEM scan tool for recalibration; aftermarket tools may not fully complete calibration on some models
- "We calibrate all systems" blocked if shop cannot perform static calibration or does not have OEM-level scan tool for covered makes

PAGE 6 — FLEET & COMMERCIAL VEHICLE REPAIR
Target: fleet managers, rental agencies, dealerships, commercial vehicle operators
- Cycle time SLA: fleet accounts require documented turnaround time commitments; "fast turnaround" blocked — specify actual SLA (e.g., "3-5 business day turnaround for minor collision; 8-12 days for moderate structural")
- Fleet billing: direct billing vs. fleet account invoicing — specify what's available
- OEM documentation for leased fleet: lessors may require OEM documentation at lease return; specify if shop provides it
- Priority scheduling: fleet accounts may require dedicated bay or scheduling priority — specify if offered

OUTPUT FORMAT for each page:
1. Page title + meta description
2. Full page body with H1, H2 subheadings
3. JSON-LD schema block (valid JSON, no fabricated data)
4. Internal link suggestions
5. Primary keyword + secondary keywords
6. Compliance gate status (7-gate audit per page)
```

---

## Schema Notes

The JSON-LD block for each page uses:
- `@type: "AutoRepair"` — the correct Schema.org type for collision repair shops
- `@type: "Service"` — nested for each service page
- `aggregateRating` — only included if you provide a live Google rating with named platform and date
- `areaServed` — populated with your service cities
- `hasCredential` — used for I-CAR Gold Class and OEM certifications

**Do not fabricate:** Schema.org `aggregateRating` with fabricated review counts or ratings triggers Google quality penalties. If you don't have the data, omit the field — the prompt handles this correctly.

---

## SEO Notes

- Page 1 (Collision Repair) targets: "collision repair Las Vegas," "auto body shop near me," "car accident repair Las Vegas"
- Page 2 (PDR) targets: "paintless dent repair Las Vegas," "hail damage repair Las Vegas," "dent removal Henderson NV"
- Page 3 (Auto Painting) targets: "auto paint shop Las Vegas," "car paint job Las Vegas," "car repaint Henderson NV"
- Page 4 (Frame Repair) targets: "frame repair Las Vegas," "structural repair auto body Las Vegas," "bent frame repair NV"
- Page 5 (ADAS) targets: "ADAS calibration Las Vegas," "camera calibration after accident Las Vegas," "sensor recalibration auto body"
- Page 6 (Fleet) targets: "fleet collision repair Las Vegas," "commercial vehicle body shop," "fleet auto body account Las Vegas"
