---
name: domainkits
description: Check availability. Search related domains. Find more possibilities. Explore connections. Turn AI into your domain agent. 
homepage: https://domainkits.com/mcp
metadata: {"openclaw":{"emoji":"🌐","primaryEnv":"DOMAINKITS_API_KEY"}}

---

## Why DomainKits?

With DomainKits MCP/Skills Your AI can now:
- **Data-driven actions** — See what's registering now, what's expiring tomorrow, what just dropped
- **Make informed decisions** — Analyze keyword value, brand risk, and safety in seconds
- **Execute instantly** — From idea to available domain with pricing in seconds

## Setup

### Claude Code
```bash
claude mcp add domainkits https://api.domainkits.com/v1/mcp
```

With API key (for higher limits):
```bash
claude mcp add domainkits https://api.domainkits.com/v1/mcp --header "X-API-Key: YOUR_KEY"
```

### Claude.ai
Connect DomainKits via **Settings → Connectors**. No manual configuration needed.

### Cursor / Other MCP Clients
Add to your MCP config:
```json
{
  "mcpServers": {
    "domainkits": {
      "url": "https://api.domainkits.com/v1/mcp"
    }
  }
}
```

With API key:
```json
{
  "mcpServers": {
    "domainkits": {
      "url": "https://api.domainkits.com/v1/mcp",
      "headers": {
        "X-API-Key": "YOUR_KEY"
      }
    }
  }
}
```


## Tools

Search
- `nrds` — Newly registered domains
- `aged` — Domains with 5-20+ years history
- `expired` — Domains entering deletion cycle
- `deleted` — Just-dropped domains, available now
- `active` — Live sites and for-sale listings
- `ns_reverse` — Domains on a specific nameserver
- `unregistered_ai` — Unregistered short .ai domains (3-letter, CVCV patterns)
- `domain_changes` — Monitor 4M+ domains for transfers, expirations, new registrations, and NS changes
- `price` — Registration costs by TLD

Query
- `available` — Availability check with pricing
- `whois` — Registration details
- `dns` — DNS records
- `safety` — Google Safe Browsing check
- `tld_check` — Keyword availability across TLDs
- `market_price` — Secondary market listings and price estimates

Analysis (requires account)
- `keyword_data` — Google Ads keyword data

Trends
- `keywords_trends` — Trending keywords in domain registrations (hot, emerging, prefix)
- `tld_trends` — TLD growth patterns
- `tld_rank` — Top TLDs by volume

Bulk
- `bulk_tld` — Check keyword popularity across TLDs
- `bulk_available` — Batch availability check with pricing

Workflows
- `analyze` — Comprehensive domain audit
- `brand_match` — Brand conflict detection with trademark links
- `plan_b` — Find alternatives when domain is taken
- `domain_generator` — Generate creative domains with validation
- `expired_analysis` — Due diligence for expired domains
- `trend_hunter` — Spot trends and find related opportunities
- `keyword_intel` — Deep keyword intelligence for domain investment
- `market_beat` — Domain market news briefing
- `name_advisor` — Professional domain naming consultation
- `valuation_cma` — Comparative Market Analysis valuation

Personal Tools (require memory)
- `preferences` — Manage memory and saved preferences (action: get/set/delete)
- `monitor` — Domain monitoring with auto WHOIS/DNS checks (action: get/set/update/delete)
- `strategy` — Automated opportunity discovery (action: get/set/update/delete)
- `usage` — Check current usage and remaining quota

## Instructions

When user wants domain suggestions:
1. Brainstorm names based on keywords
2. Call `bulk_available` to validate
3. Show available options with prices and `register_url`

When user wants to analyze a domain:
1. Call `whois`, `dns`, `safety`
2. Give a clear verdict

Output rules:
- Always show `register_url` for available domains
- Disclose affiliate links
- Default to `no_hyphen=true` and `no_number=true`

## Access Tiers

- **Guest** — Most tools, limited daily usage
- **Member** (free) — All tools, higher limits, memory features
- **AI Access** — Higher daily limits, more monitors and strategies
- **Premium** — Full access with highest limits
- **Platinum** — Unlimited

Register a free account and get your API key at https://domainkits.com

## Privacy

- Works without API key
- Memory OFF by default
- GDPR compliant
- Delete data anytime via `delete_preferences`

## Links

- Website: https://domainkits.com/mcp
- GitHub: https://github.com/ABTdomain/domainkits-mcp
- Contact: info@domainkits.com
- Developed by: https://abtdomain.com/