---
name: digital-labour
version: 1.0.0
description: "24 AI agents for business automation - sales outreach, lead gen, content creation, SEO, ad copy, bookkeeping, proposals, market research, business plans, tech docs, data entry, web scraping, CRM ops, and more. Multi-agent pipelines with QA verification on every output. Powered by GPT-4o, Claude, Gemini, and Grok."
tags: [ai-agents, business-automation, sales, lead-generation, content-creation, seo, bookkeeping, proposals, market-research, freelancing, saas, api]
author: Resonance Energy
homepage: https://bitrage-labour-api-production.up.railway.app
metadata:
  author: Resonance Energy
  version: "1.0.0"
  openclaw:
    emoji: ⚡
    homepage: "https://bitrage-labour-api-production.up.railway.app"
    requires:
      env:
        - DIGITAL_LABOUR_API_URL
      bins:
        - python3
    primaryEnv: DIGITAL_LABOUR_API_URL
compatibility: "Requires Python 3.6+ (stdlib only, no pip installs). Requires DIGITAL_LABOUR_API_URL environment variable (defaults to production API)."
---

# ⚡ Digital Labour — 24 AI Agents for Business Automation

> **Your entire back-office, automated.** Run any of 24 specialized AI agents through plain English. Sales outreach, lead generation, content repurposing, SEO, ad copy, bookkeeping, proposals, market research, tech docs — all with built-in QA verification.

## Quick Start

Set your API URL (or use the default production endpoint):
```bash
export DIGITAL_LABOUR_API_URL="https://bitrage-labour-api-production.up.railway.app"
```

Test the connection:
```bash
python3 {baseDir}/scripts/dl-api.py health
```

Run an agent:
```bash
python3 {baseDir}/scripts/dl-api.py run support_ticket '{"ticket_text": "My order has not arrived after 2 weeks"}'
```

## Available Agents (24 Total)

### Revenue & Sales (5 agents)
| Agent | Command | What it does |
|-------|---------|-------------|
| **sales_outreach** | `run sales_outreach '{"company":"Stripe","role":"Head of Sales"}'` | Company research + 3-email outreach sequence |
| **lead_gen** | `run lead_gen '{"industry":"fintech","region":"North America"}'` | Generate qualified lead lists for any industry |
| **email_marketing** | `run email_marketing '{"product":"SaaS CRM","audience":"small business owners"}'` | Full email campaign with subject lines + body copy |
| **proposal_writer** | `run proposal_writer '{"project":"Website redesign","client_name":"Acme Corp"}'` | Professional project proposals with pricing |
| **ad_copy** | `run ad_copy '{"product":"AI writing tool","platform":"google"}'` | Platform-optimized ad copy (Google/Facebook/Instagram) |

### Content & Marketing (4 agents)
| Agent | Command | What it does |
|-------|---------|-------------|
| **content_repurpose** | `run content_repurpose '{"content":"<blog post text>"}'` | Repurpose content into tweets, LinkedIn, newsletters |
| **seo_content** | `run seo_content '{"keyword":"AI automation","content_type":"blog"}'` | SEO-optimized content (blog/landing/pillar pages) |
| **social_media** | `run social_media '{"topic":"AI trends","platform":"linkedin","cta_goal":"drive signups"}'` | Platform-native social posts with CTAs |
| **press_release** | `run press_release '{"announcement":"Product launch","company":"Bitrage"}'` | PR-ready press releases |

### Operations & Data (4 agents)
| Agent | Command | What it does |
|-------|---------|-------------|
| **data_entry** | `run data_entry '{"source_data":"<raw data>","output_format":"CSV"}'` | Structure and clean raw data |
| **web_scraper** | `run web_scraper '{"source_url":"https://example.com","extraction_target":"pricing"}'` | Extract structured data from web pages |
| **crm_ops** | `run crm_ops '{"contact_data":"<contact info>","action":"segment"}'` | CRM updates, segmentation, and reporting |
| **bookkeeping** | `run bookkeeping '{"transactions":"<transaction data>","period":"monthly"}'` | Transaction categorization and financial reports |

### Documents & Research (4 agents)
| Agent | Command | What it does |
|-------|---------|-------------|
| **doc_extract** | `run doc_extract '{"document_text":"<doc text>","doc_type":"invoice"}'` | Extract structured data from invoices, contracts, resumes |
| **market_research** | `run market_research '{"topic":"electric vehicles","depth":"detailed"}'` | Market analysis at overview/detailed/comprehensive depth |
| **business_plan** | `run business_plan '{"business_idea":"AI tutoring app","market":"K-12 education"}'` | Full business plans with financial projections |
| **tech_docs** | `run tech_docs '{"code_or_api":"<code or API spec>","doc_type":"api"}'` | API docs, READMEs, and tutorials |

### Professional Services (3 agents)
| Agent | Command | What it does |
|-------|---------|-------------|
| **support_ticket** | `run support_ticket '{"ticket_text":"<customer issue>"}'` | Categorize, prioritize, draft reply for support tickets |
| **product_desc** | `run product_desc '{"product_specs":"<specs>","tone":"luxury"}'` | Product descriptions in any tone |
| **resume_writer** | `run resume_writer '{"career_data":"<career history>","target_industry":"tech"}'` | ATS-optimized resumes for any industry |

### Management Layer (4 agents)
| Agent | Command | What it does |
|-------|---------|-------------|
| **context_manager** | Internal orchestration | Maintains context across multi-agent pipelines |
| **qa_manager** | Internal orchestration | Quality assurance on every agent output |
| **production_manager** | Internal orchestration | Workflow scheduling and resource allocation |
| **automation_manager** | Internal orchestration | Autonomous task routing and retry logic |

## Helper Script

`scripts/dl-api.py` — Python script (stdlib only) for all API operations.

**Commands:**
| Command | Description |
|---------|-------------|
| `health` | Check API health status |
| `agents` | List all available agents with input schemas |
| `run <agent> <json_inputs>` | Run a specific agent with JSON inputs |
| `batch <json_file>` | Run multiple agents from a JSON batch file |

**Examples:**
```bash
# Check health
python3 {baseDir}/scripts/dl-api.py health

# List all agents
python3 {baseDir}/scripts/dl-api.py agents

# Generate sales outreach
python3 {baseDir}/scripts/dl-api.py run sales_outreach '{"company":"Tesla","role":"VP Engineering"}'

# Write a business plan
python3 {baseDir}/scripts/dl-api.py run business_plan '{"business_idea":"AI-powered pet care app","market":"pet owners 25-45"}'

# Generate SEO content
python3 {baseDir}/scripts/dl-api.py run seo_content '{"keyword":"remote work tools 2026","content_type":"pillar"}'

# Run a batch of tasks
python3 {baseDir}/scripts/dl-api.py batch {baseDir}/examples/batch.json
```

## Batch Processing

Create a JSON file with multiple tasks:
```json
[
  {"agent": "sales_outreach", "inputs": {"company": "Stripe", "role": "CTO"}},
  {"agent": "ad_copy", "inputs": {"product": "AI CRM", "platform": "facebook"}},
  {"agent": "seo_content", "inputs": {"keyword": "business automation", "content_type": "blog"}}
]
```

Run them all:
```bash
python3 {baseDir}/scripts/dl-api.py batch tasks.json
```

## Multi-Agent Workflows

Chain agents together for complex operations:

**Lead-to-Close Pipeline:**
1. `lead_gen` → find prospects in target industry
2. `market_research` → understand their pain points
3. `sales_outreach` → personalized outreach sequence
4. `proposal_writer` → ready proposal when they respond

**Content Engine:**
1. `market_research` → trending topics in your niche
2. `seo_content` → long-form SEO blog post
3. `content_repurpose` → tweets, LinkedIn, newsletter from that post
4. `social_media` → platform-native posts with CTAs
5. `ad_copy` → paid promotion copy

**Client Onboarding:**
1. `doc_extract` → pull data from client documents
2. `data_entry` → structure into your system format
3. `bookkeeping` → set up financial tracking
4. `crm_ops` → create CRM records

## API Details

- **Base URL**: `https://bitrage-labour-api-production.up.railway.app`
- **Universal Endpoint**: `POST /v1/run`
- **Agent List**: `GET /agents`
- **Health Check**: `GET /health`
- **Docs**: `GET /docs`
- **LLM Providers**: OpenAI (GPT-4o), Anthropic (Claude), Google (Gemini), xAI (Grok)
- **QA**: Every output passes through QA verification before returning

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DIGITAL_LABOUR_API_URL` | Yes | `https://bitrage-labour-api-production.up.railway.app` | API base URL |
| `DIGITAL_LABOUR_API_KEY` | No | *(none)* | Optional API key for authenticated access |

## Important Notes

- Each agent call takes 3-15 seconds (real LLM inference, not cached)
- All outputs include QA verification status
- The `provider` field is optional in all agent inputs — omit to use the server default
- Management agents (context_manager, qa_manager, etc.) are internal and run automatically during pipelines
- Batch mode processes tasks sequentially to respect rate limits
- All agent outputs are structured JSON with consistent schema
