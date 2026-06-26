---
name: agent-session-state
description: >-
  Per-channel session isolation, Write-Ahead Log (WAL) protocol, and working
  buffer management. Prevents cross-session interference, captures decisions
  and facts reliably, and provides context recovery for long or complex
  sessions. Designed to work with hierarchical-agent-memory and
  agent-provenance.
license: MIT
compatibility: "OpenClaw 2026.4.x or later."
metadata:
  openclaw:
    requires:
      bins: ["openclaw"]
    paths:
      write: ["memory/sessions/", "memory/working-buffer.md"]
      read: ["memory/sessions/", "memory/working-buffer.md", "memory/topics/", "memory/daily/", "MEMORY.md"]
  version: "2.1.4"
  clawhub: {"category": "memory", "tags": ["session", "isolation", "wal", "buffer"]}
---

# Agent Session State v2.1.4

Agents that serve multiple channels need structured per-channel state beyond what gateway transcripts capture. This skill provides curated agent-authored session files, a Write-Ahead Log (WAL) protocol for reliable decision capture, a working buffer for post-compaction context recovery, and a distillation workflow that promotes session-level state into topic files over time.

## At a glance

OpenClaw already provides per-channel transcript isolation via `session.dmScope`, gateway-owned session history, automatic session maintenance and pruning, a silent memory flush before compaction, and `sessions_history` for reading prior transcripts. If that covers your needs — "keep different users' conversations separate" and "save durable facts before compaction summarizes the chat" — you do not need this skill.

This skill operates at a different layer. It adds curated agent-authored state files per channel at `memory/sessions/{channel}.md`, a Write-Ahead Log discipline that commits decisions and corrections to disk before the agent responds, a working buffer for post-compaction context recovery, and a distillation workflow that promotes session-level state into topic files over time. The files are notebooks the agent actively maintains, not transcripts of what was said. Transcripts tell you what was said; session state files tell you what was decided.

Install this skill if your agent needs structured, human-readable, long-lived notes about each channel's ongoing work; if you find yourself losing decisions mid-session because they are never committed anywhere durable; if you want continuity after compaction that goes beyond the memory flush's single-turn save; or if you need topic-aware recovery when working on projects that span multiple sessions. For multi-user agents, run it alongside `session.dmScope = "per-channel-peer"` — they are complementary, not redundant.

## Relationship to OpenClaw native sessions

OpenClaw core handles transcript routing and raw history. The gateway owns session transcripts at `~/.openclaw/agents/<agentId>/sessions/` as JSONL per session, isolates them via `session.dmScope`, prunes them via `session.maintenance`, and exposes `sessions_list`, `sessions_history`, and `session_status` as agent tools. This skill does not replace any of that. If you run multiple users or channels, enable `session.dmScope = "per-channel-peer"` regardless of whether this skill is installed — that is what stops Alice's DMs from leaking into Bob's session at the routing level.

This skill handles curated agent-authored state in the workspace. `memory/sessions/{channel}.md` lives alongside topic files and daily notes in the agent workspace, is human-readable markdown, and is actively maintained by the agent with WAL entries and distillation rules. The paths do not collide with OpenClaw's transcript store. The two layers compose cleanly: transcripts are raw append-only history; session state files are curated decision logs the agent keeps on purpose.

OpenClaw's silent memory flush and this skill's WAL protocol also compose cleanly. Memory flush is reactive — a single turn that runs at the compaction boundary to save durable facts to MEMORY.md and daily notes. WAL is proactive — per-decision entries written throughout the session, before the agent responds. Different cadences, different granularities, no conflict. Run both.

## Filesystem Access

This skill writes to two locations within the workspace:

- `memory/sessions/` — one markdown file per channel, named with a filesystem-safe slug derived from the channel name or id (lowercase, non-alphanumerics replaced with hyphens)
- `memory/working-buffer.md` — a single file for context recovery during long sessions

This skill reads from those same paths, plus `memory/topics/`, `memory/daily/`, and `MEMORY.md` during compaction recovery. All paths are declared in the metadata above.

Set appropriate permissions on the sessions directory: `chmod 700 memory/sessions`. Each channel's session state file is only written by that channel's session, so there are no cross-session file conflicts.

## Architecture

### Per-Channel Session Files

Each conversation context (Discord channel, Slack channel, group chat, etc.) gets its own session state file under `memory/sessions/`. These files store recent context from that channel, WAL entries specific to that conversation, working buffer status, channel-specific preferences, and active topic references (pointers to topic files when using hierarchical-agent-memory).

### Write-Ahead Log (WAL) Protocol

The WAL protocol ensures that important information is captured reliably, even in the face of concurrent writes or session restarts.

**When to log:** Use your judgment. If the user states a decision, correction, preference, constraint, or important fact — log it before responding. Don't rely on keyword matching as a mechanical trigger. Instead, ask yourself: if this session ended right now, would losing this information hurt? If yes, log it.

**The protocol:** Write to the session state file FIRST, then respond. The urge to respond is the enemy. Context vanishes. Write it down.

**What to log:**

- Decisions — "We're going with approach B", agreements, commitments
- Corrections — "It's actually X, not Y", factual corrections
- Constraints — "Never do X", hard stops, gated items
- Preferences — style choices, tool preferences, workflow preferences
- Specific values — version numbers, dates, IDs, URLs, config settings
- New proper nouns — people, companies, projects the agent hasn't seen before

**What NOT to log:**

- Secrets, passwords, API keys, tokens, or credentials — never write these to session files. If the user shares a secret in conversation, log the fact that a credential exists and where it is stored (e.g., "API key for service X is in .env"), not the value itself.
- Personally identifiable information (PII) beyond what is needed for the agent's work — phone numbers, SSNs, financial account numbers, and similar sensitive data should not appear in session files.
- Casual conversation, greetings, small talk
- Information already in topic files or MEMORY.md
- Transient task context that won't matter next session

### Working Buffer

During long or complex sessions where compaction is likely, activate the working buffer. Update `memory/working-buffer.md` status to ACTIVE. Log every exchange as the user's message plus a 1-2 sentence summary of the AI's response. After compaction, read working-buffer.md FIRST to recover context — don't ask "where were we?" After compaction, clear and restart the buffer at the start of the next long session.

There's no precise context meter. This is a judgment call based on session length, conversation density, and complexity.

## Session Startup

Before doing anything else in a new session:

1. Read `memory/sessions/{channel}.md` for recent context from this channel
2. Read `memory/working-buffer.md` if active (context recovery)
3. Clear and reset the working buffer if the session is starting fresh

This ensures continuity without loading irrelevant history from other channels.

## WAL Protocol in Practice

When you receive a message that contains a decision, correction, preference, or important fact:

1. Write to session state file FIRST (before thinking about your response)
2. Include: timestamp, channel, decision/fact, reasoning if relevant
3. Then respond to the user

Example WAL entry:

```markdown
- [Time] — [Channel] — Decision: [Project] will be deployed with [feature]. Reasoning: [justification].
```

## Compaction Recovery

If a session starts mid-task or you should know something but don't:

1. Read `memory/working-buffer.md` first (raw danger-zone exchanges)
2. Read your session state file
3. Check active topic references in the session state — if the session was working on a specific project, read the relevant topic file for authoritative project state
4. Read today's and yesterday's daily notes
5. If still missing context, use memory_search
6. As a last resort, use `sessions_history` to read a raw transcript excerpt from the current or prior session — this is heavier than the other recovery paths but will surface literal exchanges when structured notes are incomplete
7. Let the user know context was recovered and what you picked up — use natural phrasing, but make it clear you're working from reconstructed context, not continuous memory

Never ask "what were we discussing?" — the buffer has it.

## Distillation Targets

During maintenance, important information from session state should be distilled to the appropriate long-term location:

- Project decisions and status changes go to the relevant topic file if using hierarchical-agent-memory v3+. Topic files are the authoritative source for project state.
- New contact information goes to the relevant contact file.
- General observations and events go to today's daily note.
- Durable constraints or pointers go to MEMORY.md as one-line entries only — MEMORY.md is a routing table, not a notebook.

Do NOT dump session state into MEMORY.md as paragraphs. If the information is project-specific, it belongs in a topic file.

## Maintenance and Retention

During heartbeat and cron routines:

- Check WAL for completeness — flag entries that haven't been distilled
- Distill important entries to topic files and daily notes, then remove them from the session file
- Clear expired working buffer entries
- Prune session state entries older than 7 days that have already been distilled — session files are active working memory, not archives
- Verify session state file integrity

Session files should stay small. If a session file exceeds 5KB, it likely contains entries that should have been distilled to topic files or daily notes. Review and distill before the file grows further.

## Integration with Other Skills

**hierarchical-agent-memory** provides the memory structure this skill writes into. With v3+, topic files are the primary working memory layer — distill important session decisions into topic files, not just daily notes. Per-channel session files prevent concurrent writes to the same memory files. Session state files can reference active topics by path for faster context recovery.

**agent-provenance** tracks file authorship. Session state files are agent-authored; provenance headers track creation and review dates. Commit tags apply to session state changes as they do to any other agent-authored file.

**OpenClaw's silent memory flush** (see `docs/concepts/compaction.md`) complements the WAL protocol. Memory flush is reactive and runs a single turn at the compaction boundary to save durable facts to MEMORY.md and daily notes. WAL is proactive and writes per-decision entries throughout the session. Run both — they cover different cadences and do not conflict. Memory flush is OpenClaw's default behavior and does not require this skill to be installed.

## Best Practices

**For session state:** Treat this as active working memory, not long-term storage. Move important decisions to topic files or daily notes during distillation. Prune old entries during maintenance routines. Include pointers to active topic files for faster recovery.

**For topic files:** Keep channel-specific runtime context in the session state file. Distill project decisions and status changes into the relevant topic file during maintenance. Cross-reference between session state and topic files as needed.

**For daily notes:** General observations and events go to daily notes. Project-specific decisions go to topic files, not daily notes. Use the WAL protocol for important facts regardless of destination.

**For working buffer:** Don't activate for short, simple sessions. Do activate for complex problem-solving, coding, or multi-step tasks. Review and clear periodically to avoid bloat.

## Related Skills

- **hierarchical-agent-memory** — Hybrid topic-based working memory with optional time-based archival layers
- **agent-provenance** — File authorship, review tracking, and governance
