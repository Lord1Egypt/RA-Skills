---
name: automation-workflow
description: Create and manage automation workflows for repetitive tasks. Use when user needs to schedule periodic data sync, chain API calls, set up triggered actions, build if-this-then-that style automation, or create multi-step business workflows.
---

# Automation Workflow

Create and manage automation workflows for repetitive tasks.

## Quick Start

```bash
# Install dependencies
pip install schedule requests

# Run a simple workflow
python scripts/workflow.py examples/simple.yaml
```

## Core Concepts

- **Trigger**: What starts the workflow (time, webhook, file change)
- **Actions**: What gets executed (API calls, notifications, data transformations)
- **Flow Control**: Conditions, loops, error handling

## Workflow Format (YAML)

```yaml
name: daily-report
trigger:
  type: schedule
  cron: "0 9 * * *"  # Daily at 9am

actions:
  - name: fetch-data
    type: http
    config:
      url: https://api.example.com/data
      method: GET
      
  - name: process
    type: transform
    config:
      template: "Report: {{results.count}} items"
      
  - name: notify
    type: telegram
    config:
      chat_id: "{{env.CHAT_ID}}"
      message: "{{processed}}"
```

## Supported Triggers

- **schedule**: Cron-based scheduling
- **webhook**: HTTP POST/GET triggers
- **file**: Watch for file changes
- **queue**: Message queue triggers

## Supported Actions

- **http**: Make HTTP requests
- **telegram**: Send Telegram messages
- **email**: Send emails
- **transform**: Data transformation
- **storage**: Save/load data

## Usage Examples

See `references/examples.md` for more.

### Daily Report Workflow
```yaml
name: daily-sales
trigger:
  type: schedule
  cron: "0 8 * * *"
actions:
  - type: http
    name: get-sales
    config:
      url: https://api.shop.com/sales
  - type: transform
    name: format
    config:
      template: "Sales: ${{results.total}}"
  - type: telegram
    name: send
    config:
      message: "{{formatted}}"
```

### Webhook Trigger
```yaml
name: github-webhook
trigger:
  type: webhook
  path: /webhook/github
actions:
  - type: transform
    name: parse
    config:
      template: "New {{payload.action}} on {{payload.repository}}"
```

## Script Usage

```bash
python scripts/workflow.py [OPTIONS]

Options:
  --file PATH      Workflow YAML file (required)
  --run-once       Run workflow once and exit
  --daemon         Run as background daemon
  --env FILE       Load environment variables
```

## Best Practices

1. Use environment variables for secrets
2. Add error handling for each action
3. Log actions for debugging
4. Test workflows with --run-once first
