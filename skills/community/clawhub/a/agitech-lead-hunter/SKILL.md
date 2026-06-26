---
name: lead-hunter
description: Autonomous lead generation skill. Finds freshly-funded companies matching your ideal customer profile, researches them, and delivers qualified leads with personalized outreach drafts. Industry-agnostic - works for dev shops, agencies, recruiters, SaaS founders, consultants. Use when asked to find leads, prospect, build a pipeline, or set up lead generation. Supports onboarding interview for first-time setup.
---

# Lead Hunter

Autonomous lead generation that finds, researches, and qualifies prospects daily.

## First Run (Onboarding)

If `skills/lead-hunter/scripts/config.json` has `"configured": false`, run the onboarding interview before anything else. See `references/onboarding.md` for the full interview flow.

After onboarding, the config is written and the skill switches to hunt mode.

## Hunt Mode (Daily Run)

### Step 1: Load Config

Read `skills/lead-hunter/scripts/config.json` for:
- `company` - who you are and what you sell
- `ideal_customer` - size, stage, geography, signals
- `sources` - where to find leads (industry-specific)
- `output` - where to put leads (asana, notion, csv, markdown)
- `outreach` - DM template and personalization rules
- `filters` - what to skip

### Step 2: Scrape Sources

For each source in `config.sources`:

1. **Try `web_fetch` first** (fastest, no deps)
2. **If blocked (403/Cloudflare):** fall back to `scripts/scrape.py` which uses Crawl4AI with stealth mode
3. **If still blocked:** use OpenClaw's managed browser via the browser tool
4. **Last resort:** use `web_search` with `site:<domain>` + freshness filter

Extract from each source:
- Company name
- Funding amount and round type
- Location
- What they do (1-2 sentences)
- Investors (if available)
- Article/announcement URL

### Step 3: Filter

Apply `config.filters` and `config.ideal_customer` to keep only matching leads:
- Round type matches (e.g., pre-seed, seed)
- Amount in range (e.g., $500K-$10M)
- Geography matches
- Industry/vertical matches
- Not in `config.filters.skip_industries`

Also deduplicate against `scripts/seen.json` (persisted list of previously found companies).

### Step 4: Research Each Lead

For each qualifying company (max 5 per run to stay fast):

1. **Website:** `web_fetch` their site - check team page, product, tech stack
2. **Team size:** `web_search` for LinkedIn company page - estimate headcount
3. **Key person:** `web_search` for founder/CEO LinkedIn - get name, background, LinkedIn URL
4. **Opportunity signals:** Flag if no CTO, small team, early product, tech stack match

### Step 5: Score & Rank

Score each lead 1-10 based on:
- Team size match (smaller = higher for services, bigger = higher for SaaS)
- Funding stage match
- Tech stack alignment
- Opportunity signals (no CTO, hiring, etc.)
- Recency of funding announcement

### Step 6: Generate Outreach

For each lead scoring 6+, generate a personalized DM draft using `config.outreach.template` with:
- Founder's first name
- Specific observation about their product/company
- How you can help (from `config.company.value_prop`)
- Soft CTA

### Step 7: Output

Depending on `config.output.type`:

**asana:**
```bash
node skills/asana-pat/scripts/asana.mjs create-task \
  --workspace <workspace_id> \
  --parent <parent_task_id> \
  --assignee me \
  --name "Lead: <Company> - <Round> <Amount>" \
  --notes "<full research + DM draft>"
```

**markdown:**
Append to `leads/YYYY-MM-DD.md` with full details per lead.

**csv:**
Append row to `leads/leads.csv` with: date, company, round, amount, location, url, key_person, linkedin, score, dm_draft

**notion:** (future - document API integration needed)

### Step 8: Update State

- Add found companies to `scripts/seen.json` for dedup
- Log summary to `memory/YYYY-MM-DD.md`

### Step 9: Report

Output structured summary:
```
## Lead Hunter Report - YYYY-MM-DD
- Sources scraped: X
- Articles found: X
- After filtering: X leads
- Researched: X
- Qualified (score 6+): X

### Top Leads
1. **Company** - Round $Amount | Score: X/10
   Key person: Name (LinkedIn)
   Signal: [why they're a fit]
```

## Scraping Fallback Chain

The skill uses a tiered approach to handle anti-bot protection:

1. `web_fetch` - default, fastest
2. `scripts/scrape.py` - Crawl4AI with stealth (handles most Cloudflare)
3. Browser tool - OpenClaw's managed browser (handles everything but slow)
4. `web_search` site: query - last resort, gets snippets not full pages

The scrape script auto-manages a venv at `scripts/.venv/`. First run:
```bash
python3 skills/lead-hunter/scripts/scrape.py --check
```
This creates the venv, installs crawl4ai + playwright chromium. Subsequent runs are instant.

## Source Discovery

When the user picks an industry during onboarding, the skill suggests relevant lead sources. See `references/sources.md` for the industry-to-source mapping.

Users can add custom sources at any time by editing `config.sources` in config.json.

## Rules
- Never send DMs automatically - only draft them
- Max 5 fully-researched leads per run (quality > quantity)
- Always deduplicate against seen.json
- Log every run to daily memory
- If a source is consistently blocked, note it in the report so the user can adjust
