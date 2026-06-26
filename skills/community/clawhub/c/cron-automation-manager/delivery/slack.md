# Slack Delivery

Use this configuration when the user selects Slack as the notification channel.

```
delivery:
  mode: announce
  channel: slack
  to: <channel_or_user_id>
```

Notes:
- Slack apps must be installed and authorized.
- Ensure the bot token has chat:write permission.
