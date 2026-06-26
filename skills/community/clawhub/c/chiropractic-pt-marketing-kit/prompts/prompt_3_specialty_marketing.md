# Prompt 3 — Specialty & Niche Marketing

## Purpose
Generate targeted marketing materials for your practice's specific specialty focus: auto accident/PI, sports performance, prenatal/pediatric, or corporate/workplace.

---

## Prompt

```
You are a healthcare marketing specialist for chiropractic and physical therapy practices. Generate specialty-specific marketing materials for the focus area chosen below. All outputs must comply with HIPAA, FTC health claim rules, ACA/APTA advertising ethics, and state board advertising regulations. No absolute outcome claims. No disparagement of other providers. License number required on all ads.

**Practice name:** [PRACTICE NAME]
**Provider name(s) and credentials:** [e.g., Dr. James Okafor DC, CCSP | Dr. Lisa Chen DPT, OCS]
**Location:** [City, State]
**Specialty focus (choose one):** [AUTO ACCIDENT/PI | SPORTS PERFORMANCE | PRENATAL/PEDIATRIC | CORPORATE/WORKPLACE]
**License numbers:** [DC License # | PT License #]

---

=== IF SPECIALTY: AUTO ACCIDENT / PERSONAL INJURY ===

**Output 1: PI Attorney Referral One-Pager**
(Already covered in Prompt 1 — skip if generated there. Run again for additional formats.)

**Output 2: Patient Education Landing Page — "What to Do After a Car Accident"**
- Length: 800-1,000 words
- SEO target keyword: "what to do after car accident [City]" or "car accident chiropractor [City]"
- Structure:
  * H1: "What to Do After a Car Accident in [City]: A Step-by-Step Guide"
  * Intro: Immediate steps (medical evaluation, documentation, police report) — not legal advice, frame as general guidance
  * H2: "Why Getting Evaluated Quickly Matters" — clinical rationale, no guarantee of outcomes
  * H2: "What Our Auto Injury Evaluation Includes" — services description, FTC-compliant
  * H2: "Working with Your Attorney and Insurance" — patient rights, lien process explained simply
  * H2: "Common Auto Injury Questions" — 4 FAQs, structured for featured snippet
  * H2: "Schedule Your Evaluation" — CTA with new patient offer
  * Disclaimer: "This page is for educational purposes. We are not attorneys and cannot provide legal advice."
- FAQ schema markup (JSON-LD): generate for 4 FAQs

**Output 3: Auto Injury Social Posts (3 posts)**
Post 1 — Educational: "3 signs your body may still be recovering from a car accident" (informational, FTC-compliant, no scare tactics)
Post 2 — Process: "Working with a PI attorney? Here's how we document your care" (professional, attorney-referral angle)
Post 3 — Patient story framing: "[First Name] was in a rear-end collision and came to us 2 weeks later. Here's what her care looked like." (FTC-compliant: "individual results, not typical outcomes")

**Output 4: Attorney Referral Follow-Up Email Sequence (3 emails)**
Email 1 — Initial outreach (Day 1): introduction, what we offer, documentation process summary, invitation to call/visit
Email 2 — Value add (Day 5): send a resource (injury documentation checklist, MMI report example), no hard sell
Email 3 — Soft follow-up (Day 12): brief, offer a lunch-and-learn or phone call to answer questions, easy opt-out

---

=== IF SPECIALTY: SPORTS PERFORMANCE / ATHLETIC RECOVERY ===

**Output 1: Sports Team Partnership Pitch Letter**
- Target: youth sports leagues, adult rec leagues (USTA, pickleball, CrossFit boxes, triathlon clubs), high school athletic directors
- Structure: practice intro → what we offer athletes → case format (not a specific patient — general "athletes we work with come to us for...") → partnership options (sideline coverage, pre-season screens, discount membership) → call to action
- FTC: no guaranteed performance improvement claims
- Length: 350-450 words

**Output 2: Athlete Testimonial Framework (FTC-compliant)**
Template for asking athletes to share their story:
- 5 questions to guide the testimonial: what was the injury/issue, what did you try before, what was your experience like, what are you able to do now, would you recommend
- Disclosure language to include: "Results vary. This is [Name]'s individual experience and may not reflect typical outcomes."
- Before/after framing rules: performance metrics only (race time, lifting PRs, return-to-sport date) — no symptom-based before/after claims without FTC disclaimer

**Output 3: Pre/Post-Event Treatment Campaign**
Choose event type: [marathon/half marathon | CrossFit competition | youth tournament | pickleball tournament | triathlon]
- Pre-event: social post + email to patient list + day-of sign-up offer
- Post-event: social post + email to patient list + recovery offer
- Event day (if applicable): flyer text + table banner copy + script for provider at the event

**Output 4: Sports Content Series — 4 Instagram Carousels**
Sport-specific — choose: [running | golf | pickleball | CrossFit | youth baseball/softball | swimming]
- Slide 1: Hook ("The #1 [sport] injury we see in [City] — and how to prevent it")
- Slides 2-4: Educational content (injury mechanics, prevention tips, when to see a provider — informational, no treatment promises)
- Slide 5: CTA (schedule an evaluation — FTC-compliant language)
- Caption: 125-150 words, 10-12 hashtags

---

=== IF SPECIALTY: PRENATAL / PEDIATRIC / FAMILY ===

**Output 1: Prenatal Chiropractic/PT Service Page**
- Length: 500-600 words
- Safety language: ACOG (American College of Obstetricians and Gynecologists) recommendation framework — what evidence supports, what we do not claim
- What we treat: round ligament discomfort, pubic symphysis, sciatic discomfort during pregnancy, pelvic floor PT (if applicable)
- Webster Technique description (chiropractic — for optimal fetal positioning): educational, no guaranteed outcome
- Postpartum section: diastasis recti, pelvic floor rehab (PT), feeding posture
- Compliance: "Always consult your OB/midwife. We coordinate with your maternity care team."

**Output 2: Pediatric Introduction for Parents (FAQ format)**
8 FAQs:
1. Is chiropractic/PT safe for children?
2. At what age can children start?
3. What conditions do pediatric chiropractors/PTs typically work with?
4. Is it different from adult care?
5. How do I know if my child needs to be evaluated?
6. What does a pediatric visit look like?
7. Do you use the same techniques as with adults?
8. What should I bring to the first visit?
Format: answer each in 75-100 words, approachable parent tone, no fear-based language

**Output 3: Family Wellness Package Framing**
- 3 package option descriptions (not "treatment plan" — wellness positioning):
  * Individual wellness: [description]
  * Couple/partner wellness: [description]
  * Family wellness: [description]
- Marketing copy for each: headline, 2-sentence description, monthly investment, what's included
- Compliance: "Wellness care is not a replacement for medical care. We recommend regular checkups with your primary care physician."

---

=== IF SPECIALTY: CORPORATE / WORKPLACE / ERGONOMICS ===

**Output 1: Corporate Wellness Pitch Deck One-Pager**
Target: HR directors, office managers, warehouse/distribution center safety coordinators
- Problem framing: musculoskeletal disorders are the #1 cause of worker absenteeism (OSHA/BLS data)
- Solution: on-site ergonomic assessments + employee wellness visits + injury prevention program
- ROI framing: "For every $1 invested in workplace ergonomics, companies report $2-6 in reduced absenteeism and workers' comp costs" (cite source)
- Program options: lunch-and-learn, monthly on-site clinic hours, discounted employee rate, workers' comp case coordination
- Call to action: 30-min HR director consultation (free)
- No guaranteed injury-reduction outcomes — frame as "part of a comprehensive ergonomic program"

**Output 2: Ergonomic Assessment Campaign**
Target: remote workers, hybrid offices, warehouses, distribution centers, call centers
- Social post: "Is your home office setup causing you pain?" (3 versions: Instagram square, LinkedIn post, Facebook post)
- Email to patient list: "We're now offering workplace ergonomic assessments — here's what's included"
- Flyer text (for office buildings or break rooms): 200 words, headline + bullet list + QR code CTA
- Assessment offer details: what's included in the evaluation, price, how to schedule

**Output 3: Workers' Comp Intake Process Explainer**
Two versions:
- Employee-facing (simple, reassuring): "What to expect when you come to us on a workers' comp claim" — intake process, documentation, your rights as a patient
- Employer-facing (professional, ROI-focused): "How we work with employers on workers' comp cases" — documentation process, return-to-work timeline, communication protocol, functional capacity evaluation (if applicable)
```

---

## Usage Notes

- Run this prompt once per specialty focus — do not mix specialties in one run
- PI attorney referral one-pager can be offered as a $49-97 standalone Fiverr gig
- Sports partnership pitch letter: target local CrossFit boxes, pickleball leagues (massive in Las Vegas), youth sports organizations (Nevada Youth Soccer, Las Vegas Youth Baseball)
- Corporate pitch: Henderson/Summerlin business parks, Amazon fulfillment centers (large workforce, high MSK injury rate), casino/hospitality back-of-house staff
