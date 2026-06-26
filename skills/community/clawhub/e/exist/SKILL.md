---
name: exist
description: Exist API integration with managed OAuth. Read health and fitness tracking data, retrieve correlations and insights, manage attribute ownership, and track wellness metrics. Use this skill when users want to query tracked health data, discover correlations between metrics, read fitness averages, or analyze lifestyle patterns.
---

# Exist

![Exist](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/exist.png)

Access health and fitness tracking data from chat -- retrieve tracked attributes, discover correlations between metrics, get AI-generated insights, and manage data ownership. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=exist) for hosted OAuth.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Exist |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Exist |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Exist API      │
│   (User Chat)   │     │   (OAuth)    │     │                  │
└─────────────────┘     └──────────────┘     └──────────────────┘
```

## Install

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

## Quick Start

```javascript
// 1. Get your profile
clawlink_call_tool({ tool: "exist_get_user_profile", parameters: {} })

// 2. See your tracked attributes
clawlink_call_tool({ tool: "exist_get_attributes_with_values", parameters: {} })

// 3. Discover correlations
clawlink_call_tool({ tool: "exist_get_correlations", parameters: {} })
```

## Authentication

ClawLink handles OAuth with Exist. No API keys needed. Connect at [claw-link.dev/dashboard?add=exist](https://claw-link.dev/dashboard?add=exist). Granted OAuth scopes determine which attribute fields are returned.

## Connection Management

```javascript
// List connections
clawlink_list_integrations()

// Verify
clawlink_call_tool({ tool: "exist_get_user_profile", parameters: {} })
```

## Security & Permissions

- **Read** tools are safe and require no confirmation
- **Write** tools (acquire/increment/release ownership) require confirmation
- Releasing ownership is high-impact and stops data flow for that attribute

## Tool Reference

### Profile & Discovery

| Tool | Description | Mode |
|------|-------------|------|
| `exist_get_user_profile` | Get authenticated user profile, timezone, and preferences | Read |
| `exist_get_attribute_templates` | Browse available attribute templates before creating data | Read |
| `exist_oauth2_authorize` | Construct OAuth2 authorization URL for Exist.io | Read |

### Attribute Reading

| Tool | Description | Mode |
|------|-------------|------|
| `exist_get_user_attributes` | List user attributes without values (metadata catalog) | Read |
| `exist_get_attributes_with_values` | Get attributes with current values and history | Read |
| `exist_get_owned_attributes` | List attributes owned by your service | Read |
| `exist_get_averages` | Get weekly averages with daily breakdowns (Mon-Sun) | Read |

### Insights & Correlations

| Tool | Description | Mode |
|------|-------------|------|
| `exist_get_insights` | Get AI-generated insights about patterns in tracked data | Read |
| `exist_get_correlations` | Discover statistical relationships between tracked attributes | Read |

### Attribute Writing

| Tool | Description | Mode |
|------|-------------|------|
| `exist_acquire_attribute_ownership` | Acquire ownership of attributes to write data | Write |
| `exist_increment_attribute_values` | Increment attribute values by a delta (counters only) | Write |
| `exist_release_attribute_ownership` | Release ownership, stopping data flow for that attribute | Write |

## Code Examples

### Example 1: Explore your tracked data

```javascript
// Get profile and timezone
const profile = await clawlink_call_tool({
  tool: "exist_get_user_profile",
  parameters: {}
});

// Get attributes with values
const attrs = await clawlink_call_tool({
  tool: "exist_get_attributes_with_values",
  parameters: {}
});

// Get weekly averages
const averages = await clawlink_call_tool({
  tool: "exist_get_averages",
  parameters: { include_historical: true }
});
```

### Example 2: Discover correlations and insights

```javascript
// Find correlations between metrics
const correlations = await clawlink_call_tool({
  tool: "exist_get_correlations",
  parameters: {}
});

// Get AI-generated insights
const insights = await clawlink_call_tool({
  tool: "exist_get_insights",
  parameters: {}
});
```

### Example 3: Write tracking data

```javascript
// Acquire ownership of a step count attribute
await clawlink_call_tool({
  tool: "exist_acquire_attribute_ownership",
  parameters: {
    attribute_names: ["steps"]
  }
});

// Increment step count
await clawlink_call_tool({
  tool: "exist_increment_attribute_values",
  parameters: {
    data: [{ date: "2026-06-08", attribute: "steps", value: 500 }]
  }
});
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm `exist` is connected.
2. Call `clawlink_list_tools --integration exist` to see the live catalog.
3. Use `clawlink_search_tools({ query: "correlation", integration: "exist" })` to find specific tools.

## Execution Workflow

```
READ (safe):     get_user_profile → get_attributes_with_values → get_correlations → get_insights
WRITE (confirm): acquire_attribute_ownership → increment_attribute_values
DELETE (high):   release_attribute_ownership
```

## Notes

- OAuth scopes control which attribute fields are visible -- missing fields indicate insufficient scopes
- Increment does not work with string, scale, or time-of-day attributes
- Releasing ownership stops data flow permanently for that attribute
- Use the profile timezone when interpreting date-based attributes

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| 401 Unauthorized | OAuth token expired -- reconnect at dashboard |
| 403 Forbidden | Insufficient OAuth scopes for requested attributes |
| 404 Not Found | Attribute template or attribute does not exist |
| 422 Unprocessable | Invalid attribute type for increment operation |

## Troubleshooting

### Tools Not Visible
- Start a fresh OpenClaw chat to reload plugin catalog
- Call `clawlink_list_integrations` to confirm pairing

### Missing Attribute Data
- Check granted OAuth scopes during connection
- Some attributes require specific integrations to be connected in Exist first
- Use `exist_get_attribute_templates` to verify available attributes

## Resources

- Exist API Docs: https://developer.exist.io/
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=exist
- ClawLink Docs: https://docs.claw-link.dev/openclaw

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=exist)** -- an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
