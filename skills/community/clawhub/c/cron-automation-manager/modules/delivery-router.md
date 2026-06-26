# Delivery Router Module

Responsible for selecting the correct push notification channel.

Supported channels:

- Feishu
- Telegram
- DingTalk
- Slack
- Discord
- WhatsApp
- Email
- Webchat

## Selection Logic

1. If the user explicitly specifies a channel → use it.
2. If multiple channels are configured → ask user preference.
3. If no channel specified → default to current chat session.

## Feishu Example

```
delivery:
  mode: announce
  channel: feishu
  to: <open_id>
```

## Telegram Example

```
delivery:
  mode: announce
  channel: telegram
  to: <chat_id>
```

## Behavior

The router ensures that cron jobs always include an explicit `delivery.channel` when multiple channels exist.
