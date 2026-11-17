---
name: available-domain-search
description: "Available Domain Search: Domain name discovery and live availability checking. Use when an agent needs available domain search, find available domain names for a new business, brainstorm brandable domain ideas from a plain language business description, check whether a specific domain name is available to register, bulk check availability across a shortlist of domain names, domains check availability, domains, domains suggest through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/available-domain-search
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/available-domain-search"}}
---
# Available Domain Search

## Freshness
Last updated: `2026-08-19`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Find the perfect domain name — and know instantly whether you can actually register it. Describe your business in plain language and get back a list of short, brandable domain ideas, or bring the shortlist you already have and check every name at once. Search a single domain or up to 1,000 in one pass across .com, .net, .org, .io, .co, .ai, .shop and hundreds of other extensions, see exactly which names are open and which are already taken, and get a direct one-click registration link for every available domain. Ideal for naming a new startup, claiming a domain for a product launch or side project, sourcing landing-page URLs for a marketing campaign, or locking down the matching extensions so nobody else can take your brand.

## When To Use
- Use this skill for `Available Domain Search` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: available domain search, find available domain names for a new business, brainstorm brandable domain ideas from a plain language business description, check whether a specific domain name is available to register, bulk check availability across a shortlist of domain names, domains check availability, domains, domains suggest.
- Supported action names: `domains_check_availability`, `domains_suggest`, `get_instructions`.

## Use Cases
- Find available domain names for a new business
- Brainstorm brandable domain ideas from a plain-language business description
- Check whether a specific domain name is available to register
- Bulk check availability across a shortlist of domain names
- Compare availability across .com .net .io .co .ai and other TLDs
- Secure matching domain extensions to protect a brand
- Source landing page domains for a marketing campaign
- Name a new product
- app
- or side project
- Get direct registration links for every available domain
- Find strong alternatives when the .com is already taken

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `3`.
x402 availability: not enabled for this product.

- `domains_check_availability` (action slug: `domains-check-availability`): Check if domain names are available for registration. Works with single domains or lists of multiple domains. Returns formatted results with availability status and registration options ready for display. IMPORTANT: Always display the registration links from the response to the user - each domain has a direct GoDaddy registration URL that must be shown. Price: `3` credits. Parameters: `domains`.
- `domains_suggest` (action slug: `domains-suggest`): Generate domain name suggestions based on keywords, seed domains, or business descriptions. Returns an interactive widget with clickable domain links for clients that support HTML rendering (browsers, web-based AI assistants), with automatic fallback to formatted text for other clients. IMPORTANT: Always display the registration links from the response to the user - each domain has a direct GoDaddy registration URL that must be shown. Price: `3` credits. Parameters: `limit`, `query`.
- `get_instructions` (action slug: `get-instructions`): Get tool instructions and available actions. Price: `3` credits. Parameters: none.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "available-domain-search"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "available-domain-search"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "available-domain-search"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "available-domain-search"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "available-domain-search"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "available-domain-search"
  }
}
```

## Call This Tool
Product slug: `available-domain-search`

Marketplace page: https://www.agentpmt.com/marketplace/available-domain-search

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Available-Domain-Search",
    "arguments": {
      "action": "domains_check_availability",
      "domains": "example domains"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "available-domain-search",
  "parameters": {
    "action": "domains_check_availability",
    "domains": "example domains"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `domains_check_availability` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/available-domain-search
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
