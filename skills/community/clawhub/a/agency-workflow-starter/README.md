# Agency Workflow Starter — Inbound Lead Router

**By Qsys | Part of the Agency Growth Pack**

---

## What This Does

The Inbound Lead Router is a production-ready n8n workflow that automatically captures inbound leads from any source and routes them to the right place — instantly, without manual triage.

**What it handles:**
- Webhook intake from contact forms, landing pages, or ad platforms
- Lead scoring by source, intent signal, and fill completeness
- Smart routing: hot leads → CRM + Slack alert; cold leads → nurture list; spam → auto-discard
- Duplicate detection before any record is created
- Timestamped logging to a Google Sheet or Airtable base

**Deploy time:** 15–30 minutes from import to live.

---

## Who It's For

- AI automation agencies delivering client projects
- Freelancers who need client-ready, handoff-quality output
- Anyone building lead gen systems who doesn't want to start from scratch

---

## What You Need

- n8n (self-hosted or n8n Cloud)
- A webhook endpoint (n8n generates this automatically)
- One of: HubSpot, Airtable, or Google Sheets for the CRM/log destination
- Slack (optional — for hot lead alerts)

---

## How to Deploy

1. **Import the workflow**
   - In n8n: Settings → Import from File → select `lead-router.json`

2. **Connect your credentials**
   - Add your CRM or Sheets credentials in the Credential nodes
   - Add Slack webhook if you want instant alerts (recommended)

3. **Set your routing rules**
   - Open the `Lead Score + Route` node
   - Adjust the score thresholds for hot/warm/cold (defaults: 7+, 4–6, <4)

4. **Point your form at the webhook**
   - Copy the webhook URL from the Webhook node
   - Paste into your contact form, Typeform, or ad platform

5. **Test with a live submission**
   - Submit a test lead, verify it routes correctly
   - Check your CRM/Sheet for the entry

6. **Activate and hand off**
   - Toggle the workflow to Active
   - Share the webhook URL with the client

---

## What's Included

```
agency-workflow-starter/
├── README.md              ← You're reading it
├── lead-router.json       ← n8n workflow export (import directly)
├── SKILL.md               ← OpenClaw skill definition
└── setup-notes.md         ← Credential setup reference
```

---

## Upgrade: Agency Growth Pack ($67)

This routes the leads. The other 4 workflows **generate them, follow up on them, report on them, and close them.**

The full Agency Growth Pack contains 5 client-ready workflows:

| # | Workflow | What It Does |
|---|----------|--------------|
| 01 | Cold Prospect Radar | Scrapes and scores prospects from LinkedIn + web; feeds your outbound list daily |
| 02 | Email Sequence Engine | Sends personalized multi-touch sequences; auto-pauses on reply detection |
| **03** | **Inbound Lead Router** | **← You have this one** |
| 04 | Client Reporting Automator | Pulls metrics from 5+ sources; generates and emails a PDF report weekly |
| 05 | Deal Closer Follow-Up | Tracks proposal status; sends timed nudges; alerts you when a deal goes cold |

**$67 on Gumroad — less than what you'd charge for a single client deployment.**

Each workflow: production-quality, tested, importable in under 30 minutes.

[→ Get the full Agency Growth Pack](https://qssys.gumroad.com/l/AgencyGrowthAutomationPack)

---

## Support

Issues with the workflow? Questions on setup?

Post in the [OpenClaw Discord](https://discord.com/invite/clawd) `#machine-room` channel.

---

_Built by Qsys. Deployed by agencies who bill by the outcome, not the hour._
