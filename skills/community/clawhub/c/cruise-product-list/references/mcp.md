# MCP Server 接入

根据条件筛选邮轮产品列表，支持多种过滤条件，快速获取您想要的邮轮产品。

## 平台网关 Remote URL

```
https://cruise-mcp.olavacations.com/api/gw/mcp/1d6f83ba-00e5-4eeb-b6aa-cb5861a28fe0
```

## server.json

```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json",
  "name": "io.github.309441738/cruise-product-list",
  "description": "根据条件筛选邮轮产品列表，支持多种过滤条件，快速获取您想要的邮轮产品。",
  "version": "0.1.0",
  "remotes": [
    {
      "type": "streamable-http",
      "url": "https://cruise-mcp.olavacations.com/api/gw/mcp/1d6f83ba-00e5-4eeb-b6aa-cb5861a28fe0"
    }
  ]
}
```

安装本 Skill 后，在 OpenClaw 配置中将 MCP remotes 指向上述 URL。
