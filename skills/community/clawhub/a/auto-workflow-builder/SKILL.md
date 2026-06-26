# Auto Workflow Builder

Build automated workflows without writing code.

## Features

- **Visual Workflow Builder** - Drag and drop connections
- **100+ Integrations** - APIs, webhooks, schedules
- **Triggers** - Webhooks, schedules, events
- **Actions** - Send email, HTTP requests, database operations
- **Conditions** - If/else logic, filters
- **History** - Execution logs and debugging

## Quick Start

```bash
# Create workflow
./workflow.sh create my-workflow

# Add trigger
./workflow.sh add-trigger my-workflow schedule "*/5 * * * *"

# Add action
./workflow.sh add-action my-workflow http "https://api.example.com"

# Run
./workflow.sh run my-workflow
```

## Triggers Supported

- Schedule (cron)
- Webhook
- HTTP
- Database changes
- File changes

## Actions Supported

- HTTP Requests
- Email
- SMS
- Database
- Slack/Discord notifications
- AWS Lambda

## Requirements

- Node.js 18+
- Redis (optional)

## Author

Sunshine-del-ux
