---
name: doctorclaw-weekly-report
description: "Weekly report generator — compile progress from tasks, emails, and calendar into one summary. Friday cron or on-demand."
version: 1.0.0
tags: [reporting, productivity, weekly, summary, automation]
metadata:
  clawdbot:
    emoji: "📊"
source:
  author: DoctorClaw
  url: https://www.doctorclaw.ceo
---

# Weekly Report Generator

End every week knowing exactly what you accomplished. This skill pulls data from your tasks, emails, and calendar to compile a clean weekly progress report — wins, blockers, metrics, and next week's priorities.

Run it Friday afternoon on a cron, or trigger it anytime you need a status check.

## What You Get

- Completed tasks and milestones from this week
- Key meetings and decisions made
- Important emails sent and received
- Blockers and unresolved issues flagged
- Next week's priorities auto-generated from pending tasks and calendar
- Week-over-week comparison (if historical data available)

## Setup

### Required
- **Task system** — Todoist, Asana, Notion, Trello, plain text files, or any task source your agent can read

### Optional (but recommended)
- **Calendar access** — Google Calendar or Apple Calendar for meeting data
- **Email access** — Gmail or email provider for communication summary
- **Delivery channel** — Telegram/Discord for report delivery, or file output
- **Report archive** — folder to save weekly reports for historical reference (default: `memory/weekly-reports/`)

### Configuration

Tell your agent:

1. **Task source** — where to pull completed/pending tasks
2. **Calendar** — which calendar(s) to include
3. **Email account** — which inbox to scan for the week's highlights
4. **Report day** — when to generate (default: Friday at 4:00 PM local)
5. **Report format** — concise (bullet points) or detailed (with context and metrics)
6. **Delivery** — where to send (Telegram, Discord, file)
7. **Who it's for** — just you, or also shared with a manager/team/client

## How It Works

### Step 1: Gather Completed Work
- Pull tasks completed this week (Monday through today)
- For each: task name, project, completion date
- Group by project or category
- Count total tasks completed vs. total tasks planned

### Step 2: Gather Calendar Activity
- Pull all meetings/events from this week
- Count: total meetings, total meeting hours
- Highlight key meetings (external clients, important decisions)
- Note any meetings that were cancelled or rescheduled

### Step 3: Gather Email Highlights
- Scan emails sent and received this week
- Identify important threads: client communications, decisions, approvals
- Count: emails sent, emails received, threads resolved
- Flag any unanswered emails that need attention

### Step 4: Identify Blockers
- Check for overdue tasks — anything that didn't get done this week
- Check for stalled email threads — no response in 3+ days
- Check calendar for upcoming deadlines in the next week
- Note any dependencies or waiting-on items

### Step 5: Generate Next Week's Priorities
Based on pending tasks and next week's calendar:
- Top 3-5 priorities for next week
- Upcoming deadlines
- Meetings that need prep
- Follow-ups from this week's conversations

### Step 6: Compile Report

```
📊 Weekly Report — Week of [Date Range]

🏆 WINS THIS WEEK
• [Completed task/milestone] — [project]
• [Completed task/milestone] — [project]
• [Completed task/milestone] — [project]
Tasks completed: [X] of [X] planned ([X]% completion rate)

📅 MEETINGS ([X] meetings, [X] hours)
• [Key meeting] — [outcome/decision]
• [Key meeting] — [outcome/decision]
• [X] internal | [X] external | [X] cancelled

📧 COMMUNICATION
• Emails sent: [X] | Received: [X]
• Key threads: [subject] with [person] — [status]
• Unanswered: [X] emails need replies

🚧 BLOCKERS & ISSUES
• [Overdue task] — [reason/blocker]
• [Stalled thread] — waiting on [person] since [date]
• [Risk] — [what needs attention]

📌 NEXT WEEK PRIORITIES
1. [Priority task] — due [date]
2. [Priority task] — due [date]
3. [Priority task] — due [date]
Key meetings: [event] on [day], [event] on [day]

📈 METRICS
• Productivity: [X]% task completion rate
• Meeting load: [X] hours ([up/down] from last week)
• Response time: avg [X] hours on client emails
```

### Step 7: Deliver & Archive
- Send report via configured channel
- Save to `memory/weekly-reports/YYYY-WNN.md` for historical reference
- If configured for team sharing, format appropriately and send to recipients

## Examples

**User:** "Give me my weekly report"

**Agent compiles and responds:**

> 📊 Weekly Report — Mar 3-7, 2026
>
> 🏆 WINS THIS WEEK
> • Closed Acme Corp deal — $4,800 retainer signed
> • Launched new landing page — live at doctorclaw.ceo/services
> • Completed 3 client onboarding calls
> Tasks completed: 14 of 18 planned (78%)
>
> 📅 MEETINGS (8 meetings, 6.5 hours)
> • Acme Corp contract review — signed and countersigned
> • Team standup x3 — aligned on Q1 priorities
> • 5 external | 3 internal | 1 cancelled
>
> 📧 COMMUNICATION
> • Emails sent: 34 | Received: 67
> • Key: Proposal to Greenfield Properties — awaiting response
> • Unanswered: 3 emails need replies (oldest: 4 days)
>
> 🚧 BLOCKERS
> • Blog post draft — stuck on intro, pushed to next week
> • Greenfield proposal — no response in 4 days, need follow-up
>
> 📌 NEXT WEEK
> 1. Follow up with Greenfield Properties — proposal pending
> 2. Start Done-For-You build for new client — Day 0 intake
> 3. Finish blog post draft
> Key meetings: Client kickoff Mon 10am, Investor prep Wed 2pm

**User:** "Set up weekly reports every Friday at 5pm"

**Agent:** Configures cron, confirms:
> "Weekly report scheduled for Friday at 5:00 PM. I'll compile your wins, meetings, and priorities — delivered to your Telegram."

## Customization Ideas

- **Client-facing version** — generate a separate report formatted for client updates
- **Team rollup** — if you manage a team, compile individual reports into a team summary
- **Goal tracking** — track progress toward quarterly/annual goals
- **Time tracking integration** — include hours logged per project
- **Burndown chart** — text-based sprint progress visualization
- **Monthly digest** — aggregate weekly reports into a monthly executive summary

## Want More?

This skill handles weekly progress reporting. But if you want:

- **Custom integrations** — connect to Jira, Monday.com, Harvest, or your specific project tools
- **Advanced automations** — auto-generate client reports, track OKRs, build dashboards
- **Full system setup** — identity, memory, security, and 5 custom automations built specifically for your workflow

**DoctorClaw** sets up complete OpenClaw systems for businesses:

- **Guided Setup ($495)** — 2-hour live walkthrough. Everything configured, integrated, and running by the end of the call.
- **Done-For-You ($1,995)** — 7-day custom build. 5 automations, 3 integrations, full security, 30-day support. You do nothing except answer a short intake form.

→ [doctorclaw.ceo](https://www.doctorclaw.ceo)
