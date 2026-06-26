---
name: freelance-pipeline-automation
description: |
  Automated freelance pipeline manager for AI agents. Discovers jobs on Upwork, Fiverr,
  LinkedIn, and niche boards, scores leads by skill match (50%) + budget (30%) + recency (20%),
  generates personalized proposals, and tracks the full pipeline from discovery to payment.

  Commands:
  - freelance_pipeline.py add "Title" "$500" "python,api"   Add new lead
  - freelance_pipeline.py score "Title" "$500" "python"    Score without adding
  - freelance_pipeline.py digest                           Morning lead digest
  - freelance_pipeline.py status 3 proposal_sent          Update lead status
  - freelance_pipeline.py list                             Show all leads

  JSON-based pipeline tracker with status states: new, qualified, proposal_sent,
  negotiating, accepted, paid, rejected. Python 3.8+, zero deps.

  Scoring thresholds: leads scoring 70+ are qualified for digest. Proposal
  generation includes matched skills analysis, budget assessment, and custom
  approach sections. Works with or without browser automation for gated sites.
compatibility: Created for Zo Computer
metadata:
  author: ssyopros.zo.computer
allowed-tools: Bash, Read
---

# Freelance Pipeline Automation

End-to-end freelance client discovery and proposal system for AI agents and independent professionals.

## Lead Scoring Algorithm

Leads are scored 0-100 based on:
- **Skill Match (50 pts max)** - How well job requirements match your skills
- **Budget Quality (30 pts max)** - Higher budgets score higher
- **Recency (20 pts max)** - Newer postings get priority

Leads scoring 70+ appear in the morning digest.

## Commands

```bash
# Add a new lead manually
python scripts/freelance_pipeline.py add "Python Bot Development" "$500-1000" "python,bot,automation"

# Score a lead without adding to pipeline
python scripts/freelance_pipeline.py score "Web Scraper" "$200" "python,scraping"

# Get morning digest of qualified leads
python scripts/freelance_pipeline.py digest

# Update lead status through lifecycle
python scripts/freelance_pipeline.py status 3 proposal_sent
python scripts/freelance_pipeline.py status 3 accepted
python scripts/freelance_pipeline.py status 3 paid

# List all leads
python scripts/freelance_pipeline.py list
```

## Pipeline Status Flow

```
new -> qualified -> proposal_sent -> negotiating -> accepted -> paid
                   \                                    \
                    -> rejected                          -> rejected
```

## Configuration

Set custom profile and pipeline file locations:
```bash
export FREELANCE_PROFILE="/path/to/profile.json"
export FREELANCE_PIPELINE="/path/to/pipeline.json"
```

## Proposal Generation

The script generates proposals with:
- Client and job specifics from input
- Matched vs unmatched skills analysis
- Custom approach section
- Pricing based on your hourly rate in profile
- Timeline estimates