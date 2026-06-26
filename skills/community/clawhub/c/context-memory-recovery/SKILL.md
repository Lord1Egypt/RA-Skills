---
name: context-memory-recovery
description: Use when a user asks an OpenClaw, Hermes, or similar file-backed agent to preserve, recover, checkpoint, or restore working context across new sessions, model changes, compaction, account switches, restarts, crashes, or memory loss. Handles triggers such as "Put it in memory", "Put it it memory", and "Initiate context memory recovery" by using structured workspace files as the source of truth.
version: "0.2.0"
author: Jeremy Martinus / Maestro
type: skill
tags: [memory, continuity, recovery, checkpoint, handoff]
license: MIT-0
---

# Context Memory Recovery

This skill gives file-backed agents a practical continuity protocol. It is for OpenClaw, Hermes, and similar agents that can read and write workspace files.

Core principle: continuity is file-based, not chat-based. If information matters later, write it down.

## What This Skill Solves

Agents lose working context after:

- new sessions
- model changes
- account switches
- compaction or summarization
- restarts, crashes, or shutdowns
- moving work between OpenClaw, Hermes, desktop, VPS, Pi, or other workers

This skill creates a repeatable recovery chain so a fresh agent can quickly answer:

1. What am I doing?
2. What has already been decided?
3. What is blocked?
4. What must I not forget?
5. What is the next safe action?

## Source-of-Truth Hierarchy

Use this hierarchy when saving or recovering context:

1. `SESSION-STATE.md` — immediate operational recovery file
2. `memory/YYYY-MM-DD.md` — daily continuity log
3. `MEMORY.md` — durable long-term memory and standing rules

If chat history conflicts with saved files, trust the files unless there is strong evidence they are stale.

## Required Files

### 1. `SESSION-STATE.md`

Workspace-root file for immediate recovery. Keep it short, structured, and operational. It must not become a diary.

Required structure:

```markdown
# SESSION-STATE.md

Last Updated: YYYY-MM-DD HH:MM TZ
Agent: <agent name / role>
Workspace: <path if known>

## Current Mission
- <one-line mission>

## Active Tasks
- [ ] <task> — status / owner / next action

## Latest Decisions
- <decision> — <date/time or source if useful>

## Blockers
- <blocker> — <what is needed to unblock>

## Important User Preferences
- <preference or standing instruction>

## Next Step If Session Restarts
- <single safest next action>
```

Agent-specific naming is allowed when the environment already has a standard name, for example:

- `CLAUDE-JUNIOR-SESSION-STATE.md`
- `MAESTRO-SESSION-STATE.md`
- `TEMPO-SESSION-STATE.md`

If no agent-specific standard exists, use `SESSION-STATE.md`.

### 2. `memory/YYYY-MM-DD.md`

Daily operational memory. Use it for:

- completed work
- in-progress work
- decisions
- blockers
- important events
- next steps
- recovery-relevant details
- file paths, job IDs, commit hashes, service names, and other evidence needed to resume work

This file may be more detailed than `SESSION-STATE.md`, but keep it practical.

Recommended entry format:

```markdown
- HH:MM TZ: <event/decision>. Evidence: <file/job/commit/tool result if useful>. Next: <next action if any>.
```

### 3. `MEMORY.md`

Durable long-term memory only. Use it for:

- standing user preferences
- recurring workflows
- durable operating rules
- long-lived project facts
- important technical decisions
- recovery instructions that should survive many sessions

Do not pollute `MEMORY.md` with temporary task noise.

## Startup Recovery Procedure

When continuity may matter, before serious work:

1. Locate the workspace root.
2. Find the recovery file:
   - Prefer the local agent-specific session-state file if one is already established.
   - Otherwise use `SESSION-STATE.md`.
   - If no recovery file exists and the user is asking to adopt this protocol, create it.
3. Read the recovery file fully.
4. Read today's `memory/YYYY-MM-DD.md` if it exists.
5. If needed, read the most recent relevant daily memory file.
6. Read `MEMORY.md` if available and appropriate for the privacy context.
7. Reconstruct:
   - current mission
   - active tasks
   - latest decisions
   - blockers
   - important preferences
   - next step
8. If the next step is clear and safe, continue. Do not wait passively.
9. If the files disagree, use this priority: session-state for immediate task state, daily memory for recent evidence, long-term memory for standing rules.

## Trigger Handling

### Save trigger: `Put it in memory`

When the user says exactly or clearly intends:

- `Put it in memory`
- `Put it it memory`
- `remember this`
- `we may need this later`
- `get ready for a new model`

Treat it as a save command. The exact phrase `Put it in memory` remains the hard trigger; nearby obvious typos should be honored rather than ignored.

Save workflow:

1. Identify what must be preserved:
   - current mission
   - active tasks
   - decisions
   - blockers
   - preferences
   - next step
   - recovery-critical file paths, service names, IDs, or commits
2. Update the recovery file with the current operational state.
3. Update today's `memory/YYYY-MM-DD.md` with the relevant event, decision, task state, or preference.
4. Update `MEMORY.md` only if the information is durable, long-term, or a standing rule/preference/decision.
5. Verify the saved content is sufficient for a fresh agent to recover without chat history.
6. Reply exactly:

`Done`

No extra words. No punctuation. No emoji. No explanation.

### Recovery trigger: `Initiate context memory recovery`

When the user says exactly or clearly intends:

- `Initiate context memory recovery`
- `initiate from recovery`
- `recover from memory`
- `start context recovery`

Treat it as a recovery command.

Recovery workflow:

1. Read the recovery file.
2. Read today's `memory/YYYY-MM-DD.md` if it exists.
3. Read the most recent relevant daily memory file if needed.
4. Read `MEMORY.md` if available and appropriate for the privacy context.
5. Reconstruct the current mission, tasks, decisions, blockers, preferences, and next step.
6. If the next step is clear and safe, resume work.
7. If action is blocked, report the blocker concisely.

Do not replace this with a generic summary. Do not claim recovery occurred unless the files were actually read.

## Checkpoint Rules

Update the recovery file whenever continuity matters, especially when:

- a task is in progress
- task state changes
- a task becomes blocked
- a decision is made
- a new instruction changes workflow
- a user preference becomes clear
- priority changes
- model switch, account switch, reset, compaction, restart, shutdown, crash risk, or migration may occur
- a background job, cron job, or delegated agent is created
- a file path, command, service, host, job ID, or commit hash is essential to continue later

Checkpoint before likely continuity breaks. Do not wait until context is already lost.

## What to Save Where

| Information | Session State | Daily Memory | Long-Term Memory |
|---|---:|---:|---:|
| Current task and next step | Yes | Yes | No |
| Temporary blocker | Yes | Yes | No |
| Completed task evidence | Optional | Yes | No |
| Durable user preference | Yes if operationally relevant | Yes | Yes |
| Standing operating rule | Yes if active | Yes | Yes |
| File path needed tomorrow | Yes | Yes | Maybe |
| One-off detail unlikely to matter | No | Optional | No |
| Credentials/secrets | Avoid plaintext | Avoid plaintext | Avoid plaintext |

## Privacy and Shared-Chat Rule

Before reading or exposing durable memory, consider the chat context.

- In private/direct owner sessions, `MEMORY.md` may usually be read if available.
- In group/shared sessions, avoid exposing private memory unless the user explicitly authorizes it and the content is safe to share.
- Never paste sensitive memory into chat unnecessarily.
- Do not store secrets in plaintext unless the user explicitly instructs it and the environment policy allows it.

## Adoption Procedure

When first installing or adopting this protocol for an agent:

1. Choose the recovery filename:
   - existing agent-specific name, or
   - default `SESSION-STATE.md`.
2. Create the file if missing.
3. Populate it with the current operational state using the required structure.
4. Create `memory/` if missing.
5. Create today's `memory/YYYY-MM-DD.md` if useful.
6. Confirm the user's preferred trigger phrases.
7. Begin using the file immediately.

First-adoption checklist:

```markdown
- [ ] Recovery file exists at workspace root
- [ ] Required sections are present
- [ ] Today's daily memory file exists or is intentionally absent
- [ ] Durable rules are in MEMORY.md when appropriate
- [ ] Trigger phrases are documented
- [ ] Next restart action is clear
```

## Recovery Output Pattern

After recovery, keep the user-facing answer concise:

```text
Recovered.

Current mission: <one line>
Next step: <one line>
Blocker: <none / one line>
```

If the trigger requires immediate continuation and no report is needed, continue work instead of summarizing.

## Quality Rules

- Keep `SESSION-STATE.md` short and operational.
- Use bullets, not essays.
- Record decisions and next steps, not every conversation detail.
- Daily memory can hold more detail.
- Long-term memory is for durable rules only.
- Files beat chat history.
- After recovery, act if the path is clear.
- If unsure whether something is durable, write it to daily memory first; promote later if it recurs.

## Minimal Example

```markdown
# SESSION-STATE.md

Last Updated: 2026-04-30 20:05 SGT
Agent: workspace assistant
Workspace: /path/to/workspace

## Current Mission
- Prepare a reusable file-based recovery protocol for future sessions.

## Active Tasks
- [ ] Review the draft skill — confirm whether it is ready to install or publish.

## Latest Decisions
- Use files as the source of truth when chat history and memory files disagree.

## Blockers
- Awaiting user approval before public publishing.

## Important User Preferences
- Keep recovery files short, operational, and easy for a fresh agent to follow.
- Reply exactly `Done` after completing a save triggered by `Put it in memory`.

## Next Step If Session Restarts
- Read this file, then continue from the active task list without relying on chat history.
```
