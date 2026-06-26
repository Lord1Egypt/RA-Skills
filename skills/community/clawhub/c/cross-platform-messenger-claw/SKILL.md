---
name: cross-platform-messenger-claw
description: "跨渠道消息推送与联络协调。核心职责：打通各类通讯工具与邮件的接口，确保预警和报告能精准推送到目标人员。业务价值：信息直达——让每一条重要消息都能触达对的人、对的设备。激活场景：用户要求发送消息到某个通讯平台（飞书、WhatsApp、Telegram、Discord、Slack、Signal、iMessage、Line、Teams 等）；用户要求跨平台群发、广播通知；用户要求配置消息推送规则（报警、报告定时推送）；用户提到发消息、推送通知、群发、广播、通知某某等；用户需要将系统预警、报告、摘要等内容推送到个人手机；用户要求设置定时推送或条件触发推送。触发关键词：发消息、推送、通知、群发、广播、告警推送、报告推送、定时通知、跨平台、飞书通知、WhatsApp、Telegram、Discord、Slack、邮件通知。"
---

# 跨平台消息联络虾

## 核心能力

通过 OpenClaw CLI `openclaw message` 命令，向 20+ 通讯渠道发送文本消息和媒体附件。

### 单条推送

```bash
openclaw message send --channel <渠道> --target <目标> --message "<消息>"
```

带附件：
```bash
openclaw message send --channel <渠道> --target <目标> --message "<消息>" --media <路径或URL>
```

### 广播/群发

```bash
openclaw message broadcast --channel <渠道> --targets <目标1> <目标2> ... --message "<消息>"
```

或使用 `scripts/notify.sh` 从文件批量推送：
```bash
./scripts/notify.sh --channel <渠道> --message "<消息>" < targets.txt
```

## 渠道参考

各渠道的 `--channel` 值和 `--target` 格式见 [references/channels.md](references/channels.md)。

**最常用渠道速查：**

| 场景 | 命令 |
|------|------|
| 飞书用户 | `--channel feishu --target ou_xxx` |
| 飞书群 | `--channel feishu --target oc_xxx` |
| WhatsApp | `--channel whatsapp --target +86138xxxx` |
| Telegram | `--channel telegram --target @username` |
| Discord 频道 | `--channel discord --target channel:<id>` |
| Slack 频道 | `--channel slack --target #channel_name` |

## 工作流程

### 即时推送

1. 确认渠道和目标（who + where）
2. 确认消息内容和格式（文本/附件/卡片）
3. 用 `openclaw message send` 执行
4. 反馈发送结果

### 定时推送（cron + notify.sh）

1. 确认推送频率、时间、内容模板
2. 编写推送脚本或使用 `scripts/notify.sh`
3. 通过 `openclaw cron` 设置定时任务
4. 验证首次执行结果

### 条件推送（预警场景）

1. 确认触发条件（阈值、事件等）
2. 确认推送目标和消息模板
3. 编写检测脚本（可用 `scripts/notify.sh` 发送结果）
4. 通过 cron 或 heartbeat 实现定期检查

## 消息格式建议

- **飞书/Discord/Slack**：支持 Markdown，善用格式化
- **WhatsApp**：纯文本为主，避免 Markdown 特殊字符
- **Telegram**：支持部分 Markdown，可用按钮交互
- **跨渠道通用**：优先使用纯文本 + Emoji，确保兼容性
- **重要通知**：建议多渠道冗余推送

## 注意事项

- 各渠道有频率限制，群发时注意间隔
- 媒体文件建议 < 30MB
- `--dry-run` 可用于测试而不实际发送
- 发送失败时检查目标格式和渠道配置
