---
name: agentpmt-docs-and-content
description: "AgentPMT Platform Search: Use this internal AgentPMT search tool when an agent needs official AgentPMT results from the website, marketplace. Use when an agent needs agentpmt platform search, agentpmt docs and content, search the agentpmt website for anything relevant to a user question, find agentpmt tools/products by capability or name, discover public agentpmt workflows, discover public agentpmt agents, get instructions, global search through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/agentpmt-docs-and-content
compatibility: "Requires AgentPMT internal handler access through the external marketplace API. Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/agentpmt-docs-and-content"}}
---
# AgentPMT Platform Search

## Freshness
Last updated: `2026-07-31`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Find anything on AgentPMT and answer questions with official sources. This tool lets your AI agents search the whole AgentPMT site at once -- marketplace tools, workflows, and prebuilt agents along with documentation, help articles, research papers, videos, and FAQs -- and bring back the most relevant results with links to the real pages. Use it to answer "is there a tool for this?", route people to the right documentation, surface the newest content, and ground agent responses in genuine AgentPMT resources instead of guessing or scraping the open web.

## Product Instructions
Choose the action based on scope.

Use `global_search` when the user asks to search AgentPMT broadly or find anything on the website, including tools/products, workflows, agents, docs, articles, papers, videos, pages, or FAQs. Provide `query` and optionally `types` and `limit`. Supported `types` values are `product`, `workflow`, `agent`, `article`, `paper`, `video`, `doc`, `page`, and `faq`. Omit `types` to search all supported result kinds. Set `limit` from 1 to 50; default is 10.

Use `search` when the user specifically wants AgentPMT public knowledge content only. Provide `query` and optionally `content_types` and `limit`. Supported `content_types` values are `article`, `paper`, `video`, `doc`, and `faq`. This action intentionally does not return tools, workflows, agents, or static pages.

Use `recent` when the user asks for the newest AgentPMT public content instead of relevance-ranked search. Optionally pass `content_types`, `limit`, and `skip`. `skip` is only for recent-content pagination and is ignored by search actions.

Use `get_instructions` to retrieve handler guidance.

Result modes are explicit: `global_search` returns `mode: "global_search"`, `search` returns `mode: "search"`, and `recent` returns `mode: "recent"`. `global_search` items include only the sanitized agent-facing fields `id`, `kind`, `title`, `summary`, `url`, `thumbnail`, `score`, `match_type`, `source`, and `visibility` when those values are available, plus response-level `facets`, `cursor`, `degraded_sources`, `query`, `types`, and counts. The global output must not include vendor names, vendor identifiers, vendor fields, or frontend badges.

`search` and `recent` return content-focused items with canonical public URLs where available. FAQ results are limited to standalone public FAQs and exclude product-linked or workflow-linked FAQ records.

This tool searches AgentPMT's own public site and catalog surfaces only. It is not a general web search engine and should not be used for arbitrary internet research.

## When To Use
- Use this skill for `AgentPMT Platform Search` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: agentpmt platform search, agentpmt docs and content, search the agentpmt website for anything relevant to a user question, find agentpmt tools/products by capability or name, discover public agentpmt workflows, discover public agentpmt agents, get instructions, global search.
- Supported action names: `get_instructions`, `global_search`, `recent`, `search`.

## Use Cases
- Search the AgentPMT website for anything relevant to a user question
- Find AgentPMT tools/products by capability or name
- Discover public AgentPMT workflows
- Discover public AgentPMT agents
- Find official AgentPMT documentation pages
- Search AgentPMT articles papers videos docs pages and FAQs in one request
- Search only knowledge content when a response should cite docs articles papers videos or FAQs
- Retrieve canonical public AgentPMT URLs for citations
- Route users to relevant marketplace tools workflows agents or docs
- Answer user questions using official AgentPMT content instead of scraping pages
- List recent AgentPMT public content by type
- Build agent responses that cite official AgentPMT resources
- Search the site without exposing vendor names or vendor identifiers in agent-facing results

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `4`.
x402 availability: not enabled for this product.

- `get_instructions` (action slug: `get-instructions`): Return usage instructions for this content search handler. Price: `0` credits. Parameters: none.
- `global_search` (action slug: `global-search`): Search the public AgentPMT site across tools, workflows, agents, articles, papers, videos, docs, pages, and FAQs. Price: `0` credits. Parameters: `cursor`, `limit`, `query`, `types`.
- `recent` (action slug: `recent`): Return the most recently published public content for selected types. Price: `0` credits. Parameters: `content_types`, `limit`, `skip`.
- `search` (action slug: `search`): Search public articles, papers, videos, docs, FAQs, or all content. Price: `0` credits. Parameters: `content_types`, `cursor`, `limit`, `query`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "agentpmt-docs-and-content"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "agentpmt-docs-and-content"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "agentpmt-docs-and-content"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "agentpmt-docs-and-content"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "agentpmt-docs-and-content"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "agentpmt-docs-and-content"
  }
}
```

## Call This Tool
Product slug: `agentpmt-docs-and-content`

Marketplace page: https://www.agentpmt.com/marketplace/agentpmt-docs-and-content

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
    "name": "AgentPMT-Platform-Search",
    "arguments": {
      "action": "get_instructions"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "agentpmt-docs-and-content",
  "parameters": {
    "action": "get_instructions"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `get_instructions` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/agentpmt-docs-and-content
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
