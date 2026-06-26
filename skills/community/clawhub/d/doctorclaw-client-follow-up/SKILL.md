---
name: client-follow-up
description: "Automated client follow-up — scan your client list, find stale leads, draft personalized outreach. Weekly cron or on-demand."
version: 1.0.0
tags: [sales, crm, follow-up, outreach, automation]
metadata:
  clawdbot:
    emoji: "🤝"
source:
  author: DoctorClaw
  url: https://www.doctorclaw.ceo
---

# Automated Client Follow-Up

Stop losing deals to silence. This skill reads your client or lead list, identifies contacts you haven't reached out to recently, and drafts personalized follow-up messages — so no opportunity slips through the cracks.

Run it weekly on a cron, or trigger it whenever you want to check who needs attention.

## What You Get

- Stale lead detection — contacts you haven't messaged in X days
- Personalized follow-up drafts for each stale contact
- Priority ranking based on deal value, last interaction, and lead stage
- Follow-up stats (total contacts, stale count, overdue count)
- Outreach log tracking — what you sent, when, and to whom

## Setup

### Required
- **Client list** — A CSV file, Google Sheet, or any structured list your agent can read. Minimum columns: name, email (or phone), last-contacted date. More columns = better personalization.

### Optional (but recommended)
- **Send access** — If you want the agent to send follow-ups after your approval (Gmail, Outlook, or SMS via Twilio)
- **CRM integration** — If you use a CRM (HubSpot, Notion database, Airtable), point the agent at it instead of a CSV
- **Calendar access** — So the agent can suggest meeting times in follow-ups
- **Delivery channel** — Telegram/Discord for follow-up digest notifications

### Configuration

Tell your agent:

1. **Client list location** — file path, Google Sheet URL, or CRM connection
2. **Stale threshold** — how many days without contact before a lead is "stale" (default: 14 days)
3. **Critical threshold** — how many days before a lead is "at risk" (default: 30 days)
4. **Follow-up style** — your tone (professional, casual, friendly, direct) so drafts match your voice
5. **Follow-up schedule** — when to run (default: every Monday at 9:00 AM local)
6. **Max follow-ups per run** — limit drafts per cycle (default: 10)
7. **Delivery** — where to send the follow-up digest (Telegram, Discord, file)
8. **Industry/context** — what your business does, so follow-ups are relevant (e.g., "web design agency", "real estate investor", "SaaS founder")

## How It Works

### Step 1: Load Client List
- Read your client list from the configured source (CSV, Google Sheet, CRM, Notion)
- For each contact, extract: name, email/phone, company (if available), last-contacted date, deal stage, deal value, notes
- If last-contacted date is missing, flag the contact for manual review

### Step 2: Identify Stale Contacts
Sort contacts into 3 categories based on days since last contact:

**🔴 AT RISK — Over critical threshold (30+ days)**
- These leads are going cold. Follow-up is urgent.
- Prioritize by deal value (highest value first)

**🟡 STALE — Over stale threshold (14-30 days)**
- Due for a check-in. Not urgent, but shouldn't wait another week.
- Prioritize by deal stage (closest to closing first)

**🟢 ACTIVE — Within threshold (< 14 days)**
- Recently contacted. No action needed this cycle.
- Skip these — don't over-contact

### Step 3: Rank & Select
- Rank all stale + at-risk contacts by priority score:
  - Deal value weight: higher value = higher priority
  - Days overdue weight: more overdue = higher priority
  - Deal stage weight: closer to closing = higher priority
- Select top N contacts (up to configured max per run)

### Step 4: Draft Follow-Ups
For each selected contact, draft a personalized follow-up message:
- **Use context:** reference their company, deal stage, last conversation topic (from notes)
- **Match tone:** use the configured follow-up style
- **Keep it short:** 3-5 sentences max
- **Include a clear CTA:** ask a question, propose a meeting, share something useful
- **Vary the approach:** don't send the same template to everyone
  - Re-engagement: "Haven't heard from you in a while — still interested in X?"
  - Value-add: "Saw this article about [their industry] and thought of you"
  - Check-in: "How's [project/initiative they mentioned] going?"
  - Nudge: "We had discussed [service/product] — any questions I can answer?"
  - Meeting request: "Would love to catch up — free for a quick call this week?"
- Mark as DRAFT — never send without user approval

### Step 5: Compile Follow-Up Digest
Format the digest:

```
🤝 Follow-Up Digest — [Date]

📊 PIPELINE STATUS
Total contacts: [X] | At risk: [X] | Stale: [X] | Active: [X]
Oldest untouched: [X days] — [Contact Name]

🔴 AT RISK ([X] contacts)
1. [Name] — [Company] | Last contact: [X days ago]
   Stage: [deal stage] | Value: [deal value]
   📝 Draft: "[First line of follow-up...]"

2. [Name] — [Company] | Last contact: [X days ago]
   Stage: [deal stage] | Value: [deal value]
   📝 Draft: "[First line of follow-up...]"

🟡 STALE ([X] contacts)
3. [Name] — [Company] | Last contact: [X days ago]
   Stage: [deal stage]
   📝 Draft: "[First line of follow-up...]"

4. [Name] — [Company] | Last contact: [X days ago]
   Stage: [deal stage]
   📝 Draft: "[First line of follow-up...]"

🟢 ACTIVE ([X] contacts) — no action needed

💡 INSIGHTS
• [X] contacts haven't been reached in 30+ days
• Top deal at risk: [Name] — $[value]
• Suggested: Block 30 min this week for follow-up calls
```

### Step 6: Deliver & Track
- Send digest via configured channel (Telegram, Discord, or save to file)
- Show full draft messages below the digest for review
- When user approves a follow-up ("send 1" or "approve all"), send the messages
- After sending, update the client list with the new last-contacted date
- Log the outreach in `memory/follow-up-log/YYYY-MM-DD.md`

## Examples

**User:** "Check my follow-ups"

**Agent runs the workflow and responds:**

> 🤝 Follow-Up Digest — Monday, March 10
>
> 📊 PIPELINE STATUS
> Total contacts: 34 | At risk: 3 | Stale: 7 | Active: 24
> Oldest untouched: 45 days — Lisa Park
>
> 🔴 AT RISK (3 contacts)
> 1. **Lisa Park** — Greenfield Properties | Last contact: 45 days ago
>    Stage: Proposal sent | Value: $4,800
>    📝 Draft: "Hi Lisa, I wanted to circle back on the proposal I sent over last month. Happy to walk through any questions or adjust the scope if needed. Would Thursday or Friday work for a quick call?"
>
> 2. **James Wu** — TechStart Inc | Last contact: 38 days ago
>    Stage: Discovery | Value: $2,400
>    📝 Draft: "Hey James, we had a great conversation about streamlining your onboarding process. I put together a few ideas since we last spoke — mind if I send them over?"
>
> 3. **Maria Santos** — Bloom Studio | Last contact: 31 days ago
>    Stage: Interested | Value: $1,200
>    📝 Draft: "Hi Maria, just checking in — are you still looking to revamp your client intake process? I'd love to help whenever the timing is right."
>
> 🟡 STALE (7 contacts)
> 4. Dave Chen — Redline Motors | 22 days ago
> 5. Priya Patel — Sapphire Consulting | 19 days ago
> 6. Tom Bradley — Bradley & Sons | 18 days ago
> 7. (+ 4 more)
>
> 🟢 ACTIVE (24 contacts) — no action needed
>
> 💡 INSIGHTS
> • 3 contacts at risk of going cold — $8,400 in pipeline value
> • Lisa Park is your highest-value stale lead
> • Suggested: Prioritize Lisa and James this week

**User:** "Send 1 and 2. Edit 3 to mention we have a spring discount."

**Agent:** Sends follow-ups 1 and 2 as drafted. Updates draft 3 with spring discount mention, shows updated version for approval.

---

**User:** "Set up weekly follow-ups every Monday"

**Agent:** Configures cron for Monday 9:00 AM, confirms:
> "Client follow-up scheduled for every Monday at 9:00 AM. I'll scan your contact list, flag anyone going cold, and draft personalized messages for your review."

---

**User:** "Add a new contact: Sarah Kim, sarah@buildright.co, met at conference, interested in the $495 setup"

**Agent:** Adds to client list with today as first-contact date, stage: "Interested", notes: "Met at conference, interested in Guided Setup ($495)." Confirms the addition.

## Customization Ideas

- **Multi-channel follow-up** — draft emails AND LinkedIn messages for the same contact
- **Auto-categorize new leads** — when a new contact is added, auto-assign a deal stage and priority
- **Follow-up sequences** — instead of one-off messages, create multi-touch sequences (Day 1: email, Day 3: LinkedIn, Day 7: call reminder)
- **Win/loss tracking** — mark deals as won or lost, track conversion rate over time
- **Referral prompts** — for active clients, suggest asking for referrals after successful projects
- **Meeting prep** — before scheduled calls, pull up the contact's history and draft talking points

## Want More?

This skill handles follow-up tracking and outreach drafting. But if you want:

- **Custom integrations** — connect to your CRM, project management tool, invoicing system, or any API your business uses
- **Advanced automations** — multi-step workflows tailored to your business (lead scoring, auto-replies, invoice follow-ups, proposal generation)
- **Full system setup** — identity, memory, security, and 5 custom automations built specifically for your workflow

**DoctorClaw** sets up complete OpenClaw systems for businesses:

- **Guided Setup ($495)** — 2-hour live walkthrough. Everything configured, integrated, and running by the end of the call.
- **Done-For-You ($1,995)** — 7-day custom build. 5 automations, 3 integrations, full security, 30-day support. You do nothing except answer a short intake form.

→ [doctorclaw.ceo](https://www.doctorclaw.ceo)
