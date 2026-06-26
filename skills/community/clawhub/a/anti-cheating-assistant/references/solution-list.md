# MCP 接口

## 服务地址

| 项目 | 值 |
|---|---|
| MCP 端点 | `https://mcp.hdconsultatio.com/mcp` |
| 健康检查 | `https://mcp.hdconsultatio.com/health` |
| 工具列表 | `https://mcp.hdconsultatio.com/mcp/tools/list` |

## 鉴权方式

**无服务器层鉴权，纯透传。** 客户在请求头中传入 `X-API-Key`，Key 值需要访问 https://hdconsultatio.com/contactus.html ，联系商务人员获取。

**如果用户未提供 X-API-Key、Key 无效或调用 MCP 失败，先明确告知用户“当前知识库检索不可用”，再转为通用建议或引导用户补充凭据。**

```
X-API-Key: <客户的 API Key>
```

## 可用工具

| 工具名 | 说明 |
|---|---|
| `rag_search` | RAG 检索 — 查询风控知识库 |

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `business_mode` | string | ✅ | 业务模式 |
| `risk_mode` | string | ✅ | 风险模式 |

## 调用方式一：MCP JSON-RPC（推荐）

适用于支持 MCP 协议的 Agent（Claude Desktop、Cursor、Hermes 等）。

**1. 列出可用工具：**

```bash
curl -s -X POST https://mcp.hdconsultatio.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

**2. 调用 rag_search：**

```bash
curl -s -X POST https://mcp.hdconsultatio.com/mcp \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <客户的扣子 API Key>" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "rag_search",
      "arguments": {
        "business_mode": "跨境电商",
        "risk_mode": "反洗钱"
      }
    }
  }'
```

**返回格式：**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"result\": \"<检索结果文本>\"}"
      }
    ]
  }
}
```

实际结果在 `result.content[0].text` 里，是 JSON 字符串，需再解析一次取 `result` 字段。

## 调用方式二：REST API（简单场景）

适用于不支持 MCP 协议、只需简单 HTTP 调用的场景。

```bash
curl -s -X POST "https://mcp.hdconsultatio.com/api/rag/search?business_mode=跨境电商&risk_mode=反洗钱" \
  -H "X-API-Key: <客户的 API Key>"
```

**返回格式：**

```json
{
  "result": "<检索结果文本>"
}
```

## 错误处理

| 情况 | 表现 | 处理 |
|---|---|---|
| 未传 X-API-Key | 返回错误 `"Missing Coze API key"` | 告知用户“当前知识库检索不可用”，并检查 header 是否正确传入 |
| Key 无效 | 服务返回 401 | 告知用户“当前知识库检索不可用”，并确认 key 是否过期或拼写错误 |
| rag_search  返回空结果 | 返回空结果或无可用数据 | 告知用户“当前知识库检索不可用”，并提供基于已知业务信息的通用风控建议 |
| 工作流执行失败 | 返回 `"Coze workflow error: ..."` | 告知用户“当前知识库检索不可用”，并提供基于已知业务信息的通用风控建议 |
| 超时或网络不可达 | 120 秒无响应或无法连接 | 停止重试，说明当前无法获取知识库结果，并给出基于用户已有信息的保守建议 |