# Drift Catalog

Known patterns of behavioral drift — things agents confidently do wrong over time. Each entry has: what it looks like, how to detect it, and how to correct it.

Use this file during `/selfcheck` or when behavior feels off.

---

## Category 1: Platform Misassumptions

Drift where the agent states or acts on incorrect beliefs about how OpenClaw works.

### 1.1 Heartbeat = Background Task
**What it looks like:** Treating heartbeat runs as if they create `/tasks` records, or expecting them to show up in task history.
**Detection:** You say "the heartbeat ran a background task" or check `/tasks` expecting heartbeat results.
**Correction:** Heartbeat = periodic main-session turns only. No task record. Use isolated cron agentTurn for detached background work with task records.

### 1.2 Skill Changes Are Live
**What it looks like:** Editing a SKILL.md mid-session and expecting new behavior immediately.
**Detection:** You make a skill edit, then refer to the "updated" skill in the same session.
**Correction:** Skills are snapshotted at session start. `/new` to pick up changes.

### 1.3 Per-Agent Skills Merge
**What it looks like:** Adding one skill to `agents.list[].skills` expecting it to add to the defaults.
**Detection:** Agent is missing skills it used to have after a config change to the skills list.
**Correction:** `agents.list[].skills` **replaces** the full skill list. Always include all desired skills.

### 1.4 Workspace Is a Sandbox
**What it looks like:** Assuming files outside the workspace are inaccessible or protected.
**Detection:** Avoiding absolute paths unnecessarily, or assuming a relative path is "safe" because it's in the workspace.
**Correction:** Workspace = default cwd. Not a security boundary. Absolute paths work unless sandbox mode is explicitly configured.

### 1.5 BOOT.md Gets a Normal Reply
**What it looks like:** Responding conversationally to a BOOT.md message.
**Detection:** Gateway startup triggers a message from BOOT.md and you write a full response.
**Correction:** Reply must be exactly `NO_REPLY` — the entire response, nothing else. Any other content gets routed as a real reply.

---

## Category 2: Memory & Context Drift

Drift where the agent loses track of what it knows, what's in context, or how full the window is.

### 2.1 Assuming Old Memory Is Loaded
**What it looks like:** Referencing something from 3+ days ago as if it's in context.
**Detection:** You mention something specific from a past session without having searched for it.
**Correction:** Only today + yesterday's daily files auto-load. Search with `memory_search` or explicitly `read` older files.

### 2.2 Mental Notes
**What it looks like:** "I'll keep that in mind" or "I'll remember that" without writing to a file.
**Detection:** You say you'll remember something without calling `write` or `edit`.
**Correction:** Nothing survives a session end unless written to disk. Write it now.

### 2.3 Context Window Blindness
**What it looks like:** Operating normally deep into a long session without monitoring context usage.
**Detection:** You haven't checked `session_status` in a while during a complex multi-tool session.
**Correction:** Run `session_status` during long sessions. The context % is not visible unless you check it. At 70%+, warn the user.

### 2.4 MEMORY.md Staleness
**What it looks like:** Trusting MEMORY.md entries without checking how current they are.
**Detection:** Acting on MEMORY.md content that references dates many weeks old as if it's current.
**Correction:** MEMORY.md is manually curated. Check the dates of entries. Stale entries can be misleading. Flag if >7 days since last meaningful update.

---

## Category 3: Storage Drift

Drift where the agent loses coherent understanding of where things are stored.

### 3.1 Path Guessing
**What it looks like:** Using a path that seems right without verifying it exists.
**Detection:** You construct a path like `<workspace>/memory/topic.md` without having confirmed the file is there.
**Correction:** `read` or `exec ls` to verify before operating. Silent "file not found" downstream is worse than a quick check upfront.

### 3.2 Relative Path Confusion
**What it looks like:** Using `./file.md` in exec commands without confirming cwd.
**Detection:** exec fails with "no such file" on a relative path.
**Correction:** In exec, use absolute paths or explicitly `cd` first. Relative paths in exec depend on cwd, which may not be the workspace.

### 3.3 Temp File Accumulation
**What it looks like:** Creating working files during a task and not cleaning them up.
**Detection:** Finding files like `output_draft.md`, `temp_results.json`, etc. with no clear purpose during a storage scan.
**Correction:** Clean up after completing a task. If a file is genuinely useful, put it in the right place with a proper name.

### 3.4 Duplicate Knowledge
**What it looks like:** The same information exists in MEMORY.md, a daily file, and a topic file — out of sync.
**Detection:** Searching for something and finding multiple conflicting versions.
**Correction:** One canonical location per piece of knowledge. MEMORY.md for distilled facts, daily files for raw notes, topic files for deep references. Pick one and remove the others.

---

## Category 4: Behavioral Drift

Drift in how the agent approaches tasks — process quality, not knowledge accuracy.

### 4.1 Lateral-Move Debugging
**What it looks like:** Trying A, it fails, trying A', it fails, trying A''.
**Detection:** You've attempted the same general approach 3+ times with minor variations.
**Correction:** Stop. Read `references/failure-protocol.md`. Diagnose root cause before trying again.

### 4.2 Confident Uncertainty
**What it looks like:** Using "I think", "usually", "probably" when the answer is verifiable.
**Detection:** You hedge on something that a tool call could answer definitively.
**Correction:** Run the tool call. Replace guesses with facts. "I think the context is around 50%" → `session_status`.

### 4.3 Output Without Verification
**What it looks like:** Writing a file, running a command, then declaring it done without checking.
**Detection:** You say "done" after a write/exec without reading back the result.
**Correction:** Always verify. `read` after `write`. Check exec output carefully. Silent exit 0 ≠ success.

### 4.4 Scope Creep on Fixes
**What it looks like:** Fixing one thing and inadvertently changing other things in the same file/config.
**Detection:** The user reports unexpected behavior after a targeted fix.
**Correction:** When making targeted edits, use `edit` (not full `write` rewrites) to minimize blast radius. Read before editing to understand what's already there.

---

## Self-Check Usage

During `/selfcheck`, go through each category and honestly ask: *am I currently doing any of these?*

Not "could I theoretically do this" — but "is there evidence in this session or recent behavior that this drift is active?"

If yes: flag it (one line to user), log it to `memory/drift-log.md`, offer to discuss.

Format for drift-log entries:
```
[YYYY-MM-DD] | [category] | [drift ID e.g. 2.3] | [what was observed] | [correction applied]
```

Example:
```
2026-04-24 | Context Drift | 2.3 | Session at 72% before checking status | Warned user, recommended /new
```
