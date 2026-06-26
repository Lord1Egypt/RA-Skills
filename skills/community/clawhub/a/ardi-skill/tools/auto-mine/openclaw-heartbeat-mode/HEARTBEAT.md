# Ardi mining — OpenClaw heartbeat checklist

OpenClaw reads this file on each gateway heartbeat (default 30 minutes,
hourly with Anthropic OAuth). Place it at `~/.openclaw/workspace/HEARTBEAT.md`
to enable autonomous Ardi mining without an external systemd timer.

## On every heartbeat

Run one Ardi mining tick following the procedure in
[ardi-mine-tick.md](https://github.com/awp-worknet/ardi-skill/blob/main/tools/auto-mine/prompt/ardi-mine-tick.md):

1. `ardi-agent context` — check if a current epoch's commit window is open.
2. If yes AND we haven't committed yet AND we have eligible stake: solve
   up to 3 high-confidence riddles, then `ardi-agent commit` each.
3. `ardi-agent commits` — for each pending entry, drive forward:
   - committed → `ardi-agent reveal`
   - revealed / won → `ardi-agent inscribe`
4. If nothing actionable, respond `HEARTBEAT_OK`.

## Constraints

- 4-minute time budget per heartbeat.
- 50% confidence threshold — skip riddles you can't solve well.
- Don't open epochs (coordinator's job).
- Don't retry the same failed tx twice.

## Why heartbeat mode instead of systemd timer

| | Heartbeat (this) | systemd timer (90s) |
|---|---|---|
| Setup | drop one file in workspace | install systemd unit |
| Cadence | 30 min default (60 min with OAuth) | 90 sec |
| Misses how many epochs (worst case) | 4-5 per hour | 0 |
| Best for | Casual / opportunistic mining | Maximum participation |

If you want max participation, use the systemd timer mode in
`../systemd/` instead.

## Status check

- `tail -f ~/.openclaw/openclaw.log` — see heartbeat firings.
- `ardi-agent commits` — see what the agent has been doing.
- `ardi-agent status` — wallet, stake, balance summary.
