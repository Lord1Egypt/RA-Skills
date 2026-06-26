# Agent Team Plugin

OpenClaw plugin that automatically injects team member information and collaboration rules into system context at session start.

## Why Use the Plugin?

The plugin provides these advantages over manually calling the skill:

1. **100% Reliable Loading**: Uses `before_prompt_build` hook to inject team information before session starts, no dependency on AI agent主动 calling tools
2. **Zero Startup Delay**: Team information is directly injected into system context without needing to guide AI to execute `python3 scripts/team.py list`
3. **Simplified Interaction**: AI agent gets team context directly, no extra steps needed

## What Gets Injected

The plugin injects:

- **Team Members**: Names, roles, expertise, and weaknesses
- **Leader Authority**: Approve task completion, reassign when delegation fails
- **Task Processing Flow**: Plan → Do → Check → Act (PDCA cycle)
- **Recording Rules**: Progress tracking in `memory/YYYY-MM-DD.md`
- **Task Delegation Rules**: Timing and process for delegating tasks to teammates

## Installation

### Method 1: Link to Global Extensions Directory (Recommended)

```bash
# Create symlink to OpenClaw global extensions directory
ln -s $(pwd) ~/.openclaw/extensions/agent-team
```

### Method 2: Specify Path in OpenClaw Config

Add to `~/.openclaw/config.json`:

```json
{
  "plugins": {
    "load": {
      "paths": ["/path/to/agent-team-skill/integrations/openclaw/agent-team"]
    },
    "entries": {
      "agent-team": {
        "enabled": true
      }
    }
  }
}
```

### Method 3: As Workspace Extension

Copy `integrations/openclaw/agent-team` directory to project's `.openclaw/extensions/` directory and enable in config:

```json
{
  "plugins": {
    "allow": ["agent-team"]
  }
}
```

## Configuration

Plugin supports these configuration options (set via `plugins.entries.agent-team.config`):

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `dataFile` | string | `~/.agent-team/team.json` | Team data file path |
| `enabled` | boolean | `true` | Enable or disable plugin |

Config example:

```json
{
  "plugins": {
    "entries": {
      "agent-team": {
        "enabled": true,
        "config": {
          "dataFile": "/custom/path/team.json"
        }
      }
    }
  }
}
```

## Data Format

Team data is stored in JSON format:

```json
{
  "team": {
    "agent-001": {
      "agent_id": "agent-001",
      "name": "Alice",
      "role": "Backend Developer",
      "is_leader": true,
      "enabled": true,
      "tags": ["backend", "database"],
      "expertise": ["python", "postgresql"],
      "not_good_at": ["frontend", "design"],
      "load_workflow": true,
      "group": "backend-team"
    }
  }
}
```

### New Fields (Optional)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `load_workflow` | boolean | `true` for leader, `false` for others | Whether to inject PDCA workflow prompts |
| `group` | string | `null` | Group name for categorizing members |

These fields are optional and backward compatible with older data files.

## How It Works

1. Plugin loads when OpenClaw Gateway starts
2. Every time AI prompt is built, `before_prompt_build` event triggers
3. Plugin receives `agentId` from OpenClaw context to identify current agent
4. Plugin reads team data file and formats as Markdown
5. **Leader Responsibilities section is only injected if current agent is the team leader**
6. Team information is appended to system context via `appendSystemContext`

### Context-Aware Injection

The plugin uses `PluginHookAgentContext.agentId` to determine which agent is running:

- **If current agent is the leader** (matches `team[id].is_leader === true`):
  - Injects full Team Members + Leader Authority
  - Injects Task Processing Flow only if `load_workflow` is true (default)

- **If current agent is NOT the leader**:
  - No team context is injected (plugin returns empty)

This ensures only the designated leader receives leadership-related prompts, and the PDCA workflow can be disabled per-member using `load_workflow: false`.

## Relationship with Skill

- **Skill** (`scripts/team.py`): Provides team member management (add, update, reset)
- **Plugin** (`integrations/openclaw/agent-team/`): Automatically injects team info and collaboration rules

They work together: use Skill CLI to manage team data, Plugin automatically injects data into AI context.

## Managing Team Data

Use the Python script to manage team members:

```bash
# List team members
python3 scripts/team.py list

# Add/update member
python3 scripts/team.py update \
  --agent-id "agent-001" \
  --name "Alice" \
  --role "Backend Developer" \
  --is-leader true \
  --enabled true \
  --tags "backend,database" \
  --expertise "python,postgresql" \
  --not-good-at "frontend,design" \
  --load-workflow true \
  --group "backend-team"

# Reset data
python3 scripts/team.py reset
```

## Slash Command

The plugin registers a `/agent-team` command that displays current team members:

```
/agent-team
```

This command returns a formatted list of all team members with their roles, expertise, and other details. It's useful for quickly checking the team configuration without invoking the AI agent.