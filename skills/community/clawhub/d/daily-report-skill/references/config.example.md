# Daily Report Config Example

Config location: `config/daily-report.json` (workspace root, not included in skill package)

```json
{
  "recipient": {
    "name": "Shiller",
    "feishu_open_id": "ou_xxx",
    "discord_id": "123456789"
  },
  "channels": [
    {
      "type": "feishu",
      "target": "ou_xxx"
    },
    {
      "type": "discord",
      "target": "123456789"
    }
  ],
  "agent_name": "Lucky",
  "timezone": "Asia/Shanghai"
}
```

## Field Reference

- `recipient.name` - Recipient name (for template variable)
- `recipient.feishu_open_id` - Feishu Open ID
- `recipient.discord_id` - Discord user ID
- `channels` - Notification channel list
  - `type` - Channel type: feishu / discord / slack / telegram
  - `target` - Target ID (user ID or channel ID)
- `agent_name` - Agent name (for signature)
- `timezone` - Timezone