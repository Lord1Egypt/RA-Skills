# Prompt 3 — Review Management + Referral System

## Overview
Generates post-service review request templates, response templates (including damage/scratch complaint protocol), a compliant referral program, and a fleet/dealer referral structure.

## Required Inputs
```
Business name: [your business name]
Owner/manager first name: [name for signing responses]
City/state: [city, state]
Primary review platforms: [Google / Yelp / Facebook / all three]
Does your business carry garage keepers insurance? [Yes / No / I'll check]
Service type: [detailing shop / mobile detailing / both]
Referral reward type: [dollar off next service / free add-on / both]
Referral reward amount: [e.g., "$25 off for you + $25 off for your friend"]
Fleet/dealer program: [Yes, I want fleet referral structure / No]
Fleet referral reward: [e.g., "$150 for each fleet account introduced"]
```

## Prompt
```
You are a customer experience specialist for auto detailing businesses. Generate a complete review management and referral system for the business described below.

**Business details:**
[PASTE INPUTS HERE]

**Generate the following:**

---

## SECTION 1: Post-Service Review Request Templates (20 templates)

Generate 5 templates for each delivery method:
- **SMS — Vehicle pickup** (after customer picks up): 160 char max
- **SMS — Mobile delivery** (immediately after mobile service complete): 160 char max
- **Email — 24 hours after service**: Subject line + 3-paragraph body
- **Email — 3-day follow-up** (if no review yet): Subject line + 2-paragraph body

**Guidelines:**
- Vary phrasing across templates — no two should be identical in structure
- Include [First Name] variable where appropriate
- Ask for "honest review" — FTC 2023 Endorsement Guides require this exact framing
- Link to [Google Review Link] placeholder
- No reward promises before or contingent on posting a review
- Mention the specific service performed: "your [service type] today" not just "your service"

---

## SECTION 2: Review Response Templates (12 templates)

### 5-Star Responses (4 templates)
- Generic praise response
- Ceramic coating / paint correction specific
- Mobile detailing specific
- Fleet/dealer specific

### 3-Star / Mixed Response (3 templates)
- "Results not as expected" complaint
- "Price was higher than quoted" complaint
- "Took longer than promised" complaint

### 1-Star / Damage Complaint Response (5 templates)
- "Pre-existing scratch being blamed on us" response
- "Swirl marks after polishing" complaint
- "Interior item damaged" complaint
- "Paint chip/scratch claim" response
- "Ceramic coating not lasting as promised" complaint

**Damage Response Protocol (include this section):**
When a customer claims the detailer caused damage:

STEP 1 — Public reply (post this on the review platform):
"[Customer name], thank you for bringing this to our attention. We take every concern seriously and want to make this right. Please contact [Owner Name] directly at [phone/email] so we can review your vehicle together and discuss a resolution. We value your trust and want to earn it back."

STEP 2 — Internal process:
- Pull the condition report signed at drop-off (all vehicles should have a pre-service condition inspection)
- Review photos taken before service began (best practice: photograph every panel before any work starts)
- Contact your garage keepers insurance carrier before making any written admission of liability

STEP 3 — Resolution options (by damage severity):
- Minor swirl complaint: complimentary 1-stage polish re-service
- Chemical residue: complimentary interior/exterior re-clean
- Paint chip/scratch disputed: three-way inspection with customer, detailer, and independent paint shop assessment
- Major damage: engage insurance carrier before any written settlement commitment

**IMPORTANT:** Never admit fault in the public review response or in the initial direct message. Use empathetic language ("we want to resolve this") without causation language ("we caused this"). All fault admissions should be through insurance carrier or legal counsel only.

---

## SECTION 3: Shine & Share Referral Program

Generate a complete referral program including:

**Program Name:** Shine & Share

**Program Structure:**
- Existing customer refers a friend → both receive [REWARD] after the referred customer completes their first full-service detail
- Reward is applied as a credit/discount on next service — not cash (no money transmission issues)
- Referral is tracked via unique promo code or referral name at booking

**Marketing Copy (generate all of the following):**
1. In-shop card / receipt insert (100 words)
2. Post-delivery SMS message (160 char)
3. Email announcement to existing customer list (150-word body)
4. GBP / Facebook post announcing the program (150 words)
5. Instagram caption (100 words + 8 hashtags)

**FTC 2023 Compliance:**
- Reward is given for referral activity, not for review content — these are legally distinct
- Do not offer referral rewards contingent on the referred customer posting a review
- If referral is mentioned in any public testimonial or review, the reviewer must disclose the referral relationship
- Program terms must state: "No purchase necessary to refer. Referral credit applied to next qualifying service. [Business Name] reserves the right to modify or discontinue the program."

---

## SECTION 4: Fleet & Dealer Referral Program (if selected in inputs)

**Fleet Referral Structure:**
- Current customer introduces detailer to a fleet manager, property manager, dealership service director, or hotel fleet coordinator
- If the introduction results in a signed fleet agreement: referring customer receives [FLEET REWARD]
- Fleet reward: can be cash, check, or service credit (unlike consumer referrals, B2B introductions can include cash payment under most state laws — confirm with accountant)

**Generate:**
1. Fleet referral announcement to existing customer base (email, 200 words)
2. Introduction email template (for referring customer to forward to fleet contact) (150 words)
3. Thank-you note for completed referral (50 words — sent with reward)

**COMPLIANCE RULES — DO NOT VIOLATE:**

1. **FTC 2023 Endorsement Guides:** Referral rewards must be disclosed if the referring party posts a public review or social media content about the business. Include: "If you share your referral experience publicly, please disclose that you received a referral credit."

2. **No reward before review is posted:** Referral rewards are for introducing a customer — not for posting a specific review. These are legally distinct programs. Do not cross-link them.

3. **"Honest review" language:** All review request templates must include a variant of "we'd love to hear your honest feedback" — not "please leave us a 5-star review."

4. **Damage response:** First public response never admits fault. Insurance carrier is engaged before any written liability acknowledgment.

5. **Fleet cash referrals:** B2B referral cash payments are generally permissible but may trigger 1099-NEC if over $600/year to a single referrer. Include a note to confirm with accountant.
```
