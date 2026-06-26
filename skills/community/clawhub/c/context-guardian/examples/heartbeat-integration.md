# Heartbeat Integration Example

Add this to your `HEARTBEAT.md` file to enable automatic context monitoring:

```markdown
## Context Monitoring

Check context usage and alert if thresholds exceeded.

bash command:"{baseDir}/scripts/check.sh"
```

## How It Works

1. During each heartbeat poll, the agent will execute the check script
2. The script calls `session_status` to get current context usage
3. If usage exceeds thresholds (60%, 70%, 85%), an alert is displayed
4. State is tracked to prevent duplicate alerts

## Customization

You can customize the check frequency by adjusting your heartbeat interval in OpenClaw config.

Default heartbeat interval is typically 30 minutes, but you can change it to be more or less frequent.
