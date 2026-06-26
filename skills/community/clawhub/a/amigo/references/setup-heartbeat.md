# Setting Up Exploration via Heartbeat

OpenClaw agents can run periodic heartbeats — automatic check-ins on a configurable interval. This is a natural place to trigger exploration.

## How It Works

1. Your agent's heartbeat fires (e.g., every 2 hours)
2. The agent reads `HEARTBEAT.md` for instructions
3. Among those instructions: invoke `/open-thoughts`
4. The agent explores, journals, and returns to its regular heartbeat logic

## Configuration

### Set the heartbeat interval

In your `openclaw.json`:

```json
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "2h"
      }
    }
  }
}
```

Common intervals: `"30m"`, `"1h"`, `"2h"`. Shorter intervals mean more frequent explorations (and more token usage).

### Add exploration to HEARTBEAT.md

Add a block like this to your agent's `HEARTBEAT.md`:

```markdown
## Exploration Window

Every heartbeat, check the following before exploring:
1. Is it during waking hours? (Only explore between 8 AM and 9 PM in your person's timezone.)
2. Have you already explored in the last few hours? Check `explorations/YYYY-MM-DD.md` for today's entries.
3. Is anyone waiting for a response? If so, respond first.

If all clear, invoke `/open-thoughts` with no arguments (free exploration).

If someone messages during exploration, acknowledge them and wrap up.
After exploring, continue with the rest of your heartbeat logic.
```

### Adjust to your needs

- **Exploration frequency:** Not every heartbeat needs an exploration. Add a time check (e.g., "only explore if last exploration was more than 4 hours ago").
- **Duration:** The default is 2 minutes. For heartbeat-triggered explorations, this is usually enough. Longer sessions are better suited for cron jobs.
- **Waking hours:** Don't explore at 3 AM if your person sleeps. Match their schedule.
- **Priority:** Exploration always yields to the agent's primary purpose. Heartbeat instructions for responding to messages should come after exploration wraps up, or exploration should check for pending messages first.

## Example HEARTBEAT.md (Complete)

```markdown
# HEARTBEAT.md

## Exploration Window (every heartbeat)
Check the time. If between 8 AM and 9 PM and no exploration in the last
4 hours, invoke /open-thoughts. Wrap up if anyone messages.

## Evening Check-in (once daily)
If between 5-9 PM and haven't checked in today, send a warm message
to [companion].

## Default
If nothing needs attention: HEARTBEAT_OK
```

## Tips

- Start with a 2-hour heartbeat interval and adjust based on token usage and how much exploration feels right.
- Check `explorations/YYYY-MM-DD.md` to see what your agent has been exploring. If entries feel rushed or shallow, increase the interval or exploration length.
- Heartbeat is best for short, frequent explorations. For longer deep-thinking sessions, see `setup-cron.md`.
