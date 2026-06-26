# Agent Team Skill

AI agent team management tool for managing team member information, including skills, roles, and task delegation.

**This skill must be used together with the OpenClaw plugin.**

## How It Works

The skill consists of two components that work together:

1. **Plugin** (`integrations/openclaw/agent-team/`) - OpenClaw native plugin that automatically injects team information and collaboration rules into system context at session start
2. **Skill** (`scripts/team.py`) - CLI tool for managing team member data (CRUD operations)

The plugin reads team data from `~/.agent-team/team.json` and injects it into the AI agent's context, enabling:
- Team member awareness
- Leader authority (approve completion, reassign tasks)
- PDCA workflow: Plan → Do → Check → Act
- Task delegation rules
- Progress recording in `memory/YYYY-MM-DD.md`

## Features

- 👥 **Member Management** - Manage team member information including skills, roles, and task assignment
- 👑 **Leader Authority** - Leader can approve task completion and reassign when delegation fails
- 🔄 **PDCA Workflow** - Plan → Do → Check → Act task processing cycle
- 📝 **Progress Recording** - Track task progress in `memory/YYYY-MM-DD.md`
- ⚡ **Auto Injection** - Plugin automatically loads team information at session start
- 🌐 **Global Sharing** - Team data is globally shared across sessions

## Installation

### Step 1: Install Plugin (Required)

The plugin must be installed for the skill to work properly.

```bash
# Method 1: Link to global extensions directory
ln -s $(pwd)/integrations/openclaw/agent-team ~/.openclaw/extensions/agent-team

# Method 2: Specify path in config
# Edit ~/.openclaw/config.json
```

Config example:
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

For detailed configuration, see [integrations/openclaw/agent-team/README.md](./integrations/openclaw/agent-team/README.md).

### Step 2: Verify Python 3.10+

```bash
python3 --version
```

## Usage

### Managing Team Members

After installing the plugin, use the CLI to manage team data:

```bash
python3 scripts/team.py <command> [options]
```

| Command | Description |
|---------|-------------|
| `list` | List all members |
| `update` | Add/update member |
| `reset` | Reset member data |

### List Members

```bash
python3 scripts/team.py list
```

Output example:
```markdown
## Team Members

**Alice** ⭐ Leader - coordination,planning,decision-making
- agent_id: alice
- expertise: task breakdown, comprehensive decisions, agent coordination
- not_good_at: code development, investment analysis

**Bob** - Backend Developer - backend,API,database
- agent_id: bob
- expertise: Python,Go,PostgreSQL
- not_good_at: frontend,design

# Total: 2 member(s), Leader: Alice (alice)
```

### Add/Update Member

```bash
python3 scripts/team.py update \
  --agent-id "agent-001" \
  --name "Alice" \
  --role "Backend Developer" \
  --is-leader "true" \
  --enabled "true" \
  --tags "backend,api,database" \
  --expertise "python,go,postgresql" \
  --not-good-at "frontend,design"
```

Parameters:
- `--agent-id`: Member unique identifier (required)
- `--name`: Member name (required)
- `--role`: Role/position (required)
- `--is-leader`: Whether team Leader (required, true/false, only one Leader per team)
- `--enabled`: Enable status true/false (required)
- `--tags`: Tags, comma-separated (required)
- `--expertise`: Expertise skills, comma-separated (required)
- `--not-good-at`: Weak areas, comma-separated (required)

### Reset Data

Clear all team data:

```bash
python3 scripts/team.py reset
```

## Custom Data File

Use `--data-file` to specify a custom data file path:

```bash
python3 scripts/team.py --data-file /path/to/team.json list
```

Default data location: `~/.agent-team/team.json`

## Data File Format

Data is stored in JSON format:

```json
{
  "team": {
    "agent-001": {
      "agent_id": "agent-001",
      "name": "Alice",
      "role": "Backend Developer",
      "is_leader": true,
      "enabled": true,
      "tags": ["backend", "api", "database"],
      "expertise": ["python", "go", "postgresql"],
      "not_good_at": ["frontend", "design"]
    }
  }
}
```

## Use Cases

- **Team Maintenance**: Record all members and their skill information
- **Task Assignment**: Assign tasks based on member expertise and tags

## Testing

```bash
python3 -m pytest tests/
```

Test coverage:
- `test_team.py` - Member management tests (15 tests)