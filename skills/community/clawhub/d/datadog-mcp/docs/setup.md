# Setting Up the Datadog MCP Server

## Prerequisites

- A Datadog account ([sign up for free trial](https://www.datadoghq.com/free-datadog-trial/))
- API Key + Application Key with appropriate permissions
- OpenClaw with the `mcporter` skill installed

## Step 1: Create Credentials

1. Go to [app.datadoghq.com](https://app.datadoghq.com)
2. Navigate to **Organization Settings** → **API Keys**
3. Click **New Key**, name it (e.g., "OpenClaw MCP")
4. Copy the API key
5. Navigate to **Application Keys** → **New Key**
6. Copy the Application key

### Recommended Permissions

For the Application Key, the creating user should have:
- `logs_read_data` — to search logs
- `metrics_read` — to query metrics
- `monitors_read` — to check monitor status
- `incidents_read` — to view incidents
- `dashboards_read` — to list dashboards
- `synthetics_read` — to view synthetic tests

For read-only observability, avoid granting write permissions.

## Step 2: Store Credentials

### Option A: Environment Variables

```bash
export DD_API_KEY="your-api-key"
export DD_APP_KEY="your-application-key"
```

### Option B: 1Password (Recommended for OpenClaw)

```bash
op item create --vault "OpenClaw" \
  --category "API Credential" \
  --title "Datadog MCP" \
  --field "API Key=$DD_API_KEY" \
  --field "App Key=$DD_APP_KEY" \
  --field "Site=datadoghq.com"
```

Then reference in your agent config or scripts:
```bash
export DD_API_KEY=$(op read "op://OpenClaw/Datadog MCP/API Key")
export DD_APP_KEY=$(op read "op://OpenClaw/Datadog MCP/App Key")
```

## Step 3: Configure MCP Connection

### Remote Server (Recommended)

```bash
mcporter add datadog \
  --transport http \
  --url "https://mcp.datadoghq.com/api/unstable/mcp-server/mcp" \
  --header "DD-API-KEY:$DD_API_KEY" \
  --header "DD-APPLICATION-KEY:$DD_APP_KEY"
```

### With Specific Toolsets

```bash
mcporter add datadog \
  --transport http \
  --url "https://mcp.datadoghq.com/api/unstable/mcp-server/mcp?toolsets=logs,metrics,monitors,incidents" \
  --header "DD-API-KEY:$DD_API_KEY" \
  --header "DD-APPLICATION-KEY:$DD_APP_KEY"
```

## Step 4: Validate

```bash
# Run the validation script
./scripts/validate.sh

# Or test manually
mcporter call datadog list_metrics --query "system.cpu"
```

## Troubleshooting

| Issue | Solution |
|---|---|
| `401 Unauthorized` | Check API key and App key are correct |
| `403 Forbidden` | App key user needs appropriate permissions |
| `MCP server timeout` | May need Preview access — check [docs](https://docs.datadoghq.com/bits_ai/mcp_server/) |
| `mcporter not found` | Install: `npm i -g mcporter` |
| Wrong site | Set `DD_SITE` to your org's region |
