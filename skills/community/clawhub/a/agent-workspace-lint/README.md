# Agent Workspace Lint

An OpenClaw skill for reviewing the files an agent reads at the start of every session:
`AGENTS.md`, `SOUL.md`, `USER.md`, `IDENTITY.md`, `MEMORY.md`, and the daily notes.

- **Measures** every file against the bootstrap limits of the installed OpenClaw version
  (per file, in total, the fixed `USER.md` limit, daily notes at session start).
- **Checks what is really loaded** with `/context list`: files that are cut, and `MEMORY.md` or
  `USER.md` that exist on disk but are no longer injected because OpenClaw classed them as
  untrusted.
- **Finds** rules in the wrong file, long procedures that belong in a skill, history instead of
  current state, contradictions inside and between files and against live configuration, stale
  facts, duplicates, template leftovers, and key-like strings (location only).
- **Proposes** exact, small edits with the character change. Nothing is written until the owner
  approves that exact edit; approved edits go through the agent's own file tools in an owner
  chat, so curated files stay trusted and loaded.

Works with local access to the workspaces or with pasted files and `/context list` output.
Everything is in the skill file itself. Tested read-only against a live OpenClaw 2026.11
installation with eight agents, November 2026.
