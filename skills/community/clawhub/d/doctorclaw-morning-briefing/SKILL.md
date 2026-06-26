---
name: morning-briefing
description: "Daily morning briefing — emails, calendar, tasks, and weather in one summary. Cron or on-demand."
version: 1.0.0
tags: [productivity, daily, briefing, email, calendar]
metadata:
  clawdbot:
    emoji: "🌅"
source:
  author: DoctorClaw
  url: https://www.doctorclaw.ceo
---

# Morning Briefing

Start your day with a single summary of everything that matters. This skill pulls your unread emails, today's calendar, pending tasks, and local weather into one concise briefing — delivered to your Telegram, Discord, or saved as a daily file.

Run it on a cron every morning, or trigger it on-demand whenever you need a status check.

## What You Get

- Unread email summary (count + top 5 by priority)
- Today's calendar events with times and locations
- Pending tasks or reminders from your task system
- Local weather forecast (temperature, conditions, rain probability)
- All in one message — no switching between 4 different apps

## Setup

### Required
- **Email access** — Gmail (via Gmail API/skill) or any email provider your agent can read
- **Calendar access** — Google Calendar API or Apple Calendar

### Optional (but recommended)
- **Weather** — No API key needed. Your agent can fetch weather from any free source (wttr.in, Open-Meteo, etc.)
- **Task system** — If you use a task manager (Todoist, Asana, Notion, plain text files), tell your agent where tasks live
- **Delivery channel** — Telegram bot, Discord bot, or file output. If no channel is configured, the briefing is saved to `memory/briefings/YYYY-MM-DD.md`

### Configuration

Tell your agent these preferences (it will store them in memory):

1. **Your timezone** — so the cron fires at the right local time
2. **Briefing time** — when you want it (default: 7:30 AM local)
3. **Email account** — which inbox to scan
4. **Calendar** — which calendar(s) to check
5. **Weather location** — your city or zip code
6. **Delivery** — where to send the briefing (Telegram, Discord, file)
7. **Format preference** — concise (bullet points) or detailed (with email previews)

## How It Works

When triggered (by cron or on-demand), your agent executes this workflow:

### Step 1: Gather Email
- Check your inbox for unread messages
- Count total unread
- Identify the top 5 by sender importance and subject urgency
- For each: sender name, subject line, 1-sentence preview
- Flag anything that looks urgent (keywords: urgent, ASAP, deadline, overdue, payment)

### Step 2: Gather Calendar
- Pull today's events from your calendar
- For each: event name, start time, end time, location (if any), attendees count
- Highlight the next upcoming event with a countdown ("Team standup in 45 minutes")
- Note any conflicts (overlapping events)

### Step 3: Gather Tasks
- Check your task system for items due today or overdue
- List up to 5 most important tasks
- Note any overdue items with how many days overdue
- If no task system is configured, skip this section

### Step 4: Gather Weather
- Fetch today's weather for the configured location
- Include: current temperature, high/low, conditions (sunny/cloudy/rain), precipitation probability
- Add a practical note if relevant ("Bring an umbrella — 80% chance of rain after 3 PM")

### Step 5: Compile & Deliver
Compile everything into a clean briefing format:

```
🌅 Morning Briefing — [Day, Month Date]

📧 EMAIL (X unread)
• [Sender] — [Subject] (preview)
• [Sender] — [Subject] (preview)
• [Sender] — [Subject] (preview)
🔴 [X] flagged as urgent

📅 CALENDAR
• 9:00 AM — Team standup (Google Meet)
• 11:30 AM — Client call with [Name] (Zoom)
• 2:00 PM — Dentist appointment
⏰ Next up: Team standup in 45 minutes

✅ TASKS
• [Task 1] — due today
• [Task 2] — due today
• [Task 3] — 2 days overdue ⚠️

🌤️ WEATHER — [City]
72°F / 22°C — Partly cloudy
High 78° Low 65° | Rain: 10%

Have a great day! ☕
```

Send via configured delivery channel, or save to `memory/briefings/YYYY-MM-DD.md`.

### Step 6: Schedule (Cron Setup)
Set up a cron job to run this briefing every morning:

- **Schedule:** Daily at configured time (default 7:30 AM local)
- **Task:** Run morning briefing workflow
- **Output:** Deliver to configured channel

Your agent should use its cron/scheduling system (LaunchAgents on Mac, cron on Linux, or the agent's built-in scheduler) to trigger this automatically.

## Examples

**User:** "Give me my morning briefing"

**Agent runs the workflow and responds:**

> 🌅 Morning Briefing — Monday, March 10
>
> 📧 EMAIL (12 unread)
> • Sarah Chen — Q1 Budget Review (needs your approval by EOD)
> • Mike Torres — Updated contract draft (3 attachments)
> • Newsletter — TechCrunch Daily (skip)
> 🔴 1 flagged as urgent: Sarah's budget review
>
> 📅 CALENDAR
> • 9:30 AM — Product sync (Google Meet, 6 attendees)
> • 1:00 PM — Lunch with Dave (The Mill, downtown)
> • 3:00 PM — Investor update prep (45 min block)
> ⏰ Next up: Product sync in 1 hour 15 minutes
>
> ✅ TASKS
> • Send revised proposal to Acme Corp — due today
> • Review PR #247 — due today
> • Follow up with Lisa re: partnership — 1 day overdue ⚠️
>
> 🌤️ WEATHER — San Francisco
> 58°F / 14°C — Foggy, clearing by noon
> High 64° Low 52° | Rain: 5%

---

**User:** "Set up my morning briefing for 6:45 AM every day on Telegram"

**Agent:** Configures cron for 6:45 AM, sets Telegram as delivery, confirms:
> "Morning briefing scheduled for 6:45 AM daily. I'll send it to your Telegram. You'll get your first one tomorrow morning."

## Customization Ideas

- **Add news headlines** — include top 3 stories from your industry
- **Add stock/crypto prices** — if you track specific tickers
- **Add team updates** — pull from Slack/Discord channels
- **Weekend mode** — different format on Sat/Sun (skip work email, add fun stuff)
- **Travel mode** — include flight status, hotel info, local tips when traveling

## Want More?

This skill gives you a solid daily briefing. But if you want:

- **Custom integrations** — connect to your CRM, project management tool, invoicing system, or any API your business uses
- **Advanced automations** — briefings that trigger actions (auto-reply to urgent emails, create tasks from calendar items, send reminders to your team)
- **Full system setup** — identity, memory, security, and 5 custom automations built specifically for your workflow

**DoctorClaw** sets up complete OpenClaw systems for businesses:

- **Guided Setup ($495)** — 2-hour live walkthrough. Everything configured, integrated, and running by the end of the call.
- **Done-For-You ($1,995)** — 7-day custom build. 5 automations, 3 integrations, full security, 30-day support. You do nothing except answer a short intake form.

→ [doctorclaw.ceo](https://www.doctorclaw.ceo)
