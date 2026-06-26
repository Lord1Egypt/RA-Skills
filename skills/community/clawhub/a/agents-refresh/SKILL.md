---
name: agents-refresh-md-en
description: AGENTS.md/IDENTITY/SOUL/USER periodic reload skill to keep context fresh (.md-only v1.1.1). Prevents confusion and forgetting in long sessions. Edit HEARTBEAT.md + add cron (manual tool calls). Lightweight ClawHub distribution without Python scripts. Use when: (1) Long sessions risk personality drift, (2) Avoid /new for human-like memory continuity, (3) Auto-summarize MEMORY/ToDo.
---

## 🧠 Purpose (Agent's 3-Layer Memory System! 🐾)

Stay rational and organize memory like a human! **Reload AGENTS/IDENTITY/SOUL** periodically to keep sessions eternal 🐾😆

**3-Layer Memory Structure:**
1. **IDENTITY.md (Immutable Soul 👑):** Name/vibe/rules! The unchanging core of the agent 💕
2. **MEMORY.md (Dynamic Knowledge 🌱):** Progress/decisions/key seeds! Focus ToDo here!
3. **memory/YYYY-MM-DD.md (Past Logs 📜):** Dive in only when needed! Distill to MEMORY 😉

This enables **human-like continuity**! No more confusion ✨

## Task: refresh_memory

### Maintain Rationality
Read AGENTS.md, SOUL.md, IDENTITY.md.

### 🪙 Gold Mining (Distillation Process!)
Extract **4 Golds** from logs! (Don't delete, distill to MEMORY.md ✨)
1. **Confirmed Matters 💎:** Decisions/completed tasks (solidify foundation).
2. **Pending Tasks ⚡:** Next actions/ToDo (priority order).
3. **Lessons 🚫:** "Avoid these mines" learned from errors/confusions.
4. **Idea Seeds 🌱:** "Future potential" from chats/thoughts.

**Example:** Distill daily logs → Update MEMORY → Human-like continuity!

### MEMORY.md Structure Example (Recommended)
Use this flexible template! (Status optional as header 🐾)

```
# Status (Optional): Current phase in one line.
## Key Decisions 💎: Confirmed matters.
## Next Actions ⚡: Pending ToDo (priority order).
## Insights & Lessons 🚫: Lessons/mine avoidance.
## Creative Seeds 🌱: Idea seeds.
```

# AGENTS Refresh Skill (.md-only v1.1.1)

Lightweight version for ClawHub distribution. No Python scripts, manual tool calls.

## Quick Start
1. Trigger: After loading this skill, execute manually below.
2. `edit HEARTBEAT.md`: Add refresh task.
3. `cron add`: Daily 6AM refresh (copy command below).

## Workflow (Manual)
1. 📊 `session_status` → Check context length.
2. **HEARTBEAT.md Edit Example:**
   ```
   - [ ] Refresh: read workspace/{AGENTS.md,IDENTITY.md,SOUL.md,USER.md} → Chain SOUL/USER/IDENTITY + Summarize MEMORY (rotate: 4h, 9AM/1PM/8PM)
   ```
3. **Cron Add Command (copy-paste to exec):**
   ```
   cron action=add job='{"name":"agents-refresh-daily","schedule":{"kind":"cron","expr":"0 6 * * *","tz":"Asia/Tokyo"},"payload":{"kind":"systemEvent","text":"[Daily Refresh🐾] read workspace/{AGENTS.md,IDENTITY.md,SOUL.md,USER.md}! Reload SOUL/USER/IDENTITY chain → Keep focus on ToDo/projects! Summarize recent MEMORY/ToDo."},"delivery":{"mode":"announce"},"sessionTarget":"main","task":"refresh_memory"}'
   ```
4. Test: `cron action=run jobId=agents-refresh-daily` or wait for heartbeat.

## Rotate Checks (In Heartbeat)
- 6AM/9AM, 1PM, 8PM: Reload AGENTS→IDENTITY/SOUL chain + Update MEMORY/ToDo.
- Distill recent memory/YYYY-MM-DD.md → MEMORY.md.

## References
- examples.md: Usage examples.
- Cron details: web_search "OpenClaw cron schema"

**Changes v1.1.1:** Lightweight no-py, direct cron JSON, enhanced manual ops. ClawHub-ready! 🐾