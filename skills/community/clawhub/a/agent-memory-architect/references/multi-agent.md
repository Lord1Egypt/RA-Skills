# Multi-Agent Memory

Share knowledge across agent teams while keeping each agent's behavior isolated.

## Architecture

```
~/agent-memory/
├── hot.md              # Main agent's HOT memory
├── agents/
│   ├── coder.md        # Coder's HOT memory
│   ├── writer.md       # Writer's HOT memory
│   └── daily.md        # Daily agent's HOT memory
├── domains/            # SHARED across all agents
│   ├── code.md
│   └── writing.md
├── projects/           # SHARED, loaded by context
│   └── my-app.md
└── archive/            # SHARED historical
```

## Memory Loading Rules

Each agent loads:
1. **Own HOT file** — `agents/{name}.md` (always)
2. **Shared domains** — `domains/*.md` (on context match)
3. **Shared projects** — `projects/*.md` (on context match)
4. **Main HOT** — `hot.md` (only if agent inherits global prefs)

### Example: 3-Agent Team

```
Main Agent (orchestrator):
  Load: hot.md + domains/* + projects/*

Coder Agent:
  Load: agents/coder.md + domains/code.md + projects/{active}.md

Daily Agent:
  Load: agents/daily.md + domains/* (read-only)
```

## Agent HOT File Format

Each `agents/{name}.md` follows the same format as `hot.md`:

```markdown
# HOT Memory — Coder Agent

## Confirmed Rules
- Always run tests before committing
- Use conventional commits format
- Prefer composition over inheritance

## Active Patterns
- User says "ship it" = merge and deploy (used 5x)

## Recent
- Use bun instead of node for scripts (1/3)
```

## Knowledge Flow

### Upward (agent → global)
When a pattern is useful across agents, promote to shared:

```
agents/coder.md has "use pnpm" (confirmed)
  → Also relevant for writer agent's tooling
  → Promote to domains/code.md
  → Remove from agents/coder.md
```

### Downward (global → agent)
Agents inherit global preferences unless overridden:

```
hot.md: "tone: direct" (global)
agents/writer.md: "tone: friendly" (override for writer)
  → Writer uses friendly, all others use direct
```

### Lateral (agent ↔ agent)
Agents share via `domains/` and `projects/`, never directly:

```
Coder learns "API uses snake_case"
  → Logs to domains/code.md (shared)
  → Writer agent picks it up next session
```

## Setup: Adding a New Agent

1. Create the agent HOT file:
   ```bash
   touch ~/agent-memory/agents/my-agent.md
   ```

2. Initialize with template:
   ```markdown
   # HOT Memory — My Agent

   ## Confirmed Rules

   ## Active Patterns

   ## Recent
   ```

3. Configure agent to load on startup:
   - Load `~/agent-memory/agents/my-agent.md` (always)
   - Load `~/agent-memory/domains/*.md` (on context match)
   - Load `~/agent-memory/projects/*.md` (on context match)

## Conflict Between Agents

When two agents learn contradictory patterns:

1. Each agent's own HOT takes priority for that agent
2. Shared files (domains/projects) use most-recent-wins
3. Log conflict for user review:
   ```
   ⚠️ Conflict: coder.md says "tabs", writer.md says "spaces"
   Resolution: each agent keeps own preference.
   Shared code.md: not set (ask user)
   ```

## Scaling

| Team Size | Strategy |
|-----------|----------|
| 1 agent | Just use hot.md, skip agents/ |
| 2-5 agents | agents/ + shared domains/ |
| 5+ agents | Add agent-groups for inheritance |

### Agent Groups (5+ agents)

```
~/agent-memory/
├── groups/
│   ├── engineering.md    # Shared by coder, architect, devops
│   └── content.md        # Shared by writer, editor, social
├── agents/
│   ├── coder.md          # Inherits: engineering
│   ├── architect.md      # Inherits: engineering
│   ├── writer.md         # Inherits: content
│   └── editor.md         # Inherits: content
```
