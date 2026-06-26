# dataworks-open-api

Alibaba Cloud DataWorks skill for AI agents. Manage data development, workflow operations, data quality, metadata lineage, and workspace administration through a single skill.

## Skill structure

```
dataworks-open-api/
├── SKILL.md                          # Main skill instructions (read by AI agent)
├── README.md                         # This file — quick start & overview
├── agents/
│   └── openai.yaml                   # Agent interface definition
├── references/
│   ├── cookbook.md                    # Verified API patterns, pitfalls, end-to-end lifecycle, recipes & FAQ
│   ├── sources.md                    # API docs, SDK, and MCP Server links
│   └── mcp_server.md                # MCP Server setup and configuration
└── scripts/
    ├── fetch_api_overview.py         # Fetch API list from official help docs
    └── list_openapi_meta_apis.py     # Fetch API specs from OpenAPI metadata
```

## Quick start

```bash
# Option A: Credentials URI (recommended for local development)
export ALIBABA_CLOUD_CREDENTIALS_URI="http://localhost:7002/api/v1/credentials/0"

# Option B: Static AK/SK
export ALIBABA_CLOUD_ACCESS_KEY_ID="your-ak"
export ALIBABA_CLOUD_ACCESS_KEY_SECRET="your-sk"

export ALIBABA_CLOUD_REGION_ID="cn-shanghai"

# Discover available APIs
python scripts/fetch_api_overview.py
python scripts/list_openapi_meta_apis.py
```

## SDK support

| Language | Package                                            |
| -------- | -------------------------------------------------- |
| Node.js  | `@alicloud/dataworks-public20240518`               |
| Python   | `alibabacloud_dataworks_public20240518`            |
| Java     | `com.aliyun:alibabacloud-dataworks_public20240518` |

## Troubleshooting fallback chain

When execution fails, escalate in this order:

1. **Cookbook** (`references/cookbook.md`) — verified patterns, pitfalls & error recovery
2. Official help docs
3. OpenAPI metadata (raw JSON spec)
4. SDK API docs
5. GitHub SDK source code
6. MCP Server
7. Browser (DataWorks Homepage)

See `SKILL.md` for full details on each level.

## Links

- [DataWorks documentation](https://www.alibabacloud.com/help/dataworks)
- [OpenAPI Explorer](https://api.aliyun.com/product/dataworks-public)
- [MCP Server (npm)](https://www.npmjs.com/package/alibabacloud-dataworks-mcp-server)
- [MCP Server (GitHub)](https://github.com/aliyun/alibabacloud-dataworks-mcp-server)
