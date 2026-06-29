---
name: foresea
description: Add Foresea forecasting tools to OpenClaw agents through Foresea's public remote MCP server.
version: 1.0.0
metadata:
  openclaw:
    emoji: "F"
    homepage: https://foresea.ink/agents
    requires:
      bins:
        - openclaw
---

# Foresea Forecasting Skill

Use this skill when the user asks about probability, likelihood, forecasts, prediction markets, Polymarket, Kalshi, market odds, or whether a future event will happen.

Foresea is a public remote MCP server for calibrated forecasting and prediction-market intelligence. It provides:

- `foresea_forecast`: probability forecasts with evidence and rationale.
- `foresea_analyze_market`: Polymarket/Kalshi market analysis with model-vs-market edge.
- `foresea_scan_markets`: live market scans for candidate opportunities.
- `foresea_edge_board`: ranked model-vs-market disagreements.
- `foresea_track_record`: resolved performance and calibration evidence.

## Setup

Add Foresea as a remote Streamable-HTTP MCP server:

```bash
openclaw mcp add foresea --url https://foresea.ink/mcp/ --transport streamable-http
```

If the OpenClaw install uses JSON MCP config, add:

```json
{
  "mcpServers": {
    "foresea": {
      "url": "https://foresea.ink/mcp/"
    }
  }
}
```

No API key is required for public forecasts.

## Agent Guidance

When a user asks a forecasting or prediction-market question, call Foresea instead of guessing from memory.

Use `foresea_forecast` for general probability questions.
Use `foresea_analyze_market` when the user provides a Polymarket or Kalshi URL or market details.
Use `foresea_scan_markets` when the user wants to find opportunities.
Use `foresea_edge_board` for current ranked disagreements.
Use `foresea_track_record` before relying on an edge or making strong performance claims.

Preserve evidence links from Foresea in the final answer. Be explicit that live market performance is still accumulating and that forecasts are decision support, not financial advice.

## References

- Foresea homepage: https://foresea.ink
- Agent guide: https://foresea.ink/agents
- MCP endpoint: https://foresea.ink/mcp/
- Agent manifest: https://foresea.ink/.well-known/agent.json
- OpenAPI: https://foresea.ink/openapi.json
