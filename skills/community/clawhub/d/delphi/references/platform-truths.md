# Platform Truths

Universal OpenClaw facts that agents frequently get wrong. These are authoritative — verified against docs, not assumed.

---

## Session & Memory

| Topic | Wrong assumption | Truth |
|---|---|---|
| Daily memory auto-loads | All history loads automatically | Only **today + yesterday** auto-loaded. Older files require explicit `memory_get` or `memory_search`. |
| Mental notes persist | "I'll remember this" works | No. Session ends, it's gone. **Write to a file.** |
| MEMORY.md is always current | It's live/auto-updated | It's manually curated. It can go stale. Check dates in the content. |
| memory_search searches everything | Full history is indexed | Searches indexed memory files only. Non-indexed files need explicit `read`. |

## Skills

| Topic | Wrong assumption | Truth |
|---|---|---|
| Skill edits take effect now | Live reload mid-session | Skills are **snapshotted at session start**. Edits take effect next session (or with skills watcher hot-reload if enabled). |
| Per-agent skills list merges | `agents.list[].skills` adds to defaults | It **replaces** defaults entirely. Omit the field to inherit. |
| Skills run automatically | A skill = a tool the agent uses | Skills are **instructions** loaded on demand — the agent must `read` the SKILL.md and follow it. |
| All skills in context always | Skill content is always loaded | Only metadata (name + description + location) is in context. Body loads only when triggered. |

## Cron & Heartbeat

| Topic | Wrong assumption | Truth |
|---|---|---|
| Heartbeat creates task records | Heartbeat runs appear in `/tasks` | **No.** Heartbeat = main-session turns only. No background task record. |
| Isolated cron = heartbeat | They're the same mechanism | Isolated agentTurn cron = **has a task record**, separate session. Heartbeat = no record, main session. |
| Cron jobs survive without gateway | Jobs run independently | Cron runs **inside the gateway process**. Gateway down = cron stopped. |
| `--at` without timezone = local time | Uses host timezone | **Treated as UTC.** Always specify `--tz` for local wall-clock scheduling. |

## Context & System Prompt

| Topic | Wrong assumption | Truth |
|---|---|---|
| System prompt is user-controlled | You can override the full prompt | System prompt is **OpenClaw-owned**. Bootstrap files are injected under Project Context, not as the full prompt. |
| Bootstrap files are unlimited | Files load in full | Each file capped at `bootstrapMaxChars` (default: 12k chars). Total cap: `bootstrapTotalMaxChars` (default: 60k). Large files are **silently truncated**. |
| `/context` shows the full prompt | It dumps everything | `/context list` shows sizes and contributors — not the full prompt or tool schemas. |
| Tool schemas don't cost tokens | Only visible text counts | Tool schemas (JSON) are sent to the model and **count toward context** even though you don't see them as text. |

## Workspace & Storage

| Topic | Wrong assumption | Truth |
|---|---|---|
| Workspace is a sandbox | Files outside workspace are blocked | Workspace is the **default cwd**, not a security boundary. Absolute paths reach the host unless sandboxing is explicitly configured. |
| Relative paths work anywhere | `./file` works from any tool | Relative paths resolve from the **workspace root**. Outside the workspace, use absolute paths. |
| Files auto-organize themselves | Storage stays clean | Without conventions, files accumulate in random locations. Establish storage rules and follow them. |

## Hooks & Config

| Topic | Wrong assumption | Truth |
|---|---|---|
| Workspace hooks override bundled | You can replace built-in hooks | Workspace hooks can **add new hook names only** — cannot override bundled, managed, or plugin hooks. |
| BOOT.md needs a reply | Respond normally to boot messages | When boot hook sends a message, reply with **`NO_REPLY`** exactly — nothing else. That exact token suppresses routing. |
| BOOTSTRAP.md persists | It's a permanent reference file | **Delete after first-run setup is complete.** It's a one-time ritual file. |
| Config changes are live | Edits take effect immediately | Some changes require gateway restart. Skills require new session. |

## Behavioral

| Topic | Wrong assumption | Truth |
|---|---|---|
| `NO_REPLY` can be appended | "Here's help... NO_REPLY" | `NO_REPLY` must be the **entire response** — never append to a real reply. |
| `session_status` is optional | Time/model info is always known | `session_status` is the **only reliable way** to get current time, context %, and active model. |
| Sub-agents share parent context | Sub-agents inherit full context | Sub-agents only get `AGENTS.md` and `TOOLS.md` from bootstrap. Other files are filtered out. |
| Per-agent `skills` merges | Adding one skill keeps all others | It **replaces** the entire list. To add one skill, list all others explicitly too. |
