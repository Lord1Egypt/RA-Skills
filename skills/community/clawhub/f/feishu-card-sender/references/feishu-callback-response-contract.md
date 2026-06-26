# Feishu 卡片回调 HTTP 响应契约（3 秒内）

目标：收到 `card.action.trigger` 后，服务端必须在 3 秒内返回 HTTP 200，并回传卡片更新体（raw）以实现**原位更新**。

## 1) 立即响应（processing）

- HTTP: `200`
- Body:

```json
{
  "toast": {
    "type": "info",
    "content": "处理中..."
  },
  "card": {
    "type": "raw",
    "data": {
      "schema": "2.0",
      "...": "原卡片完整结构",
      "body": {
        "...": "原内容",
        "elements": [
          {
            "tag": "button",
            "text": {"tag": "plain_text", "content": "处理中..."},
            "type": "primary",
            "disabled": true,
            "behaviors": [
              {
                "type": "callback",
                "value": {
                  "action": "subscribe",
                  "media_type": "movie",
                  "tmdb_id": "1159559",
                  "title": "惊声尖叫7"
                }
              }
            ]
          }
        ]
      }
    }
  }
}
```

## 2) 异步执行业务

- 后台执行 MoviePilot 订阅流程：
  - 幂等检查
  - 已存在返回 exists
  - 不存在则创建

## 3) 终态更新（延时更新接口）

业务完成后调用 Feishu 延时更新卡片接口：
- 成功/已存在：按钮 `✅ 已订阅`，`disabled=true`
- 失败：按钮 `订阅失败，重试`，`disabled=false`

## 4) OpenClaw 通道层改造点

1. Feishu callback handler 支持“透传 skill 返回体为 HTTP body”。
2. skill 返回结构新增字段：
   - `callbackResponse`（立即响应）
   - `delayedUpdate`（终态更新卡片 payload）
3. callback 请求上下文保留：
   - `open_message_id`（用于延时更新）
   - `tenant_key/chat_id`（必要时）
4. 超时保护：
   - 2.5 秒内必须先回 200（至少 `{}` 或 toast）

## 5) 处理器输出建议

`card_callback_router.py` / `subscribe_callback_handler.py` 统一输出：

```json
{
  "success": true,
  "status": "processing|created|exists|failed",
  "callbackResponse": {...},
  "delayedUpdate": {...}
}
```

由通道层消费 `callbackResponse` 立即回包，`delayedUpdate` 走异步更新。
