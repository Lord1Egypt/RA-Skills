# OpenClaw behavior sources

Use this file when deciding which files matter most in an `agent-rule-audit`.

## Core idea

In OpenClaw, agent behavior is not shaped by a single prompt file.
Behavior usually comes from several layers working together.

## Highest-priority behavior sources

### 1. Core stable bootstrap files
These are the most important default sources because they are core workspace behavior files and are the most stable default audit target.

Default first-pass scope:
- `AGENTS.md`
- `SOUL.md`
- `USER.md`
- `MEMORY.md` (if present)
- `TOOLS.md`
- `IDENTITY.md`
- `HEARTBEAT.md`

Why this matters:
- OpenClaw's system prompt and workspace bootstrap flow make these files unusually behavior-relevant.
- They often contain the real operating rules, not just notes.
- They are a better default audit scope than every possibly relevant file in the workspace.
- `MEMORY.md` belongs here when present, but it is optional in OpenClaw; if it does not exist, ignore it rather than treating the absence as a problem.

## Widen only when needed

### 2. Shared files explicitly referenced by the core files
Examples:
- shared etiquette
- shared policies
- shared workflow docs

These matter only when the agent is actually told to follow them.

### 3. Correction / learnings layer
Treat any correction / learnings / workflow-improvement layer as a meaningful behavior-shaping layer, but not necessarily part of every default first-pass audit.
Use it when:
- the target workspace has such a layer
- the user wants a deeper audit
- the core files are not enough to explain the behavior
- there is reason to believe corrections/workflow learnings are influencing current behavior

A common pattern in some workspaces is `.learnings/`, but do not assume every OpenClaw workspace has it.

### 4. Self-improvement active goal files
When an agent is under active behavior trial, these files can matter:
- goal
- plan
- tracking overview
- live trial rules pushed into `AGENTS.md`

### 5. Supporting evidence
Examples:
- daily tracking
- daily memory
- screenshots/transcripts the user provides

These are useful for diagnosis, but are not part of the default first-pass core audit.

## Audit reminder

Do not treat every file in a workspace as equal.
A good audit starts with the smallest core set that is most likely to steer real behavior, and only widens when needed.
