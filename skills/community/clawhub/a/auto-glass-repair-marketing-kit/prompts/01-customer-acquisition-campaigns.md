# Prompt 1 (FREE) — Customer Acquisition Campaign Generator

Generate a complete multi-channel customer acquisition campaign for an auto glass repair and replacement shop. All outputs enforce AGSC installation safety standards, ADAS recalibration disclosure, Nevada deductible waiver law (NRS 686A.2825), OEM glass accuracy, and FTC 2023 endorsement compliance.

---

## Input Fields

```
Shop name:
City/State:
NSCB Contractor License Number (C-8 Glass & Glazing):
Services offered [check all that apply]:
  [ ] Windshield replacement
  [ ] Chip/crack repair
  [ ] Side/rear glass replacement
  [ ] ADAS recalibration — Static (targets, controlled environment)
  [ ] ADAS recalibration — Dynamic (drive cycle with scan tool)
  [ ] Mobile service
  [ ] Fleet accounts
  [ ] RV/commercial vehicle glass

AGSC Certified technicians on staff? [Yes / No]
If Yes — adhesive brands/systems used (e.g., Sika Tack Ultra, Dow Betaseal, Equalizer):

ADAS recalibration capability:
  [ ] Yes — static
  [ ] Yes — dynamic
  [ ] Yes — both
  [ ] No — we refer to dealer/ADAS specialist
  [ ] No — we do not offer or disclose

Glass sourcing:
  [ ] True OEM (from vehicle manufacturer supply chain — specify brand: Pilkington / AGC / Fuyao OEM / Saint-Gobain Sekurit / Other)
  [ ] OEM-equivalent aftermarket, NSF-certified (specify brand: Pilkington NSF / Lynx / PGW / Other)
  [ ] Standard aftermarket (non-OEM spec)

Insurance billing? [Yes / No]
If Yes — networks/insurers (e.g., Safelite Network, Lynx Services, USAA Glass, State Farm, Allstate, Progressive):

Target customer [check all]:
  [ ] Individual residential (insurance claim)
  [ ] Individual residential (out-of-pocket)
  [ ] Commercial fleet
  [ ] Auto dealerships (glass referral)
  [ ] Insurance adjusters / TPAs

Seasonal focus or current promotion (optional):
Contact info (phone, website):
```

---

## Compliance Gate Check

Before generating any output, apply the following gates:

**Gate 1 — AGSC/Safe Drive-Away:**
- If AGSC Certified = No → REMOVE all "safe to drive in X minutes," "OEM installation," "certified installation" language. Add: "Work performed by experienced glass technicians — ask about adhesive cure time before driving."
- If AGSC Certified = Yes + adhesive brand provided → use adhesive-specific MDAT in all relevant copy (Sika Tack Ultra: 30-60 min; Dow Betaseal: 60 min minimum; always add "— verify with your technician for your vehicle and conditions")

**Gate 2 — ADAS:**
- If ADAS capability = No or not offered → ADD to every ad and campaign: "ADAS recalibration required for vehicles with cameras mounted to the windshield. We can refer you to a certified recalibration specialist." REMOVE "we handle everything" and "complete service."
- If ADAS capability = Yes → include ADAS as a featured service differentiator. Static vs dynamic explained honestly in FAQ.

**Gate 3 — Deductible Waiver (NRS 686A.2825 — HARD BLOCK):**
- REMOVE: "no out-of-pocket," "we pay your deductible," "deductible-free," "insurance covers everything," "free windshield," any deductible absorption language.
- REPLACE WITH: "Most comprehensive auto policies include glass coverage — check your policy before you call." + "We bill your insurance directly and handle the paperwork."

**Gate 4 — License Number:**
- Insert NSCB license number in Google Ads sitelink extension and email footer.
- If license number not provided → insert [NSCB LICENSE #] placeholder with note: "Nevada NRS 624 requires contractor license disclosure on advertising materials."

**Gate 5 — OEM Glass:**
- If glass sourcing = True OEM → "OEM glass" permitted.
- If glass sourcing = OEM-equivalent aftermarket → use "OEM-equivalent," "NSF-certified aftermarket glass," or "[Brand] certified replacement glass" — never "OEM glass."
- If glass sourcing = Standard aftermarket → "quality aftermarket glass" — never "OEM" or "OEM-equivalent" unless NSF-certified.

**Gate 6 — Insurance Claims:**
- Never: "Your insurance will cover this" without policy verification.
- Always: "Coverage depends on your specific policy — we can help you check."

**Gate 7 — FTC Safety Claims:**
- No "100% guaranteed safe" without AGSC certification and ADAS verification on file.
- No "best in [city]" without documented ranking source.

---

## Output

### 1. Google Ads RSA Campaign

**Campaign: Windshield Replacement**

Ad Group 1 — Windshield Replacement
Headline 1 (30 chars): [Shop Name] — Henderson NV
Headline 2 (30 chars): Windshield Replaced Today
Headline 3 (30 chars): Insurance Billing Direct
Headline 4 (30 chars): [Apply AGSC claim if certified]
Headline 5 (30 chars): ADAS Recalibration Available [if applicable]
Description 1 (90 chars): [Shop Name] replaces windshields in [City]. AGSC-certified. We bill your insurance directly.
Description 2 (90 chars): Most auto glass policies cover replacement. Call us — we'll check your coverage and schedule same-day.
Sitelinks: Book Online | Insurance Claims | ADAS Recalibration | Fleet Accounts | [License #]

[Gate note applied: no safe drive-away time unless AGSC-certified + adhesive verified; no deductible waiver language]

Ad Group 2 — Chip & Crack Repair
[Generate RSA with chip repair-specific headlines. Include "Fix before it spreads" urgency without FTC-prohibited safety scare tactics]

Ad Group 3 — ADAS Recalibration [include only if shop offers this]
[Generate RSA with ADAS recalibration-specific headlines. Focus on safety accuracy, not fear. Include make/model examples]

Negative Keywords: DIY, how to fix windshield, free windshield, cheap windshield, windshield cost, tutorial

---

### 2. Facebook/Instagram Campaign

**Ad Brief 1 — Insurance Claim Angle**
Format: Single image + copy
Visual direction: Clean windshield vs. cracked windshield split image (FTC compliant: "typical results" caption)
Headline: "Cracked Windshield? Your Insurance Probably Covers It."
Body (125 chars max): "Most comprehensive auto policies include glass coverage. [Shop Name] bills your insurance directly — no paperwork hassle."
CTA: Get a Free Quote
Compliance note: NO deductible waiver language. No "no out-of-pocket." Coverage claim must include: "Coverage depends on your specific policy."

**Ad Brief 2 — ADAS Safety Angle** [include if shop offers ADAS recalibration]
Format: Short video (15s) or carousel
Headline: "New Car? Your Windshield Replacement Isn't Complete Without This."
Body: "80% of 2020+ vehicles have cameras that need recalibration after windshield replacement. [Shop Name] offers certified ADAS recalibration."
CTA: Learn More → [ADAS service page]
Compliance note: "certified" only if AGSC + documented calibration equipment. Otherwise: "professional" or "experienced."

---

### 3. Insurance Claim Email Sequence (3 Emails)

**Email 1 — Day 1: Awareness**
Subject: "[Shop Name] — Windshield Replacement in [City]: What to Know First"
Body:
- Hi [First Name],
- Dealing with a cracked or chipped windshield is frustrating. Here's what to know before you call anyone:
  1. Check your policy first — most comprehensive auto insurance covers windshield replacement or chip repair, often with no deductible for chip repairs.
  2. ADAS matters — if your vehicle is a 2018 or newer model, there's a good chance a camera is mounted to your windshield. That camera needs recalibration after replacement. Ask any shop you consider whether they offer this — and get it in writing.
  3. OEM vs. aftermarket glass — both can be safe and FMVSS-compliant. Ask what you're getting so you can make an informed choice.
- [Shop Name] offers [services]. We bill your insurance directly and handle the paperwork. Questions? Call [phone].
- [NSCB License #: C-8 XXXXXXX]

**Email 2 — Day 3: Urgency**
Subject: "Small chip → cracked windshield: here's when it's too late to repair"
Body:
- A chip smaller than a quarter can usually be repaired in under 30 minutes. A crack longer than 6 inches typically means full replacement — and most insurance policies cover repair at no deductible.
- Don't wait: temperature changes, road vibration, and car wash pressure all turn chips into cracks.
- [Shop Name] — [phone] — we'll assess your chip for free and tell you honestly whether repair or replacement is the right call.
- [Unsubscribe] | [NSCB License #]

**Email 3 — Day 7: Close**
Subject: "Still dealing with that cracked windshield?"
Body:
- We understand — scheduling feels like one more thing. Here's how to make it easy:
- [3 booking options: call, online form, text-to-schedule if available]
- Coverage reminder: if you have comprehensive insurance, call your insurer or check your app — many policies cover glass with zero or minimal deductible. We handle the billing.
- [Shop Name] | [Phone] | [Address] | [NSCB License #]
- [Unsubscribe]

---

### 4. SMS Follow-Up (TCPA-Compliant)

Under 160 chars. Opt-out required.

"[Shop Name]: Still need that windshield fixed? We bill insurance directly. Book in 60 sec: [link] | Reply STOP to opt out"

[Gate note: no deductible waiver. No "free." No "no out-of-pocket."]

---

### 5. Google Business Profile Post

750 chars max. Seasonal/promotional angle.

Example (summer):
"Summer heat + a cracked windshield = faster spreading damage. [Shop Name] offers same-day windshield replacement in [City]. We work with all major insurance carriers and bill directly — no paperwork on your end. ADAS recalibration available for camera-equipped vehicles. AGSC-certified installation. [Phone] | [Link] | NSCB #[License]"

[Rotate monthly: chip repair awareness, ADAS safety, fleet service, insurance claim guide, new glass brand partnership, winter windshield care]
