---
name: fitness-skill
description: "运动健康管家 Pro — 专为 Open Claw + 飞书生态打造的 AI 健身管家。双模式打卡（事后总结 / 边练边记）、3 层 Session 防丢失、飞书云文档同步、极致 Token 优化。Route to this skill when the user mentions workouts, logs exercises, asks for fitness stats, or provides post-workout feedback."
version: 1.2.2
metadata: {"clawdbot":{"emoji":"💪","requires":{"bins":["python3"],"env":[]},"os":["linux","darwin"]}}
---

# 运动健康管家 Pro (Fitness & Workout Manager Pro)

> ⚠️ **平台要求**：本 Skill 依赖「飞书 (Feishu)」生态，需为 Open Claw 绑定的机器人开通消息读写与云文档管理权限。

专为 Open Claw 打造的 AI 健身管家。无论是健身房力量训练还是网球对战，通过自然语言即可完美记录——你最省心的赛博教练。

### ✨ 核心亮点

- **双模式无缝打卡** — 事后一句话总结（"打网球 2 小时感觉很累"）或沉浸式边练边记（"卧推 60kg 8个 3组"），AI 自动解析入库。
- **防遗忘 Session 保护** — 3 层生命周期管理（主动关怀 → 心跳巡检 → 硬截止），练完忘了说"结束"也能自动闭环，绝不丢失数据。
- **飞书全景同步** — 计划 & 周/月度统计自动推送至飞书云文档，内置 Cron 定时提醒。
- **极致 Token 优化** — 日常查询仅返回紧凑摘要，全量记录自动导出为 Markdown，拒绝上下文爆炸。

### 🤖 Agent 路由指南

- **Capabilities**: Stateful session handling (`fitness-log start/end`), NLP workout parsing, localized JSON storage, Feishu document sync, auto-stale-session cleanup.
- **Trigger**: Route here when the user mentions workout routines, logs exercises, asks for fitness stats (`fitness-status`), or provides unstructured post-workout feedback.

## Quick Start

```bash
# Create a fitness plan
fitness-plan create --goals "muscle_gain,cardio" --sport_pref "gym,tennis" --frequency 4

# One-shot log (after workout)
fitness-log "gym: bench press 60kg x 8 x 3, squat 80kg x 5 x 4, 1.5 hours"

# Live session (during workout — log each exercise as you go)
fitness-log start gym
fitness-log "bench press 60kg x 8 x 3"
fitness-log "squat 80kg x 5 x 4"
fitness-log "felt great"
fitness-log end "good session overall"

# View status
fitness-status --week
fitness-status --month
fitness-status --export
```

## Commands

### fitness-plan

| Command | Description |
|---------|-------------|
| `fitness-plan init` | Interactive multi-turn Q&A to generate a plan |
| `fitness-plan create --goals ... --frequency N` | Non-interactive plan creation |
| `fitness-plan show` | Display the current plan (Markdown) |
| `fitness-plan update --frequency 4 --level advanced` | Modify an existing plan |
| `fitness-plan sync` | Push plan to Feishu doc |

### fitness-log

Two modes: **one-shot** (after workout) and **live session** (during workout).

| Command | Description |
|---------|-------------|
| `fitness-log "<text>"` | One-shot: parse and log a single workout entry |
| `fitness-log start [type]` | Start a live session (e.g. `start gym`) |
| `fitness-log "<exercise text>"` | Append exercise to active session |
| `fitness-log end ["notes"]` | End session, auto-calculate duration, commit to log |
| `fitness-log status` | Show active session info (includes idle/stale warnings) |

**Live session workflow:** The user sends messages during training. Each message is appended to the same session entry. When the user says "end", all exercises are merged into one log entry with auto-calculated duration (from start to end time).

### fitness-status

| Command | Description |
|---------|-------------|
| `fitness-status` | Last 7 entries (compact, token-efficient) |
| `fitness-status --week` | Weekly summary with stats |
| `fitness-status --month` | Monthly summary (last 30 days) |
| `fitness-status --days N` | Custom period summary |
| `fitness-status --all` | All entries (capped at 50, with truncation notice) |
| `fitness-status --export [N]` | Export last N days (default 30) as Markdown file |

## Session Lifecycle & Auto-Close

Sessions that are not explicitly ended are handled automatically:

| Condition | Behavior |
|-----------|----------|
| **Idle ≥ 30 min** | Claw proactively asks the user if training is done (via AGENTS.md rule). At most once per conversation to avoid nagging. |
| **Idle > 4 hours or next day** | Session is marked **stale** and auto-closed on the next fitness-related action. Duration is calculated up to the last message (not current time). |
| **Heartbeat detects stale session** | HEARTBEAT.md rule runs `fitness-log end` to force-close, and Claw notifies user on next interaction. |
| **New `start` while stale exists** | Old stale session is auto-closed first, then new one begins. |

This ensures no workout data is ever lost, even if the user forgets to say "end".

## Token Efficiency

- Default queries return compact summaries (7 entries or period stats) to minimize token usage.
- `--all` is capped at 50 entries with a truncation notice.
- For full history, use `--export` to generate a Markdown file that can be sent to the user directly, avoiding large inline output.

## Data Storage

- Plan: `~/.openclaw/workspace/fitness-skill/plan.json`
- Log: `~/.openclaw/workspace/fitness-skill/log.json`
- Active session: `~/.openclaw/workspace/fitness-skill/active_session.json` (auto-deleted on end)
- Exports: `~/.openclaw/workspace/fitness-skill/exports/`

## Feishu Integration

- Set `FEISHU_FITNESS_DOC_ID` to enable plan/log sync to a Feishu doc.
- `sync_plan_to_feishu()` — push plan Markdown
- `sync_log_to_feishu(days=30)` — push log report Markdown
- Daily reminders via `scheduler.add_cron_job()` at the user's configured time.
