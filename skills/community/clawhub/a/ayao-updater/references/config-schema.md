# Config Schema

Config file location: `~/.openclaw/workspace/skills/openclaw-auto-update/config.json`
(Override with env var: `OPENCLAW_UPDATE_CONFIG=/path/to/config.json`)

## Full Example

```json
{
  "schedule": "0 2 * * *",
  "skipSkills": ["my-custom-skill", "work-internal"],
  "skipPreRelease": true,
  "restartGateway": true,
  "notify": true,
  "notifyTarget": "8449051145",
  "dryRun": false
}
```

## Fields

| Field | Type | Default | Description |
|---|---|---|---|
| `schedule` | string | `"0 2 * * *"` | Cron expression for update schedule (used by install-cron.sh) |
| `skipSkills` | string[] | `[]` | Skill slugs to never update (e.g. locally modified skills) |
| `skipPreRelease` | boolean | `true` | Skip alpha/beta/rc/next versions |
| `restartGateway` | boolean | `true` | Restart gateway after OpenClaw update |
| `notify` | boolean | `true` | Send completion notification |
| `notifyTarget` | string | `null` | Telegram chat_id or channel target. If null, uses `openclaw system event` |
| `dryRun` | boolean | `false` | Preview mode — show what would be updated without making changes |

## Schedule Examples

| Schedule | Meaning |
|---|---|
| `"0 2 * * *"` | Daily at 2 AM |
| `"0 3 * * 0"` | Weekly on Sunday at 3 AM |
| `"0 2 * * 1-5"` | Weekdays at 2 AM |
| `"0 2 1 * *"` | Monthly on the 1st at 2 AM |

## Locally Modified Skills

Skills that have uncommitted git changes in their directory are automatically skipped
to avoid overwriting local customizations. Add them to `skipSkills` for a permanent skip.

## Conflict Handling

| Situation | Behavior |
|---|---|
| Locally modified skill (git dirty) | Skip with warning |
| Skill in `skipSkills` | Skip silently |
| Pre-release version + `skipPreRelease: true` | Skip |
| Update fails | Log error, continue others, notify failure |
| OpenClaw update fails | Stop, notify failure |
