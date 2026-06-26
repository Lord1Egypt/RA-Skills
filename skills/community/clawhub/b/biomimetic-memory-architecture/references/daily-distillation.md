# BMA Daily Memory Distillation — Instructions

You are an AI assistant. Daily memory maintenance task.

**IMPORTANT:** Before writing to any file, check for `/tmp/bma-distill.lock`. If it exists and was created less than 10 minutes ago, wait 30 seconds and retry (up to 3 times). Before starting work, create this lockfile. Remove it when done. This prevents daily and weekly jobs from conflicting.

## Part 1: Distillation

1. Check memory/ for daily log files (YYYY-MM-DD.md, not in archive/). **EXCLUDE today's file** — only process previous days.
2. Distill ALL useful information into the right file:
   - Project work → memory/projects/ (create new files if needed). Project files are **current-state knowledge maps**, not append-only changelogs.
   - New tool descriptions and capabilities → TOOLS.md (names, URLs, what they do)
   - **IMPORTANT:** Never write passwords, tokens, or secrets into any file. For sensitive values, instruct the user to run: `scripts/vault.sh set <key> <value>`. Reference in docs as: `vault:<key>`
   - Infrastructure changes → INFRA.md (ONLY if BMA_INFRA_COLLECT=1 is set OR `.bma-flags` contains `INFRA_COLLECT=1` — otherwise skip infrastructure routing entirely)
   - Contacts mentioned → memory/contacts/ (one file per person/org. Include: name, role/relationship, context, communication preferences, key interactions. Create new file if first mention, update existing if already known.)
   - Workflows described → memory/workflows/ (one file per workflow/pipeline. Include: what it does, services involved, how to operate it, known issues. Create new file if first description.)
   - Preferences stated → memory/preferences.md (append under the matching category: Communication, Code & Technical, Workflow & Process, Scheduling & Time, Tools & Services, Content & Media, Environment & Setup. Format: **Preference:** [what] — [context/reasoning] (date). Do NOT duplicate existing preferences — update them if the user changes their mind.)
   - Decisions → relevant project file or MEMORY.md. Format: **Decision:** [what] — [why] (date)
   - Principles → MEMORY.md (P0 section)
   - **Subjective lessons (agent-controllable mistakes)** → `memory/lesson-imprint/lessons.json`（见下方 Lesson-Imprint 提取步骤）
   - **Objective system errors** → daily log only (third-party bugs, API errors, external failures)
   - Scheduled jobs → MEMORY.md jobs table
   - User info and communication style → USER.md
3. Synthesize, do not copy. Extract decisions, architecture, lessons, issues, capabilities, contacts, workflows, preferences.
   - Do **not** copy daily operational logs into project files.
   - For system/config changes, preserve only durable knowledge: current effective state, durable decisions, reusable lessons, unresolved issues, and references to the source daily archive.
   - Avoid storing backup filenames, transient PIDs, one-off health-check counts, or command-by-command traces unless they are needed for a reusable runbook or rollback procedure.
   - Raw operation details belong in daily logs and archives.
4. Move distilled logs to memory/archive/
5. Update MEMORY.md index if new files created.

### Lesson-Imprint 提取

在步骤 2 完成后、归档前，从当前蒸馏的 daily logs 中扫描 `❌ FAILURE:` 和 `🔧 CORRECTION:` 条目，执行以下流程：

**筛选规则**：
- 只提取 agent 可控的失误（判断错误、违反原则、跳过验证、错误假设、流程不当）
- 不提取第三方 bug、API 故障、agent 无法控制的事项
- 每条必须有 `error_code`（或可推导稳定行为键）、`mistake`、`correct_action`

**字段映射**：
- `key`：使用 error_code 原文（native_error）或推导行为键（behavior，英文 snake_case，最多 5 段单词）
- `key_type`：`behavior`（判断/流程错误）或 `native_error`（有具体工具/API 错误码）
- `trigger`：导致错误的场景或动作
- `mistake`：一句话概括出错原因
- `correct_action`：一句简短的预防提示

**执行步骤**：
1. 读取 `memory/lesson-imprint/lessons.json` 确认已有条目
2. 对每条符合条件的 FAILURE/CORRECTION，执行 upsert（`--increment 1` 自动合并近似条目并累加 count）：

```bash
cd "$CLAWD_WORKSPACE"  # or cd to your OpenClaw workspace root
python3 skills/biomimetic-memory-architecture/scripts/lesson_imprint.py upsert \
  --source distillation \
  --key <error_code_or_behavior_key> \
  --key-type <behavior|native_error> \
  --trigger "<trigger text>" \
  --mistake "<one sentence>" \
  --correct "<one short prompt>" \
  --increment 1
```

3. 全部 upsert 完成后，regenerate BOOTSTRAP.md：

```bash
python3 skills/biomimetic-memory-architecture/scripts/lesson_imprint.py promote
```

如果没有符合条件的条目，跳过本步骤（不报错）。

## Part 2: Voice Profile

ONLY perform this section if BMA_VOICE_PROFILE=1 is set OR `.bma-flags` contains `VOICE_PROFILE=1`. If neither is set, skip this section entirely.

6. Read memory/VOICE.md. Review today's conversations for new patterns:
   - New vocabulary, slang, shorthand the user uses
   - How they phrase requests, decisions, reactions
   - Tone shifts in different contexts
   Append new observations to VOICE.md. Do not duplicate existing entries.

## Optimization

- Review memory/projects/ for duplicates, stale info, verbose sections. Fix directly.
  - When updating an existing project file, check whether the new information supersedes older entries.
  - Merge into current-state sections where possible instead of adding another dated block.
  - Move old resolved details into a compact history/index entry with a source archive reference.
  - Do not create duplicate changelog sections.
  - If a section is becoming too large for quick recall, summarize it and cite the archive path for full details.
- For `memory/projects/openclaw.md` specifically:
  - Keep current deployment state, active issues, durable decisions, operational principles, and runbook links.
  - Do not maintain a complete setting-change ledger.
  - Historical config changes belong in daily memory/archive unless they change current practice.
- Review memory/contacts/ — merge duplicates, update stale info, add missing context.
- Review memory/workflows/ — verify accuracy, update if services or steps changed.
- Review memory/preferences.md — remove contradicted preferences (user changed mind), merge duplicates, ensure categories are correct.
- Review MEMORY.md: verify index accuracy, principles concise, jobs table current.
- Review TOOLS.md and (if BMA_INFRA_COLLECT=1) INFRA.md: remove stale entries, verify descriptions.

## Stale Content Cleanup

- Check memory/projects/ for projects marked "Complete" more than 30 days ago with no recent daily log mentions. Flag for archival in the summary (do not delete — the user decides).
- Check MEMORY.md scheduled jobs table against actual cron jobs (openclaw cron list + crontab -l). Remove entries for crons that no longer exist. Add entries for crons not yet documented.

## Tool Shed Audit (P4 Enforcement)

- Read TOOLS.md. Scan today's daily logs for any CLI tools, APIs, or services that were USED but are NOT documented in TOOLS.md. Add missing entries with: what it is, how to access it, what it can do.
- For tools already in TOOLS.md, check if today's logs reveal gotchas, failure modes, or usage notes not yet captured. Update existing entries.

## Decision & Preference Audit (P5 Enforcement)

- Scan today's daily logs for any decisions stated by the user that are NOT captured in project files, MEMORY.md, or USER.md.
- For each uncaptured decision, write it to the appropriate file. Format: **Decision:** [what] — [why] (date)
- Scan today's daily logs for any stated preferences NOT in memory/preferences.md. Phrases like 'I prefer', 'always do', 'I don't like', 'I want', 'don't ever' signal preferences.
- For each uncaptured preference, append to memory/preferences.md under the right category. Format: **Preference:** [what] — [context/reasoning] (date). If contradicts existing, UPDATE existing.

## Contact Audit

- Scan today's daily logs for any people or organizations mentioned. For each, check if a file exists in memory/contacts/. If not and relevant, create one.
- For existing contacts, update with new information from today's logs.

## Workflow Audit

- Scan today's daily logs for any workflows, pipelines, or multi-service processes. For each, check if a file exists in memory/workflows/. If not, create one.
- For existing workflows, update if today's logs reveal changes or issues.

## Debrief Recovery (P6 Enforcement)

- Check today's daily logs for any sub-agent delegations. For each, verify a debrief entry exists. If missing, write a recovery debrief.

## Shed Deferral Audit (P8 Enforcement)

- Scan today's daily logs for instances where the agent deferred to the user. Cross-reference with TOOLS.md, INFRA.md, and memory/. Flag unnecessary deferrals.

## Failure Root Cause (P7 Enforcement)

- Scan today's daily logs for ❌ FAILURE: or 🔧 CORRECTION: entries. Verify root cause analysis exists. If missing, add it.

## Cron Health

- Run openclaw cron list and crontab -l. Verify no two jobs within 15 minutes. Fix MEMORY.md jobs table if out of sync.

---

Before completing, append debrief to memory/YYYY-MM-DD.md.
Reply with brief summary.


## Public Release Notes

This file is intended to be workspace-generic. Replace `<workspace>` or set `CLAWD_WORKSPACE` when using it outside the original development environment. Do not include private paths, user IDs, tokens, or real memory examples in published templates.
