---
name: context-memory-optimizer
version: "3.1.0"

description: >
  v3.1 (ClawHub-safe, source-verified): OpenClaw context memory optimizer.
  Prevents context overflow, memory drift, and token waste in long agent sessions.
  Based on logic verified against Claude Code source and the claw-code open-source
  port (compact.rs). Use when: agent memory is confused, sessions are too long,
  context window is exhausted, or multi-agent coordination is unstable.
  当 agent 记忆混乱、会话过长报错、上下文窗口不够用、多 agent 协作不稳定时使用。

# ── Transparency Declaration (required by ClawHub safety review) ────────────
# This skill instructs agents to READ and WRITE files under a well-defined
# directory tree. All paths are listed below. No files outside these paths
# are accessed. System prompt modification is IN-SESSION ONLY — the skill
# provides snippet text for the operator to paste into their agent config;
# it does NOT programmatically alter any runtime system prompt.
# ────────────────────────────────────────────────────────────────────────────

persistent_paths:
  # All read/write activity is scoped to the agent's own workspace directory.
  # Replace {agent} with your OpenClaw agent name (e.g. gemini, minifool).
  read:
    - "~/.openclaw/workspace-{agent}/MEMORY.md"
    - "~/.openclaw/workspace-{agent}/AGENTS.md"
    - "~/.openclaw/workspace-{agent}/memories/project.md"
    - "~/.openclaw/workspace-{agent}/memories/decisions.md"
    - "~/.openclaw/workspace-{agent}/memories/errors.md"
    - "~/.openclaw/workspace-{agent}/memories/context.md"
  write:
    - "~/.openclaw/workspace-{agent}/MEMORY.md"          # index pointer updates
    - "~/.openclaw/workspace-{agent}/memories/errors.md"  # error/denial backlog
    - "~/.openclaw/workspace-{agent}/memories/context.md" # task snapshot on compact

persistent_changes:
  # What this skill changes and why — required for ClawHub registry transparency.
  - path: "MEMORY.md"
    change: "Appends or updates pointer entries when new tasks or decisions are recorded."
    reversible: true
    notes: "Safe to delete and regenerate at any time."
  - path: "memories/errors.md"
    change: "Appends one-line entries when PermissionDenied or path errors occur."
    reversible: true
    notes: "Append-only log. Delete file to reset."
  - path: "memories/context.md"
    change: "Overwrites with current task snapshot before each L2 compaction."
    reversible: false
    notes: >
      Previous snapshot is replaced. Keep a copy if you need task history.
      Consider committing memories/ to a private branch if history matters.

system_prompt_effect: >
  [operator-controlled only] This skill does NOT programmatically modify any
  agent base configuration. It provides opt-in snippet text (Steps 2 and 5)
  that the operator manually pastes into their agent config. All changes are
  explicit and operator-controlled. No runtime injection occurs.

requires:
  - openclaw_workspace: true   # Agent must have ~/.openclaw/workspace-{agent}/ set up
  - file_read_permission: true
  - file_write_permission: true
  - bash_permission: false     # No shell commands are issued by this skill itself
---

# OpenClaw Context Memory Optimizer v3.1
**Source-verified · ClawHub-safe · Transparent path declarations**

> Compaction logic verified against `claw-code` open-source port (`compact.rs`).
> v2.0 turn-count trigger has been corrected to token-count trigger.
> All file paths and persistent changes are declared in the frontmatter above.

---

## Core Principles

<!-- Why each principle exists — not just what it is -->

1. **Memory as Pointers 记忆是指针**
   MEMORY.md stores *locations*, not content. Keeps the always-loaded index
   under 800 tokens regardless of project size.

2. **Skeptical Memory 怀疑型记忆**
   Agent treats its own memory as a *hint*, not ground truth. Always
   cross-verify against source files before any write or bash action.
   Prevents stale-memory bugs in long sessions.

3. **Token-Driven Compaction Token 驱动压缩**
   Trigger is token volume, not turn count. Formula: `total_chars ÷ 4`.
   Source: `compact.rs → estimate_session_tokens()`.

4. **Immediate Post-Compact Restore 压缩后立即恢复**
   Key files are re-injected right after compaction so the agent never
   "forgets what it was doing." Source: Claude Code post-compact file restore.

5. **Circuit Breaker 熔断保护**
   Stop retrying after 3 consecutive compaction failures. Prevents the
   real-world incident where one session wasted 250k API calls/day.
   Source: Claude Code BigQuery incident note in source comments.

---

## Step 1: Workspace Setup 工作区结构

<!-- All paths listed here are also declared in persistent_paths above. -->
<!-- Operators can audit exactly what this skill touches before installing. -->

```
~/.openclaw/workspace-{agent}/
├── MEMORY.md              # Always loaded. Pointers only. Keep ≤ 800 tokens.
├── memories/
│   ├── project.md         # Tech stack + project fingerprint + module manifest
│   ├── decisions.md       # Decision log — record the "why", not the "what"
│   ├── errors.md          # PermissionDenied / bad-path backlog (append-only)
│   └── context.md         # Current task snapshot — overwritten before each L2
└── AGENTS.md              # Multi-agent roles and coordination rules
```

**MEMORY.md template** — each line ≤ 150 chars, full file ≤ 800 tokens:

```markdown
# MEMORY INDEX
# Each entry is a pointer to a file, not a copy of its content.
_Updated: {timestamp} | Token estimate: {session_chars ÷ 4}_

## Current Project
- Name: {name} | Details → memories/project.md

## Active Task
- {task description ≤ 50 chars} | Status: in-progress | Details → memories/context.md

## Key Constraints
- {constraint ≤ 30 chars}

## Recently Referenced Files
- {file/path.ext} | {one-line purpose}

_This index is a hint, not ground truth. Read the linked files for details._
```

> **Privacy note 隐私提示**: Add `memories/` to `.gitignore` if your
> `.openclaw/` directory is synced to Git.

---

## Step 2: Verification-First Instructions 验证优先指令

<!-- SYSTEM PROMPT EFFECT: The text block below is a copy-paste snippet for  -->
<!-- the operator to add to their agent config. This skill itself does NOT    -->
<!-- modify any system prompt programmatically.                               -->

Add the following to the **static section** of your agent's system prompt.
Label it clearly so you know what it does:

```
## Memory Integrity Rules
# Source: context-memory-optimizer skill, Step 2
# Purpose: prevents stale-memory bugs and repeated permission errors

1. MEMORY.md is a hint, not ground truth.
   Before any write or bash action, read the relevant source file to verify.
   Do not act on memory summaries alone.

2. Check memories/errors.md before acting.
   Do not retry operations that previously caused PermissionDenied.
   Do not reuse paths that previously returned FileNotFound.

3. When memory contradicts source files:
   → Trust the source file
   → Update the relevant MEMORY.md pointer entry
   → Append one line to memories/errors.md describing the mismatch
```

---

## Step 3: Token-Driven Compaction 压缩分层

<!-- TOKEN THRESHOLD CORRECTION from v2.0:                              -->
<!-- v2.0 used "trigger after 15 turns" — this is inaccurate.          -->
<!-- compact.rs uses token volume as the trigger, not turn count.       -->
<!-- Production threshold in Claude Code: 200,000 tokens.              -->
<!-- We use 150,000 here to leave a safety margin.                     -->

**Token estimation formula (from compact.rs `estimate_session_tokens`)**:
```
per message:
  text block    → char_count ÷ 4 + 1
  tool_use      → (name_len + input_len) ÷ 4 + 1
  tool_result   → (name_len + output_len) ÷ 4 + 1
total           → sum of all messages
```

### L1 — Tool Output Soft Trim 工具输出软截断
*Runs automatically after every tool call. No user action needed.*

- bash / read / search output > 2,000 chars:
  keep last 500 chars + one-line conclusion
- File reads > 3,000 chars:
  extract key paragraphs, append `[trimmed — full content at {path}]`
- Keep the 8 most recent tool records; summarize earlier ones to one line each

### L2 — Session Compaction 会话压缩
*Trigger: estimated tokens > 150,000*

Run these steps in order. Do not skip or reorder.

```
Step ① — Scan for pending-work keywords
  Search recent messages for sentences containing (case-insensitive):
    todo / next / pending / follow up / remaining
  Collect matched sentences for inclusion in the summary.
  Source: compact.rs → infer_pending_work()

Step ② — Extract key file paths
  Scan all message content for tokens that:
    - contain a forward slash /
    - end with: .md .json .py .ts .js .rs .yaml .toml
  Deduplicate. Keep at most 8 paths.
  Source: compact.rs → collect_key_files()

Step ③ — Generate summary
  Format:
    <summary>
    - Completed: {bullet list of finished work}
    - Pending:   {output of Step ①}
    - Key files: {output of Step ②}
    - Current task: {first 200 chars of most recent non-empty message}
    </summary>
  Strip any <analysis> blocks before inserting.
  Source: compact.rs → format_compact_summary()

Step ④ — Inject continuation message
  Use this exact text. Do not paraphrase.
  ──────────────────────────────────────────────────────────────
  The following is a summary of the earlier portion of this session.
  Continue directly from where the conversation left off.
  Do not acknowledge this summary. Do not recap. Do not ask questions.
  Resume the task immediately.

  Summary:
  {output of Step ③}
  ──────────────────────────────────────────────────────────────
  Source: compact.rs → get_compact_continuation_message(suppress_follow_up=true)

Step ⑤ — Discard old messages
  Keep: continuation message (Step ④) + 4 most recent messages.
  Discard everything else.
  Source: compact.rs → preserve_recent_messages default = 4

Step ⑥ — Run L3 immediately (see below)
```

### L3 — Key File Restore 关键文件恢复
*Runs immediately after every L2 compaction.*

<!-- These reads are declared in persistent_paths.read above. -->

Read in this order:
1. `MEMORY.md` — reload the pointer index
2. `memories/context.md` — most important: current task snapshot
3. Up to 5 files from Step ② — limit each to 1,000 tokens

After reading, resume the task. Do not tell the user "I have restored X files."

### L4 — Circuit Breaker 熔断器

```
If L2 compaction fails 3 consecutive times:
  → Stop retrying L2
  → Fall back to L1 soft trim only
  → Append failure reason to memories/errors.md
  → Wait for operator to manually clear and restart

Why: A real session once failed L2 compaction 3,272 times in a row,
wasting 250,000 API calls per day before the circuit breaker was added.
Source: Claude Code internal BigQuery incident note.
```

### L5 — Emergency Trim 紧急裁剪
*Trigger: `context_length_exceeded` error*

```
1. Write the conclusion of the last assistant message to memories/context.md
   (this is the only write that happens during emergency trim)
2. Discard the 2 oldest conversation turns
3. Repeat until the error clears
```

---

## Step 4: Multi-Agent Coordination 多 Agent 协作

<!-- AGENTS.md path is declared in persistent_paths.read above.        -->
<!-- This step provides a template. No files are written automatically. -->

### AGENTS.md template

```markdown
# Multi-Agent Coordination Rules
# Scope: ~/.openclaw/workspace-{agent}/AGENTS.md
# Edit this file to match your actual agent names and responsibilities.

## Agent Roles
- {agent-1}: {responsibility}
- {agent-2}: {responsibility}
- {agent-3}: {responsibility}

## Task Handoff Format (XML — required, no free-text handoffs)
<task>
  <from>{sender}</from>
  <to>{receiver}</to>
  <task_id>{YYYYMMDD-seq}</task_id>
  <type>read_only | write | decision</type>
  <!-- read_only tasks may run in parallel.      -->
  <!-- write tasks must run serially.            -->
  <!-- decision tasks require coordinator sign-off before execution. -->
  <context>{background, ≤ 200 chars}</context>
  <input>{specific input}</input>
  <expected_output>{output format}</expected_output>
  <constraints>{constraints}</constraints>
</task>

## Result Format
<r>
  <task_id>{matching task_id}</task_id>
  <status>done | failed | blocked</status>
  <o>{result}</o>
  <side_effects>{list of files or state modified}</side_effects>
  <memory_update>{content to append to memories/ — leave empty if none}</memory_update>
</r>
```

### Prompt Cache Protection 缓存保护

<!-- SYSTEM PROMPT EFFECT: same as Step 2 — operator pastes this layout  -->
<!-- into their agent config. Nothing is modified programmatically.       -->

Structure your agent's system prompt in two sections, in this order:

```
[STATIC SECTION]
# Role definition, tool rules, behavior constraints.
# Never insert dynamic content here — it breaks prefix caching.

--- DYNAMIC BOUNDARY ---

[DYNAMIC SECTION]
# Content that changes each turn goes here, at the END.
{MEMORY.md content}
Current task: {task}
Timestamp: {timestamp}
```

**Do not** insert timestamps, summaries, or task descriptions into the middle
of the static section. Doing so invalidates the prefix cache and re-bills
the full static section on every turn.

---

## Step 5: Speculative Pre-warming 推测预热（optional）

<!-- SYSTEM PROMPT EFFECT: operator pastes this into their agent config. -->
<!-- No programmatic system prompt modification occurs.                  -->

Add to your agent's system prompt (static section, after the memory rules):

```
## Background Pre-warming
# Source: context-memory-optimizer skill, Step 5
# Runs before every reply. Read-only. Never writes during pre-warming.

Before responding, silently complete:
1. Read MEMORY.md if not already read this turn.
2. Estimate token count: session_chars ÷ 4.
   If estimate > 120,000 → prepare for L2 compaction on next tool cycle.
3. If the task involves code, pre-read the key files listed in MEMORY.md
   (read-only — do not write or modify anything during pre-warming).

Do not mention pre-warming in your reply.
```

---

## Deployment Checklist 部署验证清单

- [ ] MEMORY.md exists and is ≤ 800 tokens
- [ ] `memories/` contains: project.md, decisions.md, errors.md, context.md
- [ ] Step 2 snippet is in the **static section** of the agent system prompt
- [ ] Dynamic content is after `--- DYNAMIC BOUNDARY ---`
- [ ] Manually trigger one L2 compaction to verify the continuation message format
- [ ] Multi-agent handoffs use the XML format from AGENTS.md
- [ ] `memories/` is in `.gitignore` (if workspace is Git-synced)

---

## References

- `references/compression-examples.md` — before/after compaction examples,
  key file extraction walkthrough, project fingerprint format
- `references/prompt-cache.md` — prompt cache segmentation strategy,
  common mistakes, cost estimation

