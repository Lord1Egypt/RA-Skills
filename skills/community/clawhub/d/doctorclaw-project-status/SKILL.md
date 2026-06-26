---
name: doctorclaw-project-status
description: "Project status board — compile daily status from tasks, calendar, and team updates into one dashboard. Daily cron or on-demand."
version: 1.0.0
tags: [project-management, status, dashboard, tasks, automation]
metadata:
  clawdbot:
    emoji: "🏗️"
source:
  author: DoctorClaw
  url: https://www.doctorclaw.ceo
---

# Project Status Board

See all your projects at a glance. This skill pulls task progress, upcoming milestones, blockers, and team activity across all your active projects into one clean status board — so you always know what's on track, what's at risk, and what needs your attention.

Run it daily on a cron, or trigger it before any planning session or standup.

## What You Get

- All active projects with health status (on track, at risk, behind)
- Task completion progress for each project
- Upcoming milestones and deadlines
- Blockers and risks flagged per project
- Team workload summary (who's overloaded, who has capacity)
- Priority actions for today

## Setup

### Required
- **Task system** — Any task/project source: Todoist, Asana, Notion, Trello, Linear, plain text files, or CSV

### Optional (but recommended)
- **Calendar access** — for milestone dates and project-related meetings
- **Multiple project sources** — track projects across different tools
- **Team member list** — for workload analysis across team members
- **Delivery channel** — Telegram/Discord for daily status updates

### Configuration

Tell your agent:

1. **Project sources** — where to pull project/task data from
2. **Active projects** — which projects to track (or track all with open tasks)
3. **Status thresholds:**
   - On track: ≥80% of tasks on schedule
   - At risk: 60-79% on schedule
   - Behind: <60% on schedule
4. **Report schedule** — when to generate (default: every morning at 8:30 AM)
5. **Team members** — names and task assignments for workload analysis
6. **Delivery** — where to send the status board

## How It Works

### Step 1: Gather Project Data
For each active project:
- Pull all tasks: total, completed, in progress, not started, overdue
- Calculate completion percentage
- Identify upcoming deadlines (next 7 days)
- Find blocked or stalled tasks (no progress in 3+ days)

### Step 2: Assess Project Health
Rate each project:

**🟢 ON TRACK** — ≥80% of tasks on schedule, no critical blockers
**🟡 AT RISK** — 60-79% on schedule, or has blockers but they're manageable
**🔴 BEHIND** — <60% on schedule, critical blockers, or missed deadlines

### Step 3: Identify Blockers
For each project, flag:
- Tasks that are overdue with no progress
- Dependencies waiting on external parties
- Tasks assigned but not started (approaching due date)
- Resource conflicts (same person overloaded across projects)

### Step 4: Analyze Team Workload
If team members are configured:
- Count active tasks per person across all projects
- Flag overloaded team members (>10 active tasks)
- Identify capacity (team members with <3 active tasks)
- Note unassigned tasks that need owners

### Step 5: Compile Status Board

```
🏗️ Project Status Board — [Date]

📊 PORTFOLIO OVERVIEW
Active projects: [X] | 🟢 On track: [X] | 🟡 At risk: [X] | 🔴 Behind: [X]

━━ PROJECT: [Project Name] ━━━━━━━━━━━
Status: 🟢 ON TRACK
Progress: ████████░░ 78% (18/23 tasks)
Due: [milestone date]

✅ Completed this week: [X] tasks
🔄 In progress: [X] tasks
📌 Upcoming: [key milestone] — [date]
⚠️ Blockers: None

━━ PROJECT: [Project Name] ━━━━━━━━━━━
Status: 🟡 AT RISK
Progress: █████░░░░░ 52% (13/25 tasks)
Due: [milestone date]

✅ Completed this week: [X] tasks
🔄 In progress: [X] tasks
📌 Upcoming: [key milestone] — [date]
⚠️ Blockers:
  • Waiting on client approval for designs (3 days)
  • API integration delayed — dependency on vendor

━━ PROJECT: [Project Name] ━━━━━━━━━━━
Status: 🔴 BEHIND
Progress: ███░░░░░░░ 31% (8/26 tasks)
Due: [milestone date] — ⚠️ AT RISK OF MISSING

✅ Completed this week: [X] tasks
🔄 In progress: [X] tasks
⚠️ Blockers:
  • 5 tasks overdue, oldest by 8 days
  • Key team member on PTO until Thursday

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👥 TEAM WORKLOAD
| Member      | Active Tasks | Projects | Status      |
|---|---|---|---|
| [Name]      | 12           | 3        | ⚠️ Overloaded|
| [Name]      | 6            | 2        | ✅ Balanced  |
| [Name]      | 2            | 1        | 💚 Capacity  |
| Unassigned  | 4            | 2        | ❓ Needs owner|

🎯 TODAY'S PRIORITIES
1. [Unblock: get client approval for Project B designs]
2. [Reassign: move 3 tasks from overloaded team member]
3. [Review: Project C timeline — may need deadline extension]
```

### Step 6: Deliver & Archive
- Send status board via configured channel
- Save to `memory/project-status/YYYY-MM-DD.md`
- Track project health trends over time
- Alert immediately if a project flips from on-track to behind

## Examples

**User:** "What's the status of my projects?"

**Agent compiles and delivers the full status board.**

**User:** "Is the website redesign on track?"

**Agent:**
> 🟡 Website Redesign — AT RISK
> Progress: 52% (13/25 tasks) | Due: March 28
>
> Blocker: Client hasn't approved the homepage mockups (sent 4 days ago).
> If we don't get approval by Wednesday, the launch date is at risk.
>
> Recommendation: Send a follow-up to the client today with a deadline for feedback.

**User:** "Set up daily project status at 8:30am"

**Agent:** Configures cron, confirms:
> "Project status board scheduled for 8:30 AM daily. I'll track all active projects and flag anything that needs your attention."

## Customization Ideas

- **Client-facing status** — generate a polished version to share with clients (hide internal notes)
- **Sprint boards** — track sprint progress with burndown visualization
- **Risk register** — maintain a running list of project risks with mitigation plans
- **Resource planning** — forecast team capacity for upcoming project phases
- **Milestone celebrations** — auto-congratulate the team when milestones are hit
- **Project retrospectives** — auto-generate retro summaries when projects close

## Want More?

This skill handles project status tracking and reporting. But if you want:

- **Custom integrations** — connect to Jira, Monday.com, Linear, ClickUp, or your specific project tools
- **Advanced automations** — auto-reassign tasks, trigger escalations, generate client reports
- **Full system setup** — identity, memory, security, and 5 custom automations built specifically for your workflow

**DoctorClaw** sets up complete OpenClaw systems for businesses:

- **Guided Setup ($495)** — 2-hour live walkthrough. Everything configured, integrated, and running by the end of the call.
- **Done-For-You ($1,995)** — 7-day custom build. 5 automations, 3 integrations, full security, 30-day support. You do nothing except answer a short intake form.

→ [doctorclaw.ceo](https://www.doctorclaw.ceo)
