# Childcare & Daycare Marketing Kit

A compliance-aware marketing generator for licensed childcare centers, daycares, preschools, and home daycare providers. Generates enrollment campaigns, parent communication templates, seasonal marketing, and digital ads — with COPPA, state licensing, NAEYC, FTC, and CACFP compliance built in at generation time.

## Who This Is For

- Licensed daycare centers and preschools
- Home daycare providers (licensed family childcare)
- Early childhood education centers (ages 0–5)
- After-school care programs (ages 5–12)
- Summer camp programs
- Montessori and play-based programs
- NAEYC-accredited centers
- Corporate childcare programs (employer-sponsored)

## The Problem

Generic AI generates childcare marketing that creates regulatory and liability exposure:

- Claims NAEYC accreditation without current enrollment status → FTC deceptive claim + potential NAEYC trademark violation
- Uses child photos in ads without appropriate consent handling → COPPA exposure
- Targets children in digital ads instead of parents → COPPA violation
- "Fully licensed" without displaying state license number → state childcare licensing board violation
- CACFP meal program mentioned without confirming enrollment → false advertising
- Staff ratio claims that exceed licensed capacity → licensing board violation
- Testimonials that show atypical outcomes ("my child was reading at age 2 after 3 months") → FTC Endorsement Guide violation
- "Background-checked staff" without specifying the screening type → misleading claim

This skill generates compliant copy at generation time. Every ad. Every time.

---

## Prompt 1: Center Brand & Enrollment Acquisition (FREE)

**Use this prompt to generate:**
- Center positioning statement and core differentiators
- Open enrollment campaign (email + Facebook + Google)
- Waitlist launch announcement
- Tour invitation sequence (3 emails + 1 SMS)
- Parent FAQ landing page copy
- Referral program announcement

**Input required:**
```
Center name:
Location (city, state):
State childcare license number:
Ages served:
Capacity (licensed):
Staff-to-child ratios by age group:
Key program approach (Montessori, play-based, academic, faith-based, etc.):
NAEYC accredited? (yes/no — current enrollment date if yes):
CACFP meal program participant? (yes/no):
Current enrollment status (open spots / waitlist / specific age groups open):
Top 3 differentiators:
Tuition range (optional):
```

**Prompt:**
```
You are a childcare marketing specialist with expertise in FTC compliance, COPPA, and state childcare licensing regulations.

Generate a complete enrollment acquisition package for the following center:

[INSERT INPUT ABOVE]

COMPLIANCE REQUIREMENTS — apply to every piece of copy:
1. Include state childcare license number in all printed/digital ads (format: "State License #[NUMBER]" or per state format)
2. NAEYC: Only mention accreditation if NAEYC=yes AND enrollment is current. Use exact language: "NAEYC Accredited (Accreditation #[ID], valid through [DATE])" — never "NAEYC-quality" or "NAEYC-level" without enrollment
3. CACFP: Only mention meal program if CACFP=yes. Use: "Proud participant in USDA CACFP — nutritious meals at no extra cost"
4. Staff ratios: Only state ratios at or within licensed capacity. Never claim "1:3" if licensed for "1:4 infants"
5. FTC testimonials: Any parent quote must be typical-results context: "[Name], parent of [age-group] student" — no outcome claims ("my child was reading at...") unless documented and typical
6. Digital ads: Target PARENTS, not children. No ads on child-directed platforms (under-13 apps/games) — COPPA
7. "Background checks": Specify type: "All staff complete FBI fingerprint background checks and state registry screening"
8. Photos/images: All child images require documented parental photo release — add: "[Note: Use only photos with signed photo release on file]"
9. Ratios in ads: If mentioned, frame as minimum guarantee, not typical: "Staff-to-child ratios meet or exceed [STATE] standards"

DELIVERABLES:

**A. Center Positioning Statement (3 versions: 1 sentence, 3 sentences, paragraph)**
Lead with the primary differentiator. Mention license and NAEYC status where applicable.

**B. Open Enrollment Email Sequence (3 emails)**
- Email 1 (Subject: Enrollment Now Open — [Center Name] [Current Season] Spots Available)
  * Hook: the parent's core fear (is my child safe? Will they thrive? Am I choosing the right place?)
  * Differentiators with compliance-safe claims
  * CTA: Schedule a tour (link placeholder)
  * P.S.: License number disclosure
- Email 2 (Subject: "What does a day look like at [Center Name]?") — Day-in-the-life narrative
- Email 3 (Subject: Only [X] spots remaining — [Center Name]) — Urgency + social proof + final CTA

**C. Facebook/Instagram Ad Set (3 ads)**
- Ad 1: Enrollment campaign (carousel or single image — parent-targeted, NOT child-targeted)
  * Audience note: "Target: parents ages 25-45, [city] + 10mi radius, interests: parenting, childcare, early education"
  * COPPA note: "Do NOT run on Instagram if audience includes under-13"
- Ad 2: Tour invitation ("See it for yourself" hook)
- Ad 3: Waitlist urgency ad

**D. Google Search Ad (RSA format)**
- 15 headlines (30 chars max each) — include license-compliant safety claims
- 4 descriptions (90 chars max each)
- 2 sitelink extensions: "Schedule a Tour" and "View Our Programs"

**E. Tour Invitation Sequence**
- Email 1: Confirmation (immediately after tour request)
- Email 2: Reminder (24 hours before tour) — what to look for on a childcare tour checklist (positions center favorably)
- SMS reminder (2 hours before): under 160 chars, include opt-out

**F. Parent Referral Program Announcement**
- Email + social post
- Fixed-dollar reward structure (not %-based)
- FTC-compliant: "Refer a family and receive a [X]-week tuition credit — full program details at [URL]"

**G. Parent FAQ Landing Page Copy**
- 8 questions covering: safety, ratios, curriculum, meals, illness policy, pickup authorization, communication, tuition
- Schema FAQ JSON-LD block for Google People Also Ask
```

---

## Prompt 2: Parent Communication & Retention

**Use this prompt to generate:**
- Monthly newsletter template (4 sections)
- Daily/weekly parent update templates
- Enrollment renewal campaign
- Emergency/incident communication framework
- Transition communication (infant → toddler, toddler → preschool)

**Input required:**
```
Center name:
Director name and title:
Current enrollment count:
Upcoming events or milestones:
Any recent staff additions or certifications:
Monthly theme or focus (optional):
```

**Prompt:**
```
You are an early childhood education communication specialist.

Generate a complete parent communication and retention package for [CENTER NAME], directed by [DIRECTOR NAME].

COMPLIANCE REQUIREMENTS:
1. Never share individual child progress, incidents, or health information in group communications — FERPA-adjacent best practice (individual matters go to individual parents only)
2. Incident/illness communication: Never name specific children in group messages. Use: "We want to keep all families informed — a child in our [room/age group] has been diagnosed with [illness]. Please watch for symptoms..."
3. Staff introductions: List credentials as stated (ECE degree, Child Development Associate CDA, CPR/First Aid certified) — do not upgrade titles
4. Photo use: "[Photos shared with permission from families with signed photo release on file]"
5. Enrollment renewal: No pressure tactics. Lead with value and relationship.

DELIVERABLES:

**A. Monthly Newsletter Template**
- Header: "[CENTER NAME] Family Update — [Month] [Year]"
- Section 1: Director's message (warm, community-focused, 100 words)
- Section 2: This month's learning focus (curriculum highlight — ties to child development milestones)
- Section 3: Upcoming events (calendar format)
- Section 4: Important reminders (illness policy reminder, weather policy, safety reminder)
- Footer: Center license number, director contact, emergency number

**B. Daily/Weekly Parent Update Templates (3 formats)**
- Daily digital update (under 200 words): Activities, meals (if CACFP), nap/rest, mood snapshot — for infant/toddler rooms
- Weekly classroom highlight (for preschool/pre-K): Learning themes, books read, outdoor time, special moments
- Emergency notification (non-health): Weather closure, facility issue, unexpected early close — clear, calm, action-focused

**C. Illness Notification Template**
- Group illness exposure notice (HIPAA/FERPA-compliant — no names, no diagnoses beyond public health standard)
- Return-to-care policy reminder format
- Doctor's note request language

**D. Enrollment Renewal Campaign (3 touchpoints)**
- 90 days before expiration: "We're saving your spot" — relationship-first, early commitment discount
- 30 days before: Specific spot availability update
- 7 days before: Final enrollment confirmation request

**E. Room Transition Communication**
- Infant → Toddler room transition letter (parent anxiety is high — address it directly)
- Toddler → Preschool transition letter
- Preschool → Kindergarten readiness letter (graduation milestone — celebrate)

**F. Difficult Situation Communication Templates**
- Staff change announcement (maintain trust, no oversharing reasons)
- Policy change notification (tuition increase, hours change) — lead with context, not just the change
- Incident communication framework (what happened → what we did → what we're doing to prevent recurrence — NO child names)
```

---

## Prompt 3: Seasonal & Event Marketing

**Use this prompt to generate:**
- Summer camp enrollment campaign
- Back-to-school enrollment push
- Holiday event invitations and social posts
- Graduation/promotion ceremony promotion
- Open house marketing campaign
- NAEYC accreditation renewal announcement (if applicable)

**Input required:**
```
Center name:
Upcoming season or event:
Summer camp offered? (yes/no — if yes: ages, dates, themes, price):
Graduation/promotion ceremony date and details:
Holiday events planned:
Current enrollment status for the season:
Special programming or themes for the season:
```

**Prompt:**
```
You are a childcare marketing specialist generating seasonal and event content for [CENTER NAME].

COMPLIANCE REQUIREMENTS:
1. Summer camp pricing: Include all fees. If additional supply fees exist: "Base tuition: $X/week. A $Y materials fee applies for [specific weeks/themes]." No hidden fees.
2. Age claims: "Accepts children ages [X] through [Y] — licensed for [STATE] ages served"
3. Summer camp staff: If different staff than year-round: "Summer staff meet all [STATE] background check and training requirements"
4. Photo releases: All event photo use requires signed release on file — include note in all event promotions
5. Graduation/promotion: Attendance/ceremony details accurate — no promises about future academic readiness beyond developmentally appropriate language
6. NAEYC announcements: Only if current. Include accreditation number and valid-through date.

DELIVERABLES:

**A. Summer Camp Enrollment Campaign**
- 3-email sequence: Early bird (6 weeks out) → program details (4 weeks out) → final spots (2 weeks out)
- Facebook/Instagram ad (parent-targeted — COPPA compliant)
- Summer camp program one-pager (for in-center display and email attachment)
- Google RSA summer camp ad (15 headlines + 4 descriptions)

**B. Back-to-School Enrollment Campaign**
- "Fall enrollment is open" announcement (email + Facebook + Google RSA)
- Preschool readiness positioning (developmentally appropriate language only — no academic guarantees)
- School-year schedule change notification template

**C. Holiday Event Marketing**
- Winter celebration invitation template (inclusive language — "Winter Celebration" not "Christmas Party")
- Spring event invitation
- Open house invitation (all-season template)
- Social media posts: 6 holiday/seasonal posts with platform-appropriate copy (Facebook 100 words, Instagram 100 words + hashtags, Google Business Profile 75 words)

**D. Graduation & Promotion Ceremony**
- Ceremony invitation (print/email format)
- Social media announcement posts (3 versions — before, day-of, after)
- Photo release reminder for ceremony photos
- "Moving on to kindergarten" parent letter (warm, celebratory, positions center well for referrals)

**E. NAEYC Accreditation Announcement (if applicable)**
- Press release format
- Parent announcement email
- Social media announcement (3 posts: Facebook, Instagram, Google Business Profile)
- Lobby/entry display copy
- All with correct accreditation number and valid-through date

**F. 30-Day Social Media Calendar**
- 20 posts: Mix of educational content (child development tips), enrollment CTAs, staff spotlights, safety reminders, community content
- Per post: platform, content, CTA, compliance notes
- Hashtag sets: local + industry (#childcare #preschool #earlychildhood + city-specific)
```

---

## Prompt 4: Digital Ads + Local SEO

**Use this prompt to generate:**
- Google LSA (Local Services Ad) profile copy
- Google RSA enrollment campaigns (2 ad groups)
- Facebook/Instagram parent-targeted campaigns
- Nextdoor community posts
- SEO landing page ("Daycare [City]" + "Preschool [City]")
- Google Business Profile optimization posts

**Input required:**
```
Center name:
City and state:
State childcare license number:
Service radius or neighborhoods served:
Ages served:
NAEYC accredited? (yes/no):
Primary competitor positioning (what are parents choosing between?):
Key differentiator for digital:
Google Business Profile URL (if available):
Budget context (local independent vs. multi-location):
```

**Prompt:**
```
You are a digital marketing specialist for childcare and early education businesses. Generate a complete digital acquisition package for [CENTER NAME] in [CITY, STATE].

COMPLIANCE REQUIREMENTS:
1. Google LSA: Childcare is a regulated service — include license number in business description
2. COPPA: ALL digital ads target parents (25-45, parent/family interests) — NEVER child-directed placements. Add audience note to every ad: "Target: parents — exclude under-13 placements"
3. Facebook/Instagram: Add placement note: "Exclude Audience Network placements on apps/games rated for under 13" — childcare centers have been cited for inadvertent child targeting
4. No enrollment guarantees in search ads: "Spots available — subject to licensing capacity and age-group availability"
5. Safety claims: Must be verifiable. "Background-checked staff" → specify: "FBI fingerprint + state registry background checks"
6. Review management: FTC-compliant. Never incentivize reviews. Response templates for all star ratings.
7. "Best daycare in [City]": FTC superlative — only usable if backed by award citation with date. Use: "Families' Choice: [X]+ 5-star reviews on Google" instead.
8. Schema markup: Do not claim NAEYC accreditation in schema unless currently enrolled

DELIVERABLES:

**A. Google LSA Profile Copy**
- Business description (250 chars): Lead with license number, key differentiator, call to action
- Service categories: Daycare, Preschool, Before & After School Care, Summer Camp (check applicable)
- Services offered list (10 items)
- 3 business highlights

**B. Google Search Ads — 2 Ad Groups**

Ad Group 1: "Daycare near me / [City] daycare"
- 15 headlines (30 chars each): safety, ratios, enrollment, license, NAEYC (if applicable)
- 4 descriptions (90 chars each)
- 4 sitelinks: Schedule Tour, Programs & Curriculum, Tuition & Rates, About Our Staff

Ad Group 2: "Preschool [City] / early learning [City]"
- 15 headlines (focus on curriculum, school readiness, developmentally appropriate)
- 4 descriptions
- Negative keyword list: 10 irrelevant terms to exclude

**C. Facebook/Instagram Campaign (3 Ad Sets)**

Ad Set 1 — Enrollment (cold audience)
- Primary text (125 chars), headline (40 chars), description (30 chars)
- Audience specification: Parents 25-45, [City] 10mi, interests: parenting, childcare, early education, kindergarten readiness
- COPPA placement note: "Exclude under-13 Audience Network placements"

Ad Set 2 — Tour Invitation (warm audience — website visitors/engagement)
- Retargeting copy: warmer tone, social proof, specific CTA
- "See what a day looks like" hook

Ad Set 3 — Waitlist (urgency)
- "Only [X] spots in [Age Group]" — scarcity without false urgency
- Parent testimonial format (FTC-compliant: typical results, parent consent)

**D. Nextdoor Community Posts (3 versions)**
- Disclosed as childcare center (not neighbor post)
- Community-first framing (local, trusted, years in neighborhood)
- Enrollment CTA without pressure

**E. SEO Landing Pages (2 pages)**

Page 1: "Daycare in [City], [State] — [Center Name]"
- Title tag (60 chars): "Daycare in [City] | Licensed & NAEYC Accredited | [Center Name]"
- Meta description (155 chars)
- H1, H2 structure (5 H2s minimum)
- 600-word body copy with license number, ratio information, enrollment CTA
- Schema FAQ JSON-LD (8 Q&A: licensing, ratios, meals, hours, enrollment, safety, curriculum, pricing)
- Local business schema: license number, hours, age range

Page 2: "Preschool in [City], [State] — [Center Name]"
- School readiness focus
- Curriculum and developmental milestones framing (no academic guarantees)
- Same schema structure

**F. Google Business Profile Posts (10 posts)**
- 2x enrollment CTAs (seasonal)
- 2x staff spotlight (no child photos — staff only, with consent)
- 2x educational tips for parents (positions center as expert)
- 2x event announcements (open house, graduation)
- 1x community involvement post
- 1x NAEYC/safety certification highlight (if applicable)
- Each post: under 1,500 chars, CTA button recommendation, compliance note

**G. Review Management Templates**
- 5-star response: warm, brief, no specifics (FERPA-adjacent: don't confirm child enrollment)
- 4-star response: thank + invite to discuss in private
- 3-star response: empathetic, direct to director contact
- 1-2 star response: de-escalate, move to private channel, no child names
- Review request script: FTC-compliant (no incentives, no conditional language): "If you have a moment, an honest Google review helps other families find us — [link]"
```

---

## Example Output

See `/examples/little-sprouts-henderson-nv/` — full 4-prompt execution for Little Sprouts Learning Center, Henderson NV (Dr. Amara Osei-Bonsu, EdD — NAEYC Accredited, ages 6 weeks–5 years, NV License #CDC-20241-3847).

---

## Compliance Summary

| Regulation | Area Covered |
|---|---|
| COPPA | No child-targeted digital ads; parent targeting only; no child data collection language |
| State Childcare Licensing | License number in all ads; ratio claims within licensed capacity |
| NAEYC Standards | Accreditation language only when current enrollment confirmed; exact citation format |
| FTC 2023 Endorsement Guides | Testimonials typical-results context; parent consent required; no incentivized reviews |
| FERPA (adjacent) | No individual child info in group communications; no enrollment confirmation in public responses |
| USDA CACFP | Meal program claims only when enrolled; correct program language |
| ADA | Accessible programming language guidance; no exclusionary claims |
| CAN-SPAM / TCPA | Opt-out in all email/SMS; commercial email identification |

---

## Pricing

**Free tier:** Prompt 1 (Center Brand & Enrollment Acquisition)

**Premium ($29 one-time):** All 4 prompts + compliance summary + worked example

**DFY service:** Full marketing kit for your center — $79 (one campaign) / $197 (complete package) / $297/month retainer
