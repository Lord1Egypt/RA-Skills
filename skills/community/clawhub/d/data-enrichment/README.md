# Data Enrichment — ClawHub Skill

> Transform raw company/contact lists into enriched, scored, CRM-ready datasets with firmographics, technographics, and social profiles.

## The Problem

Raw lead lists are nearly useless. A company name and email tells you nothing about whether they're a good fit. Manual research takes 10-15 minutes per record. At 500 leads, that's 80+ hours of grunt work.

## The Solution

Data Enrichment automates the research layer:

**Input**: Raw company names, domains, or contact info  
**Output**: Fully enriched records with industry, size, funding, tech stack, decision makers, and lead scores  
**Time**: Minutes per batch vs hours of manual research

## Quick Start

```bash
clawhub install data-enrichment
```

Then:
```
Enrich these 20 companies with industry, employee count, funding status, and key contacts. Score each 1-100 for fit as a SaaS content client.
```

## Features

| Feature | Description |
|---------|-------------|
| Company Enrichment | Industry, size, revenue, funding, location |
| Contact Discovery | Titles, LinkedIn, seniority level |
| Tech Stack Detection | CMS, analytics, email, payments, AI tools |
| Data Cleaning | Dedup, normalize, fix formatting |
| Lead Scoring | Custom weighted scoring |
| CRM Export | CSV/JSON in HubSpot/Salesforce format |

## Skill Ecosystem

Pairs perfectly with:
- **lead-gen-research** → Enrich first, then qualify with outreach angles
- **cold-email-sequence** → Enriched data feeds personalized email sequences
- **content-engine** → Use enriched firmographics to tailor content per segment

## Author

**TKDigital** — AI automation for revenue  
Built with OpenClaw | [clawhub.com](https://clawhub.com)
