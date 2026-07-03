# MCP Server 接入

专为追求奢华的旅行者推荐高端邮轮体验，提供顶级设施与服务。

## 平台网关 Remote URL

```
https://cruise-mcp.olavacations.com/api/gw/mcp/7b49d758-2bec-48a6-be3d-19b11f954c07
```

## server.json

```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json",
  "name": "io.github.309441738/craftwave-skill-7",
  "description": "专为追求奢华的旅行者推荐高端邮轮体验，提供顶级设施与服务。",
  "version": "0.1.0",
  "remotes": [
    {
      "type": "streamable-http",
      "url": "https://cruise-mcp.olavacations.com/api/gw/mcp/7b49d758-2bec-48a6-be3d-19b11f954c07"
    }
  ]
}
```

安装本 Skill 后，在 OpenClaw 配置中将 MCP remotes 指向上述 URL。
