---
name: dynamics-partner-advisor
description: "Search, compare, and shortlist Microsoft Dynamics 365 implementation partners by product, industry, and region. Use when someone asks about finding a Dynamics partner, comparing ERP/CRM consultants, selecting a Business Central or Finance & Operations implementer, or needs help choosing a Microsoft partner for an ERP or CRM project. Connects to the live Top Dynamics Partners database via MCP (Model Context Protocol)."
license: MIT
compatibility: "Requires MCP client support (Claude Desktop, Claude Code, Cursor, Windsurf, Cline, or any MCP-compatible agent). No local dependencies - connects to a hosted SSE endpoint."
metadata:
  author: Ignite Marketing
  version: 1.0.0
  tags: microsoft-dynamics, erp, crm, business-central, partner-selection, mcp
  website: https://topdynamicspartners.com
  repository: https://github.com/ignitemarketing/dynamics-partner-advisor
---

# Dynamics Partner Advisor

Search, compare, and shortlist Microsoft Dynamics 365 implementation partners — powered by the live [Top Dynamics Partners](https://topdynamicspartners.com) database.

This skill connects to a hosted MCP (Model Context Protocol) server. No local code, no dependencies, no API wrappers — just point your agent at the SSE endpoint and start querying.

## When to Use

- Someone asks "Who are the best Dynamics 365 Business Central partners in Texas?"
- A consultant needs to compare ERP implementation firms by industry vertical
- A project manager wants a shortlist of partners ranked by fit for their specific requirements
- Anyone evaluating Microsoft Dynamics partners for an ERP or CRM implementation

## Setup

Add the MCP server configuration to your agent:

### Claude Desktop / Claude Code / Cursor

\`\`\`json
{
  "mcpServers": {
    "dynamics-partner-advisor": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sse", "https://topdynamicspartners.com/api/mcp/sse"]
    }
  }
}
\`\`\`

### Direct SSE Connection

For agents that support SSE transport natively:

- **SSE Endpoint:** \`https://topdynamicspartners.com/api/mcp/sse\`
- **Messages Endpoint:** \`https://topdynamicspartners.com/api/mcp/messages\`

No API key required for basic access.

## Available Tools

### search_partners

Search for Dynamics 365 partners by product, industry, and location.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Yes | Natural language search (e.g., "Business Central partners in Chicago") |
| product | string | No | Filter by Dynamics product (e.g., "Business Central", "Finance & Operations") |
| industry | string | No | Filter by industry vertical (e.g., "Manufacturing", "Healthcare") |
| region | string | No | Filter by geographic region (e.g., "US-Midwest", "Canada") |
| limit | number | No | Max results to return (default: 10) |

### get_partner_details

Retrieve a comprehensive profile for a specific partner.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| partner_id | string | Yes | The unique partner identifier |
| include_reviews | boolean | No | Include client review summaries (default: false) |

Returns: Full partner profile including functional strengths, years in business, Microsoft designations, client size fit, geographic coverage, and notable implementations.

### recommend_shortlist

Generate an AI-scored shortlist of partners matched to specific project requirements.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| project_description | string | Yes | Describe the project needs, goals, and constraints |
| company_size | string | No | Your company size (e.g., "SMB", "Mid-Market", "Enterprise") |
| budget_range | string | No | Approximate implementation budget range |
| timeline | string | No | Desired implementation timeline |
| must_have | array | No | Required capabilities or certifications |

Returns: Ranked list of 3-5 partners with match scores, reasoning, and specific strengths relevant to the described project.

## Access Tiers

| Feature | Free (No Key) | Authenticated (API Key) |
|---------|--------------|------------------------|
| Results per query | 3 | 25 |
| Rate limit | 30 req/min | 60 req/min |
| Partner details | Basic | Full profile + reviews |
| Shortlist scoring | Standard | Enhanced AI scoring |

Request an API key at [topdynamicspartners.com/resources/mcp-server](https://topdynamicspartners.com/resources/mcp-server).

## Data Source

All data is sourced from the live [Top Dynamics Partners](https://topdynamicspartners.com) directory — a curated, continuously updated database of Microsoft Dynamics 365 implementation partners across North America.

## Links

- [Top Dynamics Partners](https://topdynamicspartners.com) — Main directory
- [MCP Server Documentation](https://topdynamicspartners.com/resources/mcp-server) — Full API docs and key registration
- [Partner Comparison Tool](https://topdynamicspartners.com/compare) — Web-based partner comparison
- [GitHub Repository](https://github.com/ignitemarketing/dynamics-partner-advisor) — Source and configuration
