---
name: adagent-facebook-ads
description: "Manage Facebook/Meta Ads — create campaigns, ad sets, ads, monitor performance, and target audiences. Use when the user says 'Facebook Ads', 'FB 廣告', 'Meta Ads', 'create Facebook ad', 'ad targeting', 'ad performance', or wants to manage their Facebook advertising."
version: 1.0.0
metadata:
  openclaw:
    emoji: "📣"
    homepage: https://adagent.10xboost.org
    requires:
      config:
        - MCP Connector link from adagent.10xboost.org (contains embedded auth token)
---

# Facebook Ads Agent

Create, manage, and optimize Facebook/Meta Ads campaigns with full control over campaigns, ad sets, targeting, and creatives. Powered by [AdAgent](https://adagent.10xboost.org).

## Security & Data Handling

- **MCP link is a credential**: Your MCP Server URL (`https://adagent.10xboost.org/api/mcp/fb-ads/{user_id}/mcp`) contains your user ID for credential lookup. Treat it like a password — do not share it publicly.
- **Token scope**: The service uses your Facebook OAuth token to access your ad accounts. It can create/modify campaigns, ad sets, and ads, manage budgets, and read performance data.
- **Token storage**: Your Facebook tokens are encrypted with Fernet (AES-128-CBC + HMAC) and stored in MongoDB. They are never exposed in API responses.
- **Token expiry**: Facebook long-lived tokens expire after ~60 days. Use `refresh_token` to extend when needed.
- **Multi-tenant isolation**: Each request is scoped to your user credentials via ASGI middleware. You can only access your own ad accounts.
- **No local credentials**: No local API keys, environment variables, or secrets are needed. All auth is embedded in the MCP link.
- **Third-party service**: This skill relies on [AdAgent](https://adagent.10xboost.org), an AI-powered ad management platform.

## Prerequisites

1. **Sign up** at [adagent.10xboost.org](https://adagent.10xboost.org) with Google
2. **Connect Facebook Ads** — authorize AdAgent to access your Facebook Ad accounts
3. **Get your MCP link**: Copy your Facebook Ads MCP Server URL from the dashboard
4. **Add to Claude**: Paste the MCP link as a Connector — no install, no API key needed

## Available Tools (22 tools)

### Account & Token
| Tool | Description |
|------|-------------|
| `list_ad_accounts` | List all accessible ad accounts |
| `get_account_info` | Get account details (currency, timezone, status) |
| `check_token_status` | Check token validity and expiry |
| `refresh_token` | Exchange short-lived token for long-lived token (60 days) |

### Campaign Management
| Tool | Description |
|------|-------------|
| `list_campaigns` | List campaigns (filter by status) |
| `get_campaign` | Get campaign details |
| `create_campaign` | Create campaign (PAUSED by default) |
| `enable_campaign` | Activate a campaign |
| `pause_campaign` | Pause a campaign |

### Ad Set Management
| Tool | Description |
|------|-------------|
| `list_ad_sets` | List ad sets (filter by campaign/status) |
| `get_ad_set` | Get ad set details with full targeting |
| `create_ad_set` | Create ad set with audience targeting |
| `enable_ad_set` | Activate an ad set |
| `pause_ad_set` | Pause an ad set |

### Ad Management
| Tool | Description |
|------|-------------|
| `list_ads` | List ads (filter by ad set/status) |
| `create_ad` | Create ad (upload image + creative + ad) |
| `enable_ad` | Activate an ad |
| `pause_ad` | Pause an ad |

### Performance & Insights
| Tool | Description |
|------|-------------|
| `get_account_insights` | Account-level performance data |
| `get_campaign_insights` | Campaign daily performance |
| `get_ad_set_insights` | Ad set performance |

### Targeting Research
| Tool | Description |
|------|-------------|
| `search_interests` | Search interest targeting (e.g. "baseball", "cooking") |
| `search_locations` | Search geographic targeting (country, city, zip) |
| `search_targeting_categories` | Browse targeting categories (interests, behaviors, demographics) |

### Compliance
| Tool | Description |
|------|-------------|
| `get_taiwan_regulation_status` | Check Taiwan ad regulation compliance |

## Workflow

### Creating a Full Ad (3-Layer Structure)

Facebook Ads uses a 3-layer hierarchy: **Campaign → Ad Set → Ad**

#### Step 1: Create Campaign
```
create_campaign(
  name="Summer Sale 2026",
  objective="OUTCOME_TRAFFIC",
  daily_budget_usd=20.0
)
```

**Objectives**: `OUTCOME_AWARENESS`, `OUTCOME_ENGAGEMENT`, `OUTCOME_LEADS`, `OUTCOME_SALES`, `OUTCOME_TRAFFIC`, `OUTCOME_APP_PROMOTION`

**Budget rule**: Set budget at Campaign OR Ad Set level, not both.

#### Step 2: Research Targeting
```
search_interests(query="AI")
search_locations(query="Taiwan", location_type="country")
```

#### Step 3: Create Ad Set (with targeting)
```
create_ad_set(
  name="AI Enthusiasts - TW",
  campaign_id="<campaign_id>",
  optimization_goal="LINK_CLICKS",
  billing_event="IMPRESSIONS",
  destination_type="WEBSITE",
  countries=["TW"],
  age_min=25,
  age_max=55,
  flexible_spec=[
    {"interests": [{"id": "6003087413192", "name": "AI"}]}
  ]
)
```

If Campaign has budget set, do NOT set `daily_budget_usd` on Ad Set.

#### Step 4: Create Ad
```
create_ad(
  name="Summer Sale Ad 1",
  ad_set_id="<ad_set_id>",
  image_url="https://example.com/ad-image.jpg",
  message="Summer Sale! 50% off all AI tools.",
  link="https://example.com/sale",
  call_to_action_type="SHOP_NOW"
)
```

**CTA types**: `LEARN_MORE`, `SHOP_NOW`, `SIGN_UP`, `DOWNLOAD`, `BOOK_TRAVEL`, `CONTACT_US`

#### Step 5: Enable (Campaign is PAUSED by default)
```
enable_campaign(campaign_id="<campaign_id>")
enable_ad_set(ad_set_id="<ad_set_id>")
enable_ad(ad_id="<ad_id>")
```

### Checking Performance

| User Request | Tool |
|-------------|------|
| "How are my ads doing?" | `get_account_insights` |
| "Campaign X performance" | `get_campaign_insights` |
| "Ad set performance" | `get_ad_set_insights` |
| "List all campaigns" | `list_campaigns` |

```
get_account_insights(
  start_date="2026-03-01",
  end_date="2026-03-30",
  time_increment="1"    // "1"=daily, "7"=weekly, "all_days"=summary
)
```

### Present Results

- **Performance**: Show metrics table (impressions, clicks, CTR, CPC, CPM, spend, reach, frequency)
- **Campaign list**: Show status, objective, budget, and delivery status
- **Targeting**: Show audience size estimates when researching interests

## Targeting Tips

- Use `search_interests` to find interest IDs before creating ad sets
- Use `search_locations` with `location_type` (country, city, zip, region) for geo-targeting
- `flexible_spec` items use OR within each element, AND between elements
- `advantage_audience=1` enables Meta's Advantage+ automatic audience (recommended for beginners)

## Error Handling

| Error | Solution |
|-------|----------|
| Token expired | Use `refresh_token` or reconnect at adagent.10xboost.org |
| Invalid account ID | Run `list_ad_accounts` to get valid IDs |
| Budget conflict | Budget must be at Campaign OR Ad Set level, not both |
| Missing Page ID | Some objectives require `page_id` — get it from account info |
| Taiwan regulation | Run `get_taiwan_regulation_status` to check compliance |
| Ad rejected | Check Facebook ad policies — image text ratio, prohibited content |

## Documentation

Product website: [adagent.10xboost.org](https://adagent.10xboost.org)
