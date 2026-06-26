# Manual Check Example

You can manually check context status at any time.

## Method 1: Direct Script Call

```bash
bash ~/.openclaw/skills/context-guardian/scripts/check.sh
```

This will:
1. Get current context usage from `session_status`
2. Check against thresholds
3. Display alert if needed
4. Update state file

## Method 2: Ask the Agent

Simply ask your agent:

```
Check my context usage
```

The agent will use the context-guardian skill to check and report.

## Method 3: View State File

Check the current state directly:

```bash
cat ~/. openclaw/workspace/memory/context-guardian-state.json
```

Example output:

```json
{
  "lastCheck": 1709452800,
  "lastUsage": 54,
  "lastAlertLevel": null,
  "lastAlertTime": null,
  "history": [
    {"timestamp": 1709452800, "usage": 54},
    {"timestamp": 1709452500, "usage": 52}
  ]
}
```

## Understanding the State

- `lastCheck`: Unix timestamp of last check
- `lastUsage`: Last recorded usage percentage
- `lastAlertLevel`: Last alert level sent (warning/danger/critical)
- `lastAlertTime`: Unix timestamp of last alert
- `history`: Array of recent usage measurements (last 100)

## Resetting State

To reset the state and allow alerts to trigger again:

```bash
rm ~/.openclaw/workspace/memory/context-guardian-state.json
```

This is useful if you want to test alerts or if the state gets corrupted.
