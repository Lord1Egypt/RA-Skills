# 跨平台渠道参考

## OpenClaw 支持的渠道

| 渠道 | `--channel` 值 | 目标格式 |
|------|---------------|----------|
| 飞书 | `feishu` | 用户 open_id 或群 chat_id |
| WhatsApp | `whatsapp` | E.164 号码（如 `+8613800138000`） |
| Telegram | `telegram` | chat id 或 @username |
| Discord | `discord` | 频道/user ID |
| Slack | `slack` | 频道/user ID |
| Signal | `signal` | E.164 号码 |
| iMessage | `imessage` | Apple ID / 手机号 |
| Line | `line` | 用户/群 ID |
| Google Chat | `googlechat` | 空间/线程 ID |
| MS Teams | `msteams` | 频道/用户 ID |
| Matrix | `matrix` | 房间/user ID |
| Mattermost | `mattermost` | 频道 ID |
| IRC | `irc` | 频道/用户 |
| Nostr | `nostr` | npub hex |
| Nextcloud Talk | `nextcloud-talk` | 会话 token |
| Synology Chat | `synology-chat` | 频道 ID |
| Tlon | `tlon` | 船/终端 ID |
| Zalo | `zalo` | 用户 ID |
| BlueBubbles | `bluebubbles` | chat GUID / 手机号 |

## 消息类型支持

- **纯文本**：所有渠道均支持
- **媒体附件**：`--media` 参数支持图片、音频、视频、文档
- **静默发送**：`--silent`（Telegram + Discord）
- **引用回复**：`--reply-to <message-id>`
- **按钮/卡片**：`--buttons`（Telegram）、`--card`（Adaptive Card）、`--components`（Discord）

## 跨渠道注意事项

1. **飞书**：target 使用 `ou_` 开头的 open_id 或 `oc_` 开头的 chat_id
2. **WhatsApp**：target 必须是 E.164 格式，带国际区号
3. **Telegram**：群组使用负数 chat_id
4. **Discord**：频道目标格式 `channel:<snowflake_id>`
5. **Slack**：频道目标使用 `#channel_name` 或 channel ID
6. **Markdown 支持**：各渠道对 Markdown 的支持程度不同；飞书/Discord/Slack 较完善，WhatsApp 不支持
7. **媒体大小**：各渠道有不同限制，建议附件 < 30MB
8. **速率限制**：群发时注意各渠道的频率限制，建议间隔 1-2 秒
