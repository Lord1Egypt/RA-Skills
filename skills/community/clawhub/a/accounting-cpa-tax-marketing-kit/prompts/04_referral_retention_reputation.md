# Prompt 4: Referral, Retention & Reputation System

## Purpose
Grow the firm through client referrals and Google reviews — the highest-ROI marketing channel for accounting firms. All outputs comply with AICPA § 1.500 (referral fees), AICPA § 1.700 (client confidentiality), FTC 2023 Endorsement Guides (review incentives), TCPA (SMS), and CAN-SPAM (email).

## Inputs Required

```
FIRM_NAME: [Your firm name]
CPA_LICENSE: [CPA license #]
CLIENT_TYPES: [Individual taxpayers / Business owners / Both]
REFERRAL_INCENTIVE: [NONE — recognition only / Gift card $25-$100 / Fee discount / Other]
STATE: [e.g., Nevada — for state CPA board referral fee rules]
REVIEW_PLATFORMS: [Google / Yelp / Facebook / All]
YEARS_IN_PRACTICE: [Number]
SPECIALIZATIONS: [List any, e.g., real estate, Spanish-speaking, IRS resolution]
```

## The Prompt

```
You are a professional services marketing copywriter specializing in compliance for accounting and CPA firms.

Generate a complete referral, retention, and reputation system for:

Firm: [FIRM_NAME] | License: [CPA_LICENSE]
Client types: [CLIENT_TYPES]
Referral incentive: [REFERRAL_INCENTIVE]
State: [STATE]
Review platforms: [REVIEW_PLATFORMS]
Years in practice: [YEARS_IN_PRACTICE]
Specializations: [SPECIALIZATIONS]

COMPLIANCE REQUIREMENTS:
1. Referral incentives: if [REFERRAL_INCENTIVE] involves cash or fee discount, confirm this is permitted under [STATE] CPA board rules (some boards prohibit cash referral incentives — flag if uncertain and provide recognition-only alternative)
2. AICPA § 1.500.001: Any referral fee or commission arrangement must be disclosed in writing to both the referring party and the referred client — include disclosure language
3. Review requests: FTC 2023 Endorsement Guides — NO conditional review requests ("leave a 5-star review to get..."), NO incentive in exchange for reviews, NO suppression of negative reviews
4. Review responses: AICPA § 1.700 — NEVER confirm or deny that someone is a client in a public review response; never discuss any details of their situation publicly
5. Annual newsletter: IRS Circular 230 § 10.37 — general tax education only; not individualized advice; include disclaimer
6. CAN-SPAM: all emails include unsubscribe + physical address
7. TCPA: all SMS include "Reply STOP to opt out"
8. CPA_LICENSE in all formal marketing materials

Generate:

**1. Referral Program Framework**

If [REFERRAL_INCENTIVE] = NONE or recognition-only:
- "Client Recognition Referral Program" — wall of fame, handwritten thank-you note, priority scheduling for next season
- Referral tracking (simple card/email system)
- Referral program description for website (100 words)

If [REFERRAL_INCENTIVE] = gift card or fee discount:
- Confirm [STATE] CPA board permits cash-equivalent referral incentives (flag if state has restrictions)
- AICPA § 1.500.001 disclosure template (to include in referral confirmation email to both referrer and referred client)
- Program structure (1 referral = $X / per new client who files with firm)
- Program description for website (100 words) + disclosure language
- Referral confirmation email template (with required AICPA disclosure)

**2. 3 Referral Request Email Templates**

Template A — Post-Filing Season (send May):
Subject (2 A/B options)
Body (150 words): Thank client for filing with firm this season + natural referral ask + program description
No pressure, no "if you don't refer no one will help them" language

Template B — Post-Advisory Win (triggered after a positive client milestone):
Subject (2 A/B options)
Body (150 words): Reference the positive outcome (in general terms — no specific numbers unless client provided written consent to use) + referral ask
"Clients like you who've experienced [general benefit] often know others in similar situations"

Template C — Annual Touch (send November/December, year-end):
Subject (2 A/B options)
Body (150 words): Year-end gratitude + referral reminder + early-season scheduling CTA

All emails: CAN-SPAM footer

**3. Google Review Request Sequence**

Email (send 1-2 weeks after filing return or completing engagement):
Subject (2 A/B options)
Body (150 words): Thank client for trusting firm + ask for honest review + [REVIEW_PLATFORMS] link
CRITICAL: "We value your honest feedback" — NOT "We'd love a 5-star review" or any implication of conditional positivity
No incentive for review (FTC 2023 Endorsement Guides violation)

SMS (send 3 days after email if no review received):
160 chars max: Brief thank-you + review link + no rating suggestion + STOP opt-out

**4. Review Response Templates**

Positive Review Responses (5 templates):
- Do NOT confirm they are a client ("clients like you" is acceptable; confirming "Yes, we handled your return" is not — AICPA § 1.700)
- Thank the reviewer, reinforce one credential/specialization, invite back
- Vary tone: warm, professional, brief

Negative/Critical Review Responses (3 templates):
Template 1: Factual complaint ("took too long") — empathetic, offer to discuss offline, phone/email contact
Template 2: Outcome disappointment ("my refund was less than expected") — CRITICAL: do not confirm they are a client; do not discuss their situation publicly; offer to speak directly
Template 3: Hostile/inaccurate review — calm, invite offline conversation, do not argue publicly
All negative responses: "I'm not able to discuss client matters publicly, but I'd welcome the chance to speak with you directly. Please contact [PHONE/EMAIL]."

**5. Year-End Tax Planning Newsletter**

Subject (2 A/B options)
Format: 500-word email newsletter
Content: 3-5 actionable year-end tax planning tips (general education — NOT advice for a specific situation)
Compliance header at top of email: "This newsletter contains general tax education. Consult a qualified tax professional for advice specific to your situation."
Topics: retirement contribution deadlines, business equipment purchases (Section 179), charitable giving timing, estimated payment adjustments, year-end review checklist
CTA: "Schedule your year-end review before December 1"
CAN-SPAM footer

**6. Client Satisfaction Survey (Internal Use)**
3 closed questions (NPS scale) + 1 open-ended
Instructions: This is for internal quality improvement — NOT for publishing as testimonials without separate written consent
Include note: "To use any survey response as a testimonial, obtain explicit written consent from the client identifying the specific quote to be used"

**7. Dormant Client Re-Engagement Campaign**
Target: clients who filed with the firm 2+ years ago but have not returned
2-email sequence:
Email 1: "We haven't seen you in a while — are you still looking for tax help?"
Email 2 (2 weeks later): Final outreach + easy unsubscribe option
Both emails: soft tone, no pressure, legitimate unsubscribe link, no implication of continued obligation
Compliance: CAN-SPAM; if you have not had contact in 3+ years, verify consent status before emailing (jurisdiction-dependent)

Format all outputs with clear headers. End with a compliance checklist covering AICPA §§ 1.500, 1.700, FTC 2023 Endorsement Guides, TCPA, and CAN-SPAM items addressed.
```

## Compliance Notes

- **AICPA § 1.500.001 (Commissions and Referral Fees):** A CPA may pay/accept referral fees only if: (a) the fee is not contingent on the outcome of attest work, and (b) the arrangement is disclosed in writing to the client. This prompt includes the required disclosure language.
- **State variations:** Some state CPA boards are more restrictive than AICPA on referral fee arrangements. Nevada, New York, California, and Texas each have specific rules. The prompt flags this for the user's state.
- **AICPA § 1.700 Client Confidentiality:** Confirming someone is your client in a public review response is a violation. Even saying "we're sorry your return took longer than expected" implicitly confirms the person is a client. The review response templates use non-confirming language.
- **FTC 2023 Endorsement Guides (16 CFR Part 255):** The FTC's updated rules explicitly prohibit conditional review requests and review incentives. "Leave us a review for 10% off your next return" is a violation.
- **TCPA:** If clients have not opted in to SMS marketing, do not send. Use appointment confirmation SMS (covered by transactional exemption) separately from marketing SMS.
