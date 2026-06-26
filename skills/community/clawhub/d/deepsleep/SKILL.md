---
name: deepsleep
description: "Two-phase daily memory persistence for AI agents. v3.0: unified pack+dispatch cron, smart silence handling, memory importance tiers, cross-group correlation, OQ health tracking, and schedule priority system."
---

# DeepSleep v3.0

Two-phase daily memory persistence for AI agents.

Like humans need sleep for memory consolidation, AI agents need DeepSleep to persist context across sessions.

## What's New in v3.0

| Change | Impact |
|---|---|
| 🔴 **Unified pack+dispatch cron** | Single 23:50 job replaces two separate crons. Saves ~2-3万 token/day in cron startup overhead |
| 🔴 **Silent day fast path** | Skips history pull on silent days. Saves ~5-8万 token/day when nothing happened |
| 🔴 **Smart晨报 delivery** | Only sends morning briefs when there's real content, P0 due items, or stale OQs. Eliminates noise |
| 🟡 **Memory importance tiers** | 🔴P0/🟡P1/🟢P2 per entry. Different retention windows (7/5/3 days). Phase 3 loads P0+P1 first |
| 🟡 **Cross-group correlation** | Detects related topics across groups. "视频训练实验室 ↔ 千问微调实验室: both discussing Qwen-VL" |
| 🟡 **OQ health tracking** | Tracks age of each Open Question. ⚠️ at 7d, escalation at 14d, archive at 30d |
| 🟡 **Schedule priority + reminders** | P0/P1/P2 priorities with differentiated reminder frequency. P0 overdue = daily nag |
| 🟢 **dispatch_policy flag** | Pack sets `active`/`silent` in daily file header; dispatch reads it to decide behavior |
| 🟢 **Memory quality audit** | Weekly self-audit: compare raw conversation vs summary to catch missed info |

## When to Activate

Activate when user mentions daily summary, memory persistence, sleep cycle, cross-session memory, morning brief, or nightly pack.

## Architecture

```
23:50  cron "deepsleep" (single unified job)
         │
         ├── PACK PHASE
         │   ├── Lock date (midnight race protection)
         │   ├── sessions_list → detect active/silent
         │   │
         │   ├── [ACTIVE DAY]
         │   │   ├── sessions_history (parallel batch)
         │   │   ├── Filter + summarize with importance tiers
         │   │   ├── Cross-group correlation detection
         │   │   ├── OQ health check (age tracking)
         │   │   ├── Schedule update (priority + dedup)
         │   │   └── Write daily file (dispatch_policy: active)
         │   │
         │   ├── [SILENT DAY — fast path, <5000 tokens]
         │   │   ├── Read recent daily file
         │   │   ├── Carry-forward with decay
         │   │   └── Write daily file (dispatch_policy: silent)
         │   │
         │   └── Update MEMORY.md (P0 only, guard rails)
         │
         └── DISPATCH PHASE (same session, skip re-read)
             ├── Dedup check (dispatch-lock.md)
             ├── Smart send decision per group
             ├── Send morning briefs (active groups only)
             ├── Schedule due-date reminders
             ├── Write per-group snapshots (tiered retention)
             ├── Write dispatch log
             └── Write dispatch lock

On-demand  Phase 3: Session Memory Restore
             ├── Load memory/groups/<chat_id>.md
             ├── Priority: load 🔴P0 + 🟡P1 first
             ├── Check cross-group correlations
             └── Check schedule.md for P0 due items
```

## Phases

### Phase 1: Deep Sleep Pack (23:50)

1. **Lock date** — Prevent midnight race condition
2. **Auto-discover sessions** — `sessions_list(kinds=['group', 'main'], activeMinutes=1440)`
3. **Silent day detection** — If no real user messages, enter fast path (no history pull, <5000 tokens)
4. **Silent Day Carry-Forward with Decay** — 4-tier decay: Days 1-3 full, 4-7 slim, 8-14 minimal, 15+ archive to MEMORY.md
5. **[Active day] Pull conversation history** — Parallel batch `sessions_history`
6. **Filter and summarize with importance tiers** — 🔴P0 strategic, 🟡P1 important, 🟢P2 routine
7. **Cross-group correlation** — Detect related topics across groups
8. **OQ health check** — Track age, warn at 7d, escalate at 14d, archive at 30d
9. **Schedule update** — With P0/P1/P2 priorities, key-based dedup
10. **Write daily file** — Idempotent, with `dispatch_policy` flag and importance tiers
11. **Self-check** — Validate chat_id annotations, importance tags, OQ dates
12. **Update MEMORY.md** — Only for P0 items, with guard rails

### Phase 2: Morning Dispatch (same session, immediately after pack)

1. **Dedup check** — `dispatch-lock.md` prevents double-sending
2. **Failure recovery** — If pack somehow failed, do emergency mini-pack
3. **Read daily file** — Already in context from pack (skip re-read in unified mode)
4. **Check dispatch_policy** — `active` = send briefs; `silent` = update snapshots only
5. **Smart send decision** — Per-group: send only if new content, P0 due items, or stale OQs
6. **Send per-group briefs** — With importance-highlighted summaries, cross-group hints, OQ warnings
7. **Schedule reminders** — P0 due/overdue = 🔥 in brief; P1 due = mention; P2 = summary only
8. **Write per-group snapshots** — Tiered retention: 🔴7d, 🟡5d, 🟢3d. OQs and todos never expire
9. **Write dispatch log** — Including send/skip counts and policy
10. **Write dispatch lock**

### Phase 3: Session Memory Restore (on demand)

When the agent receives a message in a group:

1. Check `memory/groups/<chat_id>.md` — load if exists
2. **Priority loading** — If token budget is tight, load 🔴+🟡 entries first, skip 🟢
3. Check cross-group correlations — If this group has related groups, note it
4. Check `memory/schedule.md` — Any P0 items due today? Proactively mention them
5. If snapshot missing/stale (>48h) — Fall back to `memory/YYYY-MM-DD.md`

### Phase 4: Memory Quality Audit (weekly, optional)

Once a week (suggest: Sunday heartbeat or dedicated cron), self-audit pack quality:

1. Pick 2-3 random groups from the past week
2. Pull raw `sessions_history` for those groups
3. Compare raw conversation vs the daily summary that was generated
4. Check for:
   - **Missed important info** — Decisions or lessons that didn't make it into the summary
   - **Over-compression** — Context that was lost in summarization
   - **Misclassification** — Items marked P2 that should have been P1/P0
   - **OQ staleness** — Questions that resolved in conversation but weren't marked done
5. Write audit findings to `memory/audit-log.md`
6. If patterns emerge (e.g., consistently missing technical decisions), update filtering criteria in pack-instructions.md

## Daily Summary Template

```markdown
## DeepSleep Daily Summary
<!-- dispatch_policy: active|silent -->
<!-- pack_version: 3.0 -->
<!-- silent_days: N (only if silent) -->

> Auto-discovered N active groups (24h). schedule.md: [items due / none].

### [Group Name] <!-- chat:oc_abc123 -->
- 🔴 Strategic decision summary
- 🟡 Important progress
- 🟢 Routine note

### 🔗 Cross-Group Correlations (if any)
- GroupA ↔ GroupB: related topic description

### Direct Messages
- N DMs processed (no details — privacy)

### 🔮 Open Questions
- Question [since: MM-DD, pending N days]
- ⚠️ Question [since: MM-DD, pending 14 days — escalate or shelve]

### 📋 Today (Next Day)
- Action items (reader perspective)
- 🔥 P0 due: [schedule item]

### Todo
- [ ] Immediate action items
```

## Schedule File Format

File: `memory/schedule.md`

```markdown
| Key | Date | Source | Item | Priority | Status |
|-----|------|--------|------|----------|--------|
| ds-v30 | 2026-04-04 | DeepSleep实验室 | DeepSleep v3.0 验证 | P0 | pending |
```

**Priority levels:**
- **P0** — Must complete on due date. Reminded in morning brief + Phase 3. Overdue = daily nag
- **P1** — Important, mentioned in morning brief on due date
- **P2** — Low priority, noted in daily summary only

## Per-Group Snapshot Format

File: `memory/groups/<chat_id>.md`

```markdown
# [Group Name] 近期记忆
> 更新时间：YYYY-MM-DD HH:MM
> 连续静默 N 天，最后活跃：YYYY-MM-DD (only if silent)

## 最近进展
- 🔴 [YYYY-MM-DD] Strategic item (retained 7 days)
- 🟡 [YYYY-MM-DD] Important item (retained 5 days)
- 🟢 [YYYY-MM-DD] Routine item (retained 3 days)

## 🔮 Open Questions
- Question [since: MM-DD, pending N days]

## 📋 Todo
- [ ] Incomplete (never expires)
- [x] Completed (pruned after 3 days)

## 🔗 Related Groups
- ↔ [Related Group]: topic description
```

## Setup

### 1. Create unified cron job (v3.0: single job)

```bash
# v3.0: Single unified pack+dispatch job at 23:50
openclaw cron add \
  --name "deepsleep" \
  --cron "50 23 * * *" \
  --tz "Your/Timezone" \
  --session isolated \
  --message "Execute DeepSleep v3.0. Read the deepsleep skill pack-instructions.md and follow it strictly. After pack completes, continue with dispatch (pack-instructions.md Step 6)." \
  --timeout-seconds 900 \
  --no-deliver
```

**⚠️ Migration from v2.x:** If you have two separate cron jobs (deepsleep-pack and deepsleep-dispatch), remove them and create the single unified job above:
```bash
openclaw cron remove <pack-job-id>
openclaw cron remove <dispatch-job-id>
openclaw cron add ...  # the unified job above
```

### 2. Optional: Weekly audit cron

```bash
openclaw cron add \
  --name "deepsleep-audit" \
  --cron "0 10 * * 0" \
  --tz "Your/Timezone" \
  --session isolated \
  --message "Execute DeepSleep Phase 4 memory quality audit. Read deepsleep SKILL.md Phase 4 section." \
  --timeout-seconds 600 \
  --no-deliver
```

### 3. Enable cross-session visibility

```bash
openclaw config set tools.sessions.visibility all
openclaw gateway restart
```

### 4. Initialize schedule

Create `memory/schedule.md` with the table header.

### 5. Add Phase 3 restore to AGENTS.md

See Phase 3 section above for the standing order template.

## Requirements

- OpenClaw with `tools.sessions.visibility` set to `all`
- Single cron job using `agentTurn` mode (`--session isolated`) with `--timeout-seconds 900`
- `--no-deliver` on cron job (dispatch sends messages directly via message tool)

## Privacy Notes

- Pack writes a daily summary that dispatch may broadcast to groups. Never include private MEMORY.md content.
- Each group only receives its own summary — no cross-group content leakage.
- Cross-group correlations mention only the topic connection, never specific conversation content from another group.
- MEMORY.md is updated separately and stays in the main session only.
- Per-group snapshots only contain that group's own conversation summaries.
- DM content: only "N DMs processed" in daily summary; details go to MEMORY.md only.

## Known Gotchas

1. **Cron timezone**: `--tz Asia/Shanghai` means cron expression is in LOCAL time. Don't convert to UTC.
2. **Must use isolated agentTurn**: `systemEvent` ignores `timeoutSeconds` (hardcoded ~120s). Use `--session isolated`.
3. **Timeout must be generous**: 900s (15 min). Real-world unified pack+dispatch with 8 sessions takes ~3-5 min.
4. **Parallel tool calls**: Batch `sessions_history` and snapshot writes in parallel.
5. **Chat ID in headers**: Every `### GroupName` MUST have `<!-- chat:oc_xxx -->`. Missing = group loses memory.
6. **Header must be exact**: `## DeepSleep Daily Summary` — no variations.
7. **dispatch_policy flag**: Pack MUST set `<!-- dispatch_policy: active|silent -->`. Dispatch reads this.
8. **Time perspective**: Briefs use reader perspective: "yesterday did X / today do Y".
9. **Midnight race**: Lock PACK_DATE at start, never re-fetch.
10. **Dispatch dedup**: `dispatch-lock.md` written AFTER sends complete.
11. **Schedule Key dedup**: Check existing keys before writing.
12. **Silent Day Decay**: 4-tier (1-3d full / 4-7d slim / 8-14d minimal / 15+d archive).
13. **MEMORY.md guard rails**: Append/update only. Never delete/restructure.
14. **DM privacy**: Daily summary is broadcast; MEMORY.md is diary. Don't mix.
15. **Importance tiers**: 🔴P0 retained 7d in snapshots, 🟡P1 5d, 🟢P2 3d.
16. **OQ age tracking**: All OQs must have `[since: MM-DD, pending N days]` annotation.
17. **Cross-group correlations**: Only mention topic keywords, never quote another group's conversations.

## Failure Recovery

If pack fails or times out:
- **Unified mode**: Dispatch won't run (same session). Next day's unified job will detect missing summary and do emergency mini-pack for the missed day.
- **Manual recovery**: Run dispatch-instructions.md independently — it has built-in pack-failure detection and emergency mini-pack.

## Verification Checklist

```bash
# 1. Manually trigger unified job
openclaw cron run <job-id>

# 2. Check completion
openclaw cron runs --id <job-id> --limit 1
# Expected: durationMs > 120000 (proves timeout works)

# 3. Check pack output
cat memory/YYYY-MM-DD.md | grep "DeepSleep Daily Summary"
cat memory/YYYY-MM-DD.md | grep "dispatch_policy"
cat memory/YYYY-MM-DD.md | grep "pack_version: 3.0"

# 4. Check dispatch output
ls -la memory/groups/
# Expected: updated timestamps on group snapshot files

# 5. Check dispatch log
tail -20 memory/dispatch-log.md

# 6. Check Feishu groups (only active groups should receive briefs)
```

## Inspirations

Built with insights from the community: agent-sleep (multi-level sleep), memory-reflect (filtering criteria), jarvis-memory-architecture (cron inbox), memory-curator (open questions).
