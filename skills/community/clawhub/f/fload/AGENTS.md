# Fload — Mobile App Analytics

Fload is a platform for mobile app publishers. It connects to App Store Connect, Google Play Console, ad platforms, Stripe, and RevenueCat to provide analytics, AI-powered review management, anomaly detection, and growth scoring.

## Setup

1. Create an API key at [app.fload.app](https://app.fload.app) > Settings > API Keys
2. Install the MCP server:

```json
{
  "mcpServers": {
    "fload": {
      "command": "npx",
      "args": ["-y", "@fload-ai/mcp"],
      "env": {
        "FLOAD_API_KEY": "fload_sk_your_key_here"
      }
    }
  }
}
```

## Install the Skill

```bash
npx skills add fload-ai/mcp --skill fload
```

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `list_apps` | List all apps in the organization |
| `get_app_details` | Get app info by ID or bundle ID |
| `get_reviews` | Get reviews with filtering |
| `discover_metrics` | Discover available metrics for an app |
| `get_metrics` | Query metric timeseries (30+ metrics) |
| `discover_dimensions` | Discover breakdown dimensions |
| `list_agents` | List AI agents |
| `get_agent_details` | Agent config per app |
| `get_agent_run_history` | Agent execution history |
| `get_anomalies` | Detected metric anomalies |
| `get_ads_performance` | Ad campaign data |
| `get_growth_audit` | Growth assessment |
| `get_growth_score` | 0-100 growth score |
| `get_forecasts` | Valuation forecasts |
| `get_dashboard_overview` | Portfolio overview |
| `list_pending_actions` | Pending review replies |
| `approve_action` | Approve a review reply |
| `reject_action` | Reject a review reply |

## Common Workflows

- **App health check**: `list_apps` → `get_growth_score` → `discover_metrics` → `get_metrics` → `get_anomalies`
- **Review management**: `get_reviews` → `list_pending_actions` → `approve_action`/`reject_action`
- **Business overview**: `get_dashboard_overview` → `get_growth_score` per app → `get_anomalies`
- **Ads analysis**: `get_ads_performance` → combine with `get_metrics` for downloads
