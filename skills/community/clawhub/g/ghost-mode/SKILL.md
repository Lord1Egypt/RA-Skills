---
name: ghost-mode
description: Browser-style incognito mode for your OpenClaw agent. Activate to pause all memory writes — when you deactivate, every trace of the session is securely scrubbed from logs, memory files, session transcripts, and search indexes. Like closing an incognito window: nothing persists. Any files or local outputs you independently create during the session remain untouched. Use when user says "ghost on", "ghost off", "incognito", "private mode", "privacy mode", or wants a conversation that leaves no persistent trace in agent memory.
requires:
  bins:
    - python3
optional:
  env:
    - name: OPENCLAW_WORKSPACE
      default: ~/.openclaw/workspace
      description: OpenClaw workspace root. Must be a subdirectory of home, not home itself.
    - name: OPENCLAW_HOME
      default: ~/.openclaw
      description: OpenClaw home directory. Must be a subdirectory of home, not home itself.
    - name: OPENCLAW_AGENT
      default: main
      description: OpenClaw agent name (used to locate session files).
  bins:
    - name: shred
      description: Secure file deletion. Falls back to rm if unavailable (with warning).
install:
  scripts:
    - scripts/ghost_mode.sh
    - scripts/ghost_registry.py
    - scripts/ghost_archive.py
    - scripts/ghost_scrub.py
    - scripts/ghost_verify.py
    - scripts/ghost_index_cleanup.py
---

# Ghost Mode

**Incognito mode for your OpenClaw agent — like a browser's private window, but for your AI.**

Activate, and the agent stops writing to memory. Deactivate, and every trace of the session — logs, memory files, session transcripts, search index entries — is securely scrubbed. Like closing an incognito browser window: the activity never happened, as far as the agent's memory is concerned.

**What stays:** Any files or local outputs you independently create during the session (code, documents, images, etc.) are not touched — provided `OPENCLAW_WORKSPACE` and `OPENCLAW_HOME` are correctly scoped to your OpenClaw installation (not broadly set to `$HOME` or a parent directory). Ghost Mode only impacts the agent's memory and session history; the scripts enforce this scope at startup and will refuse to run if the env vars point too broadly.

User-controlled, explicit, and auditable. No silent hooks, no background daemons, no automatic interception.

## When to Use Ghost Mode

- **Experimental work** — Trying an approach you don't want the agent to learn from or reference later. Test something wild, then close the incognito window.
- **Sensitive conversations** — Discussing personal matters, credentials, or anything you don't want persisting in the agent's long-term memory.
- **Exploring bad ideas** — Prototyping something you might discard. No point polluting the agent's context with abandoned directions.
- **One-off tasks** — Quick operations where the agent doesn't need to remember what it did.
- **Debugging the agent itself** — Testing agent behavior without creating a memory trail that could influence future sessions.
- **Shared environments** — Using an agent on a machine others can access, and you want to keep certain sessions private.
- **Resetting context pressure** — The agent accumulates context over time. Ghost Mode lets you have a "clean room" conversation without adding to that weight.

## Example Sessions

### Example 1: Quick experiment

```
You: ghost on
Agent: Ghost mode ON. This session will not be recorded. Memory writes are suppressed until you say "ghost off".

You: Let me try refactoring the auth module with a completely different pattern...
Agent: [works on refactoring, creates files, runs tests]

You: Actually, that didn't work. Let me scrap it.
Agent: [deletes the experimental code]

You: ghost off
Agent: Ghost mode OFF. Session data has been scrubbed. The agent has no memory of this conversation.
```

Result: The agent's memory is untouched. The experimental refactoring was never recorded. Any files you created or deleted during the session remain as-is.

### Example 2: Sensitive discussion

```
You: ghost on
Agent: Ghost mode ON. This session will not be recorded.

You: I need to test the integration with the staging server using my dev credentials.
Agent: [helps with integration, runs tests against staging]

You: Thanks, that's done. ghost off
Agent: Ghost mode OFF. Session scrubbed. No record of credentials or this conversation remains in my memory.
```

Result: Credentials were used during the session but never written to daily logs, memory files, or session archives. The agent won't reference them later.

### Example 3: Exploring a bad direction

```
You: ghost on
Agent: Ghost mode ON.

You: What if we rewrite the entire backend in Rust?
Agent: [explores the idea, generates code, benchmarks...]

You: Okay, this is clearly not worth it right now. ghost off
Agent: Ghost mode OFF. Scrubbed. The Rust exploration never happened, as far as my memory is concerned.
```

Result: The agent won't later suggest Rust or reference the abandoned exploration in future sessions.

### Example 4: Checking status

```
You: ghost status
Agent: Ghost mode: ACTIVE
         Session: ghost-1777145449
         Activated: 2026-04-25T19:30:49Z
         Registry shows 1 session in active state.
```

---

## ⚠️ DATA LOSS WARNING — READ BEFORE INSTALLING

**This skill permanently deletes data by design.**

When you run `ghost off` or `force-cleanup-all`, the skill:
- **Scrubbs** entries from your daily logs, semantic memory, and episodic memory files
- **Archives then shreds** session transcripts and checkpoint files using `shred -u` (secure overwrite, then remove)
- **Removes** entries from the OpenClaw memory search index

**This is irreversible.** Deleted files are not recoverable — not from trash, not from backup, not from any undo mechanism. This is the entire point of the skill, not a side effect.

**The following scenarios can cause unintended data loss:**
- **Bugs or errors** in the scrubbing logic may remove more content than intended
- **Misuse** — running `ghost off` in the wrong session or at the wrong time
- **Environment conflicts** — if your workspace layout differs from the expected OpenClaw structure, scrubbing may target the wrong files or miss files it should clean
- **Partial failures** — if the pipeline crashes mid-run, some files may be scrubbed while others remain, leaving your memory in an inconsistent state
- **Stale sessions** — if a ghost session spans multiple days, scrubbing will affect all entries in that time window across all files, including content from other sessions

**By installing this skill, you acknowledge and accept these risks.**

**Recommended: enable daily OpenClaw workspace backups.** A `tar` or `rsync` backup of `~/.openclaw/workspace/` and `~/.openclaw/data/` run daily ensures you can recover from unintended data loss. Example:

```bash
# Add to crontab for daily 2 AM backup
0 2 * * * tar -czf ~/openclaw-backup-$(date +\%F).tar.gz ~/.openclaw/workspace/ ~/.openclaw/data/
```

---

## How It Works

1. **`ghost on`** — writes a `.ghost-mode` flag file and registers the session in a local JSON registry
2. **Agent reads the flag** — on session start, checks for `.ghost-mode`. If present, suppresses all writes to memory files, daily logs, semantic/episodic files, and MEMORY.md
3. **`ghost off`** — removes the flag, then runs a 5-stage cleanup pipeline:
   - **Archive** → moves session JSONL and checkpoint files to a temporary staging directory
   - **Scrub** → removes ghost-window entries from daily logs, semantic files, episodic files, and MEMORY.md
   - **Index cleanup** → removes matching entries from the OpenClaw memory index (SQLite)
   - **Verify** → 7-layer check confirms no traces remain
   - **Shred** → secure overwrite + delete of all staged files (`shred -u`, falls back to `rm` with warning)

Each stage is idempotent — re-running is safe and produces the same result.

## Quick Start

```bash
# Activate (the agent will also do this when you say "ghost on")
./scripts/ghost_mode.sh on --session-key <key>

# Preview what would be deleted (no changes made)
./scripts/ghost_mode.sh off --dry-run

# Deactivate and scrub (with confirmation prompt)
./scripts/ghost_mode.sh off

# Skip confirmation prompt (for scripted/automated use)
./scripts/ghost_mode.sh off --yes

# Check status (includes config)
./scripts/ghost_mode.sh status

# Force cleanup of stale sessions older than 24 hours
./scripts/ghost_mode.sh force-cleanup-all
```

## Safety Interlocks

Ghost Mode includes two safety mechanisms to prevent accidental data loss:

### 1. Confirmation Prompt

By default, `ghost off` and `force-cleanup-all` require interactive confirmation before deleting anything. You must type `yes` to proceed.

```bash
$ ./scripts/ghost_mode.sh off
⚠️  You are about to permanently delete session data.
   This action is IRREVERSIBLE. Deleted data cannot be recovered.

  Type yes to confirm, or anything else to cancel:
```

- **Configurable**: Set `"confirm_before_delete": false` in `ghost-mode-config.json` to disable prompts.
- **Non-interactive fallback**: If no terminal is available (e.g., cron, piped input), confirmation is required unless you pass `--yes` / `-y`.
- **`--yes` / `-y` flag**: Skips the confirmation prompt entirely. Use in scripts, cron jobs, or automation.

### 2. Dry-Run Mode

Every destructive command supports `--dry-run` — shows exactly what would be deleted without making any changes:

```bash
$ ./scripts/ghost_mode.sh off --dry-run
[ghost DRY-RUN] Would archive session files for: ghost-1745695449
[ghost DRY-RUN]   Would copy session JSONL + checkpoints to ~/.openclaw/ghost-archive/
[ghost DRY-RUN]   Would remove originals from sessions directory
[ghost DRY-RUN] Would scrub memory files for session: ghost-1745695449
[ghost DRY-RUN]   Would remove ghost-window entries from: memory/*.md
[ghost DRY-RUN]   Would remove ghost-window entries from: memory/semantic/*.md
[ghost DRY-RUN]   Would remove ghost-window entries from: memory/episodic/*.md
[ghost DRY-RUN]   Would remove promoted ghost entries from: MEMORY.md
[ghost DRY-RUN] Would remove index entries for session: ghost-1745695449
[ghost DRY-RUN]   Would DELETE rows from memory.db matching session ID
[ghost DRY-RUN] Would run 7-layer verification for session: ghost-1745695449
[ghost DRY-RUN] Would secure-delete 3 archived file(s)
```

- **Configurable default**: `dry_run_by_default` is `true` by default — `ghost off` starts in dry-run mode. Pass `--yes` to execute for real. Set `"dry_run_by_default": false` in config to disable this safety default.

### Configuration File

Create `ghost-mode-config.json` in your workspace root (`~/.openclaw/workspace/ghost-mode-config.json`):

```json
{
  "confirm_before_delete": true,
  "dry_run_by_default": true
}
```

| Setting | Default | Description |
|---------|---------|-------------|
| `confirm_before_delete` | `true` | Require typing `yes` before any destructive operation. Set `false` to disable prompts. |
| `dry_run_by_default` | `true` | If `true` (default), `ghost off` and `force-cleanup-all` start in dry-run mode. Pass `--yes` to execute for real. Set `false` to skip dry-run by default. |

## What This Skill Touches

| Path | Read | Write | Delete | When |
|------|------|-------|--------|------|
| `memory/.ghost-mode` | ✓ | ✓ | ✓ | Flag lifecycle |
| `memory/.ghost-sessions.json` | ✓ | ✓ | — | Registry state machine |
| `memory/YYYY-MM-DD.md` | ✓ | ✓* | — | Scrub ghost-window entries |
| `memory/semantic/*.md` | ✓ | ✓* | — | Scrub ghost-window entries |
| `memory/episodic/*.md` | ✓ | ✓* | — | Scrub ghost-window entries |
| `MEMORY.md` | ✓ | ✓* | — | Scrub promoted ghost entries |
| `~/.openclaw/agents/<agent>/sessions/` | ✓ | — | ✓ | Archive then remove originals |
| `~/.openclaw/ghost-archive/` | ✓ | ✓ | ✓ | Temporary staging, shredded after verify |
| `~/.openclaw/data/memory.db` | ✓ | ✓ | — | Remove index entries for ghost sessions |

\* Writes use atomic rename (`.tmp` → target) — never partial or corrupted files.

All deletions are user-triggered. The skill only acts when you explicitly run `ghost off` or `force-cleanup-all`. No hooks, no daemons, no passive collection.

## What This Skill Does NOT Touch

- **Files you create** — code, documents, images, configs, anything you explicitly write to disk during a ghost session stays exactly where you put it
- **Local outputs** — command output, build artifacts, downloaded files, anything the agent creates as a file output (not a memory entry) is untouched
- OpenClaw gateway logs — outside agent workspace scope
- OS-level process traces — outside agent workspace scope
- Third-party service logs — outside agent workspace scope
- Files outside the OpenClaw workspace — never read or modified
- Network requests — none. Entirely local, no API calls, no cloud services

**The analogy:** Browser incognito mode doesn't delete your downloads. Ghost Mode doesn't delete your files. It only clears the agent's memory of what happened — just like closing a private browsing window clears history but leaves your saved files alone.

## File Layout

```
scripts/
├── ghost_mode.sh           # Main CLI entry point (dry-run, confirm, config)
├── ghost_registry.py       # Session registry + state machine
├── ghost_archive.py        # Session file archival
├── ghost_scrub.py          # Memory file scrubbing
├── ghost_verify.py          # 7-layer verification
└── ghost_index_cleanup.py  # OpenClaw memory index cleanup

references/
└── ARCHITECTURE.md         # Full state machine docs, edge cases, internals
```

## State Machine

```
active → completed → archived → scrubbed → verified → (shredded)
```

Each transition is recorded in the registry with a timestamp. Re-running any stage is safe.

## Post-Install Warning

**The first time the agent detects this skill after installation, it MUST deliver this warning to the user:**

> ⚠️ **Ghost Mode is installed.** This skill permanently deletes data — logs, memory files, session transcripts, and search index entries — using secure deletion (`shred -u`). This is irreversible. Bugs, misuse, or environment conflicts can cause unrecoverable data loss beyond what you intended. By keeping this skill installed, you accept these risks. **Strongly recommended: set up daily backups of `~/.openclaw/workspace/` and `~/.openclaw/data/`.** Run `ghost_mode.sh status` to check the current state at any time.

This warning must be shown **once** after installation. To prevent repeated warnings, after delivering it, create the file `memory/.ghost-mode-warning-shown` in the workspace. On subsequent sessions, check for this file — if it exists, skip the warning.

**On first install**, the agent MUST also create `ghost-mode-config.json` in the workspace root with confirmation enforced:

```json
{
  "confirm_before_delete": true,
  "dry_run_by_default": true
}
```

This ensures every new install starts with confirmation enabled. The user may change these settings later, but confirmation must never be silently disabled.

## AGENTS.md Integration

After installing, add this to your AGENTS.md so the agent respects ghost mode:

```markdown
## Ghost Mode

⚠️ This skill permanently deletes data by design. See the post-install warning for details.

- **"ghost on"** → run `ghost_mode.sh on` immediately
- **"ghost off"** → run `ghost_mode.sh off` immediately (requires confirmation unless `--yes`)
- **"ghost status"** → run `ghost_mode.sh status` and report back

When ghost mode is active (`.ghost-mode` flag exists):
- **ZERO memory writes** — no daily logs, semantic files, episodic files, MEMORY.md, AGENTS.md, USER.md, or SOUL.md updates
- Reading files is still allowed
- Do NOT mention ghost mode in channel messages unless the user asks

### Stale Flag Cleanup
If the `.ghost-mode` flag's `activatedAt` is older than 24 hours:
```bash
ghost_mode.sh force-cleanup-all
```
Remove the flag and proceed normally. Log cleanup to stderr only.
```

## Cron Integration (Optional)

The skill works without cron — `ghost off` runs the full pipeline synchronously. If you want automated cleanup of stale sessions:

```bash
# Archive completed ghost sessions every 15 min (optional)
*/15 * * * * ~/.openclaw/workspace/skills/ghost-mode/scripts/ghost_mode.sh archive-completed

# Verify scrubbed sessions hourly (optional)
0 * * * * ~/.openclaw/workspace/skills/ghost-mode/scripts/ghost_mode.sh verify-pending

# Force cleanup stale sessions daily at 3 AM (optional)
0 3 * * * ~/.openclaw/workspace/skills/ghost-mode/scripts/ghost_mode.sh force-cleanup-all
```

These are **optional** — the primary workflow is manual `ghost on` / `ghost off`.

## Requirements

- **Python 3.8+** — for registry, scrub, verify, and index cleanup scripts
- **`shred`** — standard on Linux. macOS: `brew install coreutils` then use `gshred`
- **OpenClaw workspace** — defaults to `~/.openclaw/workspace/`, configurable via `OPENCLAW_WORKSPACE` env var
- **No external dependencies** — no pip packages, no API keys, no cloud services, no network calls

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|--------|
| `OPENCLAW_WORKSPACE` | `~/.openclaw/workspace` | Path to the OpenClaw workspace directory. All memory and registry files are stored here. |
| `OPENCLAW_HOME` | `~/.openclaw` | Path to the OpenClaw home directory. Session files and archive are stored under `agents/` and `ghost-archive/` here. |
| `OPENCLAW_AGENT` | `main` | Agent directory name under `OPENCLAW_HOME/agents/`. Used to locate session JSONL and checkpoint files. |

## Security Model

**Intentionally destructive.** Ghost mode exists to remove data. This is the core purpose, not a side effect. **Multiple safety interlocks prevent accidental deletion.**

| Property | Detail |
|----------|--------|
| Deletion method | `shred -u` (secure overwrite, then remove). Falls back to `rm` with warning if `shred` unavailable |
| Registry audit trail | Every state transition is timestamped. You can inspect `memory/.ghost-sessions.json` at any time |
| 7-layer verification | Confirms: flag removed, registry correct, session files gone, checkpoints gone, daily logs free of session references, semantic files free of session references, index clean |
| Atomic writes | All file modifications use write-to-`.tmp` then rename — no partial/corrupted state |
| Confirmation prompt | `ghost off` and `force-cleanup-all` require interactive `yes` confirmation by default. Disable with config or `--yes` flag |
| Dry-run mode | `--dry-run` shows what would be deleted without making any changes. Configurable as default via `dry_run_by_default` |
| User-triggered only | No automatic hooks. No passive collection. No daemons. Acts only when you run `ghost on`, `ghost off`, or `force-cleanup-all` |
| Path validation | All file operations validate paths are within `OPENCLAW_WORKSPACE` or `OPENCLAW_HOME`. Session IDs are checked for path traversal. Operations outside these boundaries are rejected |
| Env var safety check | At startup, the scripts verify that `OPENCLAW_WORKSPACE` and `OPENCLAW_HOME` resolve to paths within the user's home directory. If either is misconfigured to point at a broader location (e.g. `/`, `/tmp`), the scripts abort with an error before performing any operations |
| Local only | No network calls. No API keys. No cloud services. Everything runs on your machine |

**What's out of scope:** Gateway logs, OS process traces, third-party service logs. Ghost mode cleans what the agent controls — your workspace.

## Limitations

- **Ghost mode is cooperative, not enforced at the OS level.** Write suppression is implemented in the agent runtime — the agent checks for the `.ghost-mode` flag at session start and during the session, and skips memory writes when it is present. The scripts in this skill handle activation (writing the flag) and cleanup (scrubbing traces after deactivation); the runtime enforcement lives in your agent's AGENTS.md integration, not in these scripts. Other processes, scripts, or non-compliant agents that bypass the flag will still write to the workspace. The flag is a coordination mechanism — it works when the agent reads and respects it.

- The OpenClaw gateway logs requests independently. Ghost mode cannot remove gateway logs.

- If the agent crashes before `ghost off`, the flag persists. The next session will detect it. Run `force-cleanup-all` to clean up sessions stale for >24 hours.

- **Scrubbing uses timestamp and filename heuristics.** The scrubber matches ghost-window entries by mtime and embedded timestamps. If your workspace layout or timestamp formats differ from standard OpenClaw conventions, the scrubber may miss some entries or — in edge cases — remove content from non-ghost sessions that falls within the same time window. Always run `--dry-run` first to preview what will be affected.

## Disclaimer

This skill is provided **as-is, with no warranties, express or implied.** There is no assurance of fitness for any particular purpose, no guarantee of data safety, and no support commitment.

By installing or using this skill, you accept full responsibility for any outcomes. You use this skill entirely at your own risk. The Author is not liable in any way for any losses, damages, or consequences — direct, indirect, incidental, or otherwise — that result from using this skill. This includes, but is not limited to, data loss, corrupted files, lost sessions, or any other damage arising from the use or inability to use this skill.

You are running a tool whose stated purpose is to permanently delete data. Use it carefully. Back up your workspace.

## Source & Issues

- **Repo:** https://github.com/stelloxx/ghost-mode
- **Install:** `clawhub install ghost-mode`
- **Report issues:** https://github.com/stelloxx/ghost-mode/issues

## License

MIT-0