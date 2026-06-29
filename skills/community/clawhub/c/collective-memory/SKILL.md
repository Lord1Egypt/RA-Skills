---
name: collective-memory
description: >
  Broadcast a single memory note to multiple AI-agent workspaces in one shot,
  upserting into MEMORY.md / AGENTS.md / TOOLS.md / USER.md across all targets.
  Pure file-ops, zero network, zero LLM. Works on OpenClaw, Claude Code,
  Cursor, and any agent runtime that stores per-project memory as Markdown.
  Triggers: "broadcast memory", "tell every agent", "remember this everywhere",
  "sync this to all agents", "make all my agents know", "集体记忆", "广播这条记忆",
  "你们全都记住", "所有agent记住", "大家都记一下", "让他们都记住".
---

# Collective Memory

- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/better-agent-skills
- **License**: MIT

Broadcast a single memory note to multiple agent workspaces in one shot —
idempotent upsert into `MEMORY.md`, `AGENTS.md`, `TOOLS.md`, `USER.md`, or
any Markdown file across all targets.

**Pure file-ops, zero network, zero LLM**. The calling agent decides what to
write and which key to look up; this script does the file work atomically.

---

## Execution Flow

### Step 1 — Extract the memory

From the user's request, extract three things:

- **`content`**: the full Markdown block (must include its own `##` heading line)
- **`key`**: 1–5 word lookup phrase used to find an existing heading to update
- **`file`**: which file to write into (default `MEMORY.md`)

**File routing rules:**

| Content type | Target file |
|---|---|
| Facts, rules, lessons, tool paths, APIs | `MEMORY.md` |
| Workflows, do/don't, dev conventions | `AGENTS.md` |
| Tool commands, config params, account info | `TOOLS.md` |
| Information about the user themselves | `USER.md` |

When unsure, default to `MEMORY.md`.

---

### Step 2 — Resolve agent targets (hybrid: explicit > discovery > confirm)

Pick the first strategy that yields targets:

**A. Explicit (preferred when known)**
```bash
--target /path/to/ws1:MEMORY.md \
--target /path/to/ws2:MEMORY.md
```
Or via env: `COLLECTIVE_MEMORY_TARGETS="/ws1:MEMORY.md,/ws2:MEMORY.md"`.

**B. Auto-discover** (when user says "all my agents")
```bash
--discover-under ~/.claude/projects --file MEMORY.md
--discover-under ~/.openclaw/agents --file MEMORY.md
--discover-under ~/code            --file AGENTS.md
```
Each `--discover-under <parent>` finds first-level subdirectories.

**Discovery defaults to check** (in order, stop at first non-empty):
1. `$COLLECTIVE_MEMORY_TARGETS` env
2. `~/.claude/projects/` (Claude Code)
3. `~/.openclaw/agents/` (OpenClaw)
4. CWD's immediate sibling directories
5. Ask the user

---

### Step 3 — Confirm before broadcasting (REQUIRED for ≥2 targets)

Show the plan and wait for user `y/n`:

```
About to broadcast to 3 target(s):
  • /home/me/code/proj-a → MEMORY.md
  • /home/me/code/proj-b → MEMORY.md
  • /home/me/code/proj-c → MEMORY.md

Content: [first 80 chars of content]
Lookup key: [key]

Proceed? (y/n)
```

Single target → skip confirmation, run directly.

**Sensitive content guard**: if `content` contains `token`, `password`,
`secret`, `api_key`, `private_key`, or `_token=` patterns, **always** add a
red warning line to the confirmation prompt:
> ⚠️ This memory contains apparent secrets. Broadcasting will write to every
> target. Are you sure? (y/n)

---

### Step 4 — (Optional) AI synonym pre-pass

Before invoking the script, the calling agent **may** read each target file's
existing `##` headings and decide if `key` semantically matches one of them.
If yes, replace `key` with the exact heading text to ensure precise overwrite.

The script itself does **no** AI calls — only literal heading tokenization
(English single-char + CJK 2-gram OR match).

---

### Step 5 — Execute broadcast

**Recommended multi-target form (single Python invocation):**

```bash
python3 <skill-install-path>/scripts/update_memory.py \
  --target /path/to/ws1:MEMORY.md \
  --target /path/to/ws2:MEMORY.md \
  --target /path/to/ws3:MEMORY.md \
  --key   "API key path" \
  --content "## API key path
stored in .secrets/api-keys.env (chmod 600)"
```

**Auto-discover form:**
```bash
python3 <skill-install-path>/scripts/update_memory.py \
  --discover-under ~/.claude/projects \
  --discover-under ~/.openclaw/agents \
  --file MEMORY.md \
  --key   "API key path" \
  --content "## API key path
..."
```

**Legacy single-target (backward compatible):**
```bash
python3 <skill-install-path>/scripts/update_memory.py \
  --workspace /path/to/ws --file MEMORY.md \
  --key "..." --content "..."
```

---

### Step 6 — Report results

The script prints one line per target with status: `updated` / `appended` /
`would_update` / `would_append` / `error`. With `--json`, the output is
machine-readable for downstream tooling.

```
Broadcast to 3 target(s):
  ✅ [appended] /home/me/code/proj-a → MEMORY.md
  ✅ [updated]  /home/me/code/proj-b → MEMORY.md
  ❌ [error]    /home/me/code/proj-c → MEMORY.md — workspace not found
```

Exit code `0` = all targets OK; `1` = at least one failure.

---

## CLI Reference

```
python3 update_memory.py [options]
```

| Flag | Repeatable | Description |
|------|-----------|-------------|
| `--workspace <path>` | no | Single workspace (legacy mode). Requires `--file`. |
| `--target <ws>:<file>` | yes | Explicit `workspace:filename` pair, e.g. `/proj:MEMORY.md` |
| `--discover-under <parent>` | yes | Auto-find first-level subdirs. Requires `--file`. |
| `--file <name>` | no | Default file used by `--workspace` and `--discover-under` |
| `--key <text>` | no | Required. Heading lookup key. |
| `--content <markdown>` | no | Required. Full block to upsert, must include its own `##` heading. |
| `--dry-run` | no | Preview only; no files written. |
| `--json` | no | Emit JSON result instead of human text. |

---

## Match Behaviour

- **Step 1**: tokenize `key` (English/digit runs lowercased, CJK 2+ char spans)
  → OR-match against every `##` heading in the file → if hit, replace that
  section up to the next same-or-higher level heading.
- **Step 2**: no heading matched → append to the end of the file.
- Both branches are **idempotent**: re-running the same command never produces
  duplicate sections.

---

## What This Skill Is NOT

- **Not** a real-time sync service. Each invocation is one-shot file write.
- **Not** an LLM-based merger. Tokenization is literal; if you want fuzzy
  semantic matching, do it in Step 4 (AI pre-pass) before calling the script.
- **Not** a remote-agent broadcaster by itself. For remote agents (ACP /
  HTTP / SSH), the calling agent must orchestrate transport separately and
  invoke this script on each remote machine.

---

## Dependencies

- Python 3.8+ (standard library only — no `pip install` required)

---

## Key Files

| File | Purpose |
|------|---------|
| `scripts/update_memory.py` | The upsert engine. Multi-target + dry-run + JSON. |
