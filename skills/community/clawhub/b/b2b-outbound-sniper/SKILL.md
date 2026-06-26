---
name: b2b-outbound-sniper
description: "Autonomous B2B outbound engine that turns job board hiring signals into qualified pipeline. 6 LLMs. Your own email. 10/10 deliverability. Battle-tested in 30-day production campaign."
metadata:
  {
    "openclaw": {
      "env": [
        {
          "key": "APIFY_TOKEN",
          "label": "Apify API Token",
          "description": "From console.apify.com — used for Indeed job board scraping via borderline~indeed-scraper actor.",
          "required": true,
          "secret": true
        },
        {
          "key": "HUNTER_API_KEY",
          "label": "Hunter.io API Key",
          "description": "From app.hunter.io/api-key — used for email verification (domain-search) and campaign management.",
          "required": true,
          "secret": true
        },
        {
          "key": "HUNTER_CAMPAIGN_ID",
          "label": "Hunter Campaign ID",
          "description": "Numeric ID of your Hunter.io outbound campaign. Find it in app.hunter.io/campaigns.",
          "required": true,
          "secret": false
        }
      ]
    }
  }
---

# B2B Outbound Sniper

Turn job board hiring signals into qualified outbound pipeline — fully automated, end-to-end. Built and battle-tested by [Lemnos AI](https://getlemnos.ai) over 30 days of live production outreach.

**The core insight:** When a company posts a $70-80K admin role, they're 72 hours away from committing that budget. Show up before they sign the offer letter.

## What's Included

All scripts are bundled in this package — no external dependencies beyond Python + pip:

| File | Purpose |
|------|---------|
| `scripts/scrape.py` | Daily Apify scrape → Hunter verify → campaign load |
| `scripts/hunter_campaigns.py` | Campaign metrics, add/remove leads |
| `config/apis.json.example` | Config template — copy to `config/apis.json`, never commit |

## Required Credentials

Three API keys needed — set as environment variables or copy `config/apis.json.example` → `config/apis.json`:

| Key | Where to get it | Cost |
|-----|----------------|------|
| `APIFY_TOKEN` | [console.apify.com](https://console.apify.com) | ~$0.25/day at 50 results/keyword |
| `HUNTER_API_KEY` | [app.hunter.io/api-key](https://app.hunter.io/api-key) | Starter $49/mo (2,000 verifications) |
| `HUNTER_CAMPAIGN_ID` | [app.hunter.io/campaigns](https://app.hunter.io/campaigns) | Included with Hunter account |

> **Security note:** Never commit `config/apis.json` with real keys. Add it to `.gitignore`. All scripts accept env vars as first priority — no keys ever need to touch source files.

## Setup (5 minutes)

```bash
# 1. Copy config template
cp config/apis.json.example config/apis.json

# 2. Fill in your keys
nano config/apis.json

# 3. Edit your target keywords in scripts/scrape.py
#    Change the KEYWORDS array to match your vertical + geography

# 4. Run your first scrape
python3 scripts/scrape.py
```

## How It Works

```
Daily (7 AM, Mon–Fri via OpenClaw heartbeat)
  → Apify scrapes KW-1 (50 results max)
  → Filter: target geography only, exclude job board domains
  → Hunter domain-search: 90%+ confidence emails only
  → Dedup: fetch all existing campaign recipients via API (ground truth)
  → Add net-new verified leads to Hunter campaign
  → Log to references/hunter-tracking.jsonl
  → 15-min gap → KW-2 → repeat for all keywords
```

Hunter handles the full send sequence automatically:
- **Day 1:** Initial outreach
- **Day 3:** Follow-up bump
- **Day 7:** Breakup email

## Campaign Metrics

```bash
python3 scripts/hunter_campaigns.py metrics YOUR_CAMPAIGN_ID
```

## Production Results (30-Day Run, CRE Vertical)

- **52.9% open rate** on cold outreach
- **Sub-3% bounce rate** enforced by 90%+ confidence gate
- **0 spam complaints** across 150+ sends
- Fully autonomous: scrape → verify → load → send → follow-up, no human in the loop

## Customizing Keywords

Edit `KEYWORDS` in `scripts/scrape.py`:

```python
KEYWORDS = [
    {"label": "KW-1", "query": "office manager",           "location": "New Jersey"},
    {"label": "KW-2", "query": "operations coordinator",   "location": "New York"},
    {"label": "KW-3", "query": "executive assistant",      "location": "South Florida"},
]
```

Any Indeed-searchable query + US location works. One keyword per run, 15-min gap between each.

## A/B Testing

Run multiple Hunter campaigns with different CTAs and compare open/reply rates:

```bash
python3 scripts/hunter_campaigns.py metrics 111111   # Version A
python3 scripts/hunter_campaigns.py metrics 111112   # Version B
```

## Compliance Note

This tool sends commercial email. You are responsible for compliance with CAN-SPAM, GDPR, and your jurisdiction's anti-spam laws. Use only verified business email addresses and always include an unsubscribe mechanism (Hunter.io handles this automatically in campaigns).

## Infrastructure Cost

| Service | Cost |
|---------|------|
| Apify (50 results × 5 KWs/day) | ~$7.50/month |
| Hunter.io Starter | $49/month |
| **Total** | **~$57/month** |

## Full Source Code

**[github.com/getlemnos32/b2b-outbound-sniper](https://github.com/getlemnos32/b2b-outbound-sniper)**

Full production scripts, reference files, webhook listener, and docs. Review before deploying — all code is open source and auditable.

## ⭐ If This Fills Your Pipeline
Star it on ClawHub: [clawhub.com/skills/b2b-outbound-sniper](https://clawhub.com/skills/b2b-outbound-sniper)

Built by [Lemnos AI](https://getlemnos.ai) — AI operations for businesses that can't afford to hire.
