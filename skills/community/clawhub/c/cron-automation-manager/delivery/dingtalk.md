# DingTalk Delivery

Use this configuration when the user selects DingTalk as the notification channel.

Example:

```
delivery:
  mode: announce
  channel: dingtalk
  to: <webhook_url>
```

Notes:
- DingTalk robots typically use webhook URLs.
- Ensure the webhook is already configured and allowed by the DingTalk robot security settings.
