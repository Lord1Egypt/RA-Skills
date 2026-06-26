# dataworks-open-api

Alibaba Cloud DataWorks skill for AI agents. Manage data development, workflow operations, data quality, metadata lineage, and workspace administration through a single skill.

## Skill structure

```
dataworks-open-api/
├── SKILL.md                          # Main skill instructions (read by AI agent)
├── agents/
│   └── openai.yaml                   # Agent interface definition
├── references/
│   ├── sources.md                    # API docs, SDK, and MCP Server links
│   └── mcp_server.md                 # MCP Server setup and configuration
└── scripts/
    ├── fetch_api_overview.py         # Fetch API list from official help docs
    └── list_openapi_meta_apis.py     # Fetch API specs from OpenAPI metadata
```

## Quick start

```bash
# Set credentials
export ALICLOUD_ACCESS_KEY_ID="your-ak"
export ALICLOUD_ACCESS_KEY_SECRET="your-sk"
export ALICLOUD_REGION_ID="cn-shanghai"

# Discover available APIs
python scripts/fetch_api_overview.py
python scripts/list_openapi_meta_apis.py
```

## SDK support

| Language   | Package                                        |
| ---------- | ---------------------------------------------- |
| Node.js    | `@alicloud/dataworks-public20240518`           |
| Python     | `alibabacloud_dataworks_public20240518`        |
| Java       | `com.aliyun:alibabacloud-dataworks_public20240518` |

## Troubleshooting fallback chain

When execution fails, escalate in this order:

1. Official help docs
2. OpenAPI metadata (raw JSON spec)
3. SDK API docs
4. GitHub SDK source code
5. MCP Server
6. Browser (DataWorks IDE)

See `SKILL.md` for full details on each level.

## Links

- [DataWorks documentation](https://www.alibabacloud.com/help/dataworks)
- [OpenAPI Explorer](https://api.aliyun.com/product/dataworks-public)
- [MCP Server (npm)](https://www.npmjs.com/package/alibabacloud-dataworks-mcp-server)
- [MCP Server (GitHub)](https://github.com/aliyun/alibabacloud-dataworks-mcp-server)
