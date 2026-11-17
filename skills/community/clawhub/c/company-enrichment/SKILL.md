---
name: company-enrichment
description: "Company firmographics, tech stack, headcount, and intelligence from a domain — agent-ready account research."
version: 2.0.14
author: superagnt
license: MIT-0
platforms: [macos, linux, windows]
required_environment_variables:
  - SUPERAGNT_API_KEY
metadata:
  hermes:
    tags: [company-enrichment, firmographics, account-research]
  openclaw:
    requires:
      env:
        - SUPERAGNT_API_KEY
      bins:
        - curl
    primaryEnv: SUPERAGNT_API_KEY
    emoji: "🎯"
    homepage: https://superagnt.com/r/ch-company-enrichment-docs
---

# Company Enrichment

Resolve a domain or company name into structured account intelligence: firmographics, headcount, funding, competitors, technographics, and the emails known on the domain. Discover and search endpoints build target lists from plain criteria; bulk enrich processes whole account lists in one call. Everything is orchestrated server-side across multiple providers, so an agent gets one consistent JSON shape per company regardless of where the data came from. Built for account research before outreach, ICP filtering over raw lists, and market-mapping jobs.

## Alternative install: the scoped MCP server

If this client speaks MCP, you can connect the Company Enrichment facet
server instead of using this skill's curl calls — the same endpoints below as
native MCP tools with structured parameters and OAuth sign-in, scoped to this
capability:

```
https://mcp.superagnt.com/mcp/company-enrichment
```

That URL publishes full OAuth discovery: an MCP-capable client needs the URL
and nothing else (approve once in the browser). On clients that hold a bearer
instead, add it as an `Authorization: Bearer` header. Per-client setup lines:
https://www.superagnt.com/install?facet=company-enrichment

This skill document stays fully usable on curl-only environments — everything
below works with just the API key.

## Authentication

Get an API key from the [superagnt app](https://superagnt.com/r/ch-company-enrichment-key) and export it as
`SUPERAGNT_API_KEY`. Every request sends it as a Bearer token:

```
Authorization: Bearer $SUPERAGNT_API_KEY
```

If the variable is not set, ask the user for their key or point them at
https://superagnt.com/r/ch-company-enrichment-key.

## Verify the install (do this first)

One call proves the key, the credit balance, and this source end to end:

```bash
curl -s https://api.superagnt.com/v1/credits \
  -H &#x27;Authorization: Bearer $SUPERAGNT_API_KEY&#x27;
```

A JSON result means you are live. A 401 means the key is wrong or missing; a
402 means the workspace is out of credits — the superagnt app shows both.

## Base URL

```
https://api.superagnt.com/v1/data/agnt
```

## Available Endpoints

| Method | Path | Summary |
|--------|------|---------|
| `POST` | `/companies/enrich` | Enrich a company |
| `POST` | `/companies/bulk-enrich` | Bulk enrich companies |
| `POST` | `/companies/search` | Search companies |
| `POST` | `/companies/discover` | Discover companies |
| `POST` | `/companies/intelligence` | Company intelligence (funding / competitors / technographics) |
| `POST` | `/companies/domain-emails` | List a domain&#x27;s emails |

## Tool Schemas

The following JSON defines every operation with its parameters. Each tool maps
to an API endpoint under the base URL.

```json
[
  {
    "name": "superagnt_agnt_companies_enrich",
    "description": "Enrich a company",
    "method": "POST",
    "path": "/companies/enrich",
    "parameters": {
      "$ref": "#/components/schemas/CompaniesEnrichRequest"
    }
  },
  {
    "name": "superagnt_agnt_companies_bulk_enrich",
    "description": "Bulk enrich companies",
    "method": "POST",
    "path": "/companies/bulk-enrich",
    "parameters": {
      "$ref": "#/components/schemas/CompaniesBulkEnrichRequest"
    }
  },
  {
    "name": "superagnt_agnt_companies_search",
    "description": "Search companies",
    "method": "POST",
    "path": "/companies/search",
    "parameters": {
      "$ref": "#/components/schemas/CompaniesSearchRequest"
    }
  },
  {
    "name": "superagnt_agnt_companies_discover",
    "description": "Discover companies",
    "method": "POST",
    "path": "/companies/discover",
    "parameters": {
      "$ref": "#/components/schemas/CompaniesDiscoverRequest"
    }
  },
  {
    "name": "superagnt_agnt_companies_intelligence",
    "description": "Company intelligence (funding / competitors / technographics)",
    "method": "POST",
    "path": "/companies/intelligence",
    "parameters": {
      "$ref": "#/components/schemas/CompaniesIntelligenceRequest"
    }
  },
  {
    "name": "superagnt_agnt_companies_domain_emails",
    "description": "List a domain's emails",
    "method": "POST",
    "path": "/companies/domain-emails",
    "parameters": {
      "$ref": "#/components/schemas/CompaniesDomainEmailsRequest"
    }
  }
]
```

## Example

```bash
curl -X POST &#x27;https://api.superagnt.com/v1/data/agnt/companies/enrich&#x27; \
  -H &#x27;Authorization: Bearer $SUPERAGNT_API_KEY&#x27; \
  -H &#x27;Content-Type: application/json&#x27; \
  -d &#x27;{&quot;...&quot;: &quot;see tool schemas below&quot;}&#x27;
```

## Use Cases


## Scope

This skill covers Company Enrichment only — the endpoints listed above,
nothing else. The same API key also works with superagnt's other data sources
and platform tools, but those are separate listings that the user installs or
enables themselves; this skill does not add or enable anything beyond what is
documented here. The public catalog is at `https://api.superagnt.com/v1/platforms`.

## Links

- [Documentation](https://superagnt.com/r/ch-company-enrichment-docs)
- [superagnt app / API keys](https://superagnt.com/r/ch-company-enrichment-key)
- [This listing](https://clawhub.ai/superagnt/skills/company-enrichment)
