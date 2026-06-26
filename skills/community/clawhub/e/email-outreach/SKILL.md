---
name: email-outreach
description: Automated email outreach campaign builder and optimizer. Use when asked to write cold emails, build outreach sequences, create follow-up cadences, personalize email templates at scale, audit existing email copy for deliverability and response rates, generate subject line variants, or build lead lists. Triggers on phrases like "cold email", "outreach sequence", "email campaign", "follow-up emails", "personalize emails", "email templates", "improve open rates", "sales emails", "lead outreach".
---

# Email Outreach Skill

Build high-converting email outreach sequences. Every output should be ready to send — no filler, no fluff.

## Workflow

### 1. Understand the Campaign
Gather (ask if not provided):
- **Sender context**: Who are you? What's your offer?
- **Target persona**: Job title, industry, company size, pain points
- **Goal**: Book a call / get a reply / drive to a link
- **Sequence length**: 1 shot or multi-touch (recommend 4–6 touch cadence)

### 2. Build the Sequence
Use the frameworks in `references/copywriting-frameworks.md`.

Standard high-converting structure:
- **Email 1 (Day 1)**: Pattern interrupt opener + specific problem + one-line offer + soft CTA
- **Email 2 (Day 3)**: Social proof / case study angle + question CTA
- **Email 3 (Day 7)**: Different angle / objection pre-empt + value add (resource/insight)
- **Email 4 (Day 14)**: Breakup email — short, direct, creates urgency

### 3. Personalization Variables
Build templates with `{{variables}}` for mail-merge personalization:
- `{{first_name}}`, `{{company}}`, `{{industry}}`, `{{pain_point}}`, `{{recent_news}}`
- Generate 3 "custom first line" variants they can rotate per segment

### 4. Subject Line Variants
Generate 5 subject line options per email:
- Question format
- Curiosity gap
- Direct/transactional
- Name/company personalized
- Contrarian/pattern interrupt

### 5. Deliverability Check
Run `scripts/deliverability_check.py` against the email copy to flag:
- Spam trigger words
- HTML-heavy formatting risks
- Link-to-text ratio issues
- Subject line length (40–60 chars ideal)
- Preheader text presence

### 6. Output Format
Deliver as:
- Numbered sequence with day gaps labeled
- Each email: Subject | Preheader | Body | CTA
- Personalization notes per email
- A/B test recommendations

See `references/copywriting-frameworks.md` for proven frameworks (AIDA, PAS, Before/After/Bridge).
See `assets/sequence-template.md` for a ready-to-copy campaign template.
