---
name: data-enrichment
version: 1.0.1
description: Enrich company and contact lists with public data — firmographics, technographics, social profiles, funding history, and employee count estimates. Clean, deduplicate, and score leads from raw CSV/JSON inputs.
author: TKDigital
category: Data & Analytics
tags: [data enrichment, CRM, lead scoring, firmographics, B2B data, data cleaning]
---

# Data Enrichment Skill

Transform raw company/contact lists into enriched, scored, CRM-ready datasets.

## What It Does

1. **Company Enrichment** — Add firmographic data (industry, size, revenue range, funding, tech stack)
2. **Contact Enrichment** — Find titles, social profiles, recent activity
3. **Data Cleaning** — Deduplicate, normalize, fix formatting issues
4. **Lead Scoring** — Score enriched records on custom criteria
5. **Export** — Output in CSV, JSON, or CRM-import format

## Usage

### Enrich a Company List
```
Enrich this list of companies:
1. Acme Corp
2. Widget Labs  
3. DataFlow Inc
4. CloudScale
5. GrowthLab

For each, find:
- Industry and sub-industry
- Employee count (estimated range)
- Funding status and last round
- Tech stack (if detectable)
- Key decision makers (CEO, CTO, CMO)
- LinkedIn company page
- Recent news (last 90 days)
```

### Clean and Deduplicate
```
Clean this CSV:
[Paste CSV or provide file]

Tasks:
- Remove exact and fuzzy duplicates
- Normalize company names (Inc/LLC/Ltd variations)
- Fix email formatting issues
- Flag incomplete records
- Standardize phone number format
- Fill missing fields where possible from public data
```

### CRM Enrichment
```
I'm importing these contacts into [HubSpot/Salesforce/Pipedrive]:

[Paste contact list]

Enrich each record with:
- Company info (size, industry, revenue)
- Contact title and seniority level
- LinkedIn profile URL
- Lead score (1-100 based on: company size 10-500, SaaS industry, recent funding)
- Tag: hot/warm/cold

Output as CSV with CRM-compatible column headers.
```

### Technographic Profiling
```
For these companies, identify their tech stack:
- What CMS do they use? (WordPress, Shopify, custom)
- What analytics? (GA4, Mixpanel, Amplitude)
- What email platform? (Mailchimp, SendGrid, HubSpot)
- What payment processor? (Stripe, PayPal, Square)
- Any AI/automation tools visible?

Companies: [list]
```

## Output Format

### Enriched Company Record
```
## [Company Name]
| Field | Value |
|-------|-------|
| Industry | [Industry / Sub-industry] |
| Employees | [Range estimate] |
| Revenue | [Range estimate] |
| Founded | [Year] |
| Funding | [Total raised / Last round] |
| Location | [HQ city, country] |
| Website | [URL] |
| LinkedIn | [URL] |
| Tech Stack | [Detected tools] |
| Recent News | [Last 90 days highlights] |

### Key Contacts
| Name | Title | LinkedIn | Seniority |
|------|-------|----------|-----------|
| [Name] | [Title] | [URL] | [C-level/VP/Director/Manager] |
```

### CSV Export Format
```csv
company_name,industry,employees,revenue_range,funding,location,website,linkedin,tech_stack,news,contact_name,contact_title,contact_linkedin,lead_score,tag
```

## Data Sources
- Public websites and About pages
- LinkedIn (public profiles)
- Crunchbase (public funding data)
- BuiltWith / Wappalyzer (tech stack)
- News aggregators (recent activity)
- Job postings (growth signals)

## Best Practices
- Provide clean input data (company names, domains, or LinkedIn URLs)
- Specify which fields matter most — enrichment is faster when focused
- For large lists (100+), process in batches of 25
- Always verify enriched data before importing to CRM
- Pair with `lead-gen-research` for full qualification + enrichment pipeline

## References
- `references/field-definitions.md` — What each enrichment field means
- `references/scoring-model.md` — Default lead scoring weights
