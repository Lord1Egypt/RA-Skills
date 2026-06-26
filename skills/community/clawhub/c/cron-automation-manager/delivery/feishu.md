# Feishu Delivery

When the user selects Feishu as a delivery channel, cron jobs should include:

```
delivery:
  mode: announce
  channel: feishu
  to: <user_open_id>
```

The open_id must correspond to the authorized Feishu user.
