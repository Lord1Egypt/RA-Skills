---
name: agent-history
description: Search and read past AI coding-agent conversation history (OpenCode, Claude Code, …) via the `ochist` CLI. Use this BEFORE doing fresh research, web searches, or codebase exploration when the user references earlier work — e.g. "what did I do before", "我之前", "上次", "earlier session", "we already discussed/configured/decided", "recall", "find that command/error/decision from a previous chat". Locates prior sessions across all installed agents, greps their content, and reads full message text on demand, paging with shell tools to avoid context bloat.
license: MIT
---

## What this skill does

`ochist` exposes past conversation history from local AI coding agents
(OpenCode, Claude Code, and any other registered source) as plain,
pipe-friendly text — so you can recover earlier research, commands, errors,
and decisions instead of redoing them.

It is READ-ONLY and never modifies any data store. By default it queries
EVERY agent whose data exists on this machine; restrict with `--source`.

## When to use

Use it proactively when the user:
- Refers to earlier work: "之前/上次/我们讨论过/已经配置过", "what did we do", "recall".
- Asks to find a past command, error+fix, file change, or decision.
- Starts research you may have already done in a prior session.

Check history FIRST in these cases — it is cheaper than re-researching.

## Scope: project vs global

`sessions` and `grep` default to the **current project** — sessions whose
working directory is the current directory or a subdirectory of it. Sibling
**git worktrees** of the same repo are included automatically, so a session run
in a linked worktree still shows up from the main checkout (and vice versa).
To widen or narrow:

- `--global` / `-g` — search ALL sessions across every directory.
- `--dir <path>` — scope to a specific directory instead of the cwd.
- `--no-worktrees` — strict single-directory scope (don't expand to worktrees).

Rule of thumb: start project-scoped (more relevant, less noise); if you find
nothing, retry with `--global`.

## Golden rule: page, don't dump

Sessions can have hundreds of parts and large tool outputs. NEVER read a
whole session blindly. Narrow first, then pull only what you need:

1. **Locate** → `ochist grep <pattern>` or `ochist sessions`
2. **Orient** → `ochist meta <session>` (cheap, reliable card)
3. **Scan**   → `ochist show <session>` (one line per part)
4. **Read**   → `ochist part <part_id>` (only the parts that matter)

Pipe through `grep`, `head`, `wc -l`, `awk`, `jq` to keep output small.

## Commands

```
ochist sources
    List known agents and whether each has data on this machine.

ochist sessions [--source N] [--global|-g] [--dir PATH] [--no-worktrees] [--limit N] [--json]
    Recent sessions (current project by default; includes sibling worktrees).
    Columns: time<TAB>source<TAB>slug<TAB>id<TAB>dir<TAB>title

ochist grep <pattern> [--source N] [--global|-g] [--dir PATH] [--no-worktrees] [--session S] [--type text|tool|patch] [--limit N] [--json]
    Search across part content (current project by default).
    Output: part_id<TAB>source<TAB>slug<TAB>tag<TAB>match

ochist meta <session> [--source N] [--json]
    Reliable metadata card: tools, cost, tokens, todos, counts, time.

ochist show <session> [--source N] [--role user|assistant] [--type text|tool|patch] [--full] [--max N] [--json]
    Outline (default): #n<TAB>part_id<TAB>tag<TAB>chars<TAB>preview. --full prints content.

ochist part <part_id> [--source N] [--json]
    Full, untruncated content of a single part.
```

`--source` values: `opencode`, `claudecode`, `qoder`, `codex` (run `ochist sources` to see all).
`<session>`/`<part_id>` accept: agent id, slug/prefix, or `latest`.

## Recommended workflow (copy these patterns)

Find which session touched a topic, then read the answer:
```
ochist grep "ssh" --limit 8                          # candidates + part_id + source
ochist meta silent-star                               # confirm the right session
ochist show silent-star | grep -i "authorized_keys"   # find the exact part id
ochist part prt_xxxxx                                  # read the full message
```

Browse recent work — current project, a specific dir, or everything:
```
ochist sessions                          # current project
ochist sessions --dir ~/code/myproject   # a specific project
ochist sessions --global                 # all projects
ochist sessions --source claudecode      # one agent only
```

Skim only the assistant's conclusions:
```
ochist show latest --role assistant | head -30
```

## Tips

- `meta` fields (tools, cost, tokens, todos, counts) are 100% reliable —
  prefer them for a quick, cheap overview.
- `grep` returns one representative line + a `part_id`; follow up with
  `ochist part <part_id>` for full text.
- Subagents are folded into their parent session (not listed separately):
  OpenCode (via `parent_id`), Codex (via `parent_thread_id`), and Claude Code
  subagent output all appear inside the parent's parts, prefixed with
  `[subagent …]`. A subagent id/slug resolves to its parent.
- Use `--json | jq` for machine parsing.
- If `ochist` is not on PATH, invoke via:
  `node <repo>/dist/cli.js <args>`.
