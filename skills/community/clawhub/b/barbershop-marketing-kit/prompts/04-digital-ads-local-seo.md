# Prompt 04 — Digital Ads & Local SEO

## Instructions

Generate a complete digital advertising and local SEO package for a Nevada barbershop. All paid ad copy must include NBHSB license where required. All claims must pass the 14-point compliance checklist.

---

## Part A — Google Local Services Ads (LSA) Checklist

### Prompt

```
Generate a Google LSA setup checklist for [SHOP_NAME].

IMPORTANT — LSA screening for barbershops:
Barbershop is NOT a screened category for Google LSA background checks (unlike home services). However, Google LSA for personal care services requires:
- Business license: NBHSB Shop License [NBHSB_SHOP_LICENSE]
- Insurance: General liability recommended (verify with Google LSA requirements at time of setup)
- Profile photo: Shop interior + barbers (compliance: do not use before/after photos as primary profile photo)

LSA SETUP CHECKLIST:
[ ] Google Business Profile verified and claimed
[ ] Business name matches NBHSB shop license registration
[ ] NBHSB shop license number on file with Google
[ ] Service categories selected: Barbershop, Haircuts, Beard Trim, Hot Shave (if applicable)
[ ] Business hours accurate and updated for holidays
[ ] Service area set to [TARGET_NEIGHBORHOODS] + [CITY]
[ ] Minimum 5 Google reviews before LSA launch (Google LSA ranking factor)
[ ] Profile photo: professional shop interior or barber-at-work (no before/after as hero)
[ ] Booking link connected if available
[ ] Phone number verified (calls are tracked by Google LSA)
[ ] Budget set: recommend $[X]/day for [CITY] market (suggest $15-30/day for Las Vegas metro)

LSA BID STRATEGY:
- LSA charges per lead (call or message), not per click
- Estimated cost per lead for barbershop in Las Vegas: $8-18/lead
- Target: 3-5 new clients/week from LSA at estimated $40-90/week spend
- Track: calls booked vs. walk-ins attributed to Google

OUTPUT: Complete checklist, ready for owner to execute.
```

---

## Part B — Google Responsive Search Ads (5 Ad Groups)

### Prompt

```
Generate 5 Google RSA ad groups for [SHOP_NAME]. Each group: 15 headlines (max 30 chars) + 4 descriptions (max 90 chars).

COMPLIANCE: NBHSB_SHOP_LICENSE must appear in at least one description per ad group (short form: "NBHSB Lic [last 7 digits]" fits in 90 chars).

AD GROUP 1 — "Barbershop Near Me / [CITY]":
Keywords (suggested): "barbershop near me," "[city] barbershop," "barber near me," "haircut near me [city]"
Headlines:
1. Las Vegas Barbershop
2. Haircuts Near [NEIGHBORHOOD]
3. Walk-Ins Welcome Today
4. Fades, Tapers & Lineups
5. [SHOP_NAME] — [CITY]
6. NBHSB-Licensed Barbers
7. Fresh Cut, No Appointment
8. [GOOGLE_RATING]★ [GOOGLE_REVIEW_COUNT] Reviews
9. Open [DAYS] [HOURS]
10. Men's Cuts From $[PRICE]
11. Family Barbershop, [CITY]
12. Your Neighborhood Barber
13. Same-Day Cuts Available
14. Serving [NEIGHBORHOOD 1], [N2]
15. Book Online or Walk In
Descriptions:
1. [SHOP_NAME] — Nevada-licensed barbershop serving [CITY]. Fades, tapers, lineups. Walk-ins welcome. Call [SHOP_PHONE]. (≤90)
2. NBHSB Shop Lic [NBHSB_SHOP_LICENSE_SHORT]. [GOOGLE_RATING]★ on Google. Professional cuts, every time. (≤90)
3. Fresh cut without the wait — [SHOP_NAME] in [NEIGHBORHOOD]. Open [DAYS]. Walk-ins always welcome. (≤90)
4. [BARBER_COUNT] licensed independent barbers. Men's cuts, fades, beard trims, kids cuts. [SHOP_ADDRESS]. (≤90)

AD GROUP 2 — "Fade Haircut Las Vegas":
Keywords: "fade haircut las vegas," "fade barber [city]," "best fade las vegas," "low fade [city]"
Headlines:
1. Fade Specialist in [CITY]
2. Low, Mid & High Fades
3. Skin Fades Available
4. [SHOP_NAME] — Fade Experts
5. Clean Fades, Every Time
6. Walk In for a Fresh Fade
7. Las Vegas Fade Barber
8. Tapers & Lineups Too
9. No Appointment Needed
10. [GOOGLE_RATING]★ Rated Fades
11. Fade Haircut From $[PRICE]
12. Serving [NEIGHBORHOOD]
13. Same-Day Fade Available
14. NBHSB-Licensed Barber
15. Book Your Fade Today
Descriptions: [4 descriptions — fade specialty + license + walk-in + location]

AD GROUP 3 — "Hot Shave / Straight Razor Las Vegas" (only if STRAIGHT_RAZOR_SERVICES = true):
Keywords: "hot shave las vegas," "straight razor shave [city]," "traditional shave barber"
Headlines:
1. Hot Towel Shave [CITY]
2. Traditional Straight Razor
3. Classic Barbershop Shave
4. Fresh Blade Every Client
5. [SHOP_NAME] Hot Shave
6. Walk-In Shaves Welcome
7. NBHSB-Licensed Barber
8. Hot Towel, Clean Shave
9. Beard Shaping Available
10. Neck Shave Add-On
11. Shave From $[PRICE]
12. [GOOGLE_RATING]★ on Google
13. Book a Shave Today
14. [NEIGHBORHOOD] Barbershop
15. Single-Use Blade, Always
Descriptions:
1. [SHOP_NAME] straight razor shaves: fresh single-use blade every client. NBHSB NAC 644 sanitation standards. Walk-ins welcome. (≤90)
2. Classic hot towel shave in [CITY]. EPA-registered disinfectant, NBHSB-licensed. Call [SHOP_PHONE] or walk in. (≤90)
3. [GOOGLE_RATING]★ [GOOGLE_REVIEW_COUNT] Google reviews. Hot shaves, straight razor, neck shave add-on. [SHOP_ADDRESS]. (≤90)
4. NBHSB Lic [SHORT]. Single-use blade. Traditional barbershop experience, modern sanitation standards. (≤90)

AD GROUP 4 — "Master Barber Las Vegas" (only if OWNER_LICENSE contains MB-IND):
Keywords: "master barber las vegas," "master barber [city]," "nevada master barber"
Headlines:
1. Nevada Master Barber
2. [OWNER_NAME] — Master Barber
3. NBHSB Master Barber Lic
4. Expert Cuts in [CITY]
5. [SHOP_NAME] — Master Cuts
6. 1,500-Hour Licensed Barber
7. [GOOGLE_RATING]★ Reviewed
8. Walk-Ins Welcome
9. Fades by a Master Barber
10. [NEIGHBORHOOD] Barbershop
11. Licensed [YEAR]+ Barber
12. Master Barber, [CITY] NV
13. Tapers, Fades & More
14. Book With a Master Today
15. NBHSB-Licensed Expertise
Descriptions:
1. [OWNER_NAME] is a Nevada Master Barber (NBHSB-MB-IND [SHORT]). Fades, tapers, hot shaves — [SHOP_NAME], [CITY]. Walk-ins welcome. (≤90)
2. NBHSB Master Barber license [OWNER_LICENSE_SHORT]. [GOOGLE_RATING]★ [REVIEW_COUNT] reviews. Call [SHOP_PHONE]. (≤90)
3. [SHOP_NAME] — [CITY]'s NBHSB-licensed master barber shop. Fresh cuts, single-use blades, professional results. (≤90)
4. Walk in or book: master barber cuts starting at $[PRICE]. [SHOP_ADDRESS]. Open [DAYS]. (≤90)

NOTE: "Master Barber" in ads ONLY if OWNER_LICENSE = NBHSB-MB-IND format is confirmed.

AD GROUP 5 — "Kids Haircut Las Vegas":
Keywords: "kids haircut las vegas," "kids barber [city]," "children's haircut [city]," "boys haircut [neighborhood]"
Headlines:
1. Kids Cuts in [CITY]
2. Family Barbershop [CITY]
3. Kids Haircuts From $[PRICE]
4. Walk-Ins for Kids Welcome
5. Boy's Haircut [CITY]
6. [SHOP_NAME] — Family Barber
7. School-Ready Cuts
8. [GOOGLE_RATING]★ Family Shop
9. No Fuss Kids Cuts
10. Open Saturdays for Kids
11. Ages [X] & Under $[PRICE]
12. [NEIGHBORHOOD] Kids Barber
13. Book a Kids Cut Today
14. Fast Friendly Kids Cuts
15. NBHSB-Licensed Shop
Descriptions: [4 descriptions — kids focus + license + walk-in + location + age range]

OUTPUT: 5 complete ad groups, all compliance gates applied.
```

---

## Part C — Facebook/Instagram Ad Briefs (6 Briefs)

### Prompt

```
Generate 6 Facebook/Instagram ad briefs for [SHOP_NAME]. Each brief: format, visual direction, headline, primary text (125 chars max for feed), CTA, compliance notes.

BRIEF 1 — Walk-In Awareness (Feed):
Format: Single image
Visual: Shop exterior, OPEN sign, clean well-lit interior
Headline: Walk-Ins Welcome at [SHOP_NAME]
Primary text: Fresh cut in [CITY] — no appointment needed. NBHSB-licensed barbers. Open [DAYS] [HOURS]. [SHOP_ADDRESS].
CTA: Get Directions
Compliance: ✓ No before/after ✓ License mentioned ✓ No superlatives

BRIEF 2 — Fade Transformation (Feed — FTC compliant):
Format: Single image or short video (Reel)
Visual: Barber working on a fade — craft-focused, NOT dramatic before/after
Compliance: If before/after used: caption = "Typical fade result at [SHOP_NAME] — individual texture and growth vary."
Headline: Clean Fades at [SHOP_NAME]
Primary text: Your neighborhood barbershop in [CITY]. Fades, tapers, lineups. Walk-ins welcome.
CTA: Book Now
FTC note: Do not use "transformation" language. Do not imply atypical result is typical.

BRIEF 3 — Booth Renter Spotlight (Feed):
Format: Single image (barber at station, professional)
COMPLIANCE: "Meet [BARBER NAME] — independent licensed barber at [SHOP_NAME] (NBHSB-BAR-IND-XXXXXXXX). [Specialty: fades, hot shaves, etc.]. Book with [BARBER NAME] at [SHOP_ADDRESS]."
Note: IC language throughout. Do not say "our barber" or "our team member." "Independent licensed barber at [SHOP_NAME]" is the correct framing.
Primary text (IC-compliant): "Meet [NAME] — independent licensed barber at [SHOP_NAME]. [Specialty]. Book your spot: [PHONE]."
CTA: Call Now

BRIEF 4 — Hot Shave Promo (Story, 9:16) — if STRAIGHT_RAZOR_SERVICES = true:
Format: Story
Visual: Hot towel on face, barbershop atmosphere
Compliance: Single-use blade disclosure required on any paid straight razor ad.
Headline: Classic Hot Shave — [SHOP_NAME]
Text: "Fresh single-use blade. Hot towel. NBHSB-licensed. The classic shave done right. [SHOP_ADDRESS]."
CTA: Book Now

BRIEF 5 — Gift Card (Feed — holiday or evergreen):
Format: Single image
Visual: Gift card mockup, warm tones
Headline: Give the Gift of a Great Cut
Primary text: [SHOP_NAME] gift cards — no expiration. Available in-shop. Nevada-licensed barbershop.
CTA: Shop Now
Compliance: "No expiration" = NRS 598.128 compliant. Do not set expiration. Do not add fees.

BRIEF 6 — Retargeting (website visitors / GBP clickers):
Format: Single image or carousel
Visual: Shop interior + service menu
Headline: Still Looking for a Barber in [CITY]?
Primary text: [SHOP_NAME] is right here — walk-ins welcome, NBHSB-licensed, [GOOGLE_RATING]★ on Google.
CTA: Get Directions
Note: Retargeting audience = website visitors last 30 days + GBP profile viewers (Google Ads remarketing list).

OUTPUT: 6 complete briefs, ready for Meta Ads Manager.
```

---

## Part D — 30-Day Google Business Profile Calendar

### Prompt

```
Generate a 30-day GBP posting calendar for [SHOP_NAME]. One post per week minimum; 2 per week recommended.

POST TYPES (alternate):
- Service spotlight (fade, beard, hot shave, kids)
- Behind the scenes (shop culture, barber at work)
- Review highlight (quote from Google review — with attribution "— [First name], Google review")
- Offer (if applicable — must be real, limited offers only)
- Educational (NBHSB info, sanitation standards, what to ask for your haircut style)
- Holiday/seasonal

COMPLIANCE RULES:
- No before/after posts presented as typical without disclosure
- No "best barbershop in Vegas" claims without substantiation
- No product drug claims
- IC barber spotlights: "independent licensed barber at [SHOP_NAME]" language
- Review quotes: only from real reviews, accurate to original text

OUTPUT: 30-day calendar table:
Day | Post type | Topic | Caption (100-150 chars) | Photo suggestion | CTA button
```

---

## Part E — 30 Keyword Clusters for Local SEO

### Prompt

```
Generate 30 keyword clusters for [SHOP_NAME] local SEO. Group by intent.

FORMAT: Keyword | Monthly Volume Range | Difficulty | Intent | Primary Page Target

INTENT GROUPS:
1. Navigational (branded): "[SHOP_NAME]", "[SHOP_NAME] [CITY]", "[SHOP_NAME] hours"
2. Local transactional: "barbershop near me [CITY]", "fade haircut [CITY]", "walk in barbershop [NEIGHBORHOOD]"
3. Service-specific: "hot shave las vegas," "straight razor barber [CITY]," "master barber [CITY]," "kids haircut [CITY]"
4. Informational: "NBHSB license Nevada," "how to ask for a fade," "barbershop vs salon [CITY]"
5. Long-tail: "barbershop open Sunday [CITY]," "best fade barber [NEIGHBORHOOD]," "affordable haircut [NEIGHBORHOOD]"

OUTPUT: 30 clusters in table format. Include notes on which terms are highest-value for [SHOP_NAME] specifically.
```

---

## Part F — B2B Cold Email Sequences (4 Sequences)

### Prompt

```
Generate 4 cold email sequences for [SHOP_NAME] B2B outreach. Each sequence: 3 emails (initial + follow-up 1 + follow-up 2).

SEQUENCE 1 — Athletic clubs / gyms:
Email 1: Subject "Quick question — [GYM NAME]"
Body: Intro [SHOP_NAME]. Male clientele overlap. Walk-in hours. Reciprocal referral proposal — "When members ask where to get a fresh cut, we'd love to be your recommendation. In return, we'll send our clients to you."
CTA: "5-minute call?" or "Reply to connect."
Email 2 (5 days later): Follow-up, one sentence, friendly nudge.
Email 3 (10 days later): "Last reach out — if the timing isn't right, no problem. Here's our card [attached]."

SEQUENCE 2 — Hotel concierge (Las Vegas):
Email 1: "[SHOP_NAME] — barbershop recommendation for your guests"
Body: Guests frequently ask concierge for barbershop recommendations. NBHSB-licensed, [GOOGLE_RATING]★, convenient to [HOTEL NEIGHBORHOOD]. Walk-in friendly for tourists. Offer: concierge referral cards to hand out.
Email 2: Brief follow-up. Offer to drop off cards.
Email 3: Final — leave the door open.

SEQUENCE 3 — Wedding/event planners:
Email 1: "Barbershop for your grooms & groomsmen — [CITY]"
Body: Group bookings available. [SHOP_NAME] has capacity for [X] barbers on-site or in-shop group booking. NBHSB-licensed. [GOOGLE_RATING]★.
Email 2: Case study or example (if available). Walk-in or appointment for wedding party day-of.
Email 3: Final.

SEQUENCE 4 — Corporate HR / office managers:
Email 1: "Professional grooming resource for your team — [SHOP_NAME]"
Body: Preferred vendor for employee grooming. NBHSB-licensed, [GOOGLE_RATING]★, convenient to [BUSINESS_DISTRICT]. Suggest: group discount for employees if applicable (must be honored).
Email 2: Brief follow-up with offer.
Email 3: Final.

OUTPUT: 4 sequences, 3 emails each, ready to send.
```
