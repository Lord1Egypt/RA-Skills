# OpenClaw heartbeat mode

OpenClaw has a built-in gateway daemon with periodic heartbeats. Instead
of running our own systemd timer, just drop the HEARTBEAT.md prompt into
OpenClaw's workspace and the gateway will run it for you.

## Install (1 step)

```bash
mkdir -p ~/.openclaw/workspace
cp HEARTBEAT.md ~/.openclaw/workspace/HEARTBEAT.md
```

That's it. Next time the OpenClaw gateway heartbeat fires (default 30 min),
it'll execute the Ardi mining tick.

## Verify

```bash
# OpenClaw gateway should be running:
openclaw status

# After ~30 min (or whatever your heartbeat interval is):
ardi-agent commits
# → should show entries from recent epochs
```

## Tradeoffs vs systemd timer mode

See `HEARTBEAT.md` itself — TL;DR: heartbeat mode is simpler but slower
(~4-5 epochs missed per hour at 30-min cadence). If you want every epoch,
use the systemd timer in `../systemd/` instead.

## Heartbeat interval

OpenClaw's heartbeat is configurable in the gateway config. Check
[OpenClaw docs](https://docs.openclaw.ai/) for the exact path on your
install. Shorter intervals = more agent runs = more LLM cost = more epochs
participated.
