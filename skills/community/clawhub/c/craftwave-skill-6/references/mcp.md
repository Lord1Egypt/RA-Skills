# MCP Server 接入

为公司团体或组织提供邮轮旅行方案，适合团队出行的需求，制定专属的邮轮产品。

## 平台网关 Remote URL

```
https://cruise-mcp.olavacations.com/api/gw/mcp/c3c56c15-63d5-472c-907b-cddb5d809871
```

## server.json

```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json",
  "name": "io.github.309441738/craftwave-skill-6",
  "description": "为公司团体或组织提供邮轮旅行方案，适合团队出行的需求，制定专属的邮轮产品。",
  "version": "0.1.0",
  "remotes": [
    {
      "type": "streamable-http",
      "url": "https://cruise-mcp.olavacations.com/api/gw/mcp/c3c56c15-63d5-472c-907b-cddb5d809871"
    }
  ]
}
```

安装本 Skill 后，在 OpenClaw 配置中将 MCP remotes 指向上述 URL。
