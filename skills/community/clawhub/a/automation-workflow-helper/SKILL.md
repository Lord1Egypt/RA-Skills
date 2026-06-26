---
name: Automation Workflow Helper
description: Turns your weekly repetitive tasks into automated bots. Identifies high-value automation opportunities, picks the right tool (Dify / Coze / n8n workflow, or zero-Token RPA scripts), designs process templates, and calculates ROI. Triggered when the user mentions "automation", "repetitive tasks", "workflow", "efficiency", "save time", "bot", "RPA", "process automation", "automate", or asks to automate repetitive browser/file tasks.
---

# Automation Workflow Helper

---

## Overview

Time is the scarcest resource. Automation lets you scale without hiring. The rule is simple: **any task you do more than twice a week that requires no creative judgment is worth automating**. This guide helps you spot opportunities, pick the right tool, and ship fast — with fewer Tokens consumed, more stable execution, and more accurate results every time.

---

## Step 1: Find Tasks Worth Automating

Not every task should be automated. Start by finding high-value opportunities.

**Automation Audit (spend 1 hour on this):**

1. List every repetitive task you did this week
2. For each task, note:
   - How many minutes it takes per run
   - How many times per month you do it
   - Whether the steps are always the same (or vary each time)
3. Calculate time cost:
```
Monthly hours = minutes per run × monthly frequency ÷ 60
```
Example: a 15-minute task done 20 times/month = 5 hours/month

4. Sort by monthly hours, highest first

**Good candidates for automation:**

- ✅ Fully fixed steps, same every time
- ✅ High frequency (at least once a week)
- ✅ Pure data shuffling — no creativity or judgment required
- ✅ Syncing information between multiple tools

**Poor candidates:**

- ❌ Requires creativity, negotiation, or human judgment
- ❌ Very infrequent (a few times a year)
- ❌ Process changes often

**Easiest wins to start with:**

- Form submission → auto send email / Slack notification
- Form data → auto save to spreadsheet
- Payment received → auto generate invoice
- Scheduled weekly report delivery to clients
- Data sync between tools (CRM ↔ spreadsheet ↔ email)

---

## Step 2: Choose Your Automation Approach

This is the most critical decision. There are two routes — picking the wrong one wastes a lot of time.

### Route A: Workflow Platforms

Workflow platforms connect SaaS services via their **APIs**, passing data and triggering actions between tools. No coding required, built visually.

**Best for:**
- Cross-platform data sync (form → CRM → email notification)
- Tools that have API / Webhook integrations
- Scheduled tasks, message pushing, data aggregation, AI processing nodes

**Top 3 tools compared:**

| Tool | Open Source | Cloud | Self-hosted | Pricing | Best for | Link |
|------|-------------|-------|-------------|---------|----------|------|
| **Dify.ai** | ✅ Open source (MIT) [GitHub](https://github.com/langgenius/dify) | ✅ [cloud.dify.ai](https://cloud.dify.ai), free tier available | ✅ Docker self-host | Free cloud tier; Pro $59/mo | AI-powered flows, smart chatbots, document Q&A, LLM nodes | [dify.ai](https://dify.ai) |
| **Coze (ByteDance)** | ❌ Closed source | ✅ [coze.com](https://www.coze.com) | ❌ Not supported | Free, pay-as-you-go | Telegram/Discord bots, content pipelines, no-code quick start | [coze.com](https://www.coze.com) |
| **n8n** | ✅ Open source (fair-code) [GitHub](https://github.com/n8n-io/n8n) | ✅ [n8n.cloud](https://n8n.cloud), 14-day free trial | ✅ Self-host for free | Cloud from $20/mo; self-host free | Complex branching logic, private deployment, data pipelines, developers | [n8n.io](https://n8n.io) |

**How to choose:**

- Need AI / LLM processing nodes → Dify.ai
- Integrating Telegram, Discord, or content pipelines; zero-code quick start → Coze
- Private deployment, data must stay on-prem → n8n or Dify.ai self-hosted
- Tight budget → n8n open-source self-host (completely free) or Dify.ai free cloud

---

### Route B: RPA (Robotic Process Automation)

RPA automates tasks by **directly controlling the browser UI** — like an invisible person clicking, filling forms, scraping data, and downloading files. **No API needed on the target website.**

**What is RPA?**

Traditional workflow platforms depend on APIs, but many websites (e-commerce platforms, government portals, internal ERPs, various SaaS tools) don't expose public APIs. RPA drives the browser UI directly, bypassing that limitation — if there's a webpage, it can be automated.

**RPA vs Workflow Platforms — Core Differences:**

| Dimension | Workflow Platform | RPA |
|-----------|------------------|-----|
| How it works | Calls API endpoints | Directly controls browser UI |
| Prerequisite | Target system has an API | Any webpage works, no API needed |
| Running cost | Platform subscription + per-call fees | Record once, replay for $0 Token |
| Execution speed | Subject to API and network latency | Runs locally, extremely fast |
| Typical use cases | SaaS tool integration, data sync | Price scraping, form filling, screenshots, report export |
| Stability depends on | API interface staying unchanged | Page structure staying unchanged |

**Core advantages of RPA:**

- **Zero-Token replay**: AI participates only once during recording; every subsequent run is a pure Python script — no AI compute consumed, cost approaches zero
- **Bypass login walls**: Log in manually once to save cookies; auto-injected on every future run — no more captchas, SMS codes, or QR scans
- **Deterministic execution**: The script is fixed at recording time; unlike LLM-driven agents that "improvise" each run, results are predictable

**Choose RPA when:**

- The target website has no public API
- Steps are fully fixed (login → search → scrape data → save)
- High-frequency execution needed (daily or even hourly)
- Task involves clicking, form filling, screenshots, or file downloads

> **Recommended tool: OpenClaw RPA**
>
> An RPA compiler built for AI Agents — describe the task in plain language, AI drives a real browser to record it once, and auto-generates a standalone Playwright Python script. Every subsequent replay runs with **zero Token, zero hallucination, in seconds**.
>
> Real-world demo videos include e-commerce price monitoring, financial reconciliation, hotel data collection, and stock news briefings:
> 👉 **[View README + Video Demos](https://github.com/laziobird/openclaw-rpa)**
>
> **Featured case tutorials:**
> - 🛒 **[Amazon Best Sellers Scraper](https://github.com/laziobird/openclaw-rpa/blob/main/articles/scenario-amazon-bestsellers.en-US.md)** — auto-extract product title, price, rating, review count & URL, export to a Word table report — zero code, zero manual work
> - 🏨 **[Airbnb Competitor Price Tracker](https://github.com/laziobird/openclaw-rpa/blob/main/articles/scenario-airbnb-compare.en-US.md)** — vision recognition + DOM analysis to extract competitor prices and ratings automatically
> - 🏦 **[AP Reconciliation](https://github.com/laziobird/openclaw-rpa/blob/main/articles/scenario-ap-reconciliation.en-US.md)** — API pull → Excel matching → Word report, fully automated end-to-end
>
> Install on the OpenClaw platform in one click:
> 👉 **[clawhub.ai/laziobird/openclaw-rpa](https://clawhub.ai/laziobird/openclaw-rpa)**
>
> Or run in terminal:
> ```bash
> openclaw skills install openclaw-rpa
> ```
> After installing, type `#RPA` in the chat to launch the guided recording flow.

**Route decision tree:**

```
Does the target system have an API?
├── Yes → Workflow platform (Dify / Coze / n8n)
└── No  → RPA (type #RPA to start recording)

Need AI judgment / LLM processing?
├── Yes → Dify.ai
└── No, pure rule-based routing → Coze or n8n
```

---

## Step 3: Design Your Flow

Before you build anything, map the flow clearly.

**Flow Design Template:**

```
Trigger: What event starts this flow?
  Example: "Every day at 9 AM" / "New form submission received" / "New email arrives"

Condition (optional): What must be true for it to run?
  Example: "Only process orders with status 'Pending Review'"

Actions:
  Step 1: [Do what]
  Step 2: [Do what]
  Step 3: [Do what]

Error handling: What happens if it fails?
  Example: "Send a Slack message to notify me"
```

**Example Flow (Lead Capture → CRM → Notification):**

```
Trigger: New form submission on website

Condition: Phone number field is not empty

Actions:
  Step 1: Write lead to spreadsheet (name, phone, requirement)
  Step 2: Send welcome email to customer
  Step 3: Send message to sales channel: "New lead: [Name] [Phone]"
  Step 4: Create follow-up task in project management tool, remind in 3 days

Error handling: If Step 1 fails, send alert email to me
```

**Design principles:**

- Start with a 2–3 step simple version; get it working before adding complexity
- Test each node individually before chaining them together
- Some APIs respond slowly; add delays between nodes if needed
- Always set up failure alerts — silent failures are more dangerous than no automation

---

## Step 4: Build and Test

Example setup steps using Dify.ai:

1. **Create a new workflow** (Dify console → Studio → Create Workflow)
2. **Choose a trigger node** (e.g. Webhook, scheduled trigger, form input)
3. **Connect accounts** (enter API Key / OAuth in the Tool or HTTP Request node)
4. **Test the trigger** (send a test request, confirm data enters the workflow)
5. **Add processing nodes** (LLM node / code node / HTTP request node)
6. **Map variables** (match upstream node outputs to downstream node input fields)
7. **Test each node individually** (click the node's "Run" button, confirm output is correct)
8. **Repeat** the above, chaining subsequent nodes one by one
9. **Publish and activate** (click "Publish"; the workflow starts listening for trigger events)

**Testing Checklist:**

- Run the full flow with test data
- Test edge cases (empty fields, special characters, very long text)
- Test error handling (intentionally break a step, confirm alerts fire correctly)
- Verify field mappings are correct

**Common Issues:**

| Issue | Cause | Fix |
|-------|-------|-----|
| Flow doesn't trigger | Trigger condition too strict | Check filter settings, relax conditions |
| Action fails | API rate limit or insufficient permissions | Add delay between nodes, re-authorize |
| Data missing or wrong | Field mapping error | Check each field mapping individually |
| Duplicate triggers | Trigger source emitting duplicate events | Deduplicate by unique ID |

**Rule:** Always do a full end-to-end run with real data before going live. Don't wait for actual customers to discover bugs.

---

## Step 5: Monitor and Maintain

Automation is not "set and forget." Tools change, APIs update, page structures shift.

**Weekly check (5 minutes):**

- Scan workflow run logs for errors
- Handle failures immediately

**Monthly audit (15 minutes):**

- Review all active automations: still in use? Still saving time?
- Deactivate flows no longer needed (avoid billing waste and logic confusion)
- Update flows that depend on deprecated tools

**Documentation recommendations:**

- Write a short description for each automation (store in Notion or a shared doc)
- Include: what it does, when it runs, which tools it connects, how to troubleshoot
- Once you have 10+ automations, this doc will save you

**Error alert setup:**

- Route all automation failure notifications to one place (Slack channel, email, or team chat)
- Review errors weekly, find root causes — don't just patch symptoms

---

## Step 6: 6 Classic Scenarios

### Scenario 1: Automation Diagnosis for Your Business (Analysis)

**Who it's for:** You know you have repetitive work but aren't sure what can be automated or which tool to use

**How to use in OpenClaw:**

Just describe your daily work in detail — the more specific, the better:

```
Help me analyze which parts of my work can be automated.

I run a small cross-border e-commerce team. My daily routine looks like this:
1. Morning: open Shopify, Amazon, and our own store backend; check yesterday's orders
   from each; copy everything into an Excel summary sheet for the daily report
2. Check competitor prices on each platform and manually record changes
3. When new orders come in, message the warehouse team in Slack with which orders to ship
4. Every Friday, compile weekly sales data using a fixed template and send the report to my boss
5. When launching new products, manually copy product info into three platform backends

Help me analyze: which can be automated? Workflow or RPA? What's the priority order?
```

---

### Scenario 2: E-commerce Competitor Price Monitoring (RPA)

**Pain point:** Manually visiting multiple e-commerce platforms every day to check competitor prices and copying data into Excel

**Solution:** `#RPA` recording, run on a daily schedule

```
Trigger: Daily scheduled (e.g. 8 AM)
Action: Open each product page → scrape price, sales volume, rating → append to price_monitor.xlsx
```

**How to use in OpenClaw:**

Step 1 — type in the chat:
```
#RPA
```

Step 2 — after the Agent asks for task name and capability code, enter (two lines):
```
Competitor Price Monitor
D
```

Step 3 — paste your task description:
```
Open https://www.amazon.com/dp/<ASIN>
Scrape: product name, current price, review count
Open https://www.ebay.com/itm/<ItemID>
Scrape: product name, current price, sold count
Append the data to price_monitor.xlsx on the Desktop.
Each row should include a timestamp. Columns: Platform, Product Name, Price, Sales/Reviews, Timestamp
```

**Why RPA instead of a workflow platform?**

| Dimension | Workflow Platform | RPA (OpenClaw RPA) |
|-----------|------------------|--------------------|
| Feasibility | ❌ Amazon/eBay don't expose public price APIs | ✅ Drives browser directly — any page works |
| Cost per run | — | **$0 Token**, pure local script |
| ROI (running once/day) | Not possible | 2 hours to record; zero cost every day after — **payback in 1 day** |

---

### Scenario 3: Sales Lead Auto-entry into CRM (Workflow)

**Pain point:** Leads from website forms, landing pages, or event registrations must be manually entered into a spreadsheet or CRM

**Solution:** Coze or n8n workflow

```
Trigger: Webhook (form submission)
Step 1: Parse fields (name, phone, source channel)
Step 2: Write to CRM / spreadsheet
Step 3: Notify sales rep in Slack with customer info
Step 4: Auto-send welcome email to customer
```

**How to use in OpenClaw:**

Describe your scenario directly in the chat:
```
I want to automate sales lead entry.
I use Typeform to collect customer info (name, phone, needs).
After submission I have to manually copy it into a Google Sheet and post in our sales Slack channel.
Help me design an automation plan and recommend the right tool with setup steps.
```

The Agent will guide you through: tool selection → mapping triggers and actions → step-by-step Coze / n8n configuration

---

### Scenario 4: AI Content Multi-platform Distribution (Workflow)

**Pain point:** After writing an article or recording a video, you must manually rewrite copy to match each platform's style before publishing

**Solution:** Dify.ai workflow

```
Trigger: New content uploaded (RSS / Webhook)
Step 1: LLM node — rewrite title and summary for each platform style (blog / LinkedIn / Twitter)
Step 2: Publish to each platform via API
Step 3: Generate image caption copy, push draft to review queue
```

**How to use in OpenClaw:**

Describe your scenario in the chat:
```
I write one blog post per week. After finishing it, I have to manually rewrite it
in LinkedIn style and Twitter style before posting.
Can you help me design an automation flow that auto-generates versions for each platform
after I finish the original? I'd prefer a tool that supports AI rewriting. I use Dify.ai.
```

The Agent will guide you: design the Dify workflow node structure → provide LLM Prompt templates → explain how to connect each platform's API

---

### Scenario 5: Financial Reconciliation Report (RPA)

**Pain point:** Every month, export data from an internal system, manually reconcile with an Excel invoice sheet, write a Word report

**Solution:** `#RPA` recording

```
Trigger: End-of-month scheduled run
Action: Log into internal system → export this month's payables list → compare with local invoices.xlsx → generate Word reconciliation report
```

**How to use in OpenClaw:**

Step 1 — type in the chat:
```
#RPA
```

Step 2 — after the Agent asks for task name and capability code, enter (two lines):
```
Financial Reconciliation Report
F
```

Step 3 — paste your task description:
```
Log in to https://<your-internal-system>, username <username>, password <password>
Go to the "Accounts Payable" page, filter for this month's data, export as CSV and save to Desktop

Read invoices.xlsx on the Desktop (invoice records).
Match against the exported CSV using the "PO Number" field:
- Match found: mark as "Cleared"
- In system only, no invoice: mark as "Invoice Pending"
- Invoice only, not in system: mark as "Exception"

Generate a Word report saved to Desktop, filename: reconciliation_report_YYYYMMDD.docx
Report includes: summary table (total amount, cleared, pending, exception counts) + detail table
```

> **Tip:** If the system requires an SMS verification code, run `#rpa-login <system-url>` first to save the login session. Subsequent recordings auto-inject the cookie — no repeated login needed.

**Why RPA instead of a workflow platform?**

| Dimension | Workflow Platform (with AI nodes) | RPA (OpenClaw RPA) |
|-----------|----------------------------------|--------------------|
| Feasibility | ❌ Internal ERP has no external API | ✅ Drives browser to log in and export directly |
| Token cost per run | LLM node ~$0.05–$0.50/run | **$0**, pure local script |
| Cost for 20 runs/month | $1–$10/month (LLM pricing) | **$0**, record once and run forever |
| Output format | Requires extra processing for Excel/Word | ✅ Natively outputs .xlsx + .docx |
| ROI | Ongoing cost | 3 hours to record, **pays back same month**, then zero cost forever |

---

### Scenario 6: New Client Onboarding Automation (Workflow)

**Pain point:** After signing a contract, you must manually create a project, send a welcome email, provision accounts, and add the client to a group — miss one step and it's embarrassing

**Solution:** n8n workflow

```
Trigger: Contract signed (DocuSign / HelloSign Webhook)
Step 1: Create project space in Notion / Google Drive
Step 2: Send welcome email + link to onboarding docs
Step 3: Create system account, send activation email
Step 4: Add client to relevant Slack / Teams channel
Step 5: Update CRM status to "Active"
```

**How to use in OpenClaw:**

Describe your scenario in the chat:
```
After we sign a contract, there's a whole onboarding checklist:
create a project doc in Notion, send a welcome email, add the client to the service Slack channel,
create an account in our system and send an activation email, and update the CRM status.
Right now it's all manual and we keep missing steps.
Help me design an n8n workflow that auto-triggers when the contract is signed and completes all these steps.
```

The Agent will guide you: confirm which tools have APIs → design the n8n workflow nodes → provide Webhook configuration and field mapping

---

**What the Agent outputs:**

For each task you describe, it analyzes:
- ✅ Can be automated / ⚠️ Partially automatable / ❌ Keep manual
- Recommended route: Workflow (Dify / Coze / n8n) or RPA (`#RPA`)
- Priority ranking (by ROI, highest first)
- Quick-start method for each item (prompt or tool configuration entry)

---

## Step 7: Calculate Automation ROI

Not every automation is worth the investment. Use this formula to prioritize.

**ROI Formula:**

```
Monthly time saved (hours) = minutes per run ÷ 60 × monthly frequency
Build cost = build time (hours) × hourly rate + monthly tool fee
Payback period (months) = build cost ÷ monthly value saved

Payback < 3 months → prioritize
Payback > 6 months → evaluate necessity first
```

**Rule:** Focus on automations with a payback period under 3 months — that's the highest ROI zone.

**How to use in OpenClaw:**

Just tell the Agent your situation and let it do the math:

```
Help me figure out if this is worth automating.

I check competitor prices on three e-commerce platforms every day — about 30 minutes each time,
roughly 20 times a month.
I plan to use RPA recording, estimate 2 hours to set up, tool is free.
My hourly rate is about $50.

Calculate the payback period and tell me whether it's worth doing.
```

**Agent output:**

```
📊 ROI Calculation

Monthly time saved: 30 min ÷ 60 × 20 runs = 10 hours/month
Monthly value saved: 10 hours × $50 = $500/month

Build cost: 2 hours × $50 = $100 (tool is free, no monthly fee)

Payback period: $100 ÷ $500 = 0.2 months (~6 days)

✅ Verdict: Strongly recommended. Pays back in 6 days; saves $500/month after that.
Recommended: RPA (e-commerce platforms have no public API). Type #RPA to start recording.
```

**You can also ask the Agent to compare priorities across multiple tasks:**

```
I have three things I want to automate. Help me figure out which to do first:

1. Daily competitor price check: 30 min/run, 20 runs/month, ~2 hours to set up (RPA, free)
2. Form lead entry into CRM: 5 min/run, 60 runs/month, ~3 hours to set up (Coze, free)
3. Weekly sales report: 45 min/run, 4 runs/month, ~4 hours to set up (Dify, $15/month)

My hourly rate is $75. Rank them by payback period and give me a recommendation.
```

---

## Common Mistakes to Avoid

- **Automating before optimizing**: automating a broken process just makes errors happen faster. Fix the process first, then automate.
- **Over-automating**: low-frequency tasks that require judgment are fine to do manually — don't automate for the sake of automating.
- **No error handling**: silent failures are more dangerous than doing things manually — data will quietly go wrong. Always set up alerts.
- **Insufficient testing**: a broken automation is worse than no automation — it creates bad data and missed tasks.
- **Starting too complex**: get a 2–3 step simple version running first, then add logic gradually.
- **No documentation**: three months later you won't remember what this workflow does.

---

## Professional Services

If you need hands-on help analyzing and implementing your automation:

| Service | Price | What's included |
|---------|-------|-----------------|
| Consultation & Diagnosis | $19 | Identify automation opportunities and recommend the right AI tools |
| Single Scenario Solution | $69 | Full automation flow design and implementation for one use case |
| Full Package | $299 | Enterprise-grade automation system |

**Contact**
Email: `jiangzhiwei@next4.ai`
