---
name: cron-helper
description: "Configure, diagnose, and fix OpenClaw cron jobs. Activate when user mentions: cron, scheduled tasks, periodic jobs, timing issues, heartbeat vs cron, or any time-based automation."
---

# Cron Helper

OpenClaw cron 定时任务配置、诊断和修复。

## When to Use

- User says "配置cron", "定时任务", "周期性任务", "每天X点"
- Cron jobs not firing or not sending messages
- Discussing heartbeat vs cron
- Debugging scheduled task failures

---

## ⚠️ CRITICAL: Cron Is Stateless — Design for Persistence

**Every cron job fires in a brand-new isolated session with ZERO memory of previous runs.**

The agent has no conversation history, no memory of what it did last time, and CANNOT ask the user questions. This means:

### ❌ Broken Cron Pattern (无状态 = 无用功)

```
Prompt: "检查邮件，看看有没有重要的"

→ Agent checks email, finds nothing, outputs "没有新邮件"
→ Nothing saved. No state recorded.
→ Next run: same check, same "没有新邮件", forever identical
→ If something WAS important last run, nobody knows now
```

### ✅ Correct Cron Pattern (落盘 = 有状态 = 跨次累积)

```
Prompt: "检查未读邮件。将新邮件摘要追加到 workspace/memory/email-log.md。
        如果发现标记为紧急的邮件，立即发送通知到飞书群。
        上次检查过的邮件ID记录在 workspace/memory/email-cursor.json。"

→ Agent reads cursor to know where it left off
→ Agent checks NEW emails since cursor
→ Agent writes updated cursor
→ Agent appends summary to log
→ Next run: picks up from cursor, never re-processes
```

### Statefulness Design Rules

Every cron prompt MUST follow at least one of these patterns:

| Pattern | How | Example |
|---------|-----|---------|
| **Cursor/Checkpoint** | Read/write a pointer file tracking progress | `memory/cursor.json` with `lastCheckTime` or `lastId` |
| **Append Log** | Append results to a growing log file | `memory/email-log.md`, `memory/daily-reports/2026-05-16.md` |
| **Idempotent Check** | Compare current state vs saved baseline, only act on delta | Read `memory/last-status.json`, compare, update if changed |
| **Time-windowed** | Use current time to query only new data | `date -v-1H` to check last hour, write results to file |
| **Counter/Tracker** | Maintain a counter or running tally | `memory/consecutive-failures.txt` to trigger escalation |

### Mandatory State Checklist (写在 prompt 里)

Before writing ANY cron prompt, ensure it answers:

- [ ] **Where does this run save its results?** (file path)
- [ ] **How does the next run know what the previous run did?** (cursor/log/state file)
- [ ] **What happens if the agent can't decide something?** (must have a default action, CANNOT ask user)
- [ ] **Is the output actionable even without human follow-up?** (if not, the prompt is incomplete)

### ⚠️ Critical: Timeout Must Be ≥ 300s

**CLI 默认 timeout=30s，这对任何 real task 都太短了。每次创建 cron job 时必须显式设置 timeout。**

| 任务类型 | 推荐 timeout |
|---------|-------------|
| 简单报告（拉数据+输出） | 60-120s |
| 中等任务（读文件+分析+写文件） | 300-600s |
| 复杂任务（查多个数据源+多步分析） | 600-1200s |
| 大规模任务（处理积压数据） | 1200-1800s |

**必须在 payload 和 CLI 中同时指定：**
```bash
# CLI 用 --timeout-seconds 参数
openclaw cron add --timeout-seconds 600 ...

# payload 中也要写
"payload": { "kind": "agentTurn", "message": "...", "timeoutSeconds": 600 }
```

> **经验教训**：ceo-agent 的每日随想分析任务默认 300s，前2天跑成功了，但数据积压后持续超时4天。改为 1200s 后解决。

### Prompt Self-Sufficiency Rules

A cron prompt is a **standalone instruction to an amnesiac agent**. It must contain:

1. **Complete context** — Don't assume the agent knows anything from previous sessions
2. **Explicit file paths** — Where to read state, where to write state
3. **Decision authority** — The agent must be able to decide and act autonomously
4. **Fallback behavior** — What to do when things go wrong (not "ask the user")

**Good prompt template:**
```
执行 [任务描述]。
- 读取上次状态：[文件路径]
- 执行检查/操作：[具体步骤]
- 保存本次状态：[文件路径]
- 如果发现 [异常情况]，[自动处理方式]
- 将结果追加到 [日志路径]
```

**Bad prompt:**
```
检查一下系统状态  ← 太模糊，没有落盘，没有状态
```

---

## Cron vs Heartbeat

| | Heartbeat | Cron |
|---|-----------|------|
| **Location** | `workspace/HEARTBEAT.md` | `~/.openclaw/cron/jobs.json` |
| **Precision** | ~30 minutes | Exact to second |
| **Context** | Has conversation context | **Stateless isolated session** |
| **Best for** | Bulk checks, monitoring | Precise timing, independent tasks |

**Choose Cron** when: precise timing, self-contained task, no conversation context needed
**Choose Heartbeat** when: bulk checks across areas, needs recent conversation context

---

## Cron Job Structure

### Required Fields

```json
{
  "id": "daily-report-001",
  "agentId": "report-agent",
  "name": "每日报告",
  "enabled": true,
  "schedule": { "kind": "cron", "expr": "0 10 * * *", "tz": "Asia/Shanghai" },
  "payload": { "kind": "agentTurn", "message": "..." },
  "delivery": { "mode": "announce", "channel": "feishu", "to": "chat:oc_xxx" }
}
```

Every job MUST have: `id`, `agentId`, `name`, `enabled`, `schedule`, `payload.kind="agentTurn"`, `payload.message`, `delivery.channel`, `delivery.to`.

### Cron Expression Format

```
┌────────── minute (0-59)
│ ┌────────── hour (0-23)
│ │ ┌────────── day of month (1-31)
│ │ │ ┌────────── month (1-12)
│ │ │ │ ┌────────── day of week (0-6, Sun=0)
│ │ │ │ │
* * * * *
```

Common patterns:
- `0 10 * * *` — Daily at 10:00
- `*/5 * * * *` — Every 5 minutes
- `0 */2 * * *` — Every 2 hours
- `*/30 0-8 * * *` — Every 30min during 0:00-8:30 (night hours)
- `0 9,17 * * *` — Twice daily at 9AM and 5PM

---

## Common Fatal Errors

| # | Error | Fix |
|---|-------|-----|
| 1 | Missing `delivery.channel` + `delivery.to` | Must have BOTH: `"channel": "feishu"`, `"to": "chat:oc_xxx"` |
| 2 | `delivery.channel = "last"` | "last" is NOT valid. Use `"feishu"` or `"discord"` |
| 3 | Missing `payload.kind` | Must be `"agentTurn"` |
| 4 | Using `peer` object in delivery | Use `to` string, not `peer` object |
| 5 | Missing `schedule.tz` | Always set `"tz": "Asia/Shanghai"` |
| 6 | jq redirect overwrite (`jq '...' file > file`) | Write to temp file first, then `mv` |
| 7 | Vague prompt with no state persistence | See "Statefulness Design Rules" above |

---

## Safety: NEVER Modify Jobs Without These Steps

1. **Backup first**: `cp ~/.openclaw/cron/jobs.json ~/.openclaw/cron/jobs.json.backup-$(date +%Y%m%d-%H%M%S)`
2. **Precise matching**: Only modify EXACTLY what user asked (not all jobs)
3. **Test jq filter before applying**: Run read-only first to verify scope
4. **Write to temp file, validate, then atomic mv** (never jq redirect to same file)
5. **Validate after write**: See `scripts/validate-jobs-syntax-v2.sh`

### Precise Matching Rules

| User Says | Scope | jq Pattern |
|-----------|-------|------------|
| "你的定时任务" | Only jobs with YOUR `agentId` | `select(.agentId == "your-agent")` |
| "每日报告任务" | Jobs matching that name | `select(.name \| contains("每日报告"))` |
| "所有定时任务" | ALL jobs (user said "所有") | `.jobs[]` |
| Unclear | **ASK first** | — |

---

## Prompt Design Examples

### Example 1: Stateful Daily Report

```json
{
  "payload": {
    "kind": "agentTurn",
    "message": "生成今日学习报告。1) 读取 memory/learning-queue.json 获取待研究主题队列。2) 研究队首主题，撰写笔记保存到 learning/YYYY-MM-DD.md。3) 从队列中移除已完成主题，追加新发现到队列。4) 将报告摘要发送到飞书群。如果队列为空，主动从 trending topics 中选择一个加入队列。"
  }
}
```

### Example 2: Idempotent Health Check

```json
{
  "payload": {
    "kind": "agentTurn",
    "message": "检查服务健康状态。读取 memory/last-health-status.json 作为基线。对每个服务执行健康检查。如果状态与基线不同：更新基线文件，发送变更通知到飞书群。如果状态相同且全部正常：更新 last-check 时间戳，不发消息（避免噪音）。如果连续3次失败：发送告警并记录到 memory/alert-log.md。"
  }
}
```

### Example 3: Broken (Anti-pattern)

```json
{
  "payload": {
    "kind": "agentTurn",
    "message": "检查系统状态"
  }
}
```
**Why broken**: No state file, no decision authority, no persistence. Every run produces identical output.

---

## Diagnostic Workflow

```bash
# 1. Check gateway status
openclaw gateway status

# 2. Validate jobs.json syntax
cat ~/.openclaw/cron/jobs.json | jq .

# 3. Run validation script
~/.openclaw/skills/cron-helper/scripts/validate-jobs-syntax-v2.sh

# 4. Check gateway logs for cron errors
openclaw gateway logs | grep -i cron
```

For detailed troubleshooting, see `references/troubleshooting.md`.
For full syntax specification, see `references/syntax-guide.md`.
For validation scripts, see `scripts/`.

---

## New Job Creation Template

```json
{
  "id": "TODO-unique-id",
  "agentId": "TODO-agent-id",
  "name": "TODO-任务描述",
  "enabled": true,
  "schedule": { "kind": "cron", "expr": "TODO * * * *", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "TODO-完整自包含指令：读取[状态文件]→执行[操作]→保存[状态文件]→如果[异常]则[自动处理]",
    "timeoutSeconds": 300
  },
  "delivery": { "mode": "announce", "channel": "feishu", "to": "chat:oc_TODO" }
}
```

**Before submitting**: Run `scripts/validate-jobs-syntax-v2.sh` on the new config.
