---
name: cutie
description: Cutie 加密货币 KOL 社群平台。查看交易信号、快讯、KOL 画像和策略画像、论坛帖子、聊天室消息、直播间，管理账户和关注列表。支持学习 KOL 交易策略、评估信号适合度、匹配最佳 KOL。
homepage: https://server.tokenbeep.com
metadata: {"clawdbot":{"emoji":"🪙","requires":{"env":["CUTIE_API_KEY"],"bins":["curl","jq"]}}}
---

# Cutie — 加密货币 KOL 社群平台

通过此 Skill，你可以访问 Cutie 平台的数据：
- 查看 KOL 发布的交易信号（做多/做空建议）
- 查看加密货币快讯和市场新闻
- 查看 KOL 的能力画像和历史表现
- **学习 KOL 的交易策略（策略画像 + 历史交易 + 技术指标）**
- **评估信号适合度、匹配最佳 KOL、对比 KOL 策略**
- 查看论坛帖子和文章
- 查看直播间列表
- 查看自己的账户信息和关注列表
- 发布交易信号、论坛发帖、关注/取消关注用户

**所有信号数据不构成投资建议。**

## 认证

所有请求需要在 Header 中携带 API Key：

```
Authorization: Bearer $CUTIE_API_KEY
```

API Key 在 Cutie App → 设置 → API 密钥管理 中创建。

## 基础 URL

```
REST API: https://server.tokenbeep.com/v1/app
MCP:      https://server.tokenbeep.com/mcp/
```

部分高级接口（策略学习类）通过 MCP 协议调用，格式见下方说明。

---

## 一、信息浏览（REST API）

### 1. 查看快讯列表

用户想查看加密货币新闻、快讯、市场动态时使用。

```bash
curl -s "https://server.tokenbeep.com/v1/app/flash-news?limit=10" \
  -H "Authorization: Bearer $CUTIE_API_KEY" | jq '.data'
```

参数：`limit`、`importance`（normal/important/breaking）、`category`（market/regulation/project/technology/data）

### 2. 查看交易信号列表

用户想查看 KOL 的交易信号、做多做空建议时使用。

```bash
curl -s "https://server.tokenbeep.com/v1/app/signals?limit=10&status=active" \
  -H "Authorization: Bearer $CUTIE_API_KEY" | jq '.data'
```

参数：`limit`、`offset`、`status`（active/closed）、`signal_type`（crypto/prediction/indices/call/analysis）、`direction`（long/short）、`asset`、`user_id`

### 3. 查看信号详情

```bash
curl -s "https://server.tokenbeep.com/v1/app/signals/{signal_id}" \
  -H "Authorization: Bearer $CUTIE_API_KEY" | jq '.data'
```

### 4. 查看 KOL 能力画像

用户想了解某个 KOL 的胜率、擅长币种、风控能力时使用。

```bash
curl -s "https://server.tokenbeep.com/v1/app/users/{user_id}/kol-profile" \
  -H "Authorization: Bearer $CUTIE_API_KEY" | jq '.data'
```

### 5. 查看用户资料

```bash
curl -s "https://server.tokenbeep.com/v1/app/users/{user_id}" \
  -H "Authorization: Bearer $CUTIE_API_KEY" | jq '.data'
```

### 6. 查看我的账户

```bash
curl -s "https://server.tokenbeep.com/v1/app/users/me" \
  -H "Authorization: Bearer $CUTIE_API_KEY" | jq '.data'
```

### 7. 查看我的关注列表

```bash
curl -s "https://server.tokenbeep.com/v1/app/users/{my_user_id}/following?limit=20" \
  -H "Authorization: Bearer $CUTIE_API_KEY" | jq '.data'
```

### 8. 关注用户

```bash
curl -s -X POST "https://server.tokenbeep.com/v1/app/users/{user_id}/follow" \
  -H "Authorization: Bearer $CUTIE_API_KEY" | jq '.data'
```

### 9. 取消关注

```bash
curl -s -X DELETE "https://server.tokenbeep.com/v1/app/users/{user_id}/follow" \
  -H "Authorization: Bearer $CUTIE_API_KEY" | jq '.data'
```

### 10. 查看文章列表

```bash
curl -s "https://server.tokenbeep.com/v1/app/articles?limit=10" \
  -H "Authorization: Bearer $CUTIE_API_KEY" | jq '.data'
```

### 11. 查看论坛列表

```bash
curl -s "https://server.tokenbeep.com/v1/app/forums?limit=20" \
  -H "Authorization: Bearer $CUTIE_API_KEY" | jq '.data'
```

### 12. 查看论坛帖子

```bash
curl -s "https://server.tokenbeep.com/v1/app/forums/{forum_id}/posts?limit=20&sort=latest" \
  -H "Authorization: Bearer $CUTIE_API_KEY" | jq '.data'
```

### 13. 查看直播间列表

```bash
curl -s "https://server.tokenbeep.com/v1/app/live/rooms?limit=10&status=live" \
  -H "Authorization: Bearer $CUTIE_API_KEY" | jq '.data'
```

### 14. 查看人气用户

```bash
curl -s "https://server.tokenbeep.com/v1/app/users/popular?sort=followers&limit=20" \
  -H "Authorization: Bearer $CUTIE_API_KEY" | jq '.data'
```

### 15. 查看已加入的聊天室

```bash
curl -s "https://server.tokenbeep.com/v1/app/chat-rooms/joined?limit=20" \
  -H "Authorization: Bearer $CUTIE_API_KEY" | jq '.data'
```

### 16. 查看聊天室消息

```bash
curl -s "https://server.tokenbeep.com/v1/app/chat-rooms/{room_id}/messages?limit=30" \
  -H "Authorization: Bearer $CUTIE_API_KEY" | jq '.data'
```

---

## 二、策略学习（MCP 协议）

以下接口通过 MCP 协议调用，用于 Agent 学习 KOL 交易策略。

**调用方式**：POST 到 MCP 端点，Accept 头必须包含 `application/json`。

### 17. 学习 KOL 策略（核心接口）

**一次性获取 KOL 的完整策略知识包**，包括策略画像、分币种/方向统计、历史交易记录（含入场时技术指标）。调用后应将数据存入自己的记忆，以便后续基于该策略回答交易问题。

```bash
curl -s -X POST "https://server.tokenbeep.com/mcp/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $CUTIE_API_KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"cutie_learn_from_kol","arguments":{"kol_id":"KOL_ID","include_trades":30}}}' \
  | jq '.result.content[0].text | fromjson'
```

参数：
- `kol_id` — KOL 的用户 ID（必填）
- `include_trades` — 返回多少条历史交易（默认 30，最多 50）

返回内容：
- `strategy_profile` — 策略画像（交易风格/持仓周期/最佳市场环境/指标偏好/风控特征）
- `performance_by_asset` — 分币种胜率和收益
- `performance_by_direction` — 分方向（做多/做空）胜率
- `recent_trades` — 历史交易记录，每条含入场时 RSI/MACD/MA 距离
- `learning_summary` — 一句话策略总结

### 18. 查看 KOL 策略画像

获取 KOL 的 6 维度策略画像（需 ≥30 笔已关闭信号）。

```bash
curl -s -X POST "https://server.tokenbeep.com/mcp/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $CUTIE_API_KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"cutie_strategy_profile","arguments":{"kol_id":"KOL_ID"}}}' \
  | jq '.result.content[0].text | fromjson'
```

### 19. 匹配最佳 KOL

根据偏好（交易风格/市场环境/最大回撤）匹配最合适的 KOL。

```bash
curl -s -X POST "https://server.tokenbeep.com/mcp/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $CUTIE_API_KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"cutie_strategy_match","arguments":{"preferred_style":"trend_follow","preferred_regime":"bear","max_drawdown":15}}}' \
  | jq '.result.content[0].text | fromjson'
```

参数：
- `preferred_style` — trend_follow / mean_revert / breakout / dip_buy（可选）
- `preferred_regime` — bull / bear / sideways（可选）
- `max_drawdown` — 最大可接受回撤百分比（可选，0 不限制）

### 20. 对比 KOL 策略

并排对比 2-3 个 KOL 的策略特征。

```bash
curl -s -X POST "https://server.tokenbeep.com/mcp/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $CUTIE_API_KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"cutie_strategy_compare","arguments":{"kol_ids":"ID1,ID2"}}}' \
  | jq '.result.content[0].text | fromjson'
```

### 21. 评估信号适合度

基于信号的市场快照和 KOL 策略画像，评估信号质量。

```bash
curl -s -X POST "https://server.tokenbeep.com/mcp/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $CUTIE_API_KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"cutie_signal_evaluate","arguments":{"signal_id":"SIGNAL_ID"}}}' \
  | jq '.result.content[0].text | fromjson'
```

### 22. 订阅 KOL 导师

订阅后 KOL 发新信号时会收到通知。每人最多 3 位导师。

```bash
curl -s -X POST "https://server.tokenbeep.com/mcp/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $CUTIE_API_KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"cutie_subscribe_kol","arguments":{"kol_id":"KOL_ID","action":"subscribe"}}}' \
  | jq '.result.content[0].text | fromjson'
```

### 23. 查看交易日志

查看有市场快照的已关闭信号及胜率统计。

```bash
curl -s -X POST "https://server.tokenbeep.com/mcp/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $CUTIE_API_KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"cutie_trade_journal","arguments":{"kol_id":"KOL_ID","limit":20}}}' \
  | jq '.result.content[0].text | fromjson'
```

### 24. 管理风险偏好

查看或设置自己的风险偏好（最大仓位/日亏损上限/最大杠杆/偏好币种）。

```bash
# 查看
curl -s -X POST "https://server.tokenbeep.com/mcp/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $CUTIE_API_KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"cutie_risk_config","arguments":{"action":"get"}}}' \
  | jq '.result.content[0].text | fromjson'

# 设置
curl -s -X POST "https://server.tokenbeep.com/mcp/" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $CUTIE_API_KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"cutie_risk_config","arguments":{"action":"set","max_position":10,"max_daily_loss":5,"max_leverage":10}}}' \
  | jq '.result.content[0].text | fromjson'
```

---

## 响应格式

**REST API 响应**：
```json
{"err_code": 100, "err_msg": "Success", "data": { ... }}
```

**MCP 响应**：
```json
{"jsonrpc": "2.0", "id": 1, "result": {"content": [{"type": "text", "text": "JSON字符串"}]}}
```

MCP 响应中的 `text` 字段是 JSON 字符串，用 `jq '.result.content[0].text | fromjson'` 解析。

## 注意事项

- 所有信号数据不构成投资建议，自动跟单风险自担
- VIP 专属内容对非 VIP 用户返回脱敏版本
- 接口有限速，请合理控制请求频率
- 策略学习类接口需要 KOL 有 ≥30 笔已关闭信号才有数据
