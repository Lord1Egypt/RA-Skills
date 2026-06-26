# Telegram Delivery

Use this delivery configuration when the user chooses Telegram (Telegram Bot or Bot API integration).

Example:

```
delivery:
  mode: announce
  channel: telegram
  to: <chat_id>
```

Notes:
- <chat_id> should correspond to the target user or group chat.
- Ensure the Telegram bot is configured and authorized in the OpenClaw environment.
