---
name: agent-local-memory
description: >
  Persistent local memory system for AI agents across conversations — file-based, zero external dependencies.
  Trigger when: (1) user asks to "remember" something, (2) user asks what you remember, (3) saving progress before context limit, (4) conversation starts — auto-check for existing memories.
metadata:
  version: "1.0"
  tags:
    - color: blue
      label: Memory Management
    - color: green
      label: Cross-Session Persistence
    - color: purple
      label: Claude Code / OpenClaw
---

# Agent Local Memory

Persistent local memory across conversations — store user preferences, project context, and behavioral feedback as plain files. No external services, no network calls, no credentials required.

## Storage Paths

| Platform | Default Memory Path |
|----------|---------------------|
| Claude Code | `~/.claude/memory/` |
| OpenClaw | `~/.openclaw/memory/` |
| Cross-platform | `~/.agent-memory/` |

## MEMORY.md Index

Maintain a `MEMORY.md` file in the memory directory as a persistent index:

- Each memory = one `.md` file with YAML frontmatter (`name` / `description` / `type`)
- `MEMORY.md` stores only links to memory files + one-line descriptions, never full content
- Trim and merge old entries when the index exceeds 200 lines

**At conversation start**: Check whether `MEMORY.md` exists. If it does, read the index and surface relevant memories to the user.

**Before context limit**: Proactively write important content from the current session into memory files and update `MEMORY.md`, so the next session can resume seamlessly.

## Memory File Format

```markdown
---
name: memory-name
description: One-line summary (used to assess relevance from the index)
type: user | feedback | project | reference
---

Memory content here.
```

## Four Memory Types

### user — User Profile

Stores the user's role, goals, preferences, and knowledge background.

**When to write**: When you learn about the user's role, tech stack, or communication style.

```markdown
---
name: user_profile
description: Senior Go engineer, new to React frontend
type: user
---

- 10 years of Go experience, strong backend background
- Just getting started with React — frame frontend concepts as backend analogues
- Communication style: concise and direct, dislikes verbose explanations
```

### feedback — Behavior Correction

Records behaviors the user has corrected. **Highest priority** — always follow these rules in future sessions.

**When to write**: When the user says "don't do that", "stop doing…", or any explicit correction.

Lead with the rule, then `**Why:**` (reason given) and `**How to apply:**` (scope).

```markdown
---
name: feedback_no_db_mock
description: Integration tests must use a real database, never mocks
type: feedback
---

Integration tests must connect to a real database — mocking is not allowed.

**Why:** A prior incident where mocked tests passed but the prod migration failed.

**How to apply:** Any test involving database operations must connect to the test database directly.
```

### project — Project Context

Records goals, key decisions, owners, and deadlines that cannot be inferred from the codebase.

**When to write**: When you learn the motivation behind a decision, a milestone, or a constraint.

Always convert relative dates ("next Friday") to absolute dates before writing.

```markdown
---
name: project_auth_rewrite
description: Auth middleware rewrite is compliance-driven, not tech debt
type: project
---

Auth middleware rewrite. Target completion: 2026-04-01.

**Why:** Legal flagged session token storage as non-compliant with new regulations.

**How to apply:** Scope decisions should prioritize compliance over engineering elegance.
```

### reference — External Resources

Records locations and purposes of external systems for quick lookup.

**When to write**: When you learn about a Linear project, Slack channel, dashboard, or any external resource.

```markdown
---
name: ref_linear_bugs
description: Pipeline bugs tracked in Linear project INGEST
type: reference
---

Pipeline bugs are tracked in Linear project "INGEST". Check there before investigating data pipeline issues.
```

## Write Rules

Before writing, scan `MEMORY.md` — update an existing entry if one applies, do not create duplicates.

**Never write to memory:**

- Passwords, API keys, tokens, or any credentials
- Secrets, private keys, or sensitive authentication data
- Code structure, file paths, or architecture conventions (derivable from the codebase)
- Temporary state from the current conversation
- Anything already in project documentation or git history

## Conversation Start Prompt

If `MEMORY.md` exists, output at conversation start:

> Local memory detected (N entries). Relevant memories: [list]
