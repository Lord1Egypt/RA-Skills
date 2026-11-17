---
name: agent-session-state
description: >-
  Per-conversation session state files and a Write-Ahead Log (WAL) protocol.
  Captures decisions, corrections, and constraints reliably, keeps one
  conversation's notes out of another's, and provides context recovery for
  long or complex sessions. Run /agent_session_state status to see this
  conversation's notes. Designed to work with hierarchical-agent-memory and
  agent-provenance.
license: MIT-0
compatibility: "OpenClaw 2026.4.x or later."
user-invocable: true
metadata:
  openclaw:
    requires:
      bins: ["openclaw"]
    paths:
      write: ["memory/sessions/", "memory/topics/", "memory/contacts/", "memory/", "MEMORY.md"]
      read: ["memory/sessions/", "memory/topics/", "memory/contacts/", "memory/", "MEMORY.md"]
  version: "2.4.0"
  clawhub: {"category": "memory", "tags": ["session", "isolation", "wal"]}
---

# Agent Session State v2.4.0

Agents that serve multiple conversations need structured per-conversation state beyond what gateway transcripts capture. This skill provides curated agent-authored session files, a Write-Ahead Log (WAL) protocol for reliable decision capture, and a distillation workflow that promotes session-level state into topic files over time.

## At a glance

OpenClaw already provides per-conversation transcript isolation via `session.dmScope`, gateway-owned session history, automatic session maintenance and pruning, a silent memory flush before compaction, `sessions_list` and `sessions_history` for reading prior transcripts, and on recent releases `sessions_search` over them, a per-session `goal`, and a session state change log. If that covers your needs ("keep different users' conversations separate", "save durable facts before compaction", "keep one objective visible") you do not need this skill.

This skill operates at a different layer. It adds curated agent-authored state files per conversation at `memory/sessions/<session-key>.md`, a Write-Ahead Log discipline that commits decisions and corrections to disk before the agent responds, and a distillation workflow that promotes session-level state into topic files over time. The files are notebooks the agent actively maintains, not transcripts of what was said. Transcripts tell you what was said; the goal tells you what the session is trying to do; session state files tell you what was decided along the way.

Install this skill if your agent needs structured, human-readable, long-lived notes about each conversation's ongoing work; if you find yourself losing decisions mid-session because they are never committed anywhere durable; if you want continuity after compaction that goes beyond the memory flush's single-turn save; or if you need topic-aware recovery when working on projects that span multiple sessions. For multi-user agents, run it alongside `session.dmScope = "per-channel-peer"`; they are complementary, not redundant.

## Slash commands

The skill is user-invocable. Where your channel registers skill commands natively, the command appears as `/agent_session_state` (the skill name with characters outside letters, digits, and underscores replaced). The generic form `/skill agent-session-state <command>` always works. Skill commands route through the model, so the agent follows the matching section of this file. Supported commands:

- `status` (default when no argument is given) shows which session file belongs to this conversation, its size, how many WAL entries are undistilled, and the age of the oldest one.
- `log <text>` writes a WAL entry for the given text immediately, before any reply. Use it when the user wants something captured without discussion.
- `recover` runs the Compaction Recovery steps and reports what context was reconstructed.
- `distill` runs the Distillation Targets workflow: proposes entries for shared memory and writes only what the user approves.
- `prune` applies the Maintenance and Retention rules to this conversation's file and reports what was removed.
- `stop` records that the user does not want notes kept in this conversation and stops writing to its file.
- `delete` deletes this conversation's session file after confirmation.

## Relationship to OpenClaw native sessions

OpenClaw core handles transcript routing and raw history. The gateway owns session transcripts in the agent's state store under `~/.openclaw/agents/<agentId>/` (SQLite from 2026.8.1, JSONL before that), isolates them via `session.dmScope`, prunes them via `session.maintenance`, and exposes `sessions_list`, `sessions_history`, and `session_status` as agent tools, with `sessions_search` added on recent releases. This skill does not replace any of that. If you run multiple users or channels, enable `session.dmScope = "per-channel-peer"` regardless of whether this skill is installed; that is what stops Alice's DMs from leaking into Bob's session at the routing level.

**Goals.** From 2026.5.31, OpenClaw has a per-session goal: one durable objective set with `/goal`, visible to the model through the goal tools, surviving restarts, with explicit pause, block, complete, and clear states. The goal is the right home for "what this session is trying to achieve". This skill does not duplicate it. If the user states an objective and your version has `/goal`, suggest setting the goal and log the decision to pursue it; the session file then holds the decisions, corrections, and constraints that accumulate while the goal is pursued.

**Session state awareness.** Recent releases keep a metadata-only change log per session (`session_status` with `changesSince`) that tells a session when a human or another agent intervened. It never carries message content, so it cannot replace a decision log, but it is the first thing to check during recovery in a multi-actor session.

**Personal USER files.** On multi-user gateways from 2026.9.6, each person can have `users/<profile-id>/USER.md` and the `personal_instructions` tool updates it. Per-person preferences belong there, not in a session file. A session file records what a conversation decided; it is not a user profile.

This skill handles curated agent-authored state in the workspace. `memory/sessions/<session-key>.md` lives alongside topic files and daily notes in the agent workspace, is human-readable markdown, and is actively maintained by the agent with WAL entries and distillation rules. The paths do not collide with OpenClaw's transcript store. The two layers compose cleanly: transcripts are raw append-only history; session state files are curated decision logs the agent keeps on purpose.

OpenClaw's silent memory flush and this skill's WAL protocol also compose cleanly. Memory flush is reactive: a single turn at the compaction boundary that appends new facts to the daily note (`memory/YYYY-MM-DD.md`), and on recent releases it rejects replayed text so it cannot be used to rewrite earlier notes. WAL is proactive: per-decision entries written throughout the session, before the agent responds. Different cadences, different granularities, no conflict. Run both.

## Filesystem Access

This skill writes to these locations within the workspace:

- `memory/sessions/`: one markdown file per OpenClaw session key (see Session identity below). This is where the agent writes during normal operation.
- `memory/topics/`, `memory/contacts/`, today's daily note at `memory/YYYY-MM-DD.md`, and `MEMORY.md`: shared long-term memory that every session can read. The agent writes here only during distillation, and only entries the user has approved (see Distillation Targets).

It reads the same paths during startup and compaction recovery. All paths are declared in the metadata above.

Set appropriate permissions on the sessions directory: `chmod 700 memory/sessions`. Each session file is only read and written by the session whose key it carries, so there are no cross-session file conflicts.

## Architecture

### Per-Conversation Session Files

Each conversation context (Discord channel, Slack channel, group chat, a DM peer under `per-channel-peer`, and so on) gets its own session state file under `memory/sessions/`. These files store recent context from that conversation, WAL entries specific to it, conversation-specific preferences, and active topic references (pointers to topic files when using hierarchical-agent-memory).

### Session identity

Each session file belongs to exactly one OpenClaw session key. That is the routing key OpenClaw assigns to the conversation, such as `agent:main:main` for the main session, and `sessions_list` returns it. The key already reflects agent, channel, account, and sender according to `session.dmScope` and `session.groupScope`, and it stays the same when a session is reset. Never derive the identity from a channel display name, and never change its case; some channel IDs are case-sensitive.

- Filename: the session key with every character other than letters, digits, `.`, `_`, and `-` replaced by `_`, plus `.md`. Case is preserved. For example, `agent:main:main` becomes `agent_main_main.md`.
- The first line of every session file is `<!-- session-key: <exact session key> -->`.
- Before reading or writing a session file, compare that line with the current session key. The comparison is exact and case-sensitive. If it does not match, the file belongs to a different conversation; do not read it or write to it. Use the first file named with a numeric suffix (`agent_main_main--2.md`, then `--3`, and so on) whose session-key line matches, or create the next free one.
- A file without a session-key line is never loaded automatically.

### Write-Ahead Log (WAL) Protocol

The WAL protocol ensures that important information is captured reliably, even in the face of concurrent writes or session restarts.

**When to log:** Use your judgment. If the user states a decision, correction, preference, constraint, or important fact, log it before responding. Don't rely on keyword matching as a mechanical trigger. Instead, ask yourself: if this session ended right now, would losing this information hurt? If yes, log it.

**The protocol:** Write to the session state file FIRST, then respond. The urge to respond is the enemy. Context vanishes. Write it down.

**What to log:**

- Decisions: "We're going with approach B", agreements, commitments
- Corrections: "It's actually X, not Y", factual corrections
- Constraints: "Never do X", hard stops, gated items
- Conversation-specific preferences: style choices, tool preferences, workflow preferences for this conversation
- Specific values: version numbers, dates, IDs, URLs, config settings
- New proper nouns: people, companies, projects the agent hasn't seen before

**What NOT to log:**

- Secrets, passwords, API keys, tokens, or credentials. Never write these to session files. If the user shares a secret in conversation, log the fact that a credential exists and where it is stored (e.g., "API key for service X is in the password manager"), not the value itself.
- Personally identifiable information (PII) beyond what is needed for the agent's work. Phone numbers, SSNs, financial account numbers, and similar sensitive data should not appear in session files.
- Casual conversation, greetings, small talk
- Information already in topic files, MEMORY.md, or USER.md
- The session objective itself, when your version has `/goal`; log the decision, set the goal
- Transient task context that won't matter next session

### What gets stored, and user control

Session files hold curated notes (decisions, corrections, constraints, preferences) written in the agent's own words. They never hold verbatim message logs; the gateway transcript already has those. A session file is only read by the session whose key matches the file's session-key line.

The first time the agent creates a session file for a conversation, it tells the user in one line that it keeps decision notes for this conversation at `memory/sessions/<session-key>.md`. If the user asks the agent to stop taking notes (or runs `/agent_session_state stop`), the agent stops writing to that conversation's file and records only that preference. If the user asks to delete the notes (or runs `/agent_session_state delete`), the agent deletes the file after confirming.

### Upgrading from earlier versions

Before v2.3, session files were named by lowercasing the channel name, which let different channels share one file. Those files have no session-key line, so v2.3 and later do not load them automatically. The agent does not read or show legacy files, because their content may come from another conversation. The workspace owner migrates them: for each file, add the session-key line for the conversation it belongs to and rename the file to match, or delete it.

Before v2.2, versions kept a shared `memory/working-buffer.md` that logged raw exchanges from every channel. v2.2 removed it: the shared buffer could carry one channel's content into another, and the gateway transcript (via `sessions_history`) already covers raw-exchange recovery. This skill no longer reads or writes that file. If it exists in your workspace, review it, copy anything worth keeping into the relevant topic file, and delete it.

v2.4 changes no file formats. It adds the slash commands, hands objectives to the native goal, and reads daily notes from `memory/YYYY-MM-DD.md` (OpenClaw's location) rather than a `memory/daily/` directory. If an older AGENTS.md startup checklist still names `memory/working-buffer.md`, lowercase channel-named session files, or `memory/daily/`, tell the user those lines are stale and show the replacement; do not edit AGENTS.md without approval.

## Session Startup

Before doing anything else in a new session:

1. Find the session file for the current session key, confirm its session-key line matches (see Session identity), and read it for recent context from this conversation.
2. If your version has `/goal`, note the active goal if one is set.

This ensures continuity without loading irrelevant history from other conversations.

## WAL Protocol in Practice

When you receive a message that contains a decision, correction, preference, or important fact:

1. Write to the session state file FIRST (before thinking about your response)
2. Include: timestamp, conversation, decision or fact, reasoning if relevant
3. Then respond to the user

Example WAL entry:

```markdown
- [Time] — [Conversation] — Decision: [Project] will be deployed with [feature]. Reasoning: [justification].
```

## Compaction Recovery

If a session starts mid-task or you should know something but don't:

1. Read your session state file
2. In a multi-actor session on a release that supports it, call `session_status` with `changesSince` to learn whether a human or another agent changed things while you were away
3. Check active topic references in the session state; if the session was working on a specific project, read the relevant topic file for authoritative project state
4. Read today's and yesterday's daily notes at `memory/YYYY-MM-DD.md` (on a bare `/new` or `/reset` the runtime has already preloaded them)
5. If still missing context, use `memory_search`
6. On releases with `sessions_search`, use it to find the relevant exchange in this conversation's transcript, then `sessions_history` to read the excerpt. On older releases, `sessions_history` alone with a bounded range. This is heavier than the other recovery paths but surfaces literal exchanges when structured notes are incomplete
7. Let the user know context was recovered and what you picked up. Use natural phrasing, but make it clear you're working from reconstructed context, not continuous memory

Never ask "what were we discussing?" The session file and transcript have it.

## Distillation Targets

Distillation copies content out of one conversation's session file into shared memory that every later session can read, including sessions in other conversations. It therefore requires approval:

- Propose first. List each entry you want to promote and where it would go, and get the user's approval in the same conversation before writing anything to shared memory. Write only the entries the user approved.
- Only distill the current conversation's own session file, never another conversation's.
- If no one is there to approve, as in an unattended maintenance run, post the proposal and write nothing to shared memory.
- Entries the user declines, and anything the user said was private, stay in the session file and are pruned on the normal schedule.

Approved entries go to the appropriate long-term location:

- Project decisions and status changes go to the relevant topic file if using hierarchical-agent-memory v3+. Topic files are the authoritative source for project state.
- New third-party contact information goes to the relevant contact file.
- A stable preference about how to assist the user goes to `USER.md` as a dated directive in OpenClaw's format, or to the user's personal USER file on a multi-user gateway. Mention it; the user may prefer to write it themselves.
- General observations and events go to today's daily note at `memory/YYYY-MM-DD.md`.
- Durable constraints or pointers go to MEMORY.md as one-line entries only. MEMORY.md is a routing table, not a notebook, and entries dreaming has promoted there are left alone.

Do NOT dump session state into MEMORY.md as paragraphs. If the information is project-specific, it belongs in a topic file.

## Maintenance and Retention

During a maintenance pass (when the user asks, runs `/agent_session_state prune`, or as part of a maintenance routine the user has already set up):

- Check WAL for completeness; flag entries that haven't been distilled
- Propose distillation (see Distillation Targets); once the user approves, write the approved entries and remove them from the session file
- Prune session state entries older than 7 days that were distilled or that the user declined to promote; session files are active working memory, not archives
- Verify session state file integrity

Session files should stay small. If a session file exceeds 5KB, it likely contains entries that should have been distilled to topic files or daily notes. Review and distill before the file grows further.

## Version notes

This skill is written for whichever OpenClaw release the user runs, including the monthly extended-stable lines (`2026.N.35`). Session keys, `session.dmScope`, `sessions_list`, `sessions_history`, the memory flush, and user-invocable skill commands exist on every supported release. From 2026.5.31 the `/goal` command and goal tools exist. From 2026.8.1 transcripts are in SQLite and the scheduler is `automations` (`cron` before). `sessions_search`, `session_status changesSince`, and personal USER files are recent mainline additions: detect them by presence in the tool list rather than assuming them, and fall back as described above when they are absent.

## Integration with Other Skills

**hierarchical-agent-memory** provides the memory structure this skill writes into. With v3+, topic files are the primary working memory layer: distill important session decisions into topic files, not just daily notes. Per-conversation session files prevent concurrent writes to the same memory files. Session state files can reference active topics by path for faster context recovery.

**agent-provenance** tracks file authorship. Session state files are agent-authored; provenance headers track creation and review dates. Commit tags apply to session state changes as they do to any other agent-authored file.

**OpenClaw's silent memory flush** (see `docs/concepts/compaction.md`) complements the WAL protocol. Memory flush is reactive and runs a single turn at the compaction boundary to append durable facts to the daily note. WAL is proactive and writes per-decision entries throughout the session. Run both; they cover different cadences and do not conflict. Memory flush is OpenClaw's default behavior and does not require this skill to be installed.

## Best Practices

**For session state:** Treat this as active working memory, not long-term storage. With the user's approval, move important decisions to topic files or daily notes during distillation. Prune old entries during maintenance routines. Include pointers to active topic files for faster recovery. Let the native goal hold the objective.

**For topic files:** Keep conversation-specific runtime context in the session state file. Distill project decisions and status changes into the relevant topic file during maintenance, after the user approves. Cross-reference between session state and topic files as needed.

**For daily notes:** General observations and events go to daily notes. Project-specific decisions go to topic files, not daily notes. Use the WAL protocol for important facts regardless of destination.

## Related Skills

- **hierarchical-agent-memory**: hybrid topic-based working memory with optional time-based archival layers
- **agent-provenance**: file authorship, review tracking, and governance
