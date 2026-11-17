---
name: domainkits
description: Check domain availability. Search domains by keyword across the full lifecycle, from newly registered to expired and deleted. Analyze keyword value and trends. Turn AI into your domain agent. domainkits.com
homepage: https://domainkits.com/mcp
metadata: {"openclaw":{"emoji":"🌐","primaryEnv":"DOMAINKITS_API_KEY"}}

---

## Why DomainKits?

With DomainKits MCP your AI can:
- **Data-driven actions**: see what's registering now, what's expiring, and what just dropped
- **Informed decisions**: analyze keyword value and brand risk in seconds
- **Fast execution**: go from an idea to an available domain with pricing in seconds

## Setup

- Endpoint: `https://api.domainkits.com/v1/mcp` (optional header `X-API-Key` for account limits)
- Claude Code: `claude mcp add --transport http domainkits https://api.domainkits.com/v1/mcp`
- Setup for Claude.ai, Claude Desktop, Gemini CLI, Cursor: [domainkits.com/mcp](https://domainkits.com/mcp)

## How to use the tools

DomainKits tools return domain data; the analysis is yours. Their data is fresher than your training knowledge, so for anything recent, go by the tool result.

Each tool's description and input schema define its data, parameters, and accepted values. Follow them as written, and do not carry one tool's parameter values over to another.

Before a multi-tool sequence the user did not ask for, confirm the goal with the user. Tool calls count against their quota.

### Pick the tool by lifecycle stage

| Stage | Tools | What they find |
|---|---|---|
| Newly registered | `nrds_live`, `nrds` | Recent registrations by keyword or TLD. `nrds_live` for the newest names, `nrds` for a longer history with more filters |
| Registered | `active`, `aged`, `market` | Live registered domains. `aged` for long registration histories, `market` for names with marketplace listing data |
| Expired | `expired` | Domains in the deletion cycle, not yet open for registration |
| Deleted | `deleted` | Domains that completed the deletion cycle and are open for registration |
| Changes | `domain_changes` | Recent registration and status changes to premium names |
| Unregistered | `unregistered_ai` | Short .ai names open for registration |

### Look up one domain

- `whois`: registration data. `epp_status` explains the status codes it returns.
- `dns`: DNS records.
- `ip_lookup`: network operator and approximate location of an IP or domain.
- `registrar`: a registrar's accreditation and parent company.
- `available`: whether one domain can be registered, and its price. `bulk_available`: the same question for a list of domains.
- `tld_check`, `bulk_tld`: one name across TLDs.
- `price`: registration and renewal prices by TLD. `market_price`: aftermarket listing price.
- `backlink_summary`: backlink profile. `keyword_data`: keyword search data.
- `keywords_trends`: what people are registering recently, as keyword lists. `tld_trends`, `tld_rank`: registration trends by TLD.

### Connect results when the user asks

- Infrastructure behind a domain: nameservers from `whois` or `dns`, then `ns_reverse` for other domains on those nameservers. `ip_lookup` adds the network operator.
- Lookalikes of a brand: `typosquat` for registered variants of a domain; `nrds_live` or `nrds` for new registrations containing the brand keyword.
- Current state of an `expired` result: `whois`.
- Registrability of a `deleted` result: `available`.
- Whether a domain is flagged as unsafe: DomainKits has no threat check. Use a URL threat-check tool the user has connected, or tell the user this check is unavailable.

### Report results

- For paged results, report the total separately from the number of results reviewed, and say how many pages were checked. Fetch more pages only when the user wants them.
- A tool's own message about a result, such as no records found, is part of the answer. Pass it on rather than treating it as a failure.
- On a limit or plan message, do not retry the same call. Tell the user what was limited.

### Account tools

- `usage`: the user's current tier and remaining quota.
- `preferences`, `monitor`, `strategy`: stored on the user's DomainKits account. Create, change, or delete them only with the user's explicit consent.

## Skills

DomainKits MCP serves raw data. For domain workflows (brand protection, domain analysis, comparative valuation, name generation, naming advice, keyword intelligence, keyword trends, and market briefings), see [DomainKits Skills](https://github.com/ABTdomain/domainkits-skills), an open-source collection of workflow skills that any AI assistant can use on top of this data.

## Access

Works without an API key on a guest quota. A free account raises it; paid tiers raise it further. Current per-tier limits are listed at [domainkits.com/pricing](https://domainkits.com/pricing); the `usage` tool reports the live quota for the current account. Register free at [domainkits.com](https://domainkits.com/register).

## Privacy

- Works without API key (guest access)
- Memory OFF by default, requires explicit consent
- All stored data encrypted at rest (AES-256-GCM)
- GDPR compliant, delete data anytime via `preferences` with action: delete

## Links

- Website: https://domainkits.com/mcp
- Skills: https://github.com/ABTdomain/domainkits-skills
- GitHub: https://github.com/ABTdomain/domainkits-mcp
- Contact: info@domainkits.com
