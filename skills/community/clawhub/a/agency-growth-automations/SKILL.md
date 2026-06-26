---
name: agency-growth-automations
description: Client acquisition methodology for agencies. Learn how 5 production-ready n8n workflows handle prospect sourcing, cold outreach, inbound routing, client reporting, and proposal follow-up — then get the full pack to deploy them.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": [] },
        "tags": ["n8n", "agency", "automation", "client-acquisition", "cold-outreach", "crm", "lead-management"],
        "price": "Free install. Full workflow JSONs + PDF guides at https://qssys.gumroad.com/l/AgencyGrowthAutomationPack ($67)"
      }
  }
---

# Agency Growth Automations

**Stop building your client acquisition from scratch.**

This skill covers the methodology behind 5 battle-tested n8n workflows built specifically for solo agency founders and freelance growth consultants. Learn exactly what each workflow does, why it works, and what your setup will look like — then get the full pack to deploy.

**5 workflows. Zero paid APIs. Built for agencies doing B2B client acquisition.**

- **Cold Prospect Radar** — automated daily signal monitoring so you never manually research leads again
- **Cold Email Sequencer** — drip outreach that runs while you sleep, tracked in Airtable
- **Inbound Lead Router** — every form submission lands in your CRM automatically, zero manual triage
- **Client Reporting Bot** — weekly HTML reports sent to clients without touching a dashboard
- **Proposal Follow-Up Engine** — day 3/7/14 follow-ups triggered automatically so no proposal goes cold

**Get the importable workflow JSONs + step-by-step PDF setup guides:**
→ **https://qssys.gumroad.com/l/AgencyGrowthAutomationPack ($67)**

---

## How This Skill Works

When you install this skill, your OpenClaw agent can walk you through:

1. **Which workflow to tackle first** — based on your biggest bottleneck
2. **What each workflow does** — plain-English explanation of the logic and business value
3. **What you'll need** — free tools, credentials, and setup time per workflow
4. **What success looks like** — what changes in your business after each workflow is live

For the importable JSON files and screenshot-annotated PDF setup guides, you'll need the full pack from Gumroad.

---

## Guided Methodology Flow

When you ask about any workflow, your agent will cover:

### Understanding the Problem

Each workflow solves one specific agency bottleneck:

| Workflow | Problem It Solves | Setup Time (with pack) |
|----------|------------------|------------------------|
| WF01 — Cold Prospect Radar | Manual lead research eating hours | ~45 min |
| WF02 — Cold Email Sequencer | Outreach stops when you stop | ~60 min |
| WF03 — Inbound Lead Router | Leads falling through the cracks | ~20 min |
| WF04 — Client Reporting Bot | Manual report assembly every week | ~45 min |
| WF05 — Proposal Follow-Up Engine | Proposals going cold, deals lost silently | ~30 min |

**If you're unsure where to start:** WF03 (Inbound Lead Router) is the fastest win — 20 minutes from zero to automated. You'll see it working the same day.

### Understanding the Architecture

Each workflow uses only free-tier tools:

- **Google Sheets + Gmail OAuth** — WF01, WF02, WF04 (one-time Google Cloud Console setup)
- **Airtable (free tier)** — WF02, WF03, WF05 (your CRM layer)
- **Tally forms (free)** — WF03 (webhook trigger for inbound leads)
- **n8n** — self-hosted on any $5/mo VPS, or n8n Cloud free tier (5 active workflows)

No paid APIs. No Hunter.io, Apollo, or GPT-4 API billing.

### Understanding the Value

Why these 5 and not 50?

Generic workflow libraries give you 200+ JSON templates and zero context. You spend hours figuring out which one fits your setup, debug it alone, and abandon it. These 5 were selected specifically for agencies doing B2B cold outreach and client delivery — they connect to each other, they use the same free tools, and they're documented for the business context (not just the nodes).

The goal: import, wire credentials, test run, go live. One workflow per session, all 5 in a week.

---

## Recommended Deployment Order

1. **WF03 — Inbound Lead Router** (fastest win, 20 min)
2. **WF05 — Proposal Follow-Up Engine** (stop leaking deals)
3. **WF01 — Cold Prospect Radar** (proactive outreach)
4. **WF02 — Cold Email Sequencer** (outreach at scale)
5. **WF04 — Client Reporting Bot** (professional reporting)

Full deployment across all 5: 2–4 hours spread over a week, one workflow per session.

---

## Get the Full Pack

Everything in this skill is the *why* and the *what*. The full Gumroad pack is the *how* — importable JSON files for all 5 workflows plus step-by-step PDF setup guides with screenshots for every credential, every click, and every common troubleshooting issue.

**→ https://qssys.gumroad.com/l/AgencyGrowthAutomationPack ($67)**

Want to test one workflow before buying? Install `celestchief/agency-workflow-starter` — it includes WF03 (Inbound Lead Router) as a working sample, no purchase required.

---

## Tool Requirements Summary

| Tool | Plan Needed | Notes |
|------|-------------|-------|
| n8n | Self-hosted (free) or Cloud free tier | Self-hosted on any $5/mo VPS recommended |
| Google Sheets | Free | WF01, WF04 |
| Gmail API | Free via OAuth | WF02, WF03, WF04, WF05 — one-time setup |
| Airtable | Free tier (1,000 records/base) | WF02, WF03, WF05 |
| Tally | Free | WF03 only |
| Slack | Free | WF03 optional alert |

---

*Built by Qssys — automation tools for service businesses.*
*Full pack: https://qssys.gumroad.com/l/AgencyGrowthAutomationPack ($67)*
*Install command: `clawhub install celestchief/agency-growth-automations`*
