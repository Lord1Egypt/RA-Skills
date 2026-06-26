# Prompt 2: Tax Season Campaign System

## Purpose
Generate a complete January 15 – April 15 (and October 15 extension) tax filing season campaign. All outputs comply with IRS Circular 230, AICPA solicitation rules, TCPA (SMS), CAN-SPAM (email), and FTC outcome-claim standards.

## Inputs Required

```
FIRM_NAME: [Your firm name]
CPA_LICENSE: [CPA license #]
PTIN: [PTIN or NONE]
TAX_SEASON_FOCUS: [Individual 1040 / Small business / Corporate / All]
STARTING_PRICE: [e.g., "$195 for individual returns" or "contact for pricing"]
SPECIAL_PROGRAMS: [e.g., IRS audit defense, back taxes, ITIN preparation, bilingual Spanish/English, same-day filing, virtual appointments, walk-in welcome]
SCHEDULING_METHOD: [Online booking link / phone / walk-in / all three]
CITY_STATE: [e.g., Las Vegas NV]
AUDIT_DEFENSE_ELIGIBLE: [Yes (CPA or EA on staff) / No]
```

## The Prompt

```
You are a professional services marketing copywriter specializing in accounting firm compliance.

Generate a complete tax season campaign for:

Firm: [FIRM_NAME]
License: [CPA_LICENSE] | PTIN: [PTIN]
Focus: [TAX_SEASON_FOCUS]
Starting price: [STARTING_PRICE]
Special programs: [SPECIAL_PROGRAMS]
Scheduling: [SCHEDULING_METHOD]
Location: [CITY_STATE]
Audit defense available: [AUDIT_DEFENSE_ELIGIBLE]

COMPLIANCE REQUIREMENTS:
1. All emails: CAN-SPAM compliant — unsubscribe link + physical address in footer
2. All SMS: TCPA compliant — "Reply STOP to opt out" in every message
3. No "guaranteed refund" or outcome promises anywhere
4. Audit defense copy: only if AUDIT_DEFENSE_ELIGIBLE=Yes; state "representation rights before the IRS" not "we'll beat the IRS for you"
5. No fabricated urgency (no "only 3 spots left" unless factually true)
6. Real deadlines ONLY: Jan 31 (W-2 deadline), Feb 15 (investment income forms), Apr 15 (filing deadline), Oct 15 (extension deadline)
7. CPA_LICENSE included in all ad copy
8. "Results may vary based on individual tax circumstances" on any claim referencing savings

Generate:

**1. Season Launch Announcement**
- Email (subject line + body, 200 words) — announces season opening, services, scheduling
- Social media post (Instagram/Facebook, 150 words) — season launch
- Google Business Profile post (1500 chars) — includes services and appointment CTA

**2. 3-Email Deadline Urgency Sequence**
Email 1 — Send February 1:
Subject (A/B test: 2 options)
Body (150 words): W-2s are out, time to schedule, what documents to bring
CTA: [SCHEDULING_METHOD]

Email 2 — Send March 15:
Subject (A/B test: 2 options)
Body (150 words): One month left, common last-minute mistakes, scheduling still open
CTA: [SCHEDULING_METHOD]

Email 3 — Send April 1:
Subject (A/B test: 2 options)
Body (100 words): 2 weeks left, last chance to avoid extension, what happens if you extend
CTA: [SCHEDULING_METHOD]

All emails: CAN-SPAM footer (firm name, address, unsubscribe link placeholder)

**3. SMS Appointment Reminder Sequence**
Message 1 (appointment confirmed, sent immediately after booking):
160 chars max. Confirm date/time, what to bring, firm name + STOP opt-out.

Message 2 (24-hour reminder):
160 chars max. Reminder of appointment, bring documents list, STOP opt-out.

Message 3 (same-day reminder, sent 2 hours before):
160 chars max. "Today at [time]" reminder, parking/directions note, STOP opt-out.

**4. Google Local Services Ad Profile Optimization**
Suggested profile fields for "Tax Preparer" Google LSA category:
- Business name and license # display
- Service types (individual, small business, etc.)
- Credential badges to enable (CPA, EA)
- Photo caption suggestions (office, not client-identifying)
- Q&A seed content (5 questions + answers, no outcome promises)

**5. Facebook Event Ad — Tax Deadline Urgency**
Headline (40 chars) + Primary text (125 chars) + Description (30 chars) + CTA
Theme: Deadline is real; appointment-based urgency (limited slots = real capacity constraint)
Compliance: no fake scarcity, real deadline date only

**6. Audit Defense Add-On Upsell Email** (only if AUDIT_DEFENSE_ELIGIBLE=Yes)
Subject (2 A/B options) + Body (150 words)
Key language rules:
- "Representation rights before the IRS" (Circular 230 § 10.3 — only CPAs and EAs have unlimited representation rights)
- "If you receive an IRS notice" (not "when" — no scare tactics)
- No promises of outcome ("we'll fight for you" is fine; "we'll win" is not)
- Price for audit response letter vs. full representation (tiered offering)

**7. Extension Season Campaign** (send September 1 for October 15 deadline)
Email 1 (September 1): "Your extension deadline is October 15" + what you still need to file
Email 2 (October 1): "2 weeks to go" + what happens if you miss the extension deadline
SMS (October 8): 160-char reminder, STOP opt-out

Format with clear section headers. Include a compliance checklist at the end.
```

## Compliance Notes

- AICPA Rule 503 prohibits "uninvited in-person solicitation" of prospective clients — email/digital marketing to opted-in contacts is permitted
- IRS Circular 230 § 10.30 applies to communications with clients/prospective clients; marketing copy that makes specific tax advice claims could be regulated
- TCPA: Text message marketing requires prior express written consent — add consent checkbox to appointment booking form
- Nevada NRS 228.550-228.600: Nevada-specific consumer protection rules for tax preparers — no deceptive pricing
- FTC Operation Hidden Fees guidance: advertised prices must be the actual price (no surprise fees not disclosed in ads)
