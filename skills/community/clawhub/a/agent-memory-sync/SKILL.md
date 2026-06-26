---
name: memory-sync
description: Use when preserving, searching, reviewing, or exporting user-owned agent memory across OpenClaw, Codex, Claude, OpenCode, Hermes, Qoder, Obsidian, and Git. Inputs are local memory/chat stores and handoff summaries; outputs are Obsidian sources, memory indexes, context/profile packs, skill inventories, and optional Git sync. Prefer after native agent memory/candidate extraction. Do not use for code debugging, unrelated backups, cloud memory, or temporary notes without durable value.
version: 1.0.2
metadata:
  openclaw:
    requires:
      bins:
        - python
    skillKey: memory-sync
    homepage: https://github.com/Wildprogrammer/memory-sync-skill
    envVars:
      - name: OPENCLAW_WORKSPACE
        required: false
        description: Optional OpenClaw workspace path. Defaults to ~/.openclaw/workspace.
      - name: OBSIDIAN_VAULT_PATH
        required: false
        description: Optional Obsidian vault path. Defaults to ~/Documents/obsidian/vault.
      - name: MEMORY_SYNC_REVIEW_MODE
        required: false
        description: Optional review mode. Use agent for current-agent review or rules for deterministic fallback.
      - name: OPENCLAW_IMPORT_DISTILLED
        required: false
        description: Optional toggle for importing OpenClaw recall and dreaming candidates.
      - name: CODEX_HOME
        required: false
        description: Optional Codex home used for local conversation archive discovery.
      - name: CLAUDE_HOME
        required: false
        description: Optional Claude home used for local conversation archive discovery.
      - name: HERMES_HOME
        required: false
        description: Optional Hermes home used for state.db and skill discovery.
      - name: HERMES_STATE_DB
        required: false
        description: Optional explicit Hermes state.db path.
      - name: QODER_HOME
        required: false
        description: Optional Qoder home used for local archive discovery.
      - name: MEMORY_SYNC_PROJECT_ROOTS
        required: false
        description: Optional path-list of project roots to scan for agent rule/profile files.
      - name: MEMORY_SYNC_AGENT_KNOWLEDGE_FILES
        required: false
        description: Optional path-list of extra rule/profile files to preserve as personal agent knowledge.
      - name: MEMORY_SYNC_SKILL_DIRS
        required: false
        description: Optional path-list of extra skill directories to include in skill inventory sync.
      - name: MEMORY_SYNC_LANGUAGE
        required: false
        description: Optional output language hint such as zh or en for human-facing Markdown.
      - name: HIT_COOLDOWN_HOURS
        required: false
        description: Optional trigger-hit cooldown in hours.
      - name: S1_TTL_MIN_DAYS
        required: false
        description: Optional minimum TTL for S1 memories.
      - name: S1_TTL_MAX_DAYS
        required: false
        description: Optional maximum TTL for S1 memories.
      - name: NOISE_MIN_HITS
        required: false
        description: Optional minimum hit count before trigger-noise checks run.
      - name: NOISE_DOMINANCE_RATIO
        required: false
        description: Optional dominance ratio for single-trigger noise detection.
      - name: CONTEXT_EXPORT_ENABLED
        required: false
        description: Optional toggle for portable context export.
      - name: LEGACY_CONTEXT_ENABLED
        required: false
        description: Optional toggle for legacy _context compatibility output.
      - name: DERIVED_OUTPUTS_ENABLED
        required: false
        description: Optional toggle for rebuilding profile, context, and Markdown surfaces.
      - name: GIT_SYNC_ENABLED
        required: false
        description: Optional toggle for running git sync during autopilot.
      - name: GIT_PUSH_ENABLED
        required: false
        description: Optional toggle for pushing during git sync.
      - name: GIT_REMOTE
        required: false
        description: Optional git remote name, default origin.
      - name: GIT_BRANCH
        required: false
        description: Optional git branch override.
      - name: APPDATA
        required: false
        description: Windows system path used for local agent discovery when present.
      - name: LOCALAPPDATA
        required: false
        description: Windows system path used for local agent discovery when present.
---

# Memory Sync

Use this skill as an OpenClaw companion and multi-agent handoff layer, not a replacement for OpenClaw's own recall/promotion system. OpenClaw remains the raw memory and slow distillation engine. This skill is the fast Obsidian/Git retention and context portability layer: copy first, index quickly, ingest agent handoff summaries, strengthen by use, forget safely, import OpenClaw's distilled candidates, keep each agent's local store separate, then publish shared profile/context/permanent knowledge for portability.

## Core Model

- Treat `OPENCLAW_WORKSPACE` as read-only.
- Copy `memory/YYYY-MM-DD.md` into `Sources/openclaw/daily/` before indexing.
- Search only `.memory-sync/index/memory_index.json`.
- Generate `Dashboard/Memory Index.md` as the human-readable Obsidian entry.
- Generate `Dashboard/Memory Dashboard.md` and `Memories/` cards so Obsidian is a readable memory console, not only a file sink.
- Import OpenClaw distilled signals from `.dreams/short-term-recall.json`, `.dreams/phase-signals.json`, `memory/dreaming/rem/`, `memory/dreaming/deep/`, and promoted `MEMORY.md` entries.
- Preserve non-daily agent knowledge such as `MEMORY.md`, `USER.md`, `AGENTS.md`, and tool/config notes into `Personal/Agent Knowledge/<agent>/`.
- Detect high-value process memories such as success patterns, corrections, failure lessons, and user rules; these enter as S2 `process_memory` records.
- Ingest explicit handoff summaries from Codex, Claude, OpenClaw, OpenCode, hermes-agent, and Qoder into their own `Sources/<agent>/handoffs/` lane before indexing.
- Archive Codex Desktop/CLI, Claude Code, OpenClaw session-corpus, Hermes, and OpenCode conversation history into `Sources/<agent>/conversations/YYYY-MM-DD/` by event timestamp where available, not file directory date.
- Build `.memory-sync/index/user_profile.json` and `Dashboard/User Profile.md` from USER.md, the memory index, and local agent configuration.
- Export portable adapter context under `Context/` for Codex, Claude, OpenClaw, OpenCode, hermes-agent, and Qoder.
- Export installed skill inventory under `.memory-sync/shared/agent_skills.json`, `.memory-sync/agents/<agent>/skills.json`, and `Personal/Agent Knowledge/Agent Skills.md`.
- Treat `_context/` as a legacy compatibility output only; it is disabled by default unless `LEGACY_CONTEXT_ENABLED=true`.
- Keep readable agent source archives under `Sources/<agent>/`; keep per-agent machine stores under `.memory-sync/agents/<agent>/` with `summaries/`, `index.json`, skills inventory, and conversation day indexes.
- Keep portable shared distilled assets under `.memory-sync/shared/`, including shared memory, profile, context JSON, and adapter Markdown.
- Reject direct legacy/session sources such as `.dreams/session-corpus` and `main/sessions/*.jsonl`; when OpenClaw surfaces high-value session evidence, first curate a stable Obsidian evidence block under `Sources/openclaw/evidence/YYYY-MM-DD.md`, then index that Obsidian block.
- Remove only Obsidian daily copies, and only when no indexed memory references them.
- Commit/push only through explicit `git sync` or `GIT_SYNC_ENABLED=true` autopilot.

## Workflow

Run commands from the skill folder:

```bash
python scripts/main.py sync
python scripts/main.py review prepare
python scripts/main.py review apply decisions.json
python scripts/main.py ingest codex --project /path/to/project --note "current project handoff"
python scripts/main.py ingest codex --stdin
python scripts/main.py ingest claude --file session.md
python scripts/main.py ingest opencode "decision: ..."
python scripts/main.py conversations scan codex --date 2026-05-20
python scripts/main.py conversations scan claude --date 2026-05-13
python scripts/main.py conversations scan openclaw --date 2026-05-19
python scripts/main.py conversations scan opencode --all
python scripts/main.py conversations scan hermes-agent --date 2026-05-20
python scripts/main.py conversations scan all --date 2026-05-20
python scripts/main.py candidates
python scripts/main.py handoff openclaw
python scripts/main.py search "keyword"
python scripts/main.py diagnose "text"
python scripts/main.py trigger check "text"
python scripts/main.py trigger hit "text"
python scripts/main.py index clean
python scripts/main.py profile build
python scripts/main.py profile show
python scripts/main.py context export all
python scripts/main.py context export hermes-agent
python scripts/main.py context brief
python scripts/main.py context doctor
python scripts/main.py skills sync
python scripts/main.py git sync
python scripts/main.py status
python scripts/main.py autopilot
```

## Agent Review Mode

Default mode is `MEMORY_SYNC_REVIEW_MODE=agent`. In this mode the script does not call an external LLM API and does not silently use rule-only indexing. The current agent running this skill is the reviewer.

When the user asks to run memory sync in agent mode:

```text
1. Run `python scripts/main.py review prepare`.
2. Read the generated `.memory-sync/review/latest-pack.json`.
3. Review every candidate in that pack.
4. Write a decisions JSON file with one decision per candidate.
5. Run `python scripts/main.py review apply <decisions.json>`.
6. Run `python scripts/main.py status` and, if requested or configured, `python scripts/main.py git sync`.

`sync` and `autopilot` are not considered complete in agent review mode until the agent has applied decisions. If they only write `.memory-sync/review/latest-pack.json`, treat the run as pending review, not as a finished memory sync.
```

The script handles deterministic work: copying OpenClaw daily files into Obsidian, splitting source material, filtering obvious junk, preserving source anchors, curating high-value OpenClaw session evidence into stable Obsidian evidence blocks, validating decisions, writing JSON/Markdown surfaces, and keeping OpenClaw source files read-only.

The current agent handles judgment work: candidate selection, summary, keywords, S1-S4 rating, process-memory classification, and duplicate/merge suggestions. Treat `rule_suggestion` as a hint only. The agent decision is the source of truth in review mode.

### Conversation Archive Sources

Conversation scanning is read-only against local agent stores. Codex scans both `CODEX_HOME/sessions/**/rollout-*.jsonl` and `CODEX_HOME/archived_sessions/rollout-*.jsonl`. Claude Code scans `CLAUDE_HOME/projects/**/*.jsonl`. OpenClaw scans curated `memory/.dreams/session-corpus/*.txt` only as source evidence. Hermes reads `HERMES_STATE_DB` or `HERMES_HOME/state.db`, and may fall back to `hermes sessions export -` if the SQLite path is missing or produces no conversations. OpenCode scans through `opencode export <session-id>` first and supplements missing session/day records from read-only `opencode.db` parsing. Qoder conversation scanning remains disabled by default because the local desktop state schema is not stable; use explicit handoff or future stable export support instead.

### Candidate Quality Gate

This quality gate applies only to promotion into the memory index, memory cards, user profile, and shared context. It must not prevent raw source archiving. Keep OpenClaw daily copies, local conversation archives, handoff records, and personal knowledge files available as evidence first; then decide whether a segment deserves to become memory.

When reviewing candidates, keep only durable knowledge. A candidate should be kept only if it helps a future agent make a better decision, avoid a mistake, understand the user, continue a task, or reuse a solution.

Discard by default:

- routine heartbeat or self-check reports
- "system normal", "gateway healthy", "redis running", "no errors", "all checks passed"
- memory-sync housekeeping such as candidate counts, coverage summaries, review-pack paths, successful apply/status reports, and stage totals
- temporary test-vault paths or one-off validation locations that do not describe a reusable setup
- repeated overdue counters with no new decision, owner, deadline, or action
- transient logs, raw tool outputs, dependency install noise, and status snapshots
- same-day repetitions of an already captured topic

Keep status-like material only when it contains:

- a new failure, regression, outage, timeout, or error
- recovery from a previous failure
- a configuration, environment, dependency, credential, or path change
- a user-visible decision, correction, constraint, or preference
- a todo, owner, deadline, blocker, or next action
- a reusable lesson, command, API limit, workflow, or debugging path

A memory-sync operational record is worth keeping only when it contains a reusable failure cause, correction, recovery method, validation rule, or design decision. A successful sync count or review status by itself is not a memory.

Duplicate rule:

- Same-day same-topic candidates must be merged.
- Number-only changes such as "overdue 23 days" -> "overdue 27 days" are not new memories.
- Keep the newest useful evidence and append older source references.
- Use `merge_with` instead of creating another memory when the topic already exists.
- If the new candidate only repeats a healthy/routine status, discard it instead of merging.

Decision `reason` should name the value type or discard reason. Good keep reasons include `decision`, `lesson`, `correction`, `todo`, `state_change`, `knowledge`, and `user_rule`. Good discard reasons include `routine_status`, `memory_sync_self_log`, `temporary_test_path`, `duplicate_operational_status`, `duplicate_status`, `tool_noise`, `too_transient`, `no_future_value`, and `covered_by_existing_memory`.

### 候选记忆质量门槛

这个质量门槛只限制“候选内容是否晋升为索引记忆、记忆卡片、用户画像和共享上下文”，不阻止原始来源归档。OpenClaw daily 副本、本地对话归档、handoff 记录和个人知识文件仍应先保存为证据层，再由 agent 判断哪些片段值得成为记忆。

审核候选记忆时，只保留能帮助未来 agent 少走弯路的内容。它至少应该能帮助未来 agent 做出更好决策、避免错误、理解用户、继续任务，或复用解决方案。

默认丢弃：

- 日常心跳、自检、健康检查
- “系统正常”“Gateway 健康”“Redis 正常运行”“无错误”“检查通过”
- memory-sync 自身的候选数量、coverage、review pack 路径、apply 成功、status 汇总和阶段计数
- 只服务于一次测试的临时 vault、测试文件路径或验证目录
- 没有新决策、负责人、截止时间或行动项的重复逾期数字
- 临时日志、原始工具输出、依赖安装噪声、普通状态快照
- 同一天同主题的重复内容

只有在包含以下信息时，才保留状态类内容：

- 新失败、回归、宕机、超时或错误
- 从之前失败中恢复
- 配置、环境、依赖、凭据或路径变化
- 用户可见的决策、纠正、约束或偏好
- 待办、负责人、截止时间、阻塞点或下一步
- 可复用的教训、命令、API 限制、工作流或排障路径

memory-sync 运行记录只有在包含可复用的失败原因、纠正方法、恢复步骤、验证规则或设计决策时才值得保留。单纯“同步成功、候选多少、状态正常”不是记忆。

重复规则：

- 同一天同主题必须合并。
- “逾期 23 天”变成“逾期 27 天”这类数字变化不是新记忆。
- 保留最新且有用的证据，旧来源作为 source 追加。
- 已有同主题记忆时使用 `merge_with`，不要创建新的 memory。
- 如果新候选只是重复健康状态，直接丢弃，不要合并。

`reason` 字段必须写明保留价值或丢弃原因。保留原因可以是 `decision`、`lesson`、`correction`、`todo`、`state_change`、`knowledge`、`user_rule`。丢弃原因可以是 `routine_status`、`memory_sync_self_log`、`temporary_test_path`、`duplicate_operational_status`、`duplicate_status`、`tool_noise`、`too_transient`、`no_future_value`、`covered_by_existing_memory`。

### Codex Conversation Review Rules

Codex conversation archives often include tool calls, tool outputs, environment context, AGENTS.md blocks, subagent notifications, command logs, and temporary encoding artifacts. These are usually evidence, not standalone memories.

When reviewing Codex conversation candidates:

- Keep the source archive unchanged.
- Do not promote raw tool-call or tool-output blocks as standalone memories.
- Tool output may be used as evidence when it proves a decision, failure, fix, path, command, or verification result.
- Environment context, AGENTS.md instructions, and subagent notifications should usually be ignored unless the user explicitly changed a persistent rule or the content contains a concrete review finding.
- Encoding-damaged text should usually be discarded, but keep the candidate if the readable parts still contain a clear decision, fix, or lesson.
- Prefer one merged memory per task outcome, but keep separate memories when one task produced distinct reusable lessons.
- Progress updates are usually not memories, unless they record a verified state transition, a failed approach, or a user-facing decision.

Promote Codex candidates when they contain:

- a verified command and result pair
- a specific file, path, or config change
- a rejected approach and why it failed
- a user correction or stable preference
- a cross-agent compatibility finding
- a repeatable workflow or safety rule

### Codex 对话候选专项规则

Codex 对话归档里常包含 tool call、tool output、环境上下文、AGENTS.md 块、subagent 通知、命令日志和临时编码事故。这些通常是证据，不是独立记忆。

审核 Codex 候选时：

- 源归档保持不变。
- 不把原始工具调用或工具输出块单独晋升为记忆。
- 但 tool output 可以作为证据使用：当它证明了决策、失败、修复、路径、命令或验证结果时，应该保留其关键信息。
- environment_context、AGENTS.md instructions、subagent_notification 通常忽略；但如果用户明确修改了持久规则，或其中包含具体 review finding，可以保留。
- 编码损坏文本通常丢弃；但如果可读部分仍包含明确决策、修复或教训，可以保留。
- 同一任务倾向合并为一条结果型记忆；但如果产生多个可复用教训，可以拆成多条。
- 进度播报通常不是记忆；除非它记录了已验证的状态变化、失败路径或用户可见决策。

应该保留的 Codex 候选：

- 已验证的命令和结果
- 具体文件、路径、配置变化
- 被否定的方案和失败原因
- 用户纠正或稳定偏好
- 跨 agent 兼容性发现
- 可复用流程或安全规则

Decision output must follow this shape:

```json
{
  "decisions": [
    {
      "candidate_id": "copy from latest-pack.json",
      "keep": true,
      "title": "short stable title",
      "summary": "evidence-backed summary",
      "keywords": ["specific", "searchable", "terms"],
      "strong_keywords": ["precise", "match", "terms"],
      "stage": "S2",
      "quality_score": 0.86,
      "memory_type": "process_memory",
      "lesson_type": "correction",
      "merge_with": null,
      "reason": "why this should be kept, discarded, or merged"
    }
  ]
}
```

Every candidate in the pack must have a decision. Use `"keep": false` for discarded material. Do not invent facts outside the candidate text. Preserve `source_file` and `source_anchor` by letting the script apply decisions rather than editing the index manually.

`review apply` rejects decisions that make obvious unsupported claims, such as file paths, URLs, IDs, failure/success markers, or process-memory labels that are not grounded in the candidate evidence. If a candidate is similar to an existing memory, use `merge_with`; it can reference either an existing `memory_###` id or another candidate id from the same pack. By default merges preserve the older canonical summary and append sources; use `"replace_summary": true` only when the newer evidence is clearly better.

The pack `_meta.coverage` section reports scanned daily files, segment count, skipped count, high-value skipped count, and curated session evidence count. If `high_value_skipped` is non-zero, inspect `skipped` before applying decisions; the filter may need tuning for the user's style. The script prints both the vault-relative pack path and the absolute filesystem path.

Use `MEMORY_SYNC_REVIEW_MODE=rules` only when the user explicitly wants the deterministic fallback, wants to save agent tokens, or needs a headless/offline run.

In `rules` mode, `sync` runs:

```text
copy OpenClaw daily files to Obsidian
-> create fast S1 memories from useful daily segments
-> import OpenClaw distilled candidates
-> ingest explicit agent handoffs when requested
-> merge duplicates
-> apply TTL/downgrade/cleanup rules
-> write JSON and Markdown indexes
-> build agent-local stores
-> build shared profile/context assets
-> preserve non-daily personal knowledge
-> sync installed skill inventory
-> build Obsidian dashboard and per-memory pages
```

Both modes refresh user profile and context outputs by default when `DERIVED_OUTPUTS_ENABLED=true`. Generated profile/context/shared files are rebuilt from current evidence, not appended incrementally.

## OpenClaw Distilled Import

Prefer OpenClaw's screened candidates over summarizing chat/session content directly.

Import priority:

```text
MEMORY.md promoted entries -> S4
dreaming/deep candidates -> S3
dreaming/rem possible lasting truths -> S3
short-term-recall high-score or recalled candidates -> S2/S3
curated high-value session-corpus evidence -> S2
plain daily segments -> S1
```

Imported records may include:

```text
candidate_origin
candidate_uid
openclaw_key
openclaw_score
openclaw_confidence
openclaw_recall_count
openclaw_daily_count
openclaw_grounded_count
openclaw_light_hits
openclaw_rem_hits
openclaw_concept_tags
```

Only import a distilled candidate directly when its evidence resolves to an existing `memory/YYYY-MM-DD.md` source that can be copied into Obsidian. Session-corpus evidence is never indexed as a raw source; high-value lines are expanded with nearby context, copied into `Sources/openclaw/evidence/YYYY-MM-DD.md` with an `Original evidence` link, then reviewed like any other Obsidian-backed candidate. Do not store curated session evidence under `Sources/openclaw/daily/`, because that directory is rebuilt from daily copies.

Search is keyword-based but query-aware: Chinese natural-language queries are expanded into useful n-grams and extracted keyword hints, so a query such as `小红书攻略提分` can still match memories tagged with `小红书` and `攻略`. Search results include summary, source, original evidence pointer, and an evidence preview.

Filtering uses three layers:

- `hard_blacklist_patterns`: discard unless the text is explicitly process memory.
- `soft_blacklist_patterns`: discard routine status/log material only when no high-value signal is present.
- `high_value_patterns`: allow operational fixes, corrections, failures, successful steps, user rules, and important project context to enter the review pack even if the text contains status-like words.

## Agent Handoff Ingest

Use `ingest <agent>` when the current agent needs to hand its session state to the shared memory layer:

```bash
python scripts/main.py ingest codex --stdin
python scripts/main.py ingest claude --file session.md
python scripts/main.py ingest hermes-agent "decision: keep OpenClaw source read-only; next action: run sync"
```

Supported agents are `codex`, `claude`, `openclaw`, `opencode`, `hermes-agent`, and `qoder`.

Ingest writes the submitted summary or captured project state to `Sources/<agent>/handoffs/YYYY-MM-DD.md` under `Summary` and `Original Context` sections. The index and portable context keep a compact summary plus `source_file`/`source_anchor` back to that original record. It creates an S1/S2 `agent_ingest` candidate when the content passes filters, merges duplicates into `.memory-sync/index/memory_index.json`, then refreshes profile and `.memory-sync/shared` context outputs.

For local chat history, prefer conversation archive over `ingest <agent> --project`:

```bash
python scripts/main.py conversations scan codex --date 2026-05-20
python scripts/main.py conversations scan claude --date 2026-05-13
python scripts/main.py conversations scan openclaw --date 2026-05-19
python scripts/main.py conversations scan hermes-agent --date 2026-05-20
python scripts/main.py conversations scan all --all
```

Codex Desktop may keep a long thread in the rollout file for the day the session was created, not the day a later message was sent. The scanner therefore scans all `CODEX_HOME/sessions/**/rollout-*.jsonl` files and groups records by each event's internal timestamp. Claude Code scans `CLAUDE_HOME/projects/**/*.jsonl`. OpenClaw scans `OPENCLAW_WORKSPACE/memory/.dreams/session-corpus/YYYY-MM-DD.txt`. Hermes scans `HERMES_HOME/state.db` (`sessions` + `messages` tables); on Windows the default is `%LOCALAPPDATA%/hermes` when that directory exists. OpenCode and Qoder currently run path probes and should use explicit handoff until their local chat schemas are verified. The archive skips turn context, base instructions, developer/system prompts, and renders user/assistant messages plus compact tool-call details to `Sources/<agent>/conversations/YYYY-MM-DD/<session-id>.md`.

Conversation archive is an evidence layer, not a memory by itself. The next `review prepare` includes high-value archived conversation segments in the review pack, and only reviewed decisions can promote them into the index.

When the user asks to sync the current chat, the active agent must write an explicit handoff summary and pipe it to `ingest <agent> --stdin`. The script cannot read hidden chat history by itself. A useful handoff should include: decisions, corrected assumptions, failed attempts, successful commands or steps, files changed, user preferences or constraints, open questions, and source links back to generated files where possible.

On Windows, prefer `--file handoff.md` for Chinese or mixed-language handoffs unless the shell is explicitly configured for UTF-8. Some PowerShell pipelines can replace non-ASCII stdin with `?` before Python receives it.

Use:

```bash
python scripts/main.py candidates
python scripts/main.py candidates codex
python scripts/main.py handoff openclaw
```

`handoff <agent>` prints and refreshes the adapter context for the target agent so OpenClaw can consume Codex/Claude/OpenCode work through `Context/openclaw.md` or the printed handoff.

## Context Source Of Truth

Portable context source:

```text
Sources/<agent>/handoffs/        raw agent-submitted handoffs and project captures
Sources/<agent>/conversations/ readable local conversation archive
.memory-sync/index/memory_index.json
.memory-sync/index/user_profile.json
.memory-sync/shared/shared_memory_index.json
.memory-sync/shared/agent_context.json
Context/<agent>.md
```

`.memory-sync/shared` is the portable context layer. `_context` is retained only for old integrations and is not generated unless `LEGACY_CONTEXT_ENABLED=true`.

## Retention

- `S1`: fast preserved memory, capacity-aware TTL of 3-10 days.
- `S2`: used once or backed by a strong OpenClaw recall signal, TTL of 7-15 days.
- `S3`: used repeatedly or surfaced by OpenClaw REM/deep signals, TTL of 14-30 days.
- `S4`: permanent memory, either hit-promoted or imported from OpenClaw `MEMORY.md` promotion.

Keep the "preserve first, forget later" principle: Obsidian copies and index entries can expire; OpenClaw source files must not be modified.

High-value process memories start at S2. This includes successful procedures, user corrections, failure lessons, and explicit operating rules. These memories are treated as behavior calibration data, not ordinary chatter.

## Personal Knowledge And Skill Inventory

Every sync refreshes personal knowledge outputs:

```text
Personal/Agent Knowledge/openclaw/MEMORY.md
Personal/Agent Knowledge/openclaw/USER.md
Personal/Agent Knowledge/openclaw/AGENTS.md
Personal/Agent Knowledge/openclaw/TOOLS.md
Personal/Agent Knowledge/codex/AGENTS.md
Personal/Agent Knowledge/codex/config.toml
Personal/Agent Knowledge/claude/CLAUDE.md
Personal/Agent Knowledge/opencode/AGENTS.md
Personal/Agent Knowledge/hermes-agent/AGENTS.md
Personal/Agent Knowledge/Agent Skills.md
Personal/Agent Knowledge/<agent>/Agent Skills.md
```

Skill inventory outputs:

```text
.memory-sync/shared/agent_skills.json
.memory-sync/agents/<agent>/skills.json
Personal/Agent Knowledge/<agent>/Agent Skills.md
Dashboard/Agent Skills.md
Personal/Agent Knowledge/Agent Skills.md
Personal/Agent Knowledge/<agent>/Agent Skills.md
```

`Dashboard/Agent Skills.md` is the Obsidian navigation entry. `Personal/Agent Knowledge/Agent Skills.md` is the personal navigation entry. The detailed human-readable inventory is split by agent under `Personal/Agent Knowledge/<agent>/Agent Skills.md`, while `.memory-sync/agents/<agent>/skills.json` remains the machine-readable per-agent store.

The skill inventory records skill name, function summary, agent, level/source directory, local path, modified time, hash, enabled state, and frontmatter validity. OpenClaw is scanned across official npm, workspace, and user skill directories so multi-level installations are not missed. Hermes is scanned from `HERMES_HOME/skills` and `%LOCALAPPDATA%/hermes/skills` on Windows. Markdown output language is inferred from the user's local profile/rules, or can be forced with `MEMORY_SYNC_LANGUAGE=zh` or `MEMORY_SYNC_LANGUAGE=en`.

### Agent Skill Routing Index

`skills sync` must generate `Personal/Agent Knowledge/<agent>/Agent Skills.md` as an Agent Skill routing index, not a flat name list. It helps the caller pick Skills by task category first, then compare candidate fit and exclusion rules inside one category entry. It does not replace each Skill's own `SKILL.md`; the final selected Skill must still be read before execution.

The per-agent source of truth for routing metadata is `.memory-sync/agents/<agent>/skills.json`. The Markdown page is generated from that JSON and must contain these sections in order: `快速路由`, `分类匹配指南`, `冲突处理规则`, `完整 Skill 清单`, and `质量问题`.

Route records should include `identity`, `primary_category`, `related_categories`, `use_when`, `avoid_when`, `specificity`, `routing_status`, `routing_confidence`, `routing_source`, and `routing_reviewed_sha256`. Preserve confirmed routing when the Skill `sha256` has not changed. Mark newly discovered Skills as `pending_review`; mark changed, disabled, weakly described, or invalid-frontmatter Skills as `needs_review`.

Agent post-processing is optional and should be targeted. Review only `pending_review`, `needs_review`, or low-confidence entries, read the target Skill's full `SKILL.md`, then update both `.memory-sync/agents/<agent>/skills.json` and the generated Markdown. Do not rewrite confirmed unchanged entries. Do not invent exclusion rules; leave `avoid_when` empty when the Skill does not state a boundary. Add a new category only when existing stable categories cannot fit and the new category has reusable value beyond a single Skill.

## Trigger Logic

- Trigger words do not make the skill auto-run by themselves. `trigger check` and `trigger hit` are diagnostic/reinforcement commands after an agent or user has already decided to query memory-sync.
- `trigger check` is read-only.
- `trigger hit` is the only command that updates hit counters.
- Enforce one effective hit per memory per 24 hours.
- Treat trigger words as activation signals only.
- Require strong keyword evidence for a match.
- Detect noisy single-trigger reinforcement and downgrade or remove weak memories.

To make an agent automatically query this memory layer when the user mentions memory-related words, install an agent rule in that agent's own persistent rule file. Do not assume every agent uses OpenClaw's rule structure.

Recommended rule entry points:

| Agent | Rule entry point |
| --- | --- |
| OpenClaw | Workspace `AGENTS.md`, or the skill/workspace rule file that OpenClaw loads for the session |
| Codex | Project `AGENTS.md`, or user-level `~/.codex/AGENTS.md` |
| Claude Code | Project `CLAUDE.md`, project `.claude/CLAUDE.md`, or user-level `~/.claude/CLAUDE.md` |
| OpenCode | Project `AGENTS.md`, user-level `~/.config/opencode/AGENTS.md`, or `CLAUDE.md` when using Claude-compatible instructions |
| hermes-agent | Its configured system prompt/rule file; if there is no persistent rule file, provide `Context/hermes-agent.md` as the handoff contract |

OpenClaw example:

````markdown
### 记忆触发词自动检索

当用户消息中包含以下触发词时，除了内置 `memory_search` 外，必须同时执行 memory-sync 的 search 命令。

触发词：记得、记忆、回忆、上次、之前、以前、曾经、历史、背景、上下文、仔细想想、想起来、记录、复盘、经验、remember、memory、recall、previous、last time、context

执行命令：

```bash
python <path-to-memory-sync>/scripts/main.py search "关键词"
```

流程：

1. 内置 `memory_search` 搜 OpenClaw 工作区。
2. memory-sync `search` 搜 Obsidian 索引。
3. 合并两个结果再回答。
````

Generic non-OpenClaw rule template:

````markdown
### Memory-Sync Automatic Retrieval

When the user asks about memory, previous context, background, history, lessons, or prior decisions, query memory-sync before answering.

Trigger words: 记得、记忆、回忆、上次、之前、以前、曾经、历史、背景、上下文、仔细想想、想起来、记录、复盘、经验、remember、memory、recall、previous、last time、context

Command:

```bash
python /path/to/memory-sync/scripts/main.py search "keyword phrase"
```

Process:

1. Use the agent's built-in memory/context search if it has one.
2. Run memory-sync `search` against the Obsidian index.
3. Merge the results, cite uncertainty, and answer from the combined evidence.
````

Use the user's actual keyword phrase as the query, not the whole chat transcript. If the memory-sync command fails, tell the user the failure and continue with the agent's built-in memory/context results when available.

## Configuration

User-adjustable rules live in:

```text
config/filters.json
config/keywords.json
config/triggers.json
```

Execution mode is controlled by:

```text
MEMORY_SYNC_REVIEW_MODE=agent  # default
MEMORY_SYNC_REVIEW_MODE=rules  # deterministic fallback
```

- `MEMORY_SYNC_PROJECT_ROOTS`: optional path-list of project roots to scan for project-level `AGENTS.md`, `CLAUDE.md`, and `.claude/CLAUDE.md`.
- `MEMORY_SYNC_AGENT_KNOWLEDGE_FILES`: optional path-list of extra rule/profile files to copy into `Personal/Agent Knowledge/custom/` and use as profile evidence.
- `filters.json`: minimum segment length, source blacklist, text blacklist, and OpenClaw import thresholds.
- `keywords.json`: generic words, broad context words, domain phrases, blocked keyword patterns, and `strong_keyword_allowlist`.
- `triggers.json`: words that activate memory checks.

Keyword extraction should favor project names, code terms, and configured domain phrases. Profile/context generation filters low-signal labels such as pronouns, generic file names, broad tech words, and trigger words so they do not become glossary or active-project claims.

Use `diagnose` before changing rules:

```bash
python scripts/main.py diagnose "remember Feishu chat_id WebSocket AutoTestPlatform"
```

## User Profile And Agent Context

Use:

```bash
python scripts/main.py profile build
python scripts/main.py context export all
python scripts/main.py context export qoder
```

Profile outputs:

```text
.memory-sync/index/user_profile.json
Dashboard/User Profile.md
```

Portable context outputs:

```text
.memory-sync/shared/agent_context.json
Context/agent_brief.md
Context/codex.md
Context/claude.md
Context/openclaw.md
Context/opencode.md
Context/hermes-agent.md
```

Each adapter context includes a memory retrieval contract that points to that agent's own rule entry point. OpenClaw uses `AGENTS.md`; Codex uses `AGENTS.md`; Claude Code uses `CLAUDE.md`; OpenCode uses `AGENTS.md` or Claude-compatible rules; hermes-agent uses its configured rule/system prompt or `Context/hermes-agent.md` as a handoff contract. OpenClaw and hermes-agent also include stricter operating contracts for rule reading, conflict reporting, and source-memory safety.

Agent-local outputs:

```text
Sources/openclaw/daily/
Sources/openclaw/summaries/
.memory-sync/agents/openclaw/index.json
.memory-sync/agents/codex/index.json
.memory-sync/agents/claude/index.json
.memory-sync/agents/opencode/index.json
.memory-sync/agents/hermes-agent/index.json
```

Shared portable outputs:

```text
.memory-sync/shared/shared_memory_index.json
.memory-sync/shared/user_profile.json
.memory-sync/shared/agent_context.json
Context/*.md
```

Obsidian-readable outputs:

```text
Dashboard/Memory Dashboard.md
Dashboard/Memory Directory.md
Memories/memory_001.md
Memories/memory_002.md
```

Memory page file names are stable and ID-only (`memory_001.md`) so Obsidian, Git, and cross-platform sync do not break on long titles, punctuation, emoji, or renamed summaries. Each memory page includes YAML frontmatter, tags, source-agent metadata, wikilinks to the source daily copy, and links back to the index/profile. Shared context uses a stricter snapshot than the full index: S1 memories remain searchable in Obsidian but do not enter adapter context until OpenClaw distills them, the user reinforces them, or they reach a stronger stage.

The profile is evidence-backed. USER.md and explicit agent configuration get higher weight; S3/S4 and hit-promoted memories get strong weight; S1/S2 provide weaker recent context. Do not treat profile claims as truth unless they have evidence references.

Use `context doctor` to check whether the profile/context pack is missing major signals or stale.

## Human-Readable Notes And Directory

Keep this simple. Do not create a separate metadata system for explanatory text.

When the skill or the current agent creates a new human-facing Markdown file, add one short explanatory blockquote below the title in the current user's language. Use `MEMORY_SYNC_LANGUAGE` when it is set; otherwise infer the language from USER.md, AGENTS.md, the existing profile, or the user's current conversation language.

Add the note to generated or agent-created navigation and summary files, such as:

```text
Dashboard/*.md
Memories/memory_*.md
Context/*.md
Personal/Agent Knowledge/**/*.md
Sources/<agent>/conversation-summaries/**/*.md
Sources/<agent>/handoffs/**/*.md
```

Do not inject explanatory text into raw evidence copies where it can break anchors or alter the source record:

```text
Sources/<agent>/daily/**/*.md
Sources/<agent>/conversations/**/*.md
.memory-sync/**/*.json
```

Preferred Chinese note style:

```markdown
> 文件说明：这是 Memory Sync 自动生成的记忆目录，用于在 Obsidian 中通过正向链接跳转到索引、记忆卡片、来源归档和个人知识页。
```

Preferred English note style:

```markdown
> File note: this Memory Sync page links the index, memory pages, source archives, and personal knowledge pages for Obsidian navigation.
```

Maintain `Dashboard/Memory Directory.md` as the Obsidian navigation directory. Keep these sections: Core Entries, Memory Pages, Cross-Agent Context, and Personal Knowledge. Keep the style consistent: use forward wikilinks for every navigation item and link to meaningful entry files, not placeholder README files or arbitrary first files. Memory Pages should link to `Dashboard/Memory Index.md` and `Dashboard/Memory Dashboard.md`. Cross-Agent Context should link to `Context/agent_brief.md` only, not `Context/README.md` or agent-specific files. Do not include Source Archives in `Dashboard/Memory Directory.md`; source files remain traceable through memory indexes and source links. Do not expose hidden machine-state folders as human navigation entries. Clean up only Memory Sync generated README placeholders whose content contains the Memory Directory parent link and the generated directory-entry wording; do not delete user-authored README files. Do not generate personal usage manuals as fixed skill outputs; personal notes can live in `Personal/` but are outside the skill's generated surfaces. The directory is a navigation surface, not the source of truth; the machine source of truth remains `.memory-sync/index/memory_index.json`.

## Git Version Management

Use:

```bash
python scripts/main.py git sync
```

The command stages `.memory-sync/index/memory_index.json`, `Dashboard/Memory Index.md`, `Sources/`, `Memories/`, `Context/`, and `.memory-sync/shared/`, then commits and pushes from the Obsidian vault repository.

## Conversation Archive

Conversation scan also writes a readable transcript under `Sources/<agent>/conversation-summaries/YYYY-MM-DD/<session-id>.md`. The full archive remains under `Sources/<agent>/conversations/` as evidence, while memory pages link to the readable transcript for Obsidian review.
