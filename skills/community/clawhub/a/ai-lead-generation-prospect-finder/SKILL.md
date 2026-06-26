---
name: ai-lead-generation-prospect-finder
description: >
  Generates ideal customer profiles (ICP), lead acquisition strategies,
  LinkedIn and Google search formulas, structured lead lists, and cold
  outreach connection tips for B2B sales prospecting.
  Trigger this skill whenever the user wants to find leads, build a prospect
  list, identify target customers, research their ideal buyer, generate
  LinkedIn search filters, or asks anything related to lead generation,
  outbound prospecting, pipeline building, or sales targeting — even when
  phrased casually such as "who should I be selling to", "help me find
  customers", "build me a lead list", or "who are my ideal buyers".
license: MIT-0
user-invocable: true
disable-model-invocation: false
compatibility:
  - claude-sonnet-4-20250514
  - claude-opus-4-20250514
  - claude-haiku-4-5-20251001
argument-hint: >
  Provide: industry (e.g. SaaS, Fintech, Healthcare), target role
  (e.g. VP of Sales, CTO, Marketing Manager), location (e.g. United States,
  Europe, Global), product or service description, and your goal
  (e.g. book 10 demos, close 5 enterprise deals, grow SMB pipeline).
  Optionally add company size, annual revenue range, and tech stack filters
  to sharpen the output.
metadata:
  category: Sales & Marketing
  subcategory: Lead Generation
  version: 1.0.0
  author: ClawHub Skill Publisher
  language: en
  tags:
    - lead-generation
    - prospecting
    - ICP
    - B2B
    - sales
    - LinkedIn
    - outbound
    - pipeline
    - GTM
    - SDR
---

# AI Lead Generation & Prospect Finder

Generate a complete B2B lead generation playbook in minutes — ideal customer
profiles, LinkedIn Boolean search strings, Google X-Ray queries, structured
lead list templates, and cold outreach connection tips. Built for founders,
SDRs, and growth teams who need a pipeline fast.

---

## What This Skill Does

Given an industry, role, location, product, and goal, this skill produces:

- **Ideal Customer Profile (ICP)** — firmographic, demographic, and
  psychographic profile of your perfect buyer
- **Lead Acquisition Strategies** — 5+ actionable channels ranked by
  effort vs. impact
- **LinkedIn Search Formulas** — ready-to-paste Boolean strings and
  Sales Navigator filter configs
- **Google X-Ray Search Queries** — find prospects on LinkedIn, company
  sites, and directories via Google
- **Structured Lead List** — a ready-to-export table with columns for
  Name, Title, Company, Industry, Location, LinkedIn URL, Email Status,
  Lead Score, and Notes
- **Cold Outreach Bridge** — how to connect each lead segment to the
  right cold email angle

---

## Skill Files

```
ai-lead-generation-prospect-finder/
├── SKILL.md       ← You are here
├── manifest.json  ← Deployment metadata
├── prompt.txt     ← Core generation logic
├── config.json    ← Input field definitions
└── README.md      ← End-user documentation
```

---

## When to Trigger This Skill

Trigger immediately when the user says anything like:

- "find me leads" / "build a prospect list" / "who should I target"
- "generate an ICP" / "who is my ideal customer"
- "LinkedIn search for prospects" / "Sales Navigator filters"
- "Google search for leads" / "X-Ray search LinkedIn"
- "I need a pipeline" / "help me fill my funnel"
- "outbound prospecting strategy" / "who to cold email"
- "target account list" / "TAL for ABM campaign"
- Mentions Apollo, Hunter, ZoomInfo, Clay, Lusha, Clearbit in research context

---

## Required Inputs

Collect all required fields in a **single ask** — do not ask one at a time.

| Field | Required | Description |
|---|---|---|
| `industry` | ✅ | Target industry (e.g. SaaS, Fintech, Healthcare) |
| `target_role` | ✅ | Job title or function (e.g. VP of Sales, CTO) |
| `location` | ✅ | Geography (e.g. United States, EMEA, Global) |
| `product` | ✅ | What you sell — be specific |
| `goal` | ✅ | Outcome you want (e.g. book 10 demos this month) |
| `company_size` | Optional | Employee range (e.g. 50–500, Enterprise 1000+) |
| `revenue_range` | Optional | ARR or revenue (e.g. $1M–$50M ARR) |
| `tech_stack` | Optional | Tools they use (e.g. Salesforce, HubSpot, AWS) |
| `excluded_segments` | Optional | Who NOT to target (e.g. agencies, solo founders) |

---

## Output Sections

```
🎯 IDEAL CUSTOMER PROFILE (ICP)
  Firmographics · Demographics · Psychographics · Pain triggers · Buying signals

📋 LEAD ACQUISITION STRATEGIES
  5+ channels ranked by effort vs. impact with action steps

🔍 LINKEDIN SEARCH FORMULAS
  Boolean search strings · Sales Navigator filter configs · InMail tips

🌐 GOOGLE X-RAY QUERIES
  Ready-to-run search strings for Google

📊 STRUCTURED LEAD LIST TEMPLATE
  Table with 10 columns · Scoring criteria · Ready to export to CSV/Sheets

🔗 COLD OUTREACH BRIDGE
  How to match each lead segment to the right email angle
```

---

## Example

**Input:**
```
Industry: B2B SaaS
Target Role: VP of Sales
Location: United States
Product: AI-powered sales coaching platform that improves rep performance
Goal: Book 20 qualified demos in 30 days
Company Size: 100–1000 employees
Tech Stack: Salesforce, Outreach or Salesloft
```

**Sample ICP Output:**

Company: Series B–D SaaS companies, 100–1000 employees, $10M–$100M ARR,
US-based, using Salesforce + a sales engagement tool, with an inside
sales team of 10+ reps.

Buyer: VP of Sales or Chief Revenue Officer. Promoted from AE or SDR.
Currently scaling a team and struggling with ramp time and quota attainment.
Has budget authority. Triggered to buy when: team misses quota 2 quarters in a
row, or headcount doubles but revenue doesn't.

**Sample LinkedIn Boolean String:**

```
("VP of Sales" OR "Vice President of Sales" OR "Head of Sales" OR "CRO")
AND ("SaaS" OR "software" OR "B2B")
AND ("Salesforce" OR "Outreach" OR "Salesloft")
NOT ("agency" OR "consultant" OR "freelance")
```

---

## Connected Skill

After running this skill, use **AI Cold Email & LinkedIn Outreach Generator**
to turn your prospect segments into personalized outreach sequences.

---

## Compatible Tools

Prospect research: LinkedIn Sales Navigator · Apollo.io · Hunter.io ·
ZoomInfo · Clay · Lusha · Clearbit

CRM import: HubSpot · Salesforce · Pipedrive · Notion · Google Sheets · Airtable

---

## Limitations

- This skill generates strategy and templates — it does not scrape or
  pull live contact data from any platform.
- Lead quality depends on how specific your inputs are. Vague inputs
  produce generic outputs.
- Always verify contact information before outreach.
- Comply with GDPR, CCPA, and platform terms of service when collecting
  and using prospect data.

---

## Changelog

| Version | Date | Notes |
|---|---|---|
| 1.0.0 | 2026-03-22 | Initial release |
