# Automation Workflow Examples

## Example 1: Daily Report to Telegram

```yaml
name: daily-report
trigger:
  type: schedule
  cron: "0 9 * * *"

actions:
  - name: fetch-metrics
    type: http
    config:
      url: https://api.example.com/metrics
      method: GET
      
  - name: format-report
    type: transform
    config:
      template: "📊 Daily Report\n\nUsers: {{fetch-metrics_result.users}}\nRevenue: ${{fetch-metrics_result.revenue}}"
      
  - name: send-telegram
    type: telegram
    config:
      chat_id: "{{env.REPORT_CHAT_ID}}"
      message: "{{format-report}}"
```

## Example 2: GitHub Webhook Handler

```yaml
name: github-notify
trigger:
  type: webhook
  path: /webhook/github

actions:
  - name: log-request
    type: log
    config:
      message: "Received GitHub webhook"
      
  - name: notify
    type: telegram
    config:
      message: "🔔 {{payload.action}} on {{payload.repository.full_name}}"
```

## Example 3: Data Sync

```yaml
name: sync-data
trigger:
  type: schedule
  cron: "*/15 * * * *"  # Every 15 minutes

actions:
  - name: fetch-new
    type: http
    config:
      url: https://api.source.com/items?since={{last_sync}}
      
  - name: transform
    type: transform
    config:
      template: "{{fetch-new_result.items}}"
      
  - name: save
    type: storage
    config:
      path: /tmp/sync-data.json
      data: "{{transform}}"
```

## Environment Variables

Create a `.env` file:
```
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
REPORT_CHAT_ID=123456789
```

## Running

```bash
# Run once
python scripts/workflow.py --file examples/daily-report.yaml --run-once

# Run as daemon
python scripts/workflow.py --file examples/daily-report.yaml --daemon

# With environment
python scripts/workflow.py --file examples/daily-report.yaml --env .env
```
