# Creator SKILL — MCP 工具说明

**服务地址：** `https://deinai.ai/mcp`

服务端实现参考：`deinai_mcp/server.py`、`deinai_mcp/tools/`。

## ping

- **作用**：检查 MCP 服务可达。
- **入参**：无。
- **返回示例**：`{ "status": "ok", "service": "<APP_NAME> MCP" }`

---

## get_location_ids

将国家/地区/城市等**文本**解析为 `searchInfluencers` 可用的 **location ID**。

### 必填参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `platform` | string | `tiktok` \| `instagram` \| `youtube` |
| `location_text` | string[] | 如 `["United States"]`、`["London","Paris"]` |

### 返回

```json
{
  "code": 0,
  "message": "success",
  "data": { "locationIds": [] }
}
```

### Agent 提示

用户给出地名时：**先** `get_location_ids`，**再** `searchInfluencers`。

---

## searchInfluencers

基于自然语言 `query` + 结构化 filters 的 AI 红人搜索。

### 必填参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `query` | string | 搜索意图、垂类、风格等 |
| `platform` | string | `tiktok` \| `instagram` \| `youtube`，缺失时必须追问 |

### 常用可选参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `page` | int | 页码，从 0 开始，默认 0 |
| `page_size` | int | 每页条数，1–50，默认 20 |
| `followers_min` / `followers_max` | int | 粉丝区间 |
| `gender` | string | `MALE` \| `FEMALE` \| `KNOWN` \| `UNKNOWN` |
| `language` | string | ISO 639-1，如 `en`、`zh` |
| `has_email` | bool | 是否要求公开邮箱 |
| `locations` | int[] | 来自 `get_location_ids` |
| `username` | string | 精确用户名（可带 `@`） |
| `engagement_rate_min` | float | 小数，如 0.03 表示 3% |

完整参数见 `tool_specs.yaml`。

### 返回与计费

- 成功：`code: 0`，`data.influencers`、`data.total`
- 积分不足：`code: 402`，`data.errorCode`: `CREDITS_INSUFFICIENT`
- 扣费：**实际返回的红人条数** × search 单价

---

## MCP Resource

- `app://info` — 应用名称与版本
