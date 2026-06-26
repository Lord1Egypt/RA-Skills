# Prompt 3: Review, Reputation & Referral System (PAID)

## Instructions

Copy this prompt into Claude. Fill in the `[BRACKETS]`. Generates your complete review request system, response templates, and referral program.

---

## The Prompt

```
You are a customer retention specialist for home services businesses. Generate a complete review, reputation, and referral system for a cleaning company.

BUSINESS DETAILS:
- Business name: [NAME]
- City: [CITY, STATE]
- Primary review platforms: [Google, Yelp, Facebook — list in order of priority]
- Current rating: [e.g., 4.9★ 312 reviews on Google, 4.7★ 88 on Yelp]
- Booking/CRM software: [e.g., Jobber, Housecall Pro, ZenMaid, manual — for automation notes]
- Referral incentive available: [e.g., $25 off for referrer + referee, free add-on, percent off — pick one]
- Business phone: [for call-to-action use]
- Owner/manager first name: [for signatures]
- Services (list your primary service types): [maid service, deep cleaning, move-out, Airbnb, etc.]

COMPLIANCE RULES — FOLLOW EXACTLY:
1. FTC 2023 Endorsement Guides: review request templates must NOT say "leave us a 5-star review," "we'd love a 5-star rating," or any language that conditions the request on a specific rating
2. No conditional review requests: "get $X off your next clean if you leave a review" = FTC violation — instead, offer the incentive separately, not conditioned on the review
3. Referral program incentives: use fixed-dollar amounts (e.g., $25 off) — disclosed as "referral discount" in any resulting review that mentions the referral
4. "Verified customer" language only usable when booking confirmation exists in your CRM
5. Google review removal: only request removal for reviews that violate Google's policies (fake, spam, off-topic) — do NOT use removal templates to suppress legitimate negative reviews

GENERATE:

**SECTION 1: 20 REVIEW REQUEST TEMPLATES**

Stage 1 — Day of service (text/SMS, 2 templates):
- End-of-visit verbal script (for cleaner to use at door)
- Same-day SMS (under 160 chars)

Stage 2 — 24 hours after (email, 2 templates):
- Subject line A and Subject line B (A/B test)
- Email body (150–200 words each)

Stage 3 — 3 days after (SMS, 2 templates):
- Friendly follow-up if no review yet
- Include direct Google review link placeholder: [GOOGLE_REVIEW_LINK]

Stage 4 — 7 days after (email, 2 templates):
- Last review nudge, light touch
- Different angle from Stage 2

Stage 5 — 30 days after (loyalty email, 2 templates):
- Ask for Yelp or Facebook review (diversify platforms)
- Mention anniversary of first clean if applicable

For EACH stage: provide 2 templates (A/B variants) = 20 total. Flag any FTC risk with ⚠️.

**SECTION 2: 15 REVIEW RESPONSE TEMPLATES**

5-star responses (5 templates):
- Template 1: Recurring customer thank you
- Template 2: First-time customer welcome
- Template 3: Airbnb/VRBO host compliment
- Template 4: Move-out cleaning success
- Template 5: Referral mention in review

4-star responses (2 templates):
- Template 1: Near-perfect, minor note mentioned
- Template 2: No specific feedback, just "really good"

3-star responses (3 templates):
- Template 1: Missed area complaint
- Template 2: Cleaner was late or rushed
- Template 3: Product smell complaint

1–2 star responses (3 templates):
- Template 1: Damage claim (use carefully — do not admit fault in public response)
- Template 2: "They broke something and didn't tell me" — de-escalation + offline resolution
- Template 3: Price complaint

Fake/spam review response (2 templates):
- Template 1: Review from someone clearly not a customer
- Template 2: Competitor attack / obvious fake

For each template: include [OWNER_NAME] placeholder. Keep responses under 150 words (Google truncates at ~250; aim for under 150 to show full response). Do NOT confirm or deny specific service details (HIPAA-adjacent: don't reveal service details even in cleaning context — privacy best practice).

**SECTION 3: SPARKLE REFERRAL CLUB PROGRAM**

Generate complete referral program package:

A. Program rules (3 tiers):
   - Silver: 1 referral = $25 off next clean for referrer + $25 off first clean for referee
   - Gold (3+ referrals): $35 off per referral + free add-on service for referee
   - Platinum (6+ referrals/year): free monthly add-on service + featured in social media

B. Launch email to existing customer list (250 words):
   - Subject line (5 variants)
   - Body with program explanation
   - Clear call to action

C. Referral card copy (for physical card or digital image):
   - Front: headline + offer
   - Back: how it works (3 steps) + referrer name field

D. Post-referral thank you SMS (2 templates):
   - Sent to referrer when their friend books
   - Under 160 chars, TCPA-compliant

E. Social share copy (for referral customers to post):
   - Facebook post (200 words)
   - Instagram caption (150 chars + 10 hashtags)
   - Nextdoor recommendation post (100 words, neighbor tone)

**SECTION 4: REVIEW REMOVAL REQUEST TEMPLATE**

Script for requesting removal of a fake/policy-violating review:
- Google support ticket template (use only for: fake reviews, spam, off-topic, reviewer was never a customer)
- Response to Google denial (one escalation template)
- Internal documentation checklist (what to save before flagging)

Include clear disclaimer: "Use this template only for reviews that violate platform policies. Attempting to remove legitimate negative reviews violates Google/Yelp Terms of Service and FTC guidelines."
```

---

## Example Referral Program Output (Partial)

**LAUNCH EMAIL — Subject line options:**
A: "Know someone who'd love a spotless home? You both win."
B: "Get $25 off — just for telling a friend about Desert Sparkle"
C: "Our best customers become our best ambassadors"
D: "Introducing the Desert Sparkle Referral Club"
E: "Share the sparkle — earn rewards every time"

**REFERRAL CARD (Front):**
GIVE $25. GET $25.
Refer a friend to Desert Sparkle Cleaning — they save $25 on their first clean. You save $25 on your next visit. Win-win for Henderson's cleanest homes.

**REFERRAL CARD (Back):**
1. Share this card (or your personal referral code) with a friend
2. They book their first clean and mention your name
3. You both receive $25 off your next service automatically

Referred by: ___________________
Desert Sparkle Cleaning | (702) 555-0183 | desertsparkle.com
