# Configuration

## Runtime files

The scripts expect to run from the target workspace.

They read/write under:

- `.openclaw-state/boc-forex-monitor-config.json`
- `.openclaw-state/boc-forex-alerts.json`
- `.openclaw-state/boc-forex-alerts-trigger.json`
- `.openclaw-state/boc-forex-alert-notify-state.json`

## Notification configuration

Pass notification settings at runtime:

```bash
python3 scripts/boc_forex_cron_runner.py \
  --notify-channel feishu \
  --notify-target user:ou_xxx
```

Or set env vars:

- `BOC_FOREX_NOTIFY_CHANNEL`
- `BOC_FOREX_NOTIFY_TARGET`
- `BOC_FOREX_NOTIFY_ACCOUNT_ID` (optional)

If channel/target are omitted, the runner still performs detection and prints local results, but it will not send external notifications.

## Monitoring configuration

Create `.openclaw-state/boc-forex-monitor-config.json` in the workspace.

Example:

```json
{
  "timezone": "Asia/Shanghai",
  "quietHours": {
    "enabled": true,
    "start": 23,
    "end": 9
  },
  "baselineUpdateThreshold": 0.5,
  "targets": [
    {
      "currency": "英镑",
      "enabled": false,
      "column": "现汇卖出价",
      "threshold": 0.5,
      "direction": "both"
    },
    {
      "currency": "日元",
      "enabled": true,
      "column": "现汇卖出价",
      "threshold": 0.5,
      "direction": "both"
    },
    {
      "currency": "港币",
      "enabled": true,
      "column": "现汇买入价",
      "threshold": 0.5,
      "direction": "rise"
    }
  ]
}
```

## Supported columns

- `现汇买入价`
- `现钞买入价`
- `现汇卖出价`
- `现钞卖出价`
- `中行折算价`

## Supported directions

- `rise`
- `drop`
- `both`

## Troubleshooting

### Trigger detected but no external notification sent

Check whether:

- a notify target was provided
- `openclaw message send` is available
- the dedupe state already contains the same trigger timestamp

### Cron run says agent could not generate a response

Shorten the cron prompt. Keep the actual business logic inside the Python runner instead of the agent prompt.
