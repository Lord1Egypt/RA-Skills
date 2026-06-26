# Coherence Network MCP Server

## Install & Run

```bash
npx coherence-mcp-server
```

Or install globally:

```bash
npm i -g coherence-mcp-server
coherence-mcp-server
```

## Configure in your AI agent

### Claude Desktop / Claude Code

Add to `~/.claude/settings.json` or project `.claude/settings.json`:

```json
{
  "mcpServers": {
    "coherence-network": {
      "command": "npx",
      "args": ["coherence-mcp-server"],
      "env": {
        "COHERENCE_API_URL": "https://api.coherencycoin.com"
      }
    }
  }
}
```

### Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "coherence-network": {
      "command": "npx",
      "args": ["coherence-mcp-server"]
    }
  }
}
```

### OpenClaw

The skill auto-detects the MCP server when `coherence-mcp-server` is installed.

## Available Tools (21)

### Ideas (6 tools)

| Tool | Description |
|------|-------------|
| `coherence_list_ideas` | Browse portfolio ranked by ROI. Params: `limit`, `search` |
| `coherence_get_idea` | Get full idea detail. Params: `idea_id` |
| `coherence_idea_progress` | Idea progress: stage, tasks, CC staked. Params: `idea_id` |
| `coherence_select_idea` | Portfolio engine picks next idea. Params: `temperature` |
| `coherence_showcase` | Validated, shipped ideas |
| `coherence_resonance` | Ideas with most activity right now |

### Specs (2 tools)

| Tool | Description |
|------|-------------|
| `coherence_list_specs` | List specs with ROI. Params: `limit`, `search` |
| `coherence_get_spec` | Full spec detail. Params: `spec_id` |

### Lineage (2 tools)

| Tool | Description |
|------|-------------|
| `coherence_list_lineage` | List value lineage chains. Params: `limit` |
| `coherence_lineage_valuation` | ROI for a lineage chain. Params: `lineage_id` |

### Identity (4 tools)

| Tool | Description |
|------|-------------|
| `coherence_list_providers` | All 37 providers in 6 categories |
| `coherence_link_identity` | Link a provider identity. Params: `contributor_id`, `provider`, `provider_id` |
| `coherence_lookup_identity` | Reverse lookup. Params: `provider`, `provider_id` |
| `coherence_get_identities` | All linked identities. Params: `contributor_id` |

### Contributions (2 tools)

| Tool | Description |
|------|-------------|
| `coherence_record_contribution` | Record contribution by name or provider identity. Params: `type`, `amount_cc`, `contributor_id`/`provider`+`provider_id` |
| `coherence_contributor_ledger` | CC balance and history. Params: `contributor_id` |

### Status & Governance (3 tools)

| Tool | Description |
|------|-------------|
| `coherence_status` | Network health, uptime, node count |
| `coherence_friction_report` | Pipeline friction signals. Params: `window_days` |
| `coherence_list_change_requests` | Governance change requests |

### Federation (2 tools)

| Tool | Description |
|------|-------------|
| `coherence_list_federation_nodes` | Federated nodes and capabilities |

## Environment Variables

| Var | Default | Description |
|-----|---------|-------------|
| `COHERENCE_API_URL` | `https://api.coherencycoin.com` | API base URL |
| `COHERENCE_API_KEY` | (none) | API key for write operations |
