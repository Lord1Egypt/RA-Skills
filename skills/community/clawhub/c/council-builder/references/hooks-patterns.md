# On-Demand Hooks

Hooks are safety guardrails that activate when an agent is invoked. They prevent specific classes of mistakes during sensitive work.

## Structure

```
agents/[name]/hooks/
├── careful.md    # Blocks destructive commands
├── freeze.md     # Locks specific directories
└── README.md     # Lists available hooks and activation
```

## How Hooks Work

1. Agent reads `hooks/` directory when starting a task
2. Active hooks add constraints to the agent's behavior for that session
3. Hooks are opt-in: the coordinator or user activates them
4. Hooks are documented in plain markdown (not code), acting as instructions

## Hook Format

```markdown
# Hook: {{HOOK_NAME}}

**Trigger:** {{WHEN_THIS_HOOK_ACTIVATES}}

**Rules:**
- {{CONSTRAINT_1}}
- {{CONSTRAINT_2}}

**Override:** {{HOW_TO_BYPASS_IF_NEEDED}}
```

## Standard Hooks

### `/careful`
Blocks destructive commands during production work.
- No `rm -rf`, `drop table`, `force push`
- Require explicit confirmation for any write to production paths
- Log all state-changing commands before executing

### `/freeze`
Locks certain directories during debugging.
- Specified directories become read-only
- Prevents accidental changes while investigating issues
- Useful when multiple agents might touch the same files

## Role-Specific Hook Examples

### Research Agent
- **read-only**: Block all web writes, only allow reads and fetches
- **source-lock**: Only use pre-approved source list, no new sources

### Dev Agent
- **no-force-push**: Block force-push and history rewriting
- **protect-main**: Block direct commits to main/develop branches
- **no-delete**: Prevent file deletion, only allow moves to trash

### Content Agent
- **draft-only**: Block publish commands, all output stays in drafts/
- **no-external**: Block sending to any external platform

### Finance Agent
- **double-check**: Require two calculation methods for any number
- **no-round**: Prevent rounding until final output

### Ops Agent
- **confirm-send**: Require explicit approval before sending any message
- **no-delete-events**: Block calendar event deletion

## Activation

In AGENTS.md or during task assignment:
```
Task: Review production logs
Hooks: /careful, /freeze agents/dev/src/
```

The agent reads the hook files and applies constraints for the session.
