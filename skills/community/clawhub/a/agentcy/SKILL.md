---
name: agentcy
description: Your OpenClaw team's marketing analyst — just tell your agent what you need to know about your clients' marketing and Agentcy delivers synthesized insights and recommendations. Covers GA4, Google Ads, Search Console, WooCommerce, and more.
version: 1.0.0
files:
  - agentcy_query.sh
  - agentcy_research.sh
  - agentcy_sources.sh
metadata:
  clawdbot:
    primaryEnv: AGENTCY_API_KEY
    homepage: https://www.goagentcy.com
    requires:
      env:
        - AGENTCY_API_KEY
      bins:
        - curl
        - jq
---

# Agentcy — Marketing Intelligence

All-in-one marketing intelligence for OpenClaw agents. Query analytics, ad campaigns, search rankings, e-commerce data, run competitive research, and discover connected data sources — all through the Agentcy REST API.

## Quick Start

### Install

```bash
npx clawhub@latest install agentcy
```

### Configure

**Step 1 — Sign up and get your API key:**
1. Create an account at [goagentcy.com](https://www.goagentcy.com)
2. Go to the portal at [app.goagentcy.com](https://app.goagentcy.com)
3. Create an API key (starts with `agcy_`)

**Step 2 — Connect your data sources:**
1. In the portal, add your client domains (e.g., "aurora-fitness.com")
2. For each domain, connect the data sources you want to query:
   - Google Analytics 4 — click Connect, authorize with Google
   - Google Search Console — click Connect, authorize with Google
   - Google Ads — click Connect, authorize with Google
   - WooCommerce — enter store URL + API credentials
   - HubSpot, SpyFu, etc. — enter API keys
3. Web utilities (PageSpeed, DNS, SSL, etc.) work automatically — no setup needed

**Step 3 — Set your API key:**

```bash
export AGENTCY_API_KEY="agcy_your_key_here"
```

### Verify

Run the sources command to confirm your domains and connected services:

```bash
./skills/agentcy/agentcy_sources.sh
```

You should see your configured domains and their connected services listed.

## Commands

This skill includes three commands:

### 1. agentcy_query.sh — Query Marketing Data

Use when you need to answer questions about marketing performance, analytics, ad campaigns, search rankings, traffic, conversions, revenue, or any other marketing data for a client domain.

```bash
./skills/agentcy/agentcy_query.sh "question" "domain" [start_date] [end_date] [source_hints]
```

| Arg | Required | Description |
|-----|----------|-------------|
| question | Yes | Natural language question about marketing data |
| domain | Yes | Client domain to query (e.g., "example.com") |
| start_date | No | Default: "30daysAgo". Accepts YYYY-MM-DD or relative ("7daysAgo") |
| end_date | No | Default: "yesterday". Accepts YYYY-MM-DD or relative ("yesterday") |
| source_hints | No | Comma-separated data source hints (e.g., "ga4,gsc") |

**Examples:**

```bash
# Basic query — Agentcy picks the right data source automatically
./skills/agentcy/agentcy_query.sh "How is organic traffic trending?" "aurora-fitness.com"

# With date range
./skills/agentcy/agentcy_query.sh "Google Ads performance" "aurora-fitness.com" "7daysAgo" "yesterday"

# With source hints
./skills/agentcy/agentcy_query.sh "Top converting pages" "aurora-fitness.com" "30daysAgo" "yesterday" "ga4,gsc"
```

### 2. agentcy_research.sh — Web Research & Competitive Intel

Use for competitive analysis, market research, industry trends, pricing comparisons, or any question that requires searching the web rather than querying connected data sources.

```bash
./skills/agentcy/agentcy_research.sh "research question" ["domain-for-context"]
```

| Arg | Required | Description |
|-----|----------|-------------|
| question | Yes | Natural language research question |
| domain | No | Client domain for context (helps scope competitive research) |

**Examples:**

```bash
./skills/agentcy/agentcy_research.sh "What pricing strategies are competitors using for protein supplements?" "aurora-fitness.com"
./skills/agentcy/agentcy_research.sh "Latest Google Ads best practices for e-commerce 2026"
```

### 3. agentcy_sources.sh — Discover Data Sources

Use to check what domains are configured and which data sources are connected before running a query.

```bash
./skills/agentcy/agentcy_sources.sh ["domain"]
```

**Examples:**

```bash
# List all configured domains
./skills/agentcy/agentcy_sources.sh

# Check a specific domain
./skills/agentcy/agentcy_sources.sh "aurora-fitness.com"
```

## Response Format

All commands return synthesized marketing insights as plain text — not raw JSON. Responses are ready to use directly in your analysis and recommendations.

- **agentcy_query.sh** — Returns an insight with a `[Sources: ...]` footer showing which data sources were used
- **agentcy_research.sh** — Returns synthesized research findings with sources cited
- **agentcy_sources.sh** — Lists domains with their connected services and always-available utilities

## Data Sources Available

| Source | Category | Auth |
|--------|----------|------|
| Google Analytics 4 | Analytics | Google OAuth |
| Google Search Console | Search / SEO | Google OAuth |
| Google Ads | Advertising | Google OAuth |
| YouTube Analytics | Video / Content | Google OAuth |
| WooCommerce | E-commerce | API Key |
| HubSpot | CRM / Marketing | API Key |
| SpyFu | Competitive Intel | API Key |
| PageSpeed, DNS, SSL, WHOIS, Sitemap, Schema, Readability, Tech Detection | Web Utilities | Included |
| Web Intelligence | Research | Included |

## External Endpoints

| Endpoint | Method | Purpose | Auth |
|----------|--------|---------|------|
| `https://data.goagentcy.com/api/query` | POST | Query marketing data sources | Bearer token (AGENTCY_API_KEY) |
| `https://data.goagentcy.com/api/research` | POST | Web research and competitive intelligence | Bearer token (AGENTCY_API_KEY) |
| `https://data.goagentcy.com/api/sources` | GET | List configured domains and data sources | Bearer token (AGENTCY_API_KEY) |

## Security & Privacy

- API key is read from the `AGENTCY_API_KEY` environment variable — never hardcoded
- The key is sent only to `data.goagentcy.com` over HTTPS
- Data isolation is enforced by the `domain` parameter — each query is scoped to a single client
- No marketing data is cached or stored by this skill
- Response content is synthesized text — no raw customer PII is returned
- All scripts use `set -euo pipefail` and build JSON payloads with `jq` (no shell injection)

## Publisher

Agentcy — [goagentcy.com](https://www.goagentcy.com)
