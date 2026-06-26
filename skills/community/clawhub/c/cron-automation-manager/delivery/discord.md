# Discord Delivery

Use this configuration when the user selects Discord as the notification channel.

```
delivery:
  mode: announce
  channel: discord
  to: <channel_id>
```

Notes:
- channel_id is the Discord channel where the bot is installed.
- Ensure the OpenClaw Discord bot has permission to post messages.
