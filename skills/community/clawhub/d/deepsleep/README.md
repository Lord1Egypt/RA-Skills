# 🧠 DeepSleep v3.0

> Like humans need sleep for memory consolidation, AI agents need DeepSleep to persist context across sessions.

Two-phase daily memory persistence for [OpenClaw](https://github.com/openclaw/openclaw) AI agents.

## What It Does

AI agents wake up fresh every session — no memory of yesterday's conversations, decisions, or context. DeepSleep fixes this with a nightly pack + dispatch cycle:

1. **Pack (23:50)** — Scans all active group chats, extracts key decisions/lessons/progress with importance tiers, detects cross-group correlations
2. **Dispatch (same session)** — Sends personalized morning briefs only to groups with real content, updates per-group memory snapshots with tiered retention
3. **Restore (on demand)** — When the agent receives a message in any group, it loads that group's memory snapshot before replying
4. **Audit (weekly)** — Self-reviews pack quality by comparing raw conversations vs summaries

The result: your agent remembers what happened yesterday, knows what's on the agenda today, and never asks you to repeat yourself.

## What's New in v3.0

- 🔴 **Unified cron** — Pack + dispatch in one job (was two). Saves token overhead + eliminates timing gaps
- 🔴 **Silent day fast path** — No history pull when nothing happened. From ~80K tokens to <5K tokens on quiet days
- 🔴 **Smart晨报** — Only sends briefs when there's real content, P0 due items, or stale OQs. No more "nothing happened" noise
- 🟡 **Memory importance tiers** — 🔴P0/🟡P1/🟢P2 per entry. Different retention (7/5/3 days). Phase 3 prioritizes P0+P1
- 🟡 **Cross-group correlation** — Detects related topics across groups for holistic context
- 🟡 **OQ health tracking** — Warns at 7 days, escalates at 14 days, archives at 30 days
- 🟡 **Schedule priorities** — P0/P1/P2 with differentiated reminder frequency. P0 overdue = daily nag
- 🟢 **Memory quality audit** — Weekly self-check catches missed info and miscategorizations
- 🟢 **dispatch_policy flag** — Pack tells dispatch whether to send or stay silent

## Architecture

```
23:50  Unified Cron → Isolated agentTurn (timeout: 900s)
         │
         ├── PACK
         │   ├── Lock date → sessions_list
         │   ├── Active? → parallel sessions_history → summarize with tiers
         │   │           → cross-group correlation → OQ health check
         │   │           → schedule update → write daily file (policy: active)
         │   │
         │   └── Silent? → fast path: carry-forward with decay
         │                → write daily file (policy: silent) [<5K tokens]
         │
         └── DISPATCH (same session)
             ├── Check dispatch_policy
             ├── active → smart send per group → tiered snapshot merge
             └── silent → snapshot timestamp update only (no messages)

On-demand  Phase 3: Restore
             └── Load snapshot → priority P0+P1 → check correlations → schedule P0 items

Weekly     Phase 4: Audit
             └── Compare raw history vs summaries → log findings
```

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) with cron support
- `tools.sessions.visibility` set to `all`
- At least one active group chat session

## Quick Start

```bash
# 1. Enable cross-session visibility
openclaw config set tools.sessions.visibility all
openclaw gateway restart

# 2. Create unified cron (23:50 local time)
openclaw cron add \
  --name "deepsleep" \
  --cron "50 23 * * *" \
  --tz "Your/Timezone" \
  --session isolated \
  --message "Execute DeepSleep v3.0. Read the deepsleep skill pack-instructions.md and follow it strictly. After pack completes, continue with dispatch (pack-instructions.md Step 6)." \
  --timeout-seconds 900 \
  --no-deliver

# 3. Optional: Weekly audit (Sunday 10:00)
openclaw cron add \
  --name "deepsleep-audit" \
  --cron "0 10 * * 0" \
  --tz "Your/Timezone" \
  --session isolated \
  --message "Execute DeepSleep Phase 4 memory quality audit. Read deepsleep SKILL.md Phase 4 section." \
  --timeout-seconds 600 \
  --no-deliver

# 4. Initialize schedule
mkdir -p memory
echo "# Schedule\n\n| Key | Date | Source | Item | Priority | Status |\n|-----|------|--------|------|----------|--------|" > memory/schedule.md

# 5. Add Phase 3 restore to AGENTS.md (see SKILL.md)
```

### Migration from v2.x

```bash
# Remove old two-cron setup
openclaw cron remove <pack-job-id>
openclaw cron remove <dispatch-job-id>

# Add unified cron (see above)
```

## File Structure

```
deepsleep/
├── SKILL.md                    # Full skill definition (OpenClaw reads this)
├── pack-instructions.md        # Phase 1+2 instructions (cron reads this)
├── dispatch-instructions.md    # Standalone dispatch (for manual/recovery use)
├── README.md                   # This file
├── chat-id-mapping.local.md    # Group name → chat_id mapping (not in git)
├── .gitignore
└── references/
    └── design.md               # Architecture & design decisions
```

## Runtime Files (generated)

```
memory/
├── YYYY-MM-DD.md              # Daily summaries with importance tiers
├── schedule.md                # Task tracking with priorities + dedup keys
├── dispatch-lock.md           # Prevents duplicate sends
├── dispatch-log.md            # Send history (rolling 30 entries)
├── audit-log.md               # Weekly quality audit findings
└── groups/
    └── <chat_id>.md           # Per-group snapshots (tiered retention)
```

## Token Economics

| Scenario | v2.1 | v3.0 |
|---|---|---|
| Active day (6 groups) | ~10万 tokens | ~8万 tokens (tiered filtering) |
| Silent day | ~8万 tokens | **<0.5万 tokens** (fast path) |
| Dispatch (active) | ~3万 tokens | **0** (same session as pack) |
| Dispatch (silent) | ~3万 tokens | **~0.2万 tokens** (snapshot update only) |

**Estimated monthly savings**: ~150万 tokens (assuming 50% silent days)

## Version History

- **v3.0** (2026-04-04): Unified cron, silent fast path, importance tiers, cross-group correlation, OQ health, schedule priorities, quality audit
- **v2.2** (2026-04-01): Silent Day Carry-Forward + Decay 4-tier system
- **v2.1** (2026-03-31): Midnight race fix, dispatch dedup, DM privacy, schedule key dedup, rolling snapshots, send logging, MEMORY.md guard rails
- **v2.0** (2026-03-29): Initial release, three-phase architecture

## License

MIT
