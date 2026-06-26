---
name: ai-cold-email-linkedin-generator
description: >
  Generates high-reply-rate cold emails, LinkedIn DMs, follow-up sequences,
  and A/B test variants for B2B sales outreach. Use this skill whenever the
  user wants to write cold outreach, sales emails, LinkedIn messages, follow-up
  emails, prospecting copy, or any kind of outbound sales communication.
  Always trigger for any task involving outbound messaging, SDR/BDR workflows,
  lead generation copy, or sales prospecting — even when phrased casually,
  such as "help me reach out to leads", "write me a sales email",
  "draft a LinkedIn message", or "I need to contact prospects".
license: MIT-0
user-invocable: true
disable-model-invocation: false
compatibility:
  - claude-sonnet-4-20250514
  - claude-opus-4-20250514
  - claude-haiku-4-5-20251001
argument-hint: >
  Provide: product/service description, target audience, pain points,
  your offer or CTA, sender name and role. Optionally include prospect name,
  prospect company, a personalization hook, preferred tone
  (friendly_professional / direct_confident / curious_consultative / casual_peer),
  and which outputs to generate
  (cold_email / linkedin_dm / followup_1 / followup_2 / ab_variants).
metadata:
  category: Sales & Marketing
  subcategory: Outbound Sales
  version: 1.2.0
  author: ClawHub Skill Publisher
  language: en
  tags:
    - cold-email
    - linkedin
    - outreach
    - sales
    - lead-generation
    - copywriting
    - follow-up
    - B2B
    - GTM
    - SDR
---

# AI Cold Email & LinkedIn Outreach Generator

Generate complete B2B outreach sequences — personalized, human-sounding, and
optimized for reply rate. No templates. No "hope this finds you well." Just
copy that actually gets responses.

---

## What This Skill Does

Given a product, audience, and context, this skill generates:

- **Cold Email** — two subject line options + body copy under 120 words
- **LinkedIn DM** — conversational message under 80 words
- **Follow-Up #1** — sent 3–5 days after initial outreach, adds new value
- **Follow-Up #2** — short final bump at day 7–10, leaves the door open
- **A/B Test Variants** — two cold email versions with different angles
  (pain-led vs. outcome/curiosity-led)

All output sounds like a real human wrote it at 8am — not a robot.

---

## Skill Files

```
ai-cold-email-linkedin-generator/
├── SKILL.md       ← You are here
├── manifest.json  ← Deployment metadata
├── prompt.txt     ← Core generation logic
├── config.json    ← Input field definitions
└── README.md      ← End-user documentation
```

---

## When to Trigger This Skill

Trigger immediately when the user says anything like:

- "write me a cold email" / "sales email" / "outreach email"
- "help me reach out to leads / prospects / clients"
- "draft a LinkedIn message / DM / InMail"
- "I need outreach copy" / "prospecting copy"
- "SDR templates" / "BDR outreach" / "cold outreach sequence"
- "follow up on my cold email" / "write a follow-up"
- "write a breakup email" / "closing the loop email"
- "A/B test my outreach" / "two versions of my email"
- Mentions Apollo, Instantly, Lemlist, Outreach, Salesloft, or LinkedIn Sales Navigator

---

## Required Inputs

Collect all required fields in a **single ask** — do not ask one at a time.

| Field | Required | Description |
|---|---|---|
| `product_service` | ✅ | What you sell — be specific |
| `target_audience` | ✅ | Job title, company type, size |
| `pain_points` | ✅ | 1–3 real problems the prospect faces |
| `offer` | ✅ | The single CTA (demo, call, question) |
| `sender_name` | ✅ | Your name |
| `sender_role` | ✅ | Your title and company |
| `prospect_name` | Optional | Adds personalization |
| `prospect_company` | Optional | Adds personalization |
| `personalization_hook` | Optional | A recent post, news item, or observation |
| `tone` | ✅ | One of four presets (see below) |
| `output_type` | ✅ | Which formats to generate |

### Tone Presets

| Value | Description |
|---|---|
| `friendly_professional` | Warm but credible. Like a trusted advisor. **(Default)** |
| `direct_confident` | No fluff. 3 punchy sentences. |
| `curious_consultative` | Question-led. Low pressure. |
| `casual_peer` | Founder-to-founder. Very short. Could be from a phone. |

### Output Type Options

| Value | What It Generates |
|---|---|
| `cold_email` | Email with two subject line options |
| `linkedin_dm` | LinkedIn message under 80 words |
| `followup_1` | Follow-Up #1 (day 3–5) |
| `followup_2` | Follow-Up #2 / Final Bump (day 7–10) |
| `ab_variants` | Two cold email variants for split testing |

---

## Generation Rules (Enforced in prompt.txt)

### Hard Word Limits
- Cold emails: **120 words maximum**
- LinkedIn DMs: **80 words maximum**
- Follow-Up #1: **6 lines maximum**
- Follow-Up #2: **4 lines maximum**
- One CTA per message only

### Banned Phrases (Never Use)
> "I hope this email finds you well" · "I wanted to reach out" · "synergy" ·
> "leverage" · "circle back" · "touch base" · "game-changer" · "revolutionary" ·
> "cutting-edge" · "seamlessly" · "disruptive" · "innovative solution"

### Spam Filter Rules
- No links in cold emails
- No trigger words: "free", "guarantee", "no obligation", "act now", "limited time"
- Subject lines: 3–7 words, lower-case preferred, no emojis or exclamation marks

### Human Tone Rules
- Use contractions: we're, I've, it's, you'll
- Vary sentence length — short punchy lines mixed with longer ones
- Lead with the prospect's world, not your product
- Every message ends with a clear, easy-to-answer question

---

## Output Format

```
📧 COLD EMAIL
  Subject Line A: ...
  Subject Line B: ...
  [body — plain text, no bullets, no bold]
  [signature]

💼 LINKEDIN DM
  [conversational message, no formal sign-off]

🔁 FOLLOW-UP #1
  Subject: Re: ...
  [4–6 lines, new value or social proof]
  [signature]

🔁 FOLLOW-UP #2
  Subject: Closing the loop
  [2–4 lines, leave door open]
  [signature]

🧪 A/B TEST VARIANTS
  Version A — Pain-Led Opening
  Version B — Outcome/Curiosity-Led Opening
```

---

## Example

**Input:**
```
Product: AI scheduling tool that auto-books meetings from email threads
Audience: Chiefs of Staff at 200–1000 person companies
Pain: 2–3 hours/day on scheduling back-and-forth
Offer: 10-minute live demo on their real calendar
Sender: Jordan Kim, Co-founder at ScheduleAI
Prospect: Maria at Vercel
Hook: Saw her LinkedIn post about async work last week
Tone: Friendly & Professional
Output: Cold Email + LinkedIn DM
```

**Cold Email:**

Subject Line A: `the scheduling tax at vercel`
Subject Line B: `2 hours a day on calendar back-and-forth?`

Maria,

Saw your post about async work last week — completely agree. One async killer
that doesn't get enough attention: scheduling. The 6-email thread just to find
a 30-min slot.

We built ScheduleAI for that. It reads email threads and books meetings
automatically — no back-and-forth, no links, no time zone math. Teams like
yours are recovering 2–3 hours a week per person.

Worth a 10-minute look? I can demo it on your actual calendar.

Jordan Kim
Co-founder, ScheduleAI

---

**LinkedIn DM:**

Maria — your post about async work resonated. Scheduling is the silent async
killer most people don't fix.

We built a tool that books meetings straight from email threads — zero
back-and-forth. Teams are saving 2+ hours a week.

Would it be useful to see a quick demo on your actual calendar?

---

## Compatible Platforms

Apollo.io · Instantly.ai · Lemlist · Smartlead · Outreach.io · Salesloft ·
HubSpot Sequences · Gmail · Outlook · LinkedIn Sales Navigator

---

## Limitations

- Generates copy only — does not send emails or connect to platforms
- Personalization quality depends on the hook you provide
- Always review before sending — AI copy is a strong starting draft
- Do not use for bulk unsolicited email in violation of CAN-SPAM, GDPR, or CASL

---

## Changelog

| Version | Date | Notes |
|---|---|---|
| 1.2.0 | 2026-03-22 | Fixed frontmatter, A/B variants, tone presets, follow-up sequence |
| 1.0.0 | 2026-01-10 | Initial release |
