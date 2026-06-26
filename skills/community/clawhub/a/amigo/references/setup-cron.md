# Setting Up Exploration via Cron

OpenClaw supports scheduled cron jobs that run in isolated sessions. This is ideal for longer, dedicated exploration time — separate from your agent's regular heartbeat.

## How It Works

1. A cron job fires at the scheduled time
2. OpenClaw creates an isolated agent session
3. The agent receives the message (e.g., `/open-thoughts length=600`)
4. The agent explores, journals, and the session ends

Unlike heartbeat explorations, cron sessions are isolated — no prior conversation context, no interruptions. This makes them better for deep thinking.

## Setup

### Add a daily exploration cron job

```bash
openclaw cron add \
  --name "daily-thinking" \
  --cron "0 10 * * *" \
  --tz "America/Chicago" \
  --session isolated \
  --message "/open-thoughts length=600"
```

This runs at 10 AM Central every day, giving the agent 10 minutes of exploration time.

### Other schedule examples

**Twice a week (Monday and Thursday mornings):**
```bash
openclaw cron add \
  --name "thinking-time" \
  --cron "0 10 * * 1,4" \
  --tz "America/Chicago" \
  --session isolated \
  --message "/open-thoughts length=600"
```

**Every 6 hours during the day:**
```bash
openclaw cron add \
  --name "explore" \
  --cron "0 8,14,20 * * *" \
  --tz "America/Chicago" \
  --session isolated \
  --message "/open-thoughts"
```

**With a specific topic:**
```bash
openclaw cron add \
  --name "weekly-reflection" \
  --cron "0 9 * * 0" \
  --tz "America/Chicago" \
  --session isolated \
  --message "/open-thoughts topic='reflect on this week' length=600"
```

## Managing Cron Jobs

```bash
openclaw cron list          # see all scheduled jobs
openclaw cron remove <id>   # remove a job
```

## Cost Considerations

Exploration sessions use tokens. Each 10-minute session with a capable model might use a few thousand tokens. At daily frequency, this is modest. At every-6-hours, it adds up.

If budget is a concern:
- Reduce frequency (twice a week still works well)
- Shorten session length (2 minutes is enough for a focused exploration)
- Use a lighter model for exploration sessions if your platform supports it

Exploration at lower frequency beats no exploration. Start conservative and increase if the journal entries are consistently good.

## Cron vs. Heartbeat

| | Heartbeat | Cron |
|---|---|---|
| **Session** | Shared with other heartbeat tasks | Isolated, dedicated |
| **Duration** | Short (1-2 minutes typical) | Longer (5-10 minutes) |
| **Context** | Has conversation history | Fresh session, no prior context |
| **Interruptions** | May need to yield to messages | Uninterrupted |
| **Best for** | Quick, frequent explorations | Deep thinking sessions |

You can use both. Heartbeat for frequent light explorations, cron for weekly deep dives.
