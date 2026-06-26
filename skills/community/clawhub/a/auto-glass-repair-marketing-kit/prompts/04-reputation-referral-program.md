# Prompt 4 — Reputation Management & Fleet Account Development

Generate a complete review acquisition system, review response library, B2B fleet prospecting letters, and customer referral program. All outputs comply with FTC 2023 Endorsement Guides, NRS 686A.2825, and Yelp/Google platform terms.

---

## Input Fields

```
[All fields from Prompt 1, plus:]

Review platforms used [check all]:
  [ ] Google Business Profile
  [ ] Yelp
  [ ] Facebook
  [ ] CarGurus
  [ ] Other: ___

Fleet account targets [check all]:
  [ ] Rental car agencies (Enterprise, Hertz, National, Avis, Budget, Dollar)
  [ ] Last-mile delivery fleets (Amazon DSP, FedEx ISP, UPS contractors, USPS vehicle contractors)
  [ ] Rideshare fleet partners (Lyft, Uber fleet/rental programs)
  [ ] Municipal / government fleets (city, county, NHP, LVMPD, school district)
  [ ] Auto dealerships (glass referral + dealer service glass work)
  [ ] Construction / equipment fleets
  [ ] Other: ___

Current fleet accounts (if any — for reference tone):
Customer referral incentive amount (dollar off next service — NOT tied to reviews): $___
Owner/manager name for letters:
```

---

## Compliance Gates

**FTC 2023 Endorsement — Review Acquisition:**
- All customers receive review request — no pre-screening based on satisfaction score (= review gating = FTC violation).
- No discount, incentive, or reward in exchange for a review — on any platform.
- No "if you had a great experience, please leave us a review" framing — implies only satisfied customers should review = FTC violation.
- Correct framing: "We'd love to hear about your experience — any feedback helps us improve."

**Yelp-Specific:**
- Yelp TOS prohibits soliciting reviews from customers. Do NOT create Yelp-specific review request emails. Provide Yelp review response content only.

**RESPA / Anti-Kickback — Dealer Referral Letters:**
- If offering referral arrangement to auto dealers (dealer refers customer → shop pays dealer per referral), this may be subject to anti-kickback analysis depending on structure. 
- Safe harbor: educational referral (dealer hands customers a list of recommended vendors with no compensation) = permissible.
- Paid referral to dealers = requires legal review before implementation; skill generates educational-referral version only, with note to consult attorney for paid-referral arrangements.

**NRS 686A.2825 — All Client Letters:**
- Zero deductible waiver language in any fleet letter or customer communication.

---

## Output

### 1. Google + Facebook Review Request Sequence

**Trigger:** 24-48 hours after service completion.

**Email 1 — Review Request (All Customers)**
Subject: "Your experience at [Shop Name] — we'd love your feedback"
Body:
Hi [First Name],

Thank you for choosing [Shop Name] for your [service: windshield replacement / chip repair / ADAS recalibration]. We hope everything went smoothly.

We'd genuinely love to hear about your experience — the good and the not-so-good. Your feedback helps us get better and helps other drivers in [City] make informed decisions.

If you'd like to share: [Google Review Link] | [Facebook Review Link]

No pressure either way — we appreciate your business.

[Shop Name] | [Phone] | NSCB #[license]

[Unsubscribe]

---

**SMS Version (under 160 chars, TCPA-compliant):**
"[Shop Name]: Hope your service went well! We'd love your honest feedback: [short link] | Reply STOP to opt out"

**Compliance note applied:** No "if you're happy" qualifier — all customers receive this. No incentive for leaving review. No review platform steering based on expected sentiment.

---

**Email 2 — 7-Day Follow-Up (No Response):**
Subject: "Quick check-in from [Shop Name]"
Body:
Hi [First Name],

Just checking in to make sure everything is looking good with your [service]. If you have any questions about your warranty, drive-away instructions, or ADAS recalibration [if applicable], we're here.

And if you had a moment to share your experience online, we'd appreciate it: [Google Review Link]

Thanks for your business.

[Shop Name] | [Phone]
[Unsubscribe]

---

### 2. GBP Review Responses — 20 Scenarios

**5-Star — General Praise**
"Thank you, [Name] — glad we could take care of your [windshield/chip repair]. We'll pass your kind words along to our team. Looking forward to helping you again whenever you need us!"

**5-Star — ADAS Recalibration Mentioned**
"Thank you for trusting us with your ADAS recalibration after your windshield replacement, [Name]. Getting those systems verified correctly is important — we appreciate you taking the time to share your experience."

**5-Star — Insurance Process Praised**
"Really appreciate this, [Name]. We know insurance paperwork can be stressful — glad we could make it easier. Thanks for choosing [Shop Name]."

**5-Star — Speed/Same-Day**
"Same-day matters when you're stuck with a cracked windshield — glad we could make it happen, [Name]. Thanks for the kind review!"

**5-Star — Fleet Account**
"Thank you, [Name] — fleet accounts are some of our favorite relationships to build. Keeping your vehicles on the road is what we're here for."

**4-Star — Good but Mentioned Wait Time**
"Thank you for the honest feedback, [Name]. We're working on scheduling flow — your input helps. Glad the installation came out well, and we hope to be faster next time."

**4-Star — Good Work, Slight Concern**
"Appreciate you taking the time, [Name]. If there's anything about your experience we can improve, please call us directly at [phone] — we want to make it right."

**3-Star — Insurance Frustration (Coverage Not What Expected)**
"Hi [Name], we're sorry the coverage situation added stress to your experience. Insurance coverage is determined by your specific policy — we do our best to help check before the appointment, and we're sorry if the outcome wasn't what you expected. Please reach out at [phone] if we can help clarify anything."
[Compliance: do not admit fault for insurance coverage outcome; do not offer deductible waiver in response]

**3-Star — Wait Time**
"Thank you for the honest review, [Name]. Wait time is something we're actively working on. We appreciate your patience and your business."

**3-Star — ADAS Not Mentioned (Customer Not Sure It Was Done)**
"Hi [Name], if you have any questions about whether your vehicle's ADAS system was recalibrated, please call us at [phone] — we keep records of every job. We want to make sure you have full confidence in your installation."

**2-Star — ADAS Concern**
"Hi [Name], we take ADAS calibration concerns very seriously — it's a safety matter. Please contact us at [phone] as soon as possible and we'll have your vehicle assessed at no charge. We want to make sure everything is working correctly."

**2-Star — Glass Quality Question**
"Hi [Name], we're sorry you have concerns about the glass quality. Please reach out at [phone] — we want to understand what happened and make it right. Our installation comes with a [warranty details] warranty."

**2-Star — Billing Dispute**
"Hi [Name], we're sorry there was confusion about your bill. Please call us at [phone] or email [email] — we'll review your invoice and work through it together."

**1-Star — Safety Concern (Strong)**
"Hi [Name], your safety is our highest priority. Please contact us immediately at [phone] so we can assess your vehicle. If there's a legitimate installation issue, we will address it. We take every safety concern seriously."
[Compliance: do not admit to AGSC violation in public response; do not deny — invite to resolve privately]

**1-Star — Aggressive / Profanity-Laced**
"Hi [Name], we understand you're frustrated. Please contact us directly at [phone] so we can understand what happened and work toward a resolution. We want to make this right."

**1-Star — Competitor Sent (Clearly Wrong Shop)**
"Hi — it looks like this review may be intended for a different business. If you'd like to discuss your experience at [Shop Name], please call us at [phone]. We're happy to help."

**1-Star — Insurance Coverage Frustration**
"Hi [Name], we're sorry the insurance coverage didn't meet your expectations — coverage is determined by your specific policy terms, and we do our best to help check before any work begins. Please call us at [phone] if you have questions about your invoice or service."

**1-Star — Drive-Away Time Complaint**
"Hi [Name], safe drive-away time is something we take seriously — it's set by the adhesive manufacturer's MDAT specification, not our preference. If you have any concerns about your installation, please contact us at [phone] immediately."

**Responding to Spam/Fake Review**
"Hi — we have no record of a customer by this name or this experience at [Shop Name]. If there's been a mix-up, please reach out at [phone]. We take every review seriously."

**5-Star — AGSC Certification Mentioned**
"Thank you, [Name] — AGSC certification is something we're proud of and it matters to us that you noticed. Safe installation is the whole point. Thanks for your trust."

---

### 3. Fleet Account Prospecting Letters (5 Variants)

**Letter 1 — Rental Car Agency**
[Shop Name] | [Address] | [Phone] | NSCB #[license]

Dear [Name / Fleet Manager],

[Shop Name] provides auto glass replacement and repair for rental car fleets in the [City] area. We understand the unique demands of rental operations: vehicle downtime is lost revenue, ADAS recalibration on newer rental inventory is increasingly required, and billing documentation needs to be clean for fleet accounting.

Here's what we offer rental operations:
- Same-day and next-day scheduling for windshield replacements and chip repairs
- Mobile service for vehicles at your lot [if applicable]
- ADAS recalibration for camera-equipped vehicles — documented, on-file [if applicable]
- [OEM-equivalent/OEM] glass [per sourcing gate] — meets manufacturer specs
- Direct invoicing with fleet account setup — no per-job credit card processing
- AGSC-certified installation [if applicable] — adhesive cure time documented on every job

We've worked with [X] fleet accounts in [City] and understand the priority is getting vehicles back in service safely and quickly.

I'd welcome 15 minutes to discuss your glass needs and explore a fleet account arrangement. No obligation.

[Owner/Manager Name]
[Shop Name] | [Phone] | [Email] | NSCB License #[license]

[Compliance: no referral fee offered; no insurance deductible language; RESPA-clean educational framing]

---

**Letter 2 — Last-Mile Delivery Fleet (Amazon DSP / FedEx ISP)**

Dear [Operations Manager / Fleet Lead],

Delivery fleet vehicles take constant road debris exposure — and in the Southwest, that means windshield damage happens faster than the national average. A chip ignored for a week becomes a crack that takes a vehicle off the road for a full replacement appointment.

[Shop Name] offers a preventive windshield assessment program for delivery fleets: we can assess your fleet on a scheduled basis, catch chips before they become cracks, and perform chip repairs in 20-30 minutes on-site [if mobile service available].

For full replacements: we provide AGSC-certified installation [if applicable], ADAS recalibration for equipped vehicles [if applicable], and fleet account billing. We know DOT compliance matters — our documentation supports your maintenance records.

Available to set up fleet account today. Please call [phone] or email [email].

[Owner/Manager Name] | [Shop Name] | NSCB #[license]

---

**Letter 3 — Municipal / Government Fleet**

Dear [Fleet Manager / Procurement Contact],

[Shop Name] is a Nevada State Contractors Board licensed glass and glazing contractor (NSCB #[license]) with experience serving government and municipal fleet accounts in [City/County].

Government vehicle glass replacement requires accurate documentation for maintenance records, budget compliance, and GSA-style billing if applicable. We provide:
- Itemized invoices per vehicle (VIN, service performed, glass type, technician)
- AGSC-certified installation documentation [if applicable]
- ADAS recalibration records for all equipped vehicles [if applicable]
- Net-30 invoicing available for qualifying government accounts
- Insurance billing for fleet coverage where applicable

We currently serve [reference existing fleet accounts if any]. Our team is available for a brief call to discuss your fleet's glass maintenance needs and set up an account.

[Owner/Manager Name] | [Shop Name] | [Phone] | [Email] | NSCB #[license]

---

**Letter 4 — Rideshare Fleet Partners**

Dear [Fleet/Vehicle Programs Contact],

Rideshare drivers and fleet operators face a specific windshield challenge: their vehicles are on the road more hours per day than average, and a cracked windshield can cause a driver to fail a vehicle inspection — taking them off the platform entirely.

[Shop Name] serves rideshare drivers and fleet operators in [City]:
- Chip repair in under 30 minutes — minimal time off the road
- Windshield replacement with [OEM/OEM-equivalent per gate] glass
- ADAS recalibration for newer model vehicles [if applicable]
- Insurance billing for drivers with comprehensive coverage
- Mobile service for larger fleet operators [if applicable]

If you manage a fleet of rideshare vehicles and want to streamline glass maintenance, let's talk. We can set up a fleet account with priority scheduling for your drivers.

[Owner/Manager Name] | [Shop Name] | [Phone] | NSCB #[license]

---

**Letter 5 — Auto Dealership (Service Department)**

Dear [Service Director / Fixed Ops Manager],

[Shop Name] provides auto glass services to dealer service departments in [City]. We understand dealer fixed ops: customer satisfaction scores matter, loaner vehicle turnaround matters, and ADAS documentation increasingly matters for CPO reconditioning.

We can support your service department with:
- Customer vehicles referred for glass replacement (we return the car on time, documented)
- Trade-in and CPO reconditioning glass work (windshield replacement + ADAS recalibration [if applicable])
- Rental/loaner fleet glass maintenance
- Quick-turn chip repairs while customers wait for other services

We are a NSCB licensed contractor (#[license]) with AGSC-certified technicians [if applicable]. We carry [OEM/OEM-equivalent] glass [per sourcing gate] and provide documentation suitable for dealer records.

This is an educational referral relationship — we're not offering any compensation for referrals; we'd simply like to be the shop your team reaches for when glass work comes up.

[Owner/Manager Name] | [Shop Name] | [Phone] | [Email]

[RESPA compliance note: this letter intentionally contains no referral fee, no split, no kickback arrangement. If dealer wants a formal referral program with compensation, consult an attorney before implementing.]

---

### 4. Customer Referral Program

**Structure:** $[input amount] off next service for referring a friend who becomes a paying customer. Dollar amount credited on next visit. NOT tied to reviews.

**Email Announcement:**
Subject: "Refer a friend, save $[amount] on your next auto glass service"
Body:
Hi [First Name],

Thank you again for trusting [Shop Name] for your recent [service]. If you know someone who needs auto glass repair or replacement, we'd love to help them too.

Here's our referral offer: when you refer a friend and they come in for service, you get $[amount] off your next visit. No hoops — just let them mention your name when they book.

This isn't tied to reviews — we want you to refer because your experience was great, not because there's a coupon on the line.

[Shop Name] | [Phone] | [Website]

**Compliance:** Referral incentive is dollar-off a future service — not a check, not a review incentive, not an insurance deductible credit (which would trigger NRS 686A.2825). FTC-clean. Yelp-clean (referral incentive is for customer-to-customer word-of-mouth, not review creation).

---

### 5. Post-Service Follow-Up Sequence

**Email 1 — 24 Hours Post-Service: Satisfaction Check**
Subject: "How's everything with your [windshield/chip repair], [First Name]?"
Body:
Hi [First Name],

Just checking in after your [service] at [Shop Name] yesterday. A few things to know:

- If you have a [brand] [adhesive], your safe drive-away time was [X] minutes from installation — that window has passed, but avoid car washes for 48 hours and don't slam the doors hard for the first day or two.
- If your vehicle has ADAS [if recalibration was performed]: your camera recalibration is documented in our records. If you notice any warning lights or system alerts over the next few days, call us right away.
- If you notice any issues with the seal, leaks, or glass quality, contact us at [phone]. Our installation is warrantied.

If everything looks good — great. If not — we're here.

[Shop Name] | [Phone] | NSCB #[license]
[Unsubscribe]

**Email 2 — 7 Days Post-Service: Review Request**
[Same as Review Request Email 1 above — send if no review yet received]
