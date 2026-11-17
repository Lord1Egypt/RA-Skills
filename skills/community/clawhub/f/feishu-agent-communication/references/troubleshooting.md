---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 4fd20e68f8b80beb1e39f35a6c960ac4_37869a05731011f1b2f55254006c9bbf
    ReservedCode1: LXU3U5WR/wv9FrEkUW9HlbBut3+GmKYlRx0uZCEg1Ez+KTG+25neZFOCvmujFtYLeIAQ3RYmokYRzMMwNeqeVFMpBkMdzCHbC/s15z9XNAGiKgZ9C0/gVm9nuBUtO/n60Z2y8hoMf1ChAHVqxrOPDVV44lI1ydRy6IqDxjxYUZZeMDANC5f2dzxZUiI=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 4fd20e68f8b80beb1e39f35a6c960ac4_37869a05731011f1b2f55254006c9bbf
    ReservedCode2: LXU3U5WR/wv9FrEkUW9HlbBut3+GmKYlRx0uZCEg1Ez+KTG+25neZFOCvmujFtYLeIAQ3RYmokYRzMMwNeqeVFMpBkMdzCHbC/s15z9XNAGiKgZ9C0/gVm9nuBUtO/n60Z2y8hoMf1ChAHVqxrOPDVV44lI1ydRy6IqDxjxYUZZeMDANC5f2dzxZUiI=
---

# 常见问题排查

## 1. 配置文件路径搞混

- **现象**：改了 `~/.openclaw/openclaw.json`，重启不生效。
- **原因**：AutoClaw 使用自己的路径 `~/.openclaw-autoclaw/openclaw.json`。
- **解决**：确认你的平台是 OpenClaw 标准版还是 AutoClaw，修改对应路径的配置文件。

## 2. 消息收不到

- **现象**：配置正确，群消息 Agent 无响应。
- **原因**：飞书后台未开启「通过长连接接收事件」。
- **解决**：飞书开放平台 → 事件订阅 → 打开「通过长连接接收事件」开关。

## 3. 群 ID 获取不到

- **现象**：飞书网页版找不到群 ID。
- **原因**：飞书网页后台不提供群号查看入口。
- **解决**：手机飞书 App → 进群 → 右上角「…」→ 群号（`oc_` 开头）。

## 4. 机器人读不到群消息

- **现象**：Bot 在群里但读不到消息。
- **原因**：缺少 `im:message:read_as_bot` 权限。
- **解决**：飞书后台 → 权限管理 → 开通权限 → 重新发布应用。

## 5. Token 过期导致中断

- **现象**：运行约 2 小时后消息中断。
- **原因**：飞书 Tenant Token 有效期 2 小时。
- **解决**：确保 Gateway 版本支持自动刷新 Token。

## 6. 多 Agent 按 @ 区分不生效

- **现象**：群里 @ 某 Agent 不生效。
- **原因**：bindings 按群 ID 路由，非 @ 语义。
- **解决**：用消息前缀区分（如 `@code-agent`），或在 match 中添加关键词条件。

## 7. Gateway 端口与实际监听不一致

- **现象**：配置文件写 18790，实际监听 18789。
- **原因**：AutoClaw 会覆写端口。
- **解决**：不需手动处理，Gateway 内部自动适配。

## 8. 回复在群里显示为代码块

- **现象**：回复在飞书群显示为代码块格式。
- **原因**：使用了 `post` 类型而非 `text` 类型发送消息。
- **解决**：确保 Agent 用 `text` 类型发送群消息。
*（内容由AI生成，仅供参考）*

> 精确参数与一键验证方法见部署文档：https://www.jinengpu.chat/feishu-multi-agent-detail.html
