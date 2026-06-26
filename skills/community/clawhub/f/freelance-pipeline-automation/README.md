# Freelance Pipeline Automation Skill

Automated freelance client discovery, lead scoring, proposal generation, and pipeline tracking for AI agents and independent professionals.

## Features

- **Lead Scoring** - Algorithm scores leads 0-100 based on budget, skills match, and recency
- **Proposal Generation** - Personalized proposals from job postings and profile data
- **Pipeline Tracking** - Markdown/JSON based tracker with status management
- **Morning Digest** - Daily summary of qualified leads ready for outreach
- **Multi-Source** - Works with Upwork, Fiverr, LinkedIn, and niche job boards
- **Python 3.8+ Compatible** - Zero external dependencies

## Setup

```bash
# Configure your profile
export FREELANCE_PROFILE="profile.json"

# Add leads manually
python scripts/freelance_pipeline.py add "Python Bot Development" "$500-1000" "python,bot,automation"

# Score a lead without adding
python scripts/freelance_pipeline.py score "Web Scraper" "$200" "python,scraping,api"

# Get morning digest
python scripts/freelance_pipeline.py digest

# Update lead status
python scripts/freelance_pipeline.py status 3 proposal_sent

# List all leads
python scripts/freelance_pipeline.py list
```

## Use Cases

- Automate morning lead discovery across multiple job boards
- Score and filter leads to focus on highest-value opportunities
- Generate personalized proposals at scale
- Track proposal win rates and optimize approach over time
- Manage freelance pipeline from discovery to payment