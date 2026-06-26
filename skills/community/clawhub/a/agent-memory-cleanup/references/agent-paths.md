# Agent Memory Paths

Use this reference only when the user has not provided explicit memory paths.
Prefer user-provided paths over discovery.

## Safe Discovery Order

1. Current workspace memory files named `user.md`, `memory.md`, `memories.md`, `profile.md`, `preferences.md`, or `agent_memory.md`.
2. Workspace agent config folders such as `.codex/`, `.claude/`, `memory/`, or `memories/`.
3. Agent-specific home variables when available.
4. User home folders only when the user explicitly asks for a broader inventory.

Avoid broad recursive home scans by default.

## Codex

Likely locations:

- `$CODEX_HOME`
- Workspace `.codex/`
- Workspace `.codex/skills/` for installed or project-level skills

Notes:

- Treat `AGENTS.md` as project policy, not global user memory.
- Treat skill `SKILL.md` files as skill instructions, not user memory.

## Claude Code

Likely locations:

- User-level Claude config under the configured Claude home.
- Project `.claude/`
- Project `.claude/skills/`

Notes:

- Treat `CLAUDE.md` as instruction policy unless the user explicitly says it is their memory file.
- Project instructions may contain durable rules, but they are not global user memory by default.

## OpenClaw

Likely locations:

- OpenClaw workspace memory folders.
- ClawHub-installed skill directories.
- User-provided OpenClaw agent home or profile paths.

Notes:

- ClawHub skill folders contain reusable skill instructions. Do not clean them as user memory.
- If publishing or installing skills, keep release metadata separate from memory cleanup.

## Hermes Agent

Likely locations:

- Configured Hermes Agent home.
- Workspace memory folders.
- User-provided memory root.

Notes:

- When Hermes reports memory storage full, run audit mode first and ask before applying edits unless automatic cleanup was explicitly authorized.

## Generic Agents

If the agent is not listed:

- Search only the current workspace and explicit config roots.
- Identify memory files by filename and content, not by filename alone.
- Skip project policy, prompt templates, system instructions, and skill/plugin manifests unless the user includes them in scope.
