# MCP Server 接入

获取特定邮轮产品的详细信息，了解产品的特点和服务，帮助决策。

## 平台网关 Remote URL

```
https://cruise-mcp.olavacations.com/api/gw/mcp/478d82fd-8ff7-46e2-9cda-7576fb74ed83
```

## server.json

```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json",
  "name": "io.github.309441738/cruise-product-info",
  "description": "获取特定邮轮产品的详细信息，了解产品的特点和服务，帮助决策。",
  "version": "0.1.0",
  "remotes": [
    {
      "type": "streamable-http",
      "url": "https://cruise-mcp.olavacations.com/api/gw/mcp/478d82fd-8ff7-46e2-9cda-7576fb74ed83"
    }
  ]
}
```

安装本 Skill 后，在 OpenClaw 配置中将 MCP remotes 指向上述 URL。
