---
name: doctorclaw-lead-qualifier
description: "Lead qualifier — score inbound leads based on custom criteria, prioritize hot prospects, draft outreach. On-demand or cron."
version: 1.0.0
tags: [sales, leads, qualification, scoring, automation]
metadata:
  clawdbot:
    emoji: "🎯"
source:
  author: DoctorClaw
  url: https://www.doctorclaw.ceo
---

# Lead Qualifier

Stop wasting time on tire-kickers. This skill scores your inbound leads based on criteria you define — company size, industry, budget signals, engagement level — so you focus on the prospects most likely to buy and skip the ones that won't.

Run it when new leads come in, or on a daily cron to process your lead pipeline.

## What You Get

- Every lead scored on a 0-100 scale with clear reasoning
- Leads ranked and sorted by qualification score
- Hot leads flagged for immediate follow-up
- Cold leads identified to save your time
- Personalized outreach drafts for qualified leads
- Disqualification reasons for low-scoring leads

## Setup

### Required
- **Lead list** — A CSV, Google Sheet, or CRM export with lead data. Minimum: name, email, company. More fields = better scoring.

### Optional (but recommended)
- **Scoring criteria** — your custom rules for what makes a good lead (industry, company size, budget, etc.)
- **Ideal customer profile (ICP)** — a description of your perfect customer for comparison
- **CRM integration** — HubSpot, Pipedrive, Notion, or Airtable for auto-import
- **Email access** — to send outreach to qualified leads after approval

### Configuration

Tell your agent:

1. **Lead source** — file path, Google Sheet URL, or CRM connection
2. **Scoring criteria** — what matters most to you:
   - Company size (employee count ranges)
   - Industry (target industries)
   - Budget indicators (revenue, funding, pricing page visits)
   - Role/title of the contact (decision maker vs. researcher)
   - Geography (target regions)
   - Engagement signals (website visits, email opens, form fills)
3. **Score weights** — how much each criterion matters (or use defaults)
4. **Qualification threshold** — minimum score to be "qualified" (default: 60/100)
5. **Hot lead threshold** — score that triggers immediate alert (default: 80/100)
6. **Outreach style** — your tone for follow-up messages
7. **Delivery** — where to send qualified lead alerts

## How It Works

### Step 1: Load Leads
- Read lead data from configured source
- For each lead, extract all available fields: name, email, company, title, industry, company size, source, notes, engagement data

### Step 2: Research & Enrich
For each lead with limited data, attempt to enrich:
- **Company lookup** — check company website for size, industry, description
- **Role assessment** — is this person a decision maker, influencer, or researcher?
- **Source quality** — where did this lead come from? (referral > organic > cold)

### Step 3: Score Each Lead
Apply scoring criteria (customizable, defaults shown):

| Criterion | Points | Example |
|---|---|---|
| **Industry match** | 0-20 | Target industry = 20, adjacent = 10, unrelated = 0 |
| **Company size** | 0-20 | Sweet spot range = 20, too small = 5, too large = 10 |
| **Decision maker** | 0-20 | C-suite/owner = 20, director = 15, manager = 10, other = 5 |
| **Budget signals** | 0-15 | Mentioned budget = 15, funded company = 10, unknown = 5 |
| **Engagement** | 0-15 | Multiple touchpoints = 15, form fill = 10, single visit = 5 |
| **Source quality** | 0-10 | Referral = 10, organic = 7, paid = 5, cold list = 2 |

Total: 0-100 points

### Step 4: Categorize Leads

**🔥 HOT (80-100) — Contact immediately**
- Strong fit, high engagement, decision maker
- Draft personalized outreach now
- Alert Stephen immediately

**🟢 QUALIFIED (60-79) — Follow up this week**
- Good fit, needs nurturing or more info
- Draft a value-add follow-up

**🟡 WARM (40-59) — Monitor and nurture**
- Partial fit, might convert with time
- Add to drip sequence or check back later

**⚪ COLD (0-39) — Deprioritize**
- Poor fit or insufficient signals
- Note disqualification reason
- Archive or mark for future review

### Step 5: Draft Outreach
For HOT and QUALIFIED leads, draft personalized messages:
- Reference their company/industry specifically
- Address their likely pain point based on their profile
- Offer something valuable (insight, case study, free resource)
- Include a clear, low-commitment CTA (quick call, demo, guide)
- Match your configured outreach style

### Step 6: Compile Lead Report

```
🎯 Lead Qualification Report — [Date]

📊 PIPELINE SUMMARY
Total leads processed: [X]
🔥 Hot: [X] | 🟢 Qualified: [X] | 🟡 Warm: [X] | ⚪ Cold: [X]

🔥 HOT LEADS — ACT NOW
1. [Name] — [Title], [Company] | Score: [X]/100
   Industry: [match] | Size: [X employees] | Source: [referral/organic]
   Why hot: [decision maker + target industry + high engagement]
   📝 Draft outreach ready

2. [Name] — [Title], [Company] | Score: [X]/100
   [Details]
   📝 Draft outreach ready

🟢 QUALIFIED — FOLLOW UP THIS WEEK
3. [Name] — [Title], [Company] | Score: [X]/100
   Why qualified: [good fit but needs nurturing]
   📝 Draft outreach ready

🟡 WARM — NURTURE ([X] leads)
[Summary of warm leads — monitor for engagement changes]

⚪ COLD — DEPRIORITIZE ([X] leads)
[Summary + disqualification reasons]
• [X] leads: wrong industry
• [X] leads: too small / no budget signals
• [X] leads: non-decision makers

💡 INSIGHTS
• Best lead source this batch: [referral/organic/paid]
• Most common industry: [industry]
• [X]% of leads are decision makers
```

### Step 7: Deliver & Act
- Send report via configured channel
- Hot leads trigger immediate alerts
- When user approves outreach ("send to lead 1"), send the message
- Update lead status in source (qualified/contacted/disqualified)

## Examples

**User:** "Qualify these leads" [provides CSV or points to sheet]

**Agent processes and responds with the full qualification report.**

**User:** "I got a new lead: Sarah Kim, sarah@buildright.co, she's a founder of a 15-person construction tech company, found us through our blog"

**Agent:**
> 🎯 Lead Score: **82/100** — 🔥 HOT
>
> • Industry: Construction Tech — strong fit (18/20)
> • Company size: 15 employees — sweet spot (18/20)
> • Role: Founder — decision maker (20/20)
> • Budget: Unknown, but funded startup signals (8/15)
> • Engagement: Blog reader, organic (7/15)
> • Source: Organic content (7/10)
>
> 📝 Draft outreach: "Hi Sarah, I noticed you found us through our blog — glad the content resonated! I work with construction tech founders to set up AI systems that handle the operational busywork. Would a quick 15-minute call make sense to see if there's a fit?"

**User:** "Send it"

**Agent:** Sends the outreach email.

## Customization Ideas

- **Auto-score on form submission** — qualify leads instantly when they fill out your contact form
- **Lead routing** — assign qualified leads to team members based on criteria
- **Re-engagement campaigns** — periodically re-score cold leads to find ones that have warmed up
- **Win rate tracking** — track which lead scores actually convert to paying customers
- **ICP refinement** — use closed deal data to improve scoring criteria over time

## Want More?

This skill handles lead scoring and qualification. But if you want:

- **Custom integrations** — connect to HubSpot, Pipedrive, Salesforce, or your specific CRM
- **Advanced automations** — auto-qualify form submissions, trigger drip sequences, sync scores to CRM
- **Full system setup** — identity, memory, security, and 5 custom automations built specifically for your workflow

**DoctorClaw** sets up complete OpenClaw systems for businesses:

- **Guided Setup ($495)** — 2-hour live walkthrough. Everything configured, integrated, and running by the end of the call.
- **Done-For-You ($1,995)** — 7-day custom build. 5 automations, 3 integrations, full security, 30-day support. You do nothing except answer a short intake form.

→ [doctorclaw.ceo](https://www.doctorclaw.ceo)
