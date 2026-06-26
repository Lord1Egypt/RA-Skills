# Prompt 2 — Patient Communication & Retention System

## Purpose
Generate a complete patient lifecycle communication system: onboarding sequence, reactivation, front desk scripts, and end-of-care transition.

---

## Prompt

```
You are a healthcare retention specialist for chiropractic and physical therapy practices. Generate a complete patient communication and retention system. All outputs must be HIPAA-compliant: no diagnosis, condition, body part, treatment type, or insurance status in any email subject line or SMS. Patient consent for marketing is assumed — all sequences include unsubscribe/STOP options.

**Practice name:** [PRACTICE NAME]
**Provider name(s) and credentials:** [e.g., Dr. James Okafor DC, CCSP]
**Specialties:** [e.g., auto injury, sports, family wellness]
**Average visit frequency:** [e.g., 2x/week acute, 1x/week maintenance]
**Maintenance/wellness care offered:** [yes/no + brief description]
**Payment options:** [e.g., insurance + cash, cash-pay only, PI liens, payment plans]

---

**OUTPUT 1: NEW PATIENT WELCOME SEQUENCE (5 emails)**

Email 1 — Appointment Confirmation (send immediately)
- Subject: "You're confirmed, [First Name]! Here's what to bring" (HIPAA-safe: no clinical info)
- Body: confirmation details, what to wear, intake form link, parking, what to expect
- Length: 150-200 words
- Footer: physical address, unsubscribe link

Email 2 — Intake Prep (send 24 hours before first visit)
- Subject: "Quick prep for tomorrow, [First Name]" (HIPAA-safe)
- Body: intake form reminder, 3 things to tell us, what the first visit looks like, how to contact us with questions
- Length: 150-200 words

Email 3 — First Visit Follow-Up (send same day or next morning)
- Subject: "Great meeting you, [First Name]" (HIPAA-safe: no reference to what was treated)
- Body: next appointment reminder, 1-2 self-care tips (general, not diagnosis-specific), how to reach us
- Length: 100-150 words

Email 4 — Care Plan Check-In (send at session 4-6)
- Subject: "How are you feeling, [First Name]?" (HIPAA-safe)
- Body: check-in on progress, reinforce care plan value, ask if any questions, referral ask (soft)
- Length: 100-150 words

Email 5 — Milestone Celebration (send at session 10 or 1-month mark)
- Subject: "One month in, [First Name] — look how far you've come" (HIPAA-safe)
- Body: celebrate the commitment, reinforce progress concept (general), introduce maintenance care option, referral ask
- Length: 150-200 words

HIPAA subject line test for all 5: Does the subject reveal any health condition, treatment, or reason for visit? If yes, rewrite.

---

**OUTPUT 2: LAPSED PATIENT REACTIVATION CAMPAIGN**

Touch 1 — 6-Month Lapse Email
- Subject: "We miss you, [First Name]" (HIPAA-safe)
- Body: friendly reconnect, what's new at the practice, seasonal wellness angle, easy scheduling CTA
- Length: 120-150 words
- PS line: note any seasonal special or new service

Touch 2 — Lapse Phone Script (for front desk outreach at 9-month mark)
- Opening: "Hi, may I speak with [First Name]? This is [Name] from [Practice Name] — I'm just calling to check in, not to pressure you at all."
- Transition: "We noticed it's been a while since your last visit. We just wanted to make sure you're doing well."
- Offer: "[Optional: we have a [reactivation offer] this month if you've been thinking about coming back]"
- Close: "No worries either way — we're always here when you need us. Have a great day."
- Objection A: "I've been feeling fine" → "That's great to hear! A lot of our patients come in for maintenance to stay that way. No pressure at all."
- Objection B: "I'm not sure if I need it" → "Totally understand. Our initial re-eval is [price/free] — it's just a check-in, no commitment."

Touch 3 — 12-Month Final Reactivation Email
- Subject: "Still here for you, [First Name]" (HIPAA-safe, warm closing tone)
- Body: genuine "we're always here" message, no guilt, seasonal wellness angle, easy scheduling
- Length: 100 words max
- No further outreach after this touch unless patient re-engages

---

**OUTPUT 3: FRONT DESK OBJECTION SCRIPTS (5 scripts, word-for-word)**

Script 1 — "I don't have insurance coverage / my insurance doesn't cover this"
Opening: "I completely understand — insurance can be really frustrating. Let me tell you what your options are here..."
- Cash-pay rate disclosure (transparent pricing)
- Payment plan framing: "A lot of our patients do [X visits] on a payment plan at $[X]/visit — it comes out to about $[X] per week"
- FSA/HSA mention if applicable
- No-pressure close: "Would it help to book just the first visit and see how it goes?"

Script 2 — "I need a referral from my doctor first"
Opening: "That's a really common question — the good news is, in [state], you can come see us directly."
- Direct access law explanation (state-specific — PT in most states, DC in all states)
- When a referral IS needed (Medicare, some insurance plans) — be honest
- "If you do want to loop in your doctor, we're happy to coordinate — but you don't have to wait."
- Close: "Want me to check your insurance to confirm before we book?"

Script 3 — "I tried chiropractic/PT before and it didn't help"
Opening: "I really appreciate you telling me that — and I want to be honest with you."
- Empathy first: "It sounds like that experience was frustrating, and that's valid."
- Differentiation without disparaging: "Every provider has a different approach. We'd love to hear what you tried and what your specific goal is — and if we don't think we're the right fit, we'll tell you."
- No guarantees: "I can't promise a specific outcome, but I can promise we'll be honest with you about what we think will help."
- Close: "Would you be open to a free 15-minute call with Dr. [Name] before committing to anything?"

Script 4 — "I just need some exercises I can do at home"
Opening: "We love hearing that — that's actually part of what we do."
- Scope clarification: "We'll definitely build you a home program. The question is whether that's all you need, or whether there's something we should address first so the exercises actually work."
- Reframe: "Think of it like this — if you're training for a 5K but you have a knee issue, running more won't fix it. We want to find out if there's something underlying before we give you the program."
- Close: "A first eval is $[X] — it's basically a roadmap for your home program. Want to start there?"

Script 5 — "My pain is mostly gone / I think I'm fine"
Opening: "That's great news — and that's actually the perfect time to talk about what's next."
- Explain the discharge → wellness transition concept
- No fear-based language: "We're not trying to keep you coming in if you don't need it."
- Maintenance care value framing: "Some patients come in once a month as a tune-up — it costs about the same as a gym membership and keeps them from ending up back in acute care."
- Respect their choice: "Whatever you decide, you can always call us. We'd rather have you come back when you need us than feel like we pushed you into something."

---

**OUTPUT 4: APPOINTMENT REMINDERS (HIPAA-safe)**

48-hour email reminder:
- Subject: "Your appointment at [Practice Name] on [Day], [First Name]"
- Body: date, time, provider, address, cancel/reschedule link, what to bring reminder
- NO clinical content

2-hour text reminder (160 chars):
"Hi [First Name]! Reminder: appt at [Practice] today at [TIME]. Reply STOP to opt out. Questions? Call [PHONE]."

---

**OUTPUT 5: END-OF-CARE TRANSITION SCRIPT**

For discharge conversation (not email — verbal/in-person):
"[First Name], I want to talk to you about where you are in your care. Based on your progress, I think we've hit the goals we set out to reach — which is great. I want to go over your options for what comes next."

Present 3 paths:
1. Formal discharge + home program: "You're doing great and the exercises I've given you should keep you there."
2. Wellness/maintenance care: "Some patients find that coming in once a month keeps them from flaring up — it's about [cost/session]."
3. Return-to-care condition: "If [general symptom — no diagnosis language] comes back or flares up, just call us. We can get you in same week."

Do NOT use fear-based language. Do NOT pressure into maintenance care. ACA/APTA ethics: recommend only what is clinically appropriate.
```

---

## Usage Notes

- The front desk objection scripts are often the highest-ROI output for retention — practices report 20-40% of new patients are lost at the front desk
- Scripts 1-5 should be laminated or posted at the front desk
- All email sequences: ensure HIPAA compliance before importing to email platform (Mailchimp, Constant Contact, etc.) — subject lines must never reveal clinical information
