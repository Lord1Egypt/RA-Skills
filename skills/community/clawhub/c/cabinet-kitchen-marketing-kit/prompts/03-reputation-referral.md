# Prompt 3 — Reputation Management & Referral System

## Cabinet Refacing & Kitchen Cabinetry | FTC 2023-Compliant Review + Referral Outreach

---

## SYSTEM INSTRUCTIONS FOR CLAUDE

Generate reputation management templates and B2B referral letters for a cabinet and kitchen cabinetry contractor. All outputs must comply with FTC 2023 Endorsement Guides (16 CFR Part 255) and applicable consumer protection standards.

**HARD BLOCKS:**
- Review requests that offer incentives (discounts, gifts, cash, free services) in exchange for reviews — FTC 2023 §255.5 requires disclosure; incentivized reviews without disclosure = deceptive practice
- Review-gating (only sending review requests to satisfied customers after screening) — technically permissible but must not filter to prevent negative reviews from being posted
- Fake review generation — never generate content designed to be posted as a customer review by anyone other than the actual customer
- "Lifetime guarantee" claims in referral materials without brand + written warranty terms
- "Solid wood" or eco-friendly claims without supporting documentation (same moats as other prompts)

---

## USER INPUTS

```
CONTRACTOR_NAME: [Business name]
NV_LICENSE: [NSCB # and classification]
EPA_RRP_FIRM: [EPA RRP Certified Firm #, or "N/A"]
KCMA_STATUS: [Certification status]
REVIEW_PLATFORM: [Primary: Google | Secondary: Houzz or Angi or BBB]
REVIEW_LINK_GOOGLE: [Direct Google review link]
REVIEW_LINK_2: [Secondary platform link]
OWNER_NAME: [First name — for email signatures]
REFERRAL_FEE: [Yes/No — if yes, amount and FTC disclosure language required]
SERVICE_AREA: [Cities served]
PHONE: [Business phone]
EMAIL: [Business email]
```

---

## OUTPUT 1 — 20 FTC 2023-Compliant Review Requests

*No incentives. No gating. Honest ask only.*

### 8 Email Review Requests

**Email R-1 (Project completion — same day):**
Subject: "[Customer first name], your [project type] is complete — one quick favor?"
Body: Thank you for choosing [CONTRACTOR_NAME]. Your [cabinet refacing / kitchen remodel] is complete — we'd love to hear how it went. [REVIEW_LINK_GOOGLE]. [Unsubscribe link]
Tone: Direct, warm, no pressure.

**Email R-2 (Day 3 follow-up):**
Subject: "Quick check-in on your new [cabinets / kitchen]"
Body: How are you enjoying the new [cabinets]? If everything looks great, a Google review helps other Henderson homeowners find us. [REVIEW_LINK_GOOGLE]

**Email R-3 (Week 2 — experience focus):**
Subject: "Two weeks in — how are the cabinets holding up?"
Body: Desert heat and humidity can be tough on materials. Checking in to make sure your [SOFT_CLOSE_BRAND] hardware and finish are performing as expected. If you're happy with the result, a quick review means a lot. [REVIEW_LINK_GOOGLE]

**Email R-4 (Month 1 — durability check):**
Subject: "30 days later — still love your kitchen?"
Body: A month out from your [project type] — we hope you're still loving it. If everything is holding up as promised (KCMA-quality construction, [SOFT_CLOSE_BRAND] hardware), your review helps us show other families what to expect. [REVIEW_LINK_GOOGLE]

**Email R-5 (Referral ask + review):**
Subject: "Know someone else who needs a kitchen upgrade?"
Body: If you've enjoyed working with [CONTRACTOR_NAME], two things would help us keep growing: a Google review [REVIEW_LINK_GOOGLE], and a referral to a neighbor or friend. [If REFERRAL_FEE: "We offer [REFERRAL_FEE] for every referred customer who completes a project — disclosed as a referral incentive per FTC guidelines."]

**Emails R-6, R-7, R-8:** Generate 3 additional variants with different subject lines, emotional angles (pride in home, investment value, neighbor trust), and slightly different CTAs. All must include unsubscribe option and no incentive promises.

---

### 6 SMS Review Requests (160 chars max each)

*TCPA compliance: only send to customers who opted in to SMS communication.*

**SMS R-1:** "Hi [Name], thanks for choosing [CONTRACTOR_NAME]! If you love your new cabinets, please leave us a Google review: [SHORT_LINK]. Reply STOP to opt out."

**SMS R-2:** "Your [project type] is done! Mind sharing your experience? [REVIEW_LINK] Means a lot — [Owner first name] at [CONTRACTOR_NAME]. STOP to opt out."

**SMS R-3 (Day 3):** "[Name], 3 days in — how's everything looking? Quick review here: [SHORT_LINK]. STOP to opt out."

**SMS R-4 (Week 2):** "Hi [Name]! Week 2 with your new [cabinets/kitchen] — still love it? [SHORT_LINK] for a quick review. STOP to opt out."

**SMS R-5 (Month 1):** "[Name], your [project] is one month old! If it's holding up great, a 2-minute review helps others find us: [SHORT_LINK]. STOP to opt out."

**SMS R-6 (Referral):** "Hi [Name]! Know anyone needing cabinet work? Send them our way. [If REFERRAL_FEE: 'We'll send you [amount] — referral incentive disclosed.'] [PHONE]"

---

### 3 Printed Card Review Requests

**Card R-1 (Project completion card — left with client):**
Front: "Thank you for trusting [CONTRACTOR_NAME] with your kitchen."
Back: "Your honest review helps Henderson families make confident decisions. [QR code to REVIEW_LINK_GOOGLE]. [CONTRACTOR_NAME] | [PHONE] | NSCB [NV_LICENSE]"
Compliance: "honest review" language satisfies FTC — no instruction to leave only positive review.

**Card R-2 (Refrigerator magnet — leave-behind):**
"[CONTRACTOR_NAME] | NSCB [NV_LICENSE] | EPA RRP [EPA_RRP_FIRM if applicable] | [PHONE]
Enjoyed your kitchen? Review us: [QR]"

**Card R-3 (Referral + review combo card):**
"Love your new cabinets? Share the experience: [QR for Google Review]
Know someone who needs a kitchen upgrade? Call [PHONE] and mention your name."

---

### 3 Verbal Review Request Scripts

**Verbal V-1 (At project completion walkthrough):**
"[Customer name], before I head out — everything look good? [Pause for response.] If you're happy with how the [cabinets/kitchen] turned out, an honest Google review means the world to us. I'll send you the link by text. Any questions in the next 30 days, call me directly."

**Verbal V-2 (Follow-up call — Day 3):**
"Hi [Customer name], just checking in — how are the cabinets holding up? Everything working as expected? [Pause.] I'm glad to hear it. If you've got 2 minutes, a Google review from a real customer helps other Henderson families know what to expect from us. I can text you the link right now if you'd like."

**Verbal V-3 (Month 1 call):**
"Hi [Customer name], [Owner name] from [CONTRACTOR_NAME]. Just hitting my 30-day check-in — how's everything holding up in the kitchen? Any soft-close issues? Finish concerns? [Handle any issues first.] If everything is solid, I'd be grateful for a review — honest one, whatever reflects your real experience. [REVIEW_LINK]"

---

## OUTPUT 2 — 15 Google Business Profile Response Templates

*Respond to every review — positive and negative. Response tone: professional, specific, non-defensive.*

**Response to 5-star reviews (3 variants):**
- R-1 (Cabinet refacing focus): "Thank you [Name]! Cabinet refacing is such a satisfying project — transforming a kitchen without the cost and disruption of full replacement. We're glad the [KCMA_STATUS / Blum hardware] quality came through. NSCB [NV_LICENSE] — [CONTRACTOR_NAME]"
- R-2 (Custom cabinet focus): "So happy to hear it, [Name]! Custom [dovetail joint / plywood box] construction is the right call for a kitchen you'll use every day. Glad the [SOFT_CLOSE_BRAND] hardware is performing. Thank you for trusting [CONTRACTOR_NAME]."
- R-3 (Full remodel focus): "Thank you, [Name]! A full kitchen remodel is a big commitment — we don't take that trust lightly. Glad the [permit process / EPA RRP steps / design phase] went smoothly. Enjoy the new space."

**Response to critical/negative reviews (12 specific scenarios):**

**Neg-1 — Soft-close failure complaint:**
"[Name], I'm sorry to hear a hinge/drawer slide is not performing as expected. [SOFT_CLOSE_BRAND] carries a [WARRANTY_TERM] warranty — please call [PHONE] so we can schedule a warranty service visit. We stand behind the hardware we install."
Compliance: Confirm warranty brand and term before responding; do not promise warranty service beyond actual warranty scope.

**Neg-2 — Door warping complaint:**
"[Name], I'm sorry about the door issue. In the Las Vegas-Henderson climate, wood movement is a real factor — low desert humidity can cause wood doors to warp if acclimation wasn't adequate. Please call [PHONE] — we'll assess the door and determine whether this is a material, installation, or acclimation issue and make it right."

**Neg-3 — Finish peeling complaint:**
"[Name], peeling finish is not acceptable work and we want to resolve it. There are a few causes — surface prep, product adhesion to original finish type, or humidity exposure — and we need to assess in person. Please call [PHONE]. We'll come out and make it right."

**Neg-4 — Lead paint concern (pre-1978 home):**
"[Name], EPA RRP compliance is our highest priority in pre-1978 homes. EPA RRP Certified Firm [EPA_RRP_FIRM if applicable] — our certified renovators follow all 40 CFR Part 745 lead-safe work practices. Please call [PHONE] directly so we can address your specific concern and provide our certification documentation."
*If EPA_RRP_FIRM is N/A: Do not use this template; flag to owner for individual response.*

**Neg-5 — Permit dispute:**
"[Name], permits are required for [scope type] under Clark County / City of Henderson code, and we take permit compliance seriously. Please call [PHONE] — I want to walk through what was permitted on your project and resolve any concern directly."

**Neg-6 — License verification request:**
"[Name], happy to verify: NSCB [NV_LICENSE] — you can confirm our license is active and in good standing at the Nevada State Contractors Board website (nscb.nv.gov). Call [PHONE] if you have additional questions."

**Neg-7 — Warranty denial complaint:**
"[Name], I'm sorry the warranty claim experience was frustrating. Please call [PHONE] — I want to review the specifics of the warranty coverage and see what we can do. If this is within the [SOFT_CLOSE_WARRANTY / finish warranty] terms, we'll honor it."

**Neg-8 — Color/finish mismatch:**
"[Name], a color or finish mismatch is a serious concern — one we want to address in person. Please call [PHONE] so we can see the issue directly. We'll assess whether this is within the expected finish variation range or requires a corrective coat."

**Neg-9 — Material/construction dispute ("these aren't solid wood"):**
"[Name], we appreciate the feedback and understand the concern. Our [project type] uses [box material / door species / panel construction] as specified in the project agreement. We're happy to review the project documentation with you. Please call [PHONE]."
Compliance: Never deny or deflect without having the project specs documentation ready.

**Neg-10 — Timeline overrun complaint:**
"[Name], we regret the project took longer than expected — timeline overruns are frustrating and we understand why. Please call [PHONE] to discuss. We value your business and want to make sure you're satisfied with the final result."

**Neg-11 — HOA approval conflict:**
"[Name], HOA approval requirements vary by community and can affect project scope or timeline. If the HOA raised concerns mid-project, we want to work through that with you. Please call [PHONE]."

**Neg-12 — Suspected fake/competitor review:**
"We don't recognize this project in our records. If there's been a mix-up, please call [PHONE] — we're happy to verify. If this review does not reflect an actual project, we've flagged it for Google review. NSCB [NV_LICENSE]."

---

## OUTPUT 3 — 6 B2B Referral Letters

*Professional tone. No commission promises unless compliant with NV contractor referral regulations.*

**Letter B-1 — Custom Home Builder:**
Target: Residential custom home builders (B-2 GCs) in Henderson/Las Vegas who need subcontractor cabinet work.
Angle: KCMA quality, NV B-2 license, CARB Phase 2 compliance, EPA RRP for pre-1978 rehab projects, clean sub relationship (no callbacks, no warranty issues).

**Letter B-2 — Real Estate Agent:**
Target: Real estate agents listing homes that need pre-sale kitchen refresh.
Angle: Cabinet refacing ROI (kitchen updates increase sale price faster than any other room per NAR data), fast turnaround (5-7 days for refacing vs. 3-6 weeks full remodel), licensed and insured.

**Letter B-3 — Interior Designer:**
Target: Interior designers specifying cabinets for clients.
Angle: KCMA specs on request, custom finish matching capability, GREENGUARD Gold finish options (healthy home clients), NV license.

**Letter B-4 — Property Manager:**
Target: Property management companies with rental unit kitchen upgrades.
Angle: Volume pricing for multi-unit refacing, durable commercial-friendly materials (thermofoil or laminate for rental environments), fast turnaround to minimize vacancy, licensed and bonded.

**Letter B-5 — HOA Management Company:**
Target: HOA management firms overseeing community common area kitchen upgrades (clubhouses, fitness centers, community kitchens).
Angle: Commercial-grade materials, NSF/ANSI 2 compliance if food service applies, permit-managed, B-2 license for structural scope, insurance certificate available on request.

**Letter B-6 — Kitchen Appliance Showroom:**
Target: Appliance showrooms (Sub-Zero, Wolf, Bosch dealers) that encounter clients needing cabinet work to accommodate new appliances.
Angle: Cabinet modification for appliance integration (new range width, refrigerator panel program, dishwasher panel), coordination with appliance delivery timeline, NV license.

*If REFERRAL_FEE is Yes: Include FTC-compliant referral fee disclosure in each letter: "We offer [REFERRAL_FEE] for referred customers who complete a project — this is disclosed to the referred customer as a referral incentive in accordance with FTC guidelines."*
