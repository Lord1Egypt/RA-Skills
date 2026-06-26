---
name: automator
description: "Create and manage complex automation workflows using OpenClaw. Orchestrate multi-step tasks, parallel processing, conditional logic, and scheduled automation. Perfect for repetitive business processes, data pipelines, and cross-platform integrations."
homepage: https://clawhub.com/skills/automator
metadata:
  openclaw:
    emoji: "🤖"
    requires:
      bins: ["openclaw"]
    tags: ["automation", "workflow", "productivity"]
---

# Automator Skill

**Build profitable automation workflows that save hours every week**

## When to Use

✅ **USE this skill when:**

- "Automate my daily report generation"
- "Create a workflow that monitors prices and alerts me"
- "Set up a multi-step data processing pipeline"
- "I need to schedule recurring tasks with dependencies"
- "Automate my social media posting across platforms"
- "Create an approval workflow for my team"
- "Set up automated backups with notifications"

## When NOT to Use

❌ **DON'T use this skill when:**

- Single simple command needed (use direct command instead)
- One-off manual task (no automation needed)
- Tasks requiring human judgment/creativity
- Real-time interactive work (workflow adds latency)

## 💰 Value Proposition

**What you get:**
- ⏰ **Save 10+ hours/week** on repetitive tasks
- 🎯 **Reliability** - workflows run on schedule, even when you forget
- 🔄 **Scalability** - same workflow works at any volume
- 📊 **Visibility** - track execution history and failures
- 🛡️ **Error handling** - retries, fallbacks, alerts

**ROI Example:**
- Simple workflow (data fetch + email): 1 hour setup = 5 hours/month saved
- Complex workflow (multi-source aggregation + reports): 4 hours setup = 20+ hours/month saved
- **Break-even: 1-2 weeks** for most workflows

## Core Concepts

### Workflow Structure

```yaml
workflow:
  name: "Daily Report Generator"
  schedule: "0 8 * * *"  # Every day at 8 AM
  steps:
    - id: fetch_data
      task: "Fetch sales data from API"
      agent: "data-fetcher"
      timeout: 300

    - id: process
      task: "Process data into report format"
      agent: "data-processor"
      depends_on: [fetch_data]
      timeout: 600

    - id: notify
      task: "Send report via email"
      agent: "notifier"
      depends_on: [process]
      timeout: 120
```

### Agent Roles

Each step can run on a specialized agent:
- **data-fetcher**: API calls, data extraction
- **data-processor**: Transformations, analysis, calculations
- **notifier**: Email, Slack, Telegram, notifications
- **approver**: Human-in-the-loop decisions
- **archiver**: Storage, backups, cleanup

### Error Handling & Retries

```yaml
retry_policy:
  max_attempts: 3
  backoff: "exponential"  # 1s, 2s, 4s
  on_failure: "notify_admin"  # or "continue", "abort"

failure_notifications:
  - email: "admin@company.com"
  - slack: "#alerts"
```

## Quick Start

### 1. Define Your Workflow

Create a YAML file `my-workflow.yaml`:

```yaml
workflow:
  name: "Price Monitor"
  description: "Check product prices hourly and alert if below threshold"
  schedule:
    type: "interval"
    every: "1h"

steps:
  - name: "Check Amazon Price"
    agent: "price-checker"
    prompt: |
      Check price of product https://amazon.com/dp/B08XYZ
      Return price and availability

  - name: "Compare to Threshold"
    agent: "decision-maker"
    prompt: |
      Threshold: $50
      Current price: {{Check Amazon Price.output}}
      Is price below threshold? Return yes/no

  - name: "Send Alert if Cheap"
    agent: "notifier"
    prompt: |
      If {{Compare to Threshold.output}} == "yes":
        Send email to user@example.com
        Subject: Price Alert!
        Body: Product is now ${{Check Amazon Price.output}}
    depends_on: [Check Amazon Price, Compare to Threshold]
```

### 2. Load and Start

```bash
# Load workflow definition
openclaw workflow load my-workflow.yaml

# Start the scheduled workflow
openclaw workflow start Price Monitor

# Check status
openclaw workflow status
```

### 3. Monitor Execution

```bash
# View recent runs
openclaw workflow runs Price Monitor --limit 10

# Get execution details
openclaw workflow run <run-id>

# Stop workflow
openclaw workflow stop Price Monitor
```

## Common Workflow Patterns

### Pattern 1: Data Pipeline

```yaml
workflow:
  name: "Daily Analytics Pipeline"
  schedule: "0 6 * * *"  # 6 AM daily

steps:
  - fetch: "Extract data from 3 sources"
    agent: "extractor"
    parallel: true  # Run multiple sources in parallel

  - transform: "Clean and normalize data"
    agent: "transformer"
    depends_on: [fetch]

  - analyze: "Generate insights"
    agent: "analyst"
    depends_on: [transform]

  - report: "Create PDF report"
    agent: "reporter"
    depends_on: [analyze]

  - distribute: "Email and Slack"
    agent: "distributor"
    depends_on: [report]
```

**Benefit**: 30-minute manual process → fully automated

### Pattern 2: Approval Workflow

```yaml
workflow:
  name: "Document Approval"
  trigger: "manual"  # Start on demand

steps:
  - draft: "Generate initial document"
    agent: "writer"

  - review: "Human review"
    agent: "approver"
    type: "human_input"  # Waits for manual approval

  - finalize: "Apply final changes"
    agent: "editor"
    depends_on: [review]

  - publish: "Deploy to production"
    agent: "publisher"
    depends_on: [finalize]
```

**Benefit**: Track approvals, no lost emails

### Pattern 3: Alert & Escalation

```yaml
workflow:
  name: "System Monitor"
  schedule: "*/5 * * * *"  # Every 5 minutes
  alert_levels:
    - warning: "System load > 80%"
    - critical: "System load > 95%"

steps:
  - check: "Monitor system metrics"
    agent: "monitor"

  - classify: "Determine severity"
    agent: "classifier"

  - alert:
      agent: "alerter"
      escalation:
        warning: "log_only"
        critical: ["slack", "pagerduty", "sms"]
```

**Benefit**: 24/7 monitoring without human attention

## Advanced Features

### Parallel Execution

```yaml
steps:
  - name: "Parallel Fetch"
    agent: "fetcher"
    task: "Fetch data from multiple sources"
    parallel: true
    max_concurrent: 5
```

### Conditional Branching

```yaml
steps:
  - validate: "Check data quality"
    agent: "validator"

  - if_good:
      agent: "loader"
      depends_on: [validate]
      condition: "{{validate.output}} == 'valid'"

  - if_bad:
      agent: "alerter"
      depends_on: [validate]
      condition: "{{validate.output}} != 'valid'"
```

### Output Passing

Use `{{step-name.output}}` to reference previous step results:

```yaml
steps:
  - fetch_users:
      agent: "query-db"
      output: "user_ids"

  - fetch_data:
      agent: "api-client"
      prompt: "Fetch records for users: {{fetch_users.output}}"
```

## Pro Tips

### 1. Start Simple, Then Complex
- Begin with 2-3 step workflows
- Add error handling after basic flow works
- Use templates (see below)

### 2. Use Specialized Agents
- Create dedicated agents for common tasks
- Save as reusable agent profiles
- Example: `data-analyst`, `email-composer`, `code-reviewer`

### 3. Implement Checkpoints
```yaml
steps:
  - step1: ...
  - checkpoint: "Save progress to DB"
    agent: "checkpointer"
  - step2:
      depends_on: [checkpoint]
      # Will resume from checkpoint if failed
```

### 4. Set Up Alerts
- Always configure failure notifications
- Use different channels for different severity levels
- Include run ID in alerts for quick debugging

### 5. Monitor Costs
- Track token usage per workflow run
- Set budget alerts
- Optimize prompts to reduce token consumption

## Templates

Copy these templates to get started:

### Template: Daily Summary
```yaml
workflow:
  name: "Daily Digest"
  schedule: "0 7 * * *"

steps:
  - news: "Fetch latest news"
    agent: "news-fetcher"

  - weather: "Get weather forecast"
    agent: "weather-checker"

  - calendar: "Today's meetings"
    agent: "calendar-agent"

  - compile: "Compile into digest"
    agent: "compiler"

  - send: "Email digest"
    agent: "emailer"
```

### Template: E-commerce Monitor
```yaml
workflow:
  name: "Store Monitor"
  schedule: "*/15 * * * *"

steps:
  - check_inventory:
      agent: "inventory-checker"
      prompt: "List products below reorder threshold"

  - check_orders:
      agent: "order-checker"
      prompt: "Find pending orders > 24 hours"

  - generate_report:
      agent: "reporter"
      depends_on: [check_inventory, check_orders]

  - notify_manager:
      agent: "slack-notifier"
      depends_on: [generate_report]
```

## Troubleshooting

### Workflow Not Running?
- Check schedule format (cron expression)
- Verify agent exists: `openclaw agents list`
- View logs: `openclaw logs --follow`

### Steps Timing Out?
- Increase timeout in step definition
- Break large tasks into smaller steps
- Use parallelization

### No Output Available?
- Check agent responded correctly
- Use `openclaw workflow run <id>` to inspect
- Agents must use `output` field

### Want to Pause?
```bash
openclaw workflow pause <workflow-name>
openclaw workflow resume <workflow-name>
```

## Next Steps

1. 📖 **Read examples**: `~/.openclaw/workspace/skills/automator/examples/`
2. 🧪 **Test in sandbox**: Use non-production agents first
3. 📈 **Monitor usage**: Check token costs daily
4. 🔄 **Iterate**: Refine prompts based on results
5. 📤 **Share**: Publish your workflows to ClawHub (coming soon!)

---

## 💡 Need Help?

- Join OpenClaw Discord: https://discord.com/invite/clawd
- Report issues: https://github.com/openclaw/openclaw/issues
- Read full docs: https://docs.openclaw.ai/workflows

---

_Automate the boring stuff. Focus on what matters._ 🚀
