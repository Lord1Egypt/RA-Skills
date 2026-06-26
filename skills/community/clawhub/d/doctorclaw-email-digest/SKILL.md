---
name: email-digest
description: "Smart email digest — categorize unread emails by priority, draft replies for urgent ones. On-demand or scheduled."
version: 1.0.0
tags: [email, productivity, inbox, automation]
metadata:
  clawdbot:
    emoji: "📧"
source:
  author: DoctorClaw
  url: https://www.doctorclaw.ceo
---

# Smart Email Digest

Stop drowning in your inbox. This skill scans your unread emails, sorts them into priority categories, and drafts suggested replies for the urgent ones — so you spend 5 minutes reviewing instead of 45 minutes reading.

Run it on a schedule (morning + afternoon) or trigger on-demand whenever your inbox feels overwhelming.

## What You Get

- All unread emails categorized into 4 priority tiers
- Suggested replies drafted for urgent emails
- Newsletter/marketing clutter identified and separated
- Action items extracted from email bodies
- Summary stats (total unread, urgent count, oldest unread age)

## Setup

### Required
- **Email access** — Gmail (via Gmail API/skill) or any email provider your agent can read. The agent needs read access to your inbox and the ability to list unread messages.

### Optional
- **Send access** — If you want the agent to send drafted replies after your approval, it needs send permissions too
- **Delivery channel** — Telegram/Discord for digest delivery, or file output
- **Contact context** — If you have a CRM or contact list, tell the agent where it is. This helps it prioritize emails from important contacts.

### Configuration

Tell your agent:

1. **Email account** — which inbox to scan
2. **VIP list** — email addresses or domains that are always high priority (your boss, top clients, family)
3. **Mute list** — senders to always categorize as low priority (newsletters you don't read, automated notifications)
4. **Digest schedule** — when to run (default: 8:00 AM and 2:00 PM local)
5. **Delivery** — where to send the digest
6. **Reply style** — how you write emails (professional, casual, direct, friendly) so drafted replies match your voice
7. **Max emails to process** — limit per run (default: 50)

## How It Works

### Step 1: Scan Inbox
- Fetch all unread emails (up to configured max)
- For each email, extract: sender, subject, date received, body preview (first 200 chars), any attachments

### Step 2: Categorize
Sort every email into one of 4 categories:

**🔴 URGENT — Action required today**
- Matches: VIP senders, keywords (urgent, ASAP, deadline, overdue, payment due, action required, EOD, by tomorrow)
- Contains: direct questions to you, approval requests, time-sensitive items
- Has: deadlines within 24 hours mentioned in body

**🟡 ACTION NEEDED — Requires a response but not immediately**
- Contains: questions directed at you, requests for information, meeting invites
- From: known contacts or business-related senders
- Needs: a reply within 2-3 days

**🔵 FYI — Read when you have time**
- Contains: updates, status reports, shared documents, CC'd threads
- No direct questions or action items for you
- Good to know but not blocking anything

**⚪ NOISE — Skip or bulk-handle**
- From: muted senders, marketing lists, automated notifications
- Contains: newsletters, promotional offers, social media notifications
- Action: archive, unsubscribe suggestion, or ignore

### Step 3: Extract Action Items
For URGENT and ACTION NEEDED emails, pull out specific action items:
- Direct questions that need answers
- Deadlines mentioned
- Documents to review
- Meetings to confirm
- Approvals to give

### Step 4: Draft Replies (Urgent Only)
For each URGENT email, draft a suggested reply:
- Match the user's configured reply style
- Address the specific ask in the email
- Keep it concise (3-5 sentences max)
- Include a clear next step or answer
- Mark as DRAFT — never send without user approval

### Step 5: Compile Digest
Format the digest:

```
📧 Email Digest — [Time]

📊 INBOX STATUS
Total unread: [X] | Urgent: [X] | Action needed: [X]
Oldest unread: [X days ago] from [sender]

🔴 URGENT ([X] emails)
1. [Sender] — [Subject]
   → [Action item / question]
   📝 Draft reply ready

2. [Sender] — [Subject]
   → [Action item / question]
   📝 Draft reply ready

🟡 ACTION NEEDED ([X] emails)
3. [Sender] — [Subject]
   → [What they need from you]

4. [Sender] — [Subject]
   → [What they need from you]

🔵 FYI ([X] emails)
5. [Sender] — [Subject] (status update)
6. [Sender] — [Subject] (shared doc)

⚪ NOISE ([X] emails)
[X] newsletters | [X] notifications | [X] marketing
💡 Consider unsubscribing from: [top 3 noisy senders]
```

### Step 6: Deliver
Send digest via configured channel. If draft replies were generated, include them below the digest for review.

When the user approves a draft reply ("send reply 1" or "approve all replies"), send the emails.

## Examples

**User:** "Check my email"

**Agent runs the digest and responds:**

> 📧 Email Digest — 2:30 PM
>
> 📊 INBOX STATUS
> Total unread: 23 | Urgent: 2 | Action needed: 4
> Oldest unread: 3 days ago from LinkedIn
>
> 🔴 URGENT (2 emails)
> 1. **Sarah Chen** — Q1 Budget needs approval by 5 PM
>    → She needs your sign-off on the revised numbers
>    📝 Draft reply: "Hi Sarah, reviewed the Q1 numbers — approved. Go ahead and submit. Thanks!"
>
> 2. **Client: Acme Corp** — Contract expiring Friday
>    → They're asking if you want to renew at the same rate
>    📝 Draft reply: "Hi Tom, yes we'd like to renew. Same terms work for us. Can you send the updated agreement?"
>
> 🟡 ACTION NEEDED (4 emails)
> 3. Mike Torres — Updated proposal draft (review requested)
> 4. HR — Benefits enrollment reminder (due March 15)
> 5. Dave Kim — Meeting reschedule request (Thursday → Friday?)
> 6. Accounting — Missing receipt for Feb expense report
>
> 🔵 FYI (8 emails)
> Status updates, shared docs, CC'd threads
>
> ⚪ NOISE (9 emails)
> 5 newsletters | 3 LinkedIn notifications | 1 promo
> 💡 Consider unsubscribing from: LinkedIn Digest, TechCrunch, Product Hunt

**User:** "Send reply 1, edit reply 2 to say we want to negotiate the rate down 10%"

**Agent:** Sends reply 1 as-is. Updates reply 2 with the negotiation language, shows the updated draft for approval.

---

**User:** "Set up email digest twice daily"

**Agent:** Configures cron for 8:00 AM and 2:00 PM, confirms:
> "Email digest scheduled for 8:00 AM and 2:00 PM daily. I'll categorize your inbox and draft replies for anything urgent."

## Customization Ideas

- **Auto-archive noise** — automatically archive emails categorized as NOISE after 7 days
- **Weekly inbox report** — track email volume trends, response time, top senders
- **Smart follow-up** — flag emails you replied to but never got a response
- **Team digest** — if you manage a team, compile digests from multiple inboxes
- **Label/folder sync** — apply Gmail labels or move to folders based on categories

## Want More?

This skill handles inbox triage and reply drafting. But if you want:

- **Custom integrations** — connect your email to your CRM, auto-create tasks from emails, sync with project management tools
- **Advanced automations** — auto-replies for common questions, lead scoring from inbound emails, invoice detection and routing
- **Full system setup** — identity, memory, security, and 5 custom automations built specifically for your workflow

**DoctorClaw** sets up complete OpenClaw systems for businesses:

- **Guided Setup ($495)** — 2-hour live walkthrough. Everything configured, integrated, and running by the end of the call.
- **Done-For-You ($1,995)** — 7-day custom build. 5 automations, 3 integrations, full security, 30-day support. You do nothing except answer a short intake form.

→ [doctorclaw.ceo](https://www.doctorclaw.ceo)
