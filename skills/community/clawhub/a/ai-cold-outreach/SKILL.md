---
name: ai-cold-outreach
description: Complete cold email outreach system for AI agents. Handles lead generation via Apollo API, email enrichment, Saleshandy sequence creation, prospect import, warmup monitoring, and campaign management. Use when setting up cold outreach, finding decision-maker emails, building email sequences, or managing cold email campaigns. Includes proven email copy templates and deliverability best practices.
---

# AI Cold Outreach System

End-to-end cold email outreach managed by your AI agent. From lead discovery to sending sequences — no human in the loop.

## Prerequisites

- **Apollo.io account** with API key (Basic plan $59/mo for email enrichment)
- **Saleshandy account** with API key (Outreach plan)
- **Google Workspace sending accounts** (2+ domains recommended)
- **SPF, DKIM, DMARC** configured on sending domains

## Quick Start

### 1. Configure API Keys

Store keys in your workspace:
```bash
# Apollo
export APOLLO_API_KEY="your_key"

# Saleshandy  
export SALESHANDY_API_KEY="your_key"
```

Or save to a JSON config (see [references/config-template.json](references/config-template.json)).

### 2. Find Leads

Use the Apollo lead generation script to search for decision-makers:
```bash
python3 scripts/apollo-search.py --titles "Owner,Founder,CEO" --keywords "aesthetic clinic" --location "United States" --max 100
```

This outputs a CSV with: name, email, title, organization, city, state, country.

### 3. Enrich Emails

Search results don't include emails. Enrich them:
```bash
python3 scripts/apollo-enrich.py --input leads-raw.csv --output leads-enriched.csv
```

Uses Apollo's `people/match` endpoint (1 credit per enrichment). Budget ~500 credits for 300 verified emails.

### 4. Import to Saleshandy

```bash
python3 scripts/saleshandy-import.py --csv leads-enriched.csv --step-id "YOUR_STEP_ID" --api-key "YOUR_KEY"
```

### 5. Monitor Warmup

Check email account health before sending:
```bash
python3 scripts/check-warmup.py --api-key "YOUR_KEY"
```

**Do NOT activate sequences until all accounts score 85+.**

## Architecture

```
Apollo API (lead gen) → CSV → Saleshandy API (import) → Email Sequence → Prospects
                                    ↑
                          Email Copy Templates (references/)
```

## Key API Endpoints

### Apollo
- **Search**: `POST /api/v1/mixed_people/api_search` — find people by title, keyword, location
- **Enrich**: `POST /api/v1/people/match` — get email from person ID (1 credit each)
- **Bulk Enrich**: `POST /api/v1/people/bulk_match` — batch enrichment (use name+company, not IDs)

### Saleshandy
- **Base URL**: `https://open-api.saleshandy.com`
- **Auth Header**: `x-api-key: YOUR_KEY`
- **List Sequences**: `GET /v1/sequences`
- **Import Prospects**: `POST /v1/sequences/prospects/import-with-field-name`
- **List Email Accounts**: `POST /v1/email-accounts`
- **Add Account to Sequence**: `POST /v1/sequences/{id}/email-accounts/add`

See [references/api-reference.md](references/api-reference.md) for full endpoint documentation.

## Email Copy Best Practices

See [references/email-templates.md](references/email-templates.md) for proven templates.

Key rules:
1. **Short punchy lines.** One thought per line.
2. **Story-driven.** Every email tells a specific story with real results.
3. **Real numbers always.** Never round. "$457,500" not "almost half a million."
4. **P.S. lines are punchlines.** The best hook lives in the P.S.
5. **Never beg.** Confident, almost amused tone.
6. **3-step sequences minimum:** Opener → Proof → Close
7. **3-5 day gaps** between steps

## Deliverability Checklist

Before activating any sequence:
- [ ] SPF record configured on sending domain
- [ ] DKIM record configured and passing
- [ ] DMARC record configured
- [ ] Email accounts warming for 7-14 days minimum
- [ ] Health scores above 85 on all accounts
- [ ] Using "get" prefix domains for cold outreach (protect main domain)
- [ ] Daily sending limits set conservatively (15-25/account/day to start)
- [ ] Warmup tool running (Saleshandy built-in or TrulyInbox)

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Apollo search returns 0 emails | Emails require enrichment — search only returns IDs |
| Apollo `people/search` returns 403 | Use `/mixed_people/api_search` endpoint instead |
| Saleshandy API "Invalid token" | Header must be `x-api-key` not `api-key` or `Authorization` |
| Saleshandy import fails "conflictAction" | Valid values: `overwrite`, `noUpdate`, `addMissingFields` |
| Emails going to spam | Check warmup scores, verify DKIM, reduce daily volume |
| Merge tags not rendering | Use `{{First Name}}` format in Saleshandy content |
