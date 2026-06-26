# Prompt 03 — Reputation Management & Referral System

## Instructions

Generate a complete reputation management and referral system for a Nevada barbershop. All GBP review responses must be legally safe — no admissions of liability, no HIPAA-equivalent disclosures (barbershops don't handle PHI, but client complaint details should not be repeated publicly). All review requests must follow FTC 2023 guidelines.

---

## Part A — Post-Service Review Request Sequence

### Prompt

```
Generate a 3-touchpoint review request sequence for [SHOP_NAME] clients. The goal is to encourage authentic Google reviews without incentivizing or filtering reviews (FTC prohibition).

COMPLIANCE GATES:
- No review gating (do not send review requests only to satisfied clients while suppressing dissatisfied ones)
- No incentivized reviews (no "leave a review and get $5 off") — FTC Section 5 violation
- Review requests must be sent to all clients equally, not selectively
- "Leave us a review if you're happy" = selective solicitation = review gating = FTC violation. Use neutral language.

TOUCHPOINT 1 — SMS (same day, 2 hours post-service):
[SHOP_NAME]: Thanks for coming in today, [FIRST_NAME if available]! We'd appreciate your honest feedback on Google — it helps other clients find us: [GOOGLE_REVIEW_LINK]. Reply STOP to opt out.
[Max 160 chars. Neutral — does not filter on satisfaction.]

TOUCHPOINT 2 — Email (3 days post-service, if email captured):
Subject: How was your visit to [SHOP_NAME]?
Body (100-150 words): Thank you for your visit. [Shop name + date of service]. We'd value your honest Google review — takes 30 seconds, helps our shop grow. [LINK]. For any concerns, contact us directly at [SHOP_PHONE] or [EMAIL]. No reply needed if we hit the mark.
Footer: [SHOP_NAME] | [SHOP_ADDRESS] | NBHSB [NBHSB_SHOP_LICENSE] | Unsubscribe: [link]

TOUCHPOINT 3 — In-shop card (printed, handed at checkout):
Front: "We appreciate your business."
Back: "Leave us a Google review — your honest feedback helps other clients find a shop they can trust." QR code to [GOOGLE_REVIEW_LINK]. No incentive. No conditional language.

OUTPUT: 3 fully written touchpoints.
```

---

## Part B — Google Business Profile Response Templates

### Prompt

```
Generate 15 Google Business Profile review response templates for [SHOP_NAME]. Responses must be legally safe, professionally warm, and consistent with NBHSB licensure context.

LEGAL SAFETY RULES for review responses:
- Never admit fault in a way that creates liability (e.g., "you're right, our barber cut you" = admission)
- Never repeat specific complaint details publicly (reduces spread of negative narrative)
- Never violate client privacy (do not reference appointment details, services, or personal info publicly)
- Never offer refunds or settlements in a public response (direct to phone/email)
- Never threaten or argue
- Always invite offline resolution for complaints

Generate responses for:

RESPONSE 1 — 5-star, enthusiastic review:
"[OWNER_NAME or 'Thank you so much!'] [First name of reviewer if available] — appreciate you taking the time. [Specific call-back to what they mentioned without over-promising]. We look forward to seeing you at [SHOP_NAME] again!"

RESPONSE 2 — 5-star, brief review ("Great cuts!"):
Short warm acknowledgment. Mention neighborhood/city. Invite back. Under 50 words.

RESPONSE 3 — 5-star, mentions specific barber (if IC — booth rental context):
"So glad [Barber's name] took great care of you! [Barber name] is one of the talented independent barbers at [SHOP_NAME] — always great to hear great feedback. See you next time!"
[NOTE: For booth rental model, acknowledging the IC barber without claiming them as "our employee" is correct.]

RESPONSE 4 — 4-star, good but mentions wait time:
"Thank you for the kind words and for the honest feedback on the wait — we appreciate it. [Acknowledgment of busy periods]. Walk-ins are always welcome; for shorter waits, [booking option if available]. Hope to see you back soon."

RESPONSE 5 — 3-star, vague dissatisfaction ("It was okay"):
Warm invite to reach out directly. No defensive language. Ask for a second chance. Under 75 words.

RESPONSE 6 — 2-star, cut didn't come out right:
LEGAL SAFETY REQUIRED. Do not: repeat the complaint, admit the cut was bad, name the barber.
Template: "Thank you for the feedback — we take every visit seriously. We'd like the opportunity to make this right. Please contact us directly at [SHOP_PHONE] or [EMAIL] and we'll take care of you. We value your trust and hope to earn it back."

RESPONSE 7 — 1-star, angry/profanity review (no detail):
Brief, professional, de-escalating. Invite offline. Do not engage with emotion. Under 50 words.

RESPONSE 8 — 1-star, license / credential challenge ("Are these guys even licensed?"):
"[SHOP_NAME] is fully licensed by the Nevada State Barber Health & Sanitation Board (Shop License [NBHSB_SHOP_LICENSE]). [IF BOOTH_RENTAL_MODEL: Each independent barber at our shop holds an individual NBHSB license.] Our licenses are posted in-shop. Happy to answer any questions at [SHOP_PHONE]."

RESPONSE 9 — 1-star, sanitation complaint:
LEGAL SAFETY REQUIRED. Do not repeat sanitation concern details publicly.
Template: "Thank you for bringing this to our attention. We take sanitation standards seriously and follow Nevada NBHSB NAC 644 protocols. We'd like to address your specific concern directly — please contact us at [SHOP_PHONE]. We want to make this right."

RESPONSE 10 — 1-star, injury/cut complaint:
HIGHEST LEGAL RISK. Do NOT: admit fault, describe the incident, name personnel.
Template: "We're sorry to hear about your experience. We take client safety very seriously. Please contact us directly at [SHOP_PHONE] or [EMAIL] so we can address this privately. Thank you."
[Note: If injury involves blood exposure, owner should consult OSHA BBP protocols and potentially legal counsel before responding further.]

RESPONSE 11 — 1-star, pricing complaint ("Too expensive"):
Acknowledge. Explain value briefly. Do not argue or discount publicly. Under 75 words.

RESPONSE 12 — NBHSB license display complaint ("I didn't see a license on the wall"):
"Thank you for the heads up — our NBHSB shop license ([NBHSB_SHOP_LICENSE]) is posted in the shop as required by NRS 644. If you didn't see it during your visit, please let us know and we'll make sure it's clearly visible. We appreciate you caring about licensed shops."

RESPONSE 13 — Positive review mentioning kids cut:
Warm acknowledgment. Mention kid-friendly hours or walk-in welcome. Under 50 words.

RESPONSE 14 — Review asking about products ("Where can I buy what they used?"):
"[Product name(s)] are available in-shop! Stop by or call us at [SHOP_PHONE] to check availability. We're happy to recommend the right one for your hair type."

RESPONSE 15 — Review mentioning booth renter by name with high praise:
"So glad [NAME] delivered a great experience! [NAME] is an independent licensed barber at [SHOP_NAME] — [brief 1-sentence compliment]. Always great to hear this kind of feedback. See you again!"
[Maintains IC language — not "our employee" or "our team member."]

OUTPUT: 15 complete, ready-to-use response templates.
```

---

## Part C — Referral Program

### Prompt

```
Design a referral program for [SHOP_NAME] that complies with Nevada law and FTC guidelines.

COMPLIANCE GATES:
- Referral rewards are permissible if disclosed upfront and applied consistently
- "Refer a friend, get $[X] off your next cut" = permissible (disclosed incentive for referral, not review)
- Do NOT tie incentives to reviews (FTC Section 5 review incentive prohibition)
- Rewards must be honored as advertised (FTC free/discount truth-in-advertising)
- NRS 598.128: Any shop credit issued as a "gift" cannot expire in less than 18 months (treat like a gift card)

Generate:

REFERRAL PROGRAM STRUCTURE:
Name: [e.g., "The Sharp Circle" or "Refer a Barber Club"]
Offer: [Referrer gets $X off next service when referred client completes first paid service]
Tracking method: [Referral card / promo code / verbal tracking — suggest simple system for barbershop]
Limits: [Per customer limit, if any — must be honored as stated]

IN-SHOP CARD (front/back):
Front: Program name + offer
Back: How it works (3 steps, simple). No expiration on credit (NRS 598.128 compliant).

EMAIL ANNOUNCEMENT:
Subject: Invite a friend — get [REWARD] at [SHOP_NAME]
Body (100-150 words): Program intro. How it works. Redemption instructions. Reward details.
Footer: [Standard NBHSB footer + reward terms: "Referral credit valid for any service. No expiration. Not redeemable for cash."]

INSTAGRAM POST:
Caption: Program announcement. Visual suggestion. 20 hashtags.
Compliance: No "review for reward" language. Reward is for referral only.
```

---

## Part D — B2B Partnership Letters

### Prompt

```
Generate 6 B2B cold outreach letters for [SHOP_NAME] targeting local business partnerships. Tone: professional, peer-to-peer, not salesy.

TARGETS:

LETTER 1 — Athletic club / gym:
[Angle: male clientele overlap, pre/post-workout grooming, reciprocal referral. Walk-in welcome for their members.]

LETTER 2 — Men's clothing / suit retailer:
[Angle: head-to-toe grooming coordination. "Your clients invest in how they look — we handle the haircut." Cross-referral card exchange proposal.]

LETTER 3 — Hotel concierge (Las Vegas):
[Angle: business traveler and tourist market. "When guests ask where to get a fresh cut in [NEIGHBORHOOD], we want to be your recommendation." Concierge card with walk-in hours.]

LETTER 4 — Corporate HR / office manager (Las Vegas business park):
[Angle: employee benefit or preferred vendor. "For your team's professional appearance needs — a licensed Nevada barbershop with convenient hours near [BUSINESS_DISTRICT]." Group booking option if available.]

LETTER 5 — Wedding / event planner:
[Angle: groom, groomsmen, wedding party. Group booking. Day-of grooming. NBHSB licensed, insured, professional setup possible for on-site if applicable.]

LETTER 6 — Real estate agent / broker:
[Angle: the "looking sharp for open houses" angle. Agents frequently need quick professional grooming. Reciprocal referral: "When clients relocating to [CITY] ask about neighborhood services, we'd love to be on your list."]

Each letter: 150-200 words. Professional letterhead format. Include SHOP_NAME, SHOP_ADDRESS, SHOP_PHONE, NBHSB_SHOP_LICENSE.

OUTPUT: 6 complete letters, ready to print or email.
```
