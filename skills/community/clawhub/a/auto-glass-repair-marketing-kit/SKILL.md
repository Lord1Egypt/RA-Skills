# Skill #238 — Auto Glass Repair & Replacement Marketing Kit

## Overview
Generate compliance-accurate marketing content for auto glass repair and replacement shops. Every output enforces AGSC/AGRSS installation safety standards, ADAS recalibration disclosure requirements, Nevada's deductible waiver insurance fraud statute, OEM vs. aftermarket glass truth-in-advertising rules, and FTC 2023 endorsement guidelines. No general AI tool knows any of these gates exist.

## Pricing
- Free: Prompt 1 (customer acquisition campaigns)
- Full Kit: $47 one-time
- DFY: $127/campaign package (Max runs it for your shop)

## Compliance Moats (7)

### Moat 1 [ANCHOR] — AGSC/AGRSS Certification & Safe Drive-Away Gate
Auto Glass Safety Council Standard 150 (formerly AGRSS) governs adhesive type (urethane-based, FMVSS 212/208 compatible), primer application, surface prep, and minimum safe drive-away time (MDAT). MDAT is adhesive-specific — Sika Tack Ultra ranges from 30-60 min; Dow Betaseal 1 hour minimum; some OEM restoration adhesives require 8 hours. Marketing claims like "out in 30 minutes" or "safe to drive immediately" without AGSC-certified technician verifying MDAT for the specific adhesive used = implied safety misrepresentation under FTC Act Section 5 and Nevada NRS 598. "OEM installation standards" requires AGSC certification. This skill enforces AGSC certification disclosure on every installation claim.

**Gate:** If AGSC certification not held → remove all "safe drive-away," "OEM installation," and "certified installation" claims. Replace with honest capability framing only.

### Moat 2 — ADAS Recalibration Safety & Disclosure Gate
Any vehicle with a camera or sensor mounted on or near the windshield (forward collision warning, lane departure, adaptive cruise, automatic emergency braking) requires post-installation recalibration. Affected systems include: Tesla Autopilot, Subaru EyeSight, Toyota Pre-Collision System, Honda Sensing, Mazda 360° View, Ford Co-Pilot360, GM Super Cruise, Volvo IntelliSafe, Hyundai SmartSense. Two types: **static recalibration** (targets mounted at fixed distances in controlled environment — Autel ADAS Pro, Launch X-431 ADAS Pro+, Bosch DAS 3000) and **dynamic recalibration** (drive cycle under specific speed/road conditions with scan tool connected). Shops that advertise "complete windshield service" or "we handle everything" without ADAS recalibration disclosure when the vehicle has ADAS = deceptive trade practice + safety liability. NHTSA has flagged improperly calibrated ADAS as crash causation. This is a life-safety disclosure requirement, not a marketing preference.

**Gate:** If shop does not perform ADAS recalibration → mandatory disclaimer added to all ads: "ADAS recalibration required for camera-equipped vehicles. Ask us about certified recalibration or we can refer you to a dealer." No "complete service" or "we handle everything" language permitted.

### Moat 3 — Nevada Insurance Deductible Waiver Fraud Gate (NRS 686A.2825)
Nevada Revised Statutes 686A.2825 explicitly prohibits auto glass shops from waiving, absorbing, rebating, or otherwise eliminating an insured's deductible as an inducement for business. Violations = insurance fraud exposure under NRS 686A.291, potential criminal referral to Nevada DOI. Active enforcement in Clark County — DOI has issued cease-and-desist letters and referred shops for criminal prosecution. Common violations: "No out-of-pocket," "We pay your deductible," "Deductible-free windshield," "Insurance covers 100%," "Come in, pay nothing." This skill generates zero deductible-waiver language. If shop is accustomed to using this as a marketing hook, the skill explains the legal exposure and provides compliant alternative messaging.

**Gate:** HARD BLOCK — no deductible waiver language in any output regardless of input. Replace with: "Most comprehensive insurance policies cover windshield replacement — check your coverage before you come in" + "We bill your insurance directly."

### Moat 4 — Nevada Contractor Licensing & NRS 598 Deceptive Trade Gate
Auto glass installation is a licensed trade in Nevada. Nevada State Contractors Board (NSCB) License Class C-8 (Glass and Glazing) required for installation work. Operating without a license or advertising without disclosing license status = NRS 624 violation. Nevada NRS 598.0923 prohibits representing that services conform to standards they don't meet — directly applicable to AGSC, OEM, and ADAS claims. NRS 598.0915 prohibits knowingly making false claims about insurance coverage ("your insurance will definitely cover this"). Advertising compliance required: NSCB license number must be on all print/digital advertising over certain thresholds.

**Gate:** License number required in output template. If not provided, placeholder inserted with note that NRS 624 requires disclosure on advertising materials.

### Moat 5 — OEM vs. Aftermarket Glass FMVSS 205 Truth-in-Advertising Gate
Federal Motor Vehicle Safety Standard 205 (Glazing Materials) requires auto glass meet minimum optical quality, impact resistance, and UV transmission standards — both OEM and qualifying aftermarket glass can be FMVSS 205-compliant. However: "OEM glass" specifically means glass manufactured by or for the original vehicle manufacturer (Pilkington, AGC, Fuyao OEM line, Saint-Gobain Sekurit). "OEM-equivalent" or "OEM-quality" or "meets OEM specs" is truthful for compliant aftermarket glass. Advertising "OEM glass" while installing aftermarket = federal false advertising claim under FTC Act Section 5. Insurance company billing for OEM when installing aftermarket = insurance fraud. This distinction matters: some shops use the term loosely; this skill enforces accuracy.

**Gate:** Input collects actual glass source (true OEM / OEM-equivalent aftermarket / standard aftermarket) and outputs matching truthful claim language only. Never upgrades "aftermarket" to "OEM" in copy.

### Moat 6 — Nevada Insurance Anti-Steering & Preferred Shop Gate (NRS 686A.220)
Nevada law prohibits insurers from requiring policyholders to use specific repair shops — and prohibits kickback/referral arrangements between shops and insurance adjusters. "Insurance-preferred shop" without documented preferred provider agreement = deceptive. "Your insurance company sent us" without actual referral = false authority claim. "We work with all insurance companies" is truthful and permissible. Nevada DOI Insurance Division investigates anti-steering complaints. Additionally: representing that a specific insurer will cover a claim without verifying the specific policy = NRS 598.0915 deceptive representation. This skill does not generate any language implying shop has special insurer status it doesn't have.

**Gate:** No "preferred by [insurer]," no "your insurance company recommends," no guaranteed coverage statements. Replace with: "We work with all major insurers and bill directly" + "Coverage depends on your specific policy — we can help you check."

### Moat 7 — FTC 2023 Endorsement & Safety Claims Gate
FTC's 2023 revised Endorsement Guides (16 CFR Part 255) require: (a) material connections disclosed — if shop offers discount for reviews, that's a material connection requiring disclosure; (b) typical results disclosure for any before/after or results-based claims; (c) no manufactured reviews. Auto glass specific: "guaranteed safe" or "100% safety guaranteed" without AGSC-certified installation + ADAS verification = unsubstantiated safety claim. "Best glass in Las Vegas" without objective ranking = puffery but "rated #1 by customers" without survey documentation = FTC violation. Review gating (only asking satisfied customers to review) = FTC 2023 violation.

**Gate:** No incentivized reviews without disclosure. No "100% safe" claims without certification backing. No rank claims without documentation. Review sequences ask all customers, not screened by satisfaction.

---

## Prompts

### Prompt 1 (FREE) — Customer Acquisition Campaign Generator
Generate a complete multi-channel customer acquisition campaign for an auto glass shop.

**Input:**
- Shop name, city/state, NSCB license number
- Services offered (windshield replacement, chip repair, side/rear glass, ADAS recalibration, fleet service)
- AGSC certification held? (yes/no)
- ADAS recalibration capability? (yes — static/dynamic/both; no; referral program)
- Glass sourcing (true OEM / OEM-equivalent aftermarket / standard aftermarket — specify brand if known: Pilkington, AGC, Lynx, PGW, etc.)
- Insurance billing? (yes/no, insurers worked with)
- Target customer (residential / commercial fleet / dealerships / insurance direct)
- Seasonal focus or promotion (optional)
- Contact info / website

**Output:**
- Google Ads RSA campaign (1 RSA per service line: windshield replacement, chip repair, ADAS recalibration if offered; all headlines/descriptions within 30/90 char limits; license number in sitelink extension; no deductible waiver language)
- Facebook/Instagram campaign (2 ad briefs: insurance-claim angle + ADAS safety angle; before/after with FTC typical results disclosure; no deductible waiver)
- 3-email insurance claim outreach sequence (post-incident: Day 1 awareness, Day 3 urgency, Day 7 close; all NRS 686A.2825-clean)
- SMS follow-up (under 160 chars; TCPA opt-out; no deductible waiver)
- Google Business Profile post (750 chars; seasonal/promotional; all moat-compliant)

---

### Prompt 2 — Digital Advertising Suite + GBP Optimization
Generate a complete paid + organic digital presence for an auto glass shop.

**Input:**
- All fields from Prompt 1
- Service area (list cities)
- Competitor names to differentiate from (optional)
- Budget range (optional: low/mid/high)
- Customer reviews/ratings snapshot (optional)

**Output:**
- Google Search Ads (full campaign: 6 ad groups — windshield replacement, chip repair, ADAS recalibration, fleet glass, emergency glass, insurance claim; all RSA headlines/descriptions; negative keyword list: DIY, how to, free, tutorial)
- Google Display remarketing brief (3 audience segments: viewed service page, abandoned quote form, past customer reactivation)
- Facebook/Instagram (6 ad briefs covering all service lines; Fair Housing-clean demographic targeting brief; no deductible waiver; ADAS safety awareness angle)
- Google Business Profile optimization (12 monthly post templates, seasonal; Q&A 15 scenarios — including "do you do ADAS recalibration," "do you use OEM glass," "will my insurance cover this"; hours, service area, attributes)
- Yelp profile optimization (business description, response to common question types, photo caption copy)
- Local SEO article (1,200 words: "Windshield Replacement in [City]: What to Know About ADAS Recalibration and Insurance" — targets informational search intent; all moat-compliant)

---

### Prompt 3 — Website Content + JSON-LD Schema
Generate SEO-optimized service pages with technically accurate auto glass and ADAS language.

**Input:**
- All fields from Prompt 1
- Services to build pages for
- Brands/equipment used (glass brands, calibration equipment brands)
- Team credentials/certifications

**Output (per service):**
- Service page (600-900 words; H1/H2/H3; technical accuracy on glass construction — laminated vs tempered, acoustic interlayer, UV-blocking PVB layer; ADAS section if applicable)
- ADAS Recalibration explainer page (what it is, which vehicles need it, static vs dynamic, how long it takes, why it matters — educational tone, not fear-based)
- Fleet services landing page (B2B angle: fleet account pricing, mobile service, ROI framing for fleet managers)
- FAQ page (15 Q: OEM vs aftermarket, insurance coverage, safe drive-away time, ADAS recalibration, chip repair limits, mobile service radius, warranty)
- JSON-LD schema block (LocalBusiness + AutoRepair + Offer entities; GeoCoordinates; aggregateRating if reviews provided)
- Meta title (55-60 chars) + meta description (150-160 chars) per page

**Compliance:**
- "Safe to drive immediately" → never without AGSC-certified MDAT verification
- "OEM glass" → only if true OEM sourced
- "ADAS calibrated" → only if shop has documented calibration equipment and process
- All insurance language passes NRS 686A.2825 and NRS 598.0915 gates

---

### Prompt 4 — Reputation Management & Fleet Account Development
Generate a complete review acquisition system and B2B fleet outreach program.

**Input:**
- Shop name, city/state, license number
- Review platforms (Google, Yelp, Facebook, CarGurus)
- Fleet targets (rental car agencies, delivery fleets, rideshare, government/municipal, auto dealers)
- Current fleet accounts (if any)
- Referral incentive (dollar amount — for customer-to-customer referral, not review incentive)

**Output:**
- Google/Yelp review request sequence (3 emails + SMS; FTC 2023-compliant — all customers asked, not screened; no incentive tied to review; no review gating)
- GBP review responses (20 scenarios: 5-star praise, 4-star "good but waited," 3-star insurance frustration, 2-star ADAS concern, 1-star aggressive complaint; all responses within 200 words; no admission of AGSC/safety violations in responses)
- Fleet account prospecting letters (5 variants: rental car agency, last-mile delivery fleet, rideshare platform partner, municipal/government fleet, auto dealership glass referral program; all RESPA/anti-kickback clean — no referral fee language to dealers without RESPA analysis)
- Customer referral program (dollar-off next service for referring a friend — NOT tied to reviews; FTC-clean; NRS 686A.2825-clean)
- Post-service follow-up sequence (2 emails: satisfaction check + review request; ADAS recalibration reminder if vehicle flagged at intake)
