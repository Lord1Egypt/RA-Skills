---
name: founder-briefing
description: Generate real-estate buyer lead follow-up plans from open house notes, inquiry messages, or CRM exports. Use when the user asks to prioritize leads, write personalized SMS/email follow-ups, handle objections, or produce a 7-day cadence to book buyer appointments.---

# Real Estate Buyer Follow-Up Pro

## Overview

Turn messy open house notes and lead messages into a structured follow-up system that helps buyer agents book more appointments. Focus on speed, clarity, personalization, and next best action.

## Workflow

1. Parse all lead inputs (notes, texts, emails, form submissions, CRM snippets).
2. Classify each lead as Hot / Warm / Cold using urgency and intent signals.
3. Extract known details: timeline, budget, preferred areas, financing status, objections.
4. Generate personalized communication for each lead:
- First-touch SMS
- First-touch email
- Follow-up replies for common objections
5. Build a 7-day follow-up cadence with exact daily actions.
6. Output a concise action board so the agent knows exactly who to contact first.

## Lead Priority Rules

Classify as **Hot** if 2+ signals are present:
- Wants to tour this week
- Pre-approved or cash buyer
- Specific area + budget + timeline given
- Replied within last 24h

Classify as **Warm** if:
- Some intent but incomplete details
- Timeline is “next few months”
- Engaged but not ready to schedule

Classify as **Cold** if:
- No clear timeline, low responsiveness
- Vague inquiry with no follow-up behavior

If data is missing, mark as “Needs Data” and ask for specific missing fields.

## Output Format (always use)

### 1) Priority Queue
- Hot: ...
- Warm: ...
- Cold: ...

### 2) Lead-by-Lead Follow-Up Kit
For each lead include:
- Summary (1-2 lines)
- First SMS draft
- First email draft
- Objection reply draft (if needed)
- Next-best action

### 3) 7-Day Cadence
- Day 0:
- Day 1:
- Day 3:
- Day 5:
- Day 7:

### 4) CRM Paste Block
Provide compact bullets for copy/paste into CRM notes:
- Status:
- Timeline:
- Key pain point:
- Last contact:
- Next action:

## Writing Rules

- Keep messages short, human, and local-market friendly.
- Never fabricate facts about listings, rates, or financing.
- Do not use hype or spammy language.
- Separate known facts from assumptions.
- If uncertainty exists, label it clearly as "Unverified".

## Example User Prompts

- “Turn these open house notes into follow-up texts and emails.”
- “Rank these leads and give me a 7-day follow-up plan.”
- “Write objection replies for buyers saying they want to wait for rates.”
- “Convert this CRM export into hot/warm/cold and next actions.”