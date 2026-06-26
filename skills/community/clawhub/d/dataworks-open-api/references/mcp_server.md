# MCP Server Integration

DataWorks MCP Server exports all DataWorks Open APIs as MCP tools, allowing AI agents to interact with DataWorks through the Model Context Protocol.

## Installation

```bash
npm install -g alibabacloud-dataworks-mcp-server
```

## Configuration

### For Cursor / Cline / MCP-compatible clients

Option A — Static AK/SK:

```json
{
  "mcpServers": {
    "alibabacloud-dataworks-mcp-server": {
      "command": "npx",
      "args": ["alibabacloud-dataworks-mcp-server"],
      "env": {
        "REGION": "cn-shanghai",
        "ALIBABA_CLOUD_ACCESS_KEY_ID": "<YOUR_ACCESS_KEY_ID>",
        "ALIBABA_CLOUD_ACCESS_KEY_SECRET": "<YOUR_ACCESS_KEY_SECRET>"
      }
    }
  }
}
```

Option B — Credentials URI (recommended for local development):

```json
{
  "mcpServers": {
    "alibabacloud-dataworks-mcp-server": {
      "command": "npx",
      "args": ["alibabacloud-dataworks-mcp-server"],
      "env": {
        "REGION": "cn-shanghai",
        "ALIBABA_CLOUD_CREDENTIALS_URI": "http://localhost:7002/api/v1/credentials/0"
      }
    }
  }
}
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `REGION` | Yes | DataWorks API region (e.g. `cn-shanghai`) |
| `ALIBABA_CLOUD_CREDENTIALS_URI` | No* | Credentials URI endpoint for dynamic AK/SK/STS token |
| `ALIBABA_CLOUD_ACCESS_KEY_ID` | No* | Alibaba Cloud Access Key ID |
| `ALIBABA_CLOUD_ACCESS_KEY_SECRET` | No* | Alibaba Cloud Access Key Secret |
| `TOOL_CATEGORIES` | No | Comma-separated category filter |
| `TOOL_NAMES` | No | Comma-separated API name filter |
| `TOOL_FILE_URI` | No | Local file URI for tools metadata (overrides remote) |

\* Provide either `ALIBABA_CLOUD_CREDENTIALS_URI` or both `ALIBABA_CLOUD_ACCESS_KEY_ID` + `ALIBABA_CLOUD_ACCESS_KEY_SECRET`.

### Tool Categories

Filter tools by category using `TOOL_CATEGORIES`:

- `DATA_DEVELOP` — Data development (nodes, resources, workflows)
- `OPS_CENTER` — Operations center (task instances, alerts)
- `DATA_QUALITY` — Data quality rules and evaluation
- `DATA_MAP` — Metadata, lineage, catalogs
- `WORKSPACE` — Project and member management
- `DATA_INTEGRATION` — DI jobs
- `DATA_SOURCE` — Data source management
- `RESOURCE_GROUP` — Resource groups and networks
- `SERVER_IDE_DEFAULT` — Default IDE tool set

## Architecture

The MCP Server dynamically fetches tool definitions from:
- `https://dataworks.data.aliyun.com/pop-mcp-tools` (production)
- `https://pre-dataworks.data.aliyun.com/pop-mcp-tools` (pre-release, when `NODE_ENV=development`)

This means the tool list always reflects the latest available DataWorks APIs.

## API Invocation

The server uses Alibaba Cloud's generic OpenAPI client (RPC style) to invoke DataWorks APIs. Input parameters are validated against Zod schemas derived from the tool metadata.
