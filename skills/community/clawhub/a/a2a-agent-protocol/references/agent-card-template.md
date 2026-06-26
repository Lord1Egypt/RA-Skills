# AgentCard Template and Reference

> Reference: https://a2a-protocol.org/latest/specification/ Section 8

The AgentCard is a JSON document that represents an agent's public identity and capabilities.
It is served at `/.well-known/agent.json` on the agent's host.

## Minimal AgentCard

```json
{
  "name": "string (required)",
  "description": "string (required)",
  "version": "string (required)",
  "capabilities": {
    "streaming": "SUPPORTED | NOT_SUPPORTED",
    "pushNotifications": "SUPPORTED | NOT_SUPPORTED",
    "agentPrivilege": false,
    "signedAgentCard": false
  },
  "authentication": {
    "schemes": ["string"],
    "credentials": "required | optional"
  }
}
```

## Annotated AgentCard (Complete)

```json
{
  "name": "financial-analysis-agent",
  "description": "Specialized agent for financial data extraction, ratio analysis, and trend reporting",
  "version": "1.0",
  "provider": {
    "organization": "Acme Corp",
    "description": "Acme financial analytics division",
    "url": "https://acme.example.com"
  },
  "capabilities": {
    "streaming": "SUPPORTED",
    "pushNotifications": "SUPPORTED",
    "agentPrivilege": false,
    "signedAgentCard": false,
    "dataStreamingSupported": true,
    "supportsAuthenticatedExtendedAgentCard": true
  },
  "skills": [
    {
      "id": "financial-data-extraction",
      "name": "Financial Data Extraction",
      "description": "Extracts financial metrics from raw CSV, Excel, and JSON data sources",
      "tags": ["finance", "extraction", "csv", "excel"],
      "examples": ["Extract revenue and EBITDA from Q3 report.csv"]
    },
    {
      "id": "ratio-analysis",
      "name": "Ratio Analysis",
      "description": "Computes liquidity, profitability, and leverage ratios from financial statements",
      "tags": ["finance", "ratios", "analysis"],
      "examples": ["Calculate current ratio and ROIC for FY2025"]
    },
    {
      "id": "trend-reporting",
      "name": "Trend Reporting",
      "description": "Generates time-series trend visualizations and narrative reports",
      "tags": ["finance", "reporting", "trends", "charts"],
      "examples": ["Generate a 5-year revenue trend report"]
    }
  ],
  "authentication": {
    "schemes": ["httpBearer"],
    "credentials": "required"
  },
  "defaultInputModes": ["text", "json"],
  "defaultOutputModes": ["text", "json", "png"],
  "endpoint": "https://financial-agent.acme.example.com/a2a/",
  "url": "https://financial-agent.acme.example.com"
}
```

## Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique agent name within the deployment |
| `description` | Yes | Human-readable description of what the agent does |
| `version` | Yes | Semantic version string for capability negotiation |
| `capabilities` | Yes | Declares streaming, push notification, and auth support |
| `capabilities.streaming` | Yes | `SUPPORTED`, `NOT_SUPPORTED`, or `STREAMABLE` |
| `capabilities.pushNotifications` | Yes | `SUPPORTED` or `NOT_SUPPORTED` |
| `capabilities.agentPrivilege` | No | If true, agent can act with elevated privileges |
| `capabilities.signedAgentCard` | No | If true, AgentCard is cryptographically signed |
| `capabilities.dataStreamingSupported` | No | If true, agent can stream data parts (not just status) |
| `capabilities.supportsAuthenticatedExtendedAgentCard` | No | If true, agent exposes extended card with auth |
| `authentication.schemes` | Yes | Auth methods: `apiKey`, `httpBearer`, `oauth2`, `mutualTLS`, `openIdConnect` |
| `authentication.credentials` | Yes | `required` or `optional` |
| `provider` | No | Provider organization info |
| `skills` | No | Array of `AgentSkill` objects describing exposed capabilities |
| `defaultInputModes` | No | MIME types the agent accepts (e.g., `text`, `json`, `image/png`) |
| `defaultOutputModes` | No | MIME types the agent produces (e.g., `text`, `json`, `image/png`) |
| `endpoint` | No | Explicit A2A endpoint URL (if not inferable from `url`) |
| `url` | No | Base URL for the agent service |

## skills[] — Capability Declaration

The `skills` array declares specific capabilities other agents can request:

```json
{
  "id": "skill-id (required, unique within agent)",
  "name": "Human-readable skill name",
  "description": "What this skill does and when to request it",
  "tags": ["optional", "category", "tags"],
  "examples": ["Example invocation phrases"]
}
```

## AgentCard Discovery Flow

```
1. Client fetches GET https://<target-agent>/.well-known/agent.json
2. Client reads capabilities, skills, auth requirements
3. Client verifies capability compatibility
4. Client constructs and sends task via appropriate A2A operation
```

## AgentCard Caching

- **Servers** should set `Cache-Control: max-age=3600` (or similar) on the AgentCard endpoint
- **Clients** should cache the AgentCard for the duration of a session; re-fetch on explicit refresh
- Extended AgentCard (authenticated) should NOT be cached