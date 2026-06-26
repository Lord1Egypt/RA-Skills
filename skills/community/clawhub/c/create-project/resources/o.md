---
description: Activate Orchestrix Agent (e.g., /o dev, /o sm --lang=zh)
---

# Orchestrix Agent Activation

## Available Agents

| ID | Agent | Description |
|----|-------|-------------|
| `dev` | Full Stack Developer | implementation, debugging, refactoring |
| `sm` | Scrum Master | story creation, epic management, agile guidance |
| `qa` | QA Engineer | E2E testing, quality verification |
| `architect` | Solution Architect | system design, tech selection, API design |
| `pm` | Product Manager | PRDs, product strategy, roadmap planning |
| `po` | Product Owner | backlog management, story refinement |
| `analyst` | Business Analyst | market research, competitive analysis |
| `ux-expert` | UX Expert | UI/UX design, wireframes, prototypes |
| `orchestrix-orchestrator` | Workflow Coordinator | multi-agent tasks |
| `orchestrix-master` | Master Agent | one-off tasks across domains |
| `decision-evaluator` | Decision Evaluator | execute decision rules |

## Language Support

Use `--lang=xx` to load agent content in a specific language:
- `--lang=en` - English (default)
- `--lang=zh` - Chinese / 中文

Examples:
- `/o dev` - Load Developer agent in English (default)
- `/o dev --lang=zh` - Load Developer agent in Chinese
- `/o sm --lang=zh` - Load Scrum Master agent in Chinese

## Action Required

**FIRST**: Parse `$ARGUMENTS` to extract agent ID and language option.

Arguments format: `[agent_id] [--lang=xx]`

Parsing rules:
1. If `$ARGUMENTS` is empty or blank → Show agent table, ask user to select
2. If `$ARGUMENTS` contains `--lang=xx` → Extract language code (en or zh)
3. Extract agent ID (everything before `--lang` or the entire argument if no `--lang`)

If `$ARGUMENTS` is empty or blank:
- Show the table above directly
- Ask user to select an agent
- **DO NOT** call ReadMcpResourceTool with empty arguments

If agent ID is provided, proceed to load the agent:

## Step 1: Read Agent Configuration

**CRITICAL**: You MUST use `ReadMcpResourceTool` (NOT prompts!) with the EXACT parameters below.

`ReadMcpResourceTool` only accepts `server` and `uri` parameters. Language MUST be encoded in the URI as a query parameter.

**Without language** (default English):
- server: `orchestrix`
- uri: `orchestrix://agents/{agent_id}.yaml`

**With language** (e.g., `--lang=zh`):
- server: `orchestrix`
- uri: `orchestrix://agents/{agent_id}.yaml?lang=zh`

### Examples

For `/o pm`:
```
ReadMcpResourceTool(server="orchestrix", uri="orchestrix://agents/pm.yaml")
```

For `/o pm --lang=zh`:
```
ReadMcpResourceTool(server="orchestrix", uri="orchestrix://agents/pm.yaml?lang=zh")
```

**DO NOT** use `orchestrix://prompts/` - agents are exposed as **resources**, not prompts!
**DO NOT** pass `lang` as a separate parameter - it MUST be in the URI query string.

## Step 2: After Loading Agent

1. Adopt the persona defined in the `agent` section completely
2. Follow `activation_instructions` exactly
3. Display greeting with agent name/role
4. Show the numbered command list from `commands.help.output_format`
5. Wait for user selection
