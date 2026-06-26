---
name: doctorclaw-meeting-prep
description: "Meeting prep — pull context on attendees, topics, and action items before every calendar event. Auto or on-demand."
version: 1.0.0
tags: [meetings, calendar, productivity, preparation, automation]
metadata:
  clawdbot:
    emoji: "📋"
source:
  author: DoctorClaw
  url: https://www.doctorclaw.ceo
---

# Meeting Prep

Walk into every meeting prepared. This skill scans your upcoming calendar events, pulls context on attendees (past emails, notes, deal stage), surfaces relevant documents, and compiles a prep brief — so you spend 2 minutes reviewing instead of 15 minutes scrambling.

Trigger it before a specific meeting or set it to auto-run 30 minutes before each event.

## What You Get

- Prep brief for each upcoming meeting with attendee context
- Relevant email threads and conversation history surfaced
- Open action items and pending tasks related to meeting topics
- Suggested talking points and questions
- Previous meeting notes pulled from memory

## Setup

### Required
- **Calendar access** — Google Calendar API, Apple Calendar, or any calendar your agent can read

### Optional (but recommended)
- **Email access** — Gmail or email provider to pull recent conversations with attendees
- **Contact/CRM context** — client list, CRM, or contact notes for attendee background
- **Task system** — Todoist, Asana, Notion, or text files for related action items
- **Meeting notes storage** — where to save post-meeting notes (memory, file, Notion)

### Configuration

Tell your agent:

1. **Calendar** — which calendar(s) to scan
2. **Prep lead time** — how far before the meeting to generate the brief (default: 30 minutes)
3. **Email lookback** — how far back to search for relevant emails (default: 30 days)
4. **Prep depth** — concise (bullet points) or detailed (full context with email excerpts)
5. **Auto-prep** — run automatically before each meeting, or only on-demand
6. **Delivery** — where to send the brief (Telegram, Discord, file, or inline)

## How It Works

### Step 1: Scan Calendar
- Pull upcoming events from the configured calendar
- For each event: title, start time, end time, location, attendees, description/agenda
- If auto-prep: focus on the next event within prep lead time
- If on-demand ("prep me for my 2pm call"): find the matching event

### Step 2: Research Attendees
For each attendee (excluding yourself):
- **Email history** — search inbox for recent threads with this person. Pull subject lines, last message date, any open questions
- **Contact notes** — check CRM or contact list for: company, role, deal stage, relationship notes
- **Meeting history** — search memory/notes for previous meeting notes mentioning this person
- **Action items** — check task system for open tasks related to this person or their company

### Step 3: Surface Context
- **Related documents** — find any shared docs, proposals, or files mentioned in recent emails with attendees
- **Open threads** — emails you haven't replied to from attendees
- **Pending deliverables** — tasks assigned to you that involve attendees
- **Last interaction** — when you last communicated and what about

### Step 4: Generate Talking Points
Based on the gathered context, suggest:
- **Follow-ups** — "You promised Dave the revised proposal last week — status?"
- **Questions to ask** — "Sarah mentioned budget concerns in her last email — address?"
- **Updates to share** — "The Q1 numbers are in — relevant to this discussion"
- **Decisions needed** — "Contract renewal is due Friday — get alignment today"

### Step 5: Compile Prep Brief
Format the brief:

```
📋 Meeting Prep — [Event Title]
⏰ [Start Time] - [End Time] | 📍 [Location/Link]

👥 ATTENDEES
• [Name] — [Role, Company]
  Last contact: [X days ago] — [subject/topic]
  Context: [deal stage, relationship note]
• [Name] — [Role, Company]
  Last contact: [X days ago] — [subject/topic]

📧 RELEVANT THREADS
• [Subject] — [date] — [status: awaiting reply / resolved]
• [Subject] — [date] — [status]

✅ OPEN ACTION ITEMS
• [Task] — assigned to you, related to [attendee]
• [Task] — due [date]

💡 SUGGESTED TALKING POINTS
1. [Follow up on X with attendee]
2. [Discuss Y — relates to open email thread]
3. [Decision needed on Z by Friday]

📝 PREVIOUS MEETING NOTES
[Summary of last meeting with these attendees, if found]
```

### Step 6: Deliver & Follow Up
- Send the prep brief via configured channel
- After the meeting: prompt user for quick notes ("How did the meeting go?")
- Save meeting notes to memory for future prep briefs
- Create any follow-up tasks mentioned

## Examples

**User:** "Prep me for my next meeting"

**Agent scans calendar and responds:**

> 📋 Meeting Prep — Client Check-in with Acme Corp
> ⏰ 2:00 PM - 2:30 PM | 📍 Zoom
>
> 👥 ATTENDEES
> • **Tom Bradley** — VP Operations, Acme Corp
>   Last contact: 5 days ago — discussed Q1 deliverables
>   Context: Active client, $4,800/mo retainer, up for renewal in April
> • **Sarah Kim** — Project Lead, Acme Corp
>   Last contact: 12 days ago — sent updated timeline
>
> 📧 RELEVANT THREADS
> • "Q1 Deliverables Update" — Mar 5 — awaiting Tom's feedback
> • "Timeline Revision v3" — Feb 26 — Sarah confirmed receipt, no response since
>
> ✅ OPEN ACTION ITEMS
> • Send revised SOW to Tom — due this week
> • Follow up with Sarah on design feedback — 5 days overdue
>
> 💡 SUGGESTED TALKING POINTS
> 1. Check if Tom reviewed Q1 deliverables — need his sign-off
> 2. Ask Sarah about design feedback (she's been quiet for 12 days)
> 3. Bring up April renewal — gauge interest in expanding scope
> 4. Mention the revised SOW is coming this week

**User:** "Good meeting. Tom approved Q1 deliverables. Sarah needs one more week on design. Renewal looks positive — they want to add social media management."

**Agent:** Saves meeting notes, creates tasks: "Send revised SOW to Tom (include social media scope)" and "Follow up with Sarah on design — due March 17." Updates contact notes.

---

**User:** "Auto-prep all my meetings tomorrow"

**Agent:** Generates briefs for each event, sends them the morning of or 30 minutes before each.

## Customization Ideas

- **Post-meeting summary** — auto-generate meeting minutes from your notes
- **Attendee LinkedIn lookup** — pull current role/company from LinkedIn for new contacts
- **Meeting analytics** — track how many meetings per week, with whom, duration trends
- **Agenda builder** — draft a formal agenda based on open items and send to attendees beforehand
- **No-show follow-up** — if someone doesn't join, auto-draft a reschedule email

## Want More?

This skill handles meeting prep and context surfacing. But if you want:

- **Custom integrations** — connect to your CRM, project management tool, or any API your business uses
- **Advanced automations** — auto-generate agendas, send prep docs to attendees, create post-meeting tasks
- **Full system setup** — identity, memory, security, and 5 custom automations built specifically for your workflow

**DoctorClaw** sets up complete OpenClaw systems for businesses:

- **Guided Setup ($495)** — 2-hour live walkthrough. Everything configured, integrated, and running by the end of the call.
- **Done-For-You ($1,995)** — 7-day custom build. 5 automations, 3 integrations, full security, 30-day support. You do nothing except answer a short intake form.

→ [doctorclaw.ceo](https://www.doctorclaw.ceo)
