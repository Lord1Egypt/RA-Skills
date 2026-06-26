---
name: adagent-google-ads
description: "Manage Google Ads campaigns — create, monitor, pause, and optimize. Use when the user says 'Google Ads', 'Google 廣告', 'keyword research', 'search ads', 'create Google campaign', 'ad performance', or wants to manage their Google Ads account."
version: 1.0.0
metadata:
  openclaw:
    emoji: "🔍"
    homepage: https://adagent.10xboost.org
    requires:
      config:
        - MCP Connector link from adagent.10xboost.org (contains embedded auth token)
---

# Google Ads Agent

Create, manage, and optimize Google Search Ads campaigns directly from Claude Code. Powered by [AdAgent](https://adagent.10xboost.org).

## Security & Data Handling

- **MCP link is a credential**: Your MCP Server URL (`https://adagent.10xboost.org/api/mcp/google-ads/{user_id}/mcp`) contains your user ID for credential lookup. Treat it like a password — do not share it publicly.
- **Token scope**: The service uses your Google Ads OAuth refresh token to access your ad accounts. It can create campaigns, modify budgets, enable/pause campaigns, and read performance data.
- **Token storage**: Your Google Ads OAuth tokens are encrypted with Fernet (AES-128-CBC + HMAC) and stored in MongoDB. They are never exposed in API responses.
- **Multi-tenant isolation**: Each request is scoped to your user credentials via ASGI middleware. You can only access your own ad accounts.
- **No local credentials**: No local API keys, environment variables, or secrets are needed. All auth is embedded in the MCP link.
- **Third-party service**: This skill relies on [AdAgent](https://adagent.10xboost.org), an AI-powered ad management platform.

## Prerequisites

1. **Sign up** at [adagent.10xboost.org](https://adagent.10xboost.org) with Google
2. **Connect Google Ads** — authorize AdAgent to access your Google Ads account
3. **Get your MCP link**: Copy your Google Ads MCP Server URL from the dashboard
4. **Add to Claude**: Paste the MCP link as a Connector — no install, no API key needed

## Available Tools

| Tool | Description |
|------|-------------|
| `list_accessible_customers` | List all accessible Google Ads accounts (MCC + sub-accounts) |
| `get_customer_info` | Get account details (name, type, etc.) |
| `list_campaigns` | List all campaigns (active + paused) |
| `create_campaign` | Create a complete Search Ads campaign (budget, ad group, keywords, ads) |
| `get_performance` | Get all campaigns performance (impressions, clicks, cost, CTR, CPC) |
| `get_campaign_performance` | Get daily performance for a specific campaign |
| `keyword_research` | Research keywords — get suggestions and search volume |
| `enable_campaign` | Enable a paused campaign |
| `pause_campaign` | Pause an active campaign |

## Workflow

### Step 1: List Accounts

Call `list_accessible_customers` to see all available Google Ads accounts. Then `get_customer_info` for details.

### Step 2: Determine What the User Wants

| User Request | Tool to Use |
|-------------|------------|
| "Show my Google Ads accounts" | `list_accessible_customers` |
| "List my campaigns" | `list_campaigns` |
| "How are my ads doing?" | `get_performance` |
| "Campaign X performance" | `get_campaign_performance` |
| "Research keywords for ..." | `keyword_research` |
| "Create a search ad for ..." | `create_campaign` |
| "Pause campaign X" | `pause_campaign` |
| "Enable campaign X" | `enable_campaign` |

### Step 3: Execute

#### Check Performance
```
get_performance(
  start_date="2026-03-01",
  end_date="2026-03-30"
)
```

#### Keyword Research
```
keyword_research(
  keywords=["AI agent", "automation tool"],
  location_ids=["2158"],   // 2158=Taiwan, 2840=US
  language_id="1000"        // 1000=Chinese
)
```

#### Create Campaign
```
create_campaign(
  name="Spring Sale 2026",
  daily_budget_usd=10.0,
  keywords=["AI agent", "automation tool", "AI assistant"],
  ad_headlines=["Build Your AI Agent", "Automate Your Work", "Try AI Agent Free"],
  ad_descriptions=["Create powerful AI agents in minutes.", "Boost productivity with AI automation."],
  final_url="https://example.com",
  location_ids=["2158"],
  language_id="1000"
)
```

**Important**: Campaigns are created in **PAUSED** state. Use `enable_campaign` to activate.

### Step 4: Present Results

- **Performance**: Show key metrics in a table (impressions, clicks, CTR, CPC, cost, conversions)
- **Keyword research**: Show keywords ranked by search volume with competition level
- **Campaign creation**: Confirm campaign ID and remind user it's paused until enabled

## Common Location IDs

| Location | ID |
|----------|-----|
| Taiwan | 2158 |
| United States | 2840 |
| Japan | 2392 |
| Hong Kong | 2344 |
| Singapore | 2702 |

## Common Language IDs

| Language | ID |
|----------|-----|
| Chinese (Traditional) | 1018 |
| Chinese (Simplified) | 1017 |
| English | 1000 |
| Japanese | 1005 |

## Error Handling

| Error | Solution |
|-------|----------|
| Account not found | Run `list_accessible_customers` to get valid IDs |
| Permission denied | Reconnect Google Ads at adagent.10xboost.org |
| Budget too low | Google Ads has minimum budget requirements per market |
| Campaign creation failed | Verify all required fields (headlines >= 3, descriptions >= 2) |
| Token expired | Reconnect Google Ads at adagent.10xboost.org (refresh token is long-lived) |

## Documentation

Product website: [adagent.10xboost.org](https://adagent.10xboost.org)
