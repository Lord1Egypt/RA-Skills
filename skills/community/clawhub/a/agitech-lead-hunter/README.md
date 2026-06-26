# 🎯 Lead Hunter

**Autonomous lead generation for OpenClaw agents.**

Finds freshly-funded companies matching your ideal customer profile, researches them, scores them, and delivers qualified leads with personalized outreach drafts — all on autopilot.

Industry-agnostic. Works for dev shops, agencies, recruiters, SaaS founders, consultants, or anyone who sells to startups.

---

## How It Works

```
Funding Sources → Scrape → Filter → Research → Score → Outreach Draft → Output
```

1. **Scrape** — pulls recent funding announcements from configurable sources (TechCrunch, Crunchbase, finsmes, EU-Startups, etc.)
2. **Filter** — matches against your ICP: round type, amount, geography, industry, team size
3. **Research** — deep-dives each qualifying company: website, team page, tech stack, founder LinkedIn
4. **Score** — ranks leads 1–10 based on fit signals
5. **Outreach** — generates personalized DM/email drafts for leads scoring 6+
6. **Output** — delivers to Asana, Markdown files, or CSV (your choice)

---

## Quick Start

### 1. Install

```bash
clawhub install lead-hunter
```

Or clone directly into your OpenClaw skills directory:
```bash
git clone https://github.com/AgiTechGroup/lead-hunter.git skills/lead-hunter
```

### 2. Onboard

Just tell your agent:

> "Find me some leads"

On first run, Lead Hunter walks you through a conversational onboarding interview:

- **What does your company do?** — your offering, value prop, one-liner
- **Who's your ideal customer?** — stage, team size, industry, geography, buying signals
- **Where to look?** — suggests industry-specific sources, lets you add custom ones
- **Where to put leads?** — Asana tasks, Markdown files, or CSV
- **How to reach out?** — LinkedIn DM, email, or Twitter; tone and template
- **What to skip?** — industries, funding ranges, filters
- **How often?** — daily, weekdays, or twice a week (auto-creates a cron job)

Config is saved to `scripts/config.json`. Edit anytime to adjust.

### 3. Hunt

After onboarding, Lead Hunter runs automatically on your chosen schedule, or on demand:

> "Run lead hunter"
> "Find leads for me today"
> "Hunt for new prospects"

---

## Output Formats

### Markdown (default)
Creates `leads/YYYY-MM-DD.md` files with full research and DM drafts per lead.

### Asana
Creates subtasks under a parent task with company details, research notes, and outreach draft in the task description.

### CSV
Appends to `leads/leads.csv` — easy to import into any CRM:
```
date, company, round, amount, location, url, key_person, linkedin, score, dm_draft
```

---

## Lead Sources

Lead Hunter ships with **40+ pre-configured sources** across industries:

### General Funding News
- finsmes.com — daily funding announcements, global
- Crunchbase News — funding rounds, acquisitions
- TechCrunch Startups — US-heavy, Series A+
- PR Newswire — press releases
- EU-Startups — European funding
- Tech in Asia — APAC startup funding
- UKTN — UK tech
- Startup Daily — Australia/NZ

### Industry-Specific
- **SaaS:** ProductHunt, BetaList, Y Combinator, Wellfound
- **Fintech:** Fintech Global, The Fintech Times, Finovate
- **Healthtech:** MobiHealthNews, Fierce Healthcare, Digital Health
- **E-commerce:** Retail Dive, Modern Retail
- **AI/ML:** AI News, VentureBeat AI, The AI Journal
- **HR Tech:** HR Tech Feed, Recruiting Daily, HR Dive
- **Proptech:** Propmodo, The Real Deal, CREtech
- **Climate:** CleanTechnica, GreenBiz
- **EdTech:** EdSurge, EdTech Magazine
- **Legal Tech:** Artificial Lawyer, Legaltech News

Add any custom source — the skill auto-detects RSS feeds for reliable, block-free scraping.

---

## Scraping Architecture

Lead Hunter uses a **4-tier fallback chain** to handle anti-bot protection:

| Tier | Method | Speed | Reliability |
|------|--------|-------|-------------|
| 1 | `web_fetch` | ⚡ Fastest | Works for most sites |
| 2 | `scrape.py` (Crawl4AI) | 🔄 Medium | Handles Cloudflare |
| 3 | Managed Browser | 🐢 Slow | Handles everything |
| 4 | `web_search` site: query | 🔍 Snippets only | Last resort |

### Crawl4AI Setup

The scraping fallback auto-manages its own Python virtual environment. First run:

```bash
python3 skills/lead-hunter/scripts/scrape.py --check
```

This creates `.venv/`, installs Crawl4AI + Playwright Chromium. Subsequent runs are instant.

**Standalone usage:**
```bash
# Get markdown output
python3 scripts/scrape.py https://finsmes.com

# Get JSON with links
python3 scripts/scrape.py https://finsmes.com --output json
```

---

## Scoring System

Each lead is scored 1–10 based on:

| Signal | Weight |
|--------|--------|
| Team size match | High — smaller teams = higher score for services |
| Funding stage match | High — must match your ICP stages |
| Tech stack alignment | Medium — more relevant for dev shops |
| Opportunity signals | Medium — no CTO, hiring, early product |
| Funding recency | Low-Medium — fresher = better |

Only leads scoring **6+** get outreach drafts generated. The rest are logged but not actioned.

---

## Configuration

All config lives in `scripts/config.json`. Full schema:

```json
{
  "configured": true,
  "company": {
    "name": "Your Company",
    "offering": "services|saas|consulting|recruiting|other",
    "one_liner": "We build MVPs for funded startups",
    "value_prop": "Ship in 4 weeks, not 4 months"
  },
  "ideal_customer": {
    "stages": ["pre-seed", "seed", "series-a"],
    "team_size": { "min": 1, "max": 50 },
    "industries": ["fintech", "saas", "ai"],
    "geographies": ["US", "UK", "Singapore"],
    "signals": ["no CTO", "hiring engineers", "early product"]
  },
  "sources": [
    {
      "name": "finsmes",
      "url": "https://finsmes.com",
      "type": "funding_news",
      "search_fallback": "site:finsmes.com"
    }
  ],
  "output": {
    "type": "asana|markdown|csv|all",
    "asana_workspace": "optional",
    "asana_parent_task": "optional",
    "leads_dir": "leads/"
  },
  "outreach": {
    "channel": "linkedin_dm|email|twitter_dm",
    "tone": "casual|professional|technical|founder",
    "template": "Hi {first_name}, congrats on the {round} raise! ...",
    "always_mention": [],
    "never_mention": []
  },
  "filters": {
    "skip_industries": ["biotech", "hardware"],
    "min_funding": 500000,
    "max_funding": 15000000,
    "max_leads_per_run": 5
  },
  "schedule": {
    "frequency": "daily|weekdays|twice_weekly",
    "time": "06:30",
    "timezone": "Asia/Kuala_Lumpur"
  }
}
```

---

## Deduplication

Lead Hunter maintains a `scripts/seen.json` file tracking every company it's found. Subsequent runs skip already-seen companies so you never get duplicate leads.

---

## Project Structure

```
lead-hunter/
├── SKILL.md                    # Agent skill definition (how the AI uses it)
├── README.md                   # This file
├── .gitignore                  # Ignores .venv, seen.json, leads/
├── scripts/
│   ├── config.json             # Your configuration (created during onboarding)
│   ├── scrape.py               # Crawl4AI stealth scraper fallback
│   ├── seen.json               # Dedup state (auto-managed)
│   └── .venv/                  # Python venv for Crawl4AI (auto-created)
├── references/
│   ├── onboarding.md           # Onboarding interview flow
│   └── sources.md              # Industry-to-source mapping (40+ sources)
└── leads/                      # Output directory (if using markdown/csv)
    ├── YYYY-MM-DD.md
    └── leads.csv
```

---

## Run Report

After each run, Lead Hunter outputs a structured summary:

```
## Lead Hunter Report — 2026-03-21
- Sources scraped: 6
- Articles found: 23
- After filtering: 8 leads
- Researched: 5
- Qualified (score 6+): 3

### Top Leads
1. **Acme AI** — Seed $2.5M | Score: 9/10
   Key person: Jane Smith (LinkedIn)
   Signal: No CTO, hiring full-stack devs, launching in 6 weeks

2. **PayFlow** — Pre-seed $800K | Score: 7/10
   Key person: John Doe (LinkedIn)
   Signal: 3-person team, fintech, needs engineering partner
```

---

## Safety & Rules

- **Never sends DMs automatically** — only drafts them for your review
- **Max 5 fully-researched leads per run** — quality over quantity
- **Always deduplicates** against previously seen companies
- **Logs every run** to daily memory for audit trail
- **Reports blocked sources** so you can adjust your source list

---

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) agent runtime
- Python 3.10+ (for Crawl4AI fallback scraper)
- Internet access for web scraping and research
- Optional: Asana PAT (if outputting to Asana)

---

## License

MIT

---

Built for [OpenClaw](https://openclaw.ai) · Published on [ClawHub](https://clawhub.com)
