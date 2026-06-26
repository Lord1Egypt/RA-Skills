# OpenClaw Deployment — Template and Adaptation Rules

This reference documents how to generate an `openclaw-install.sh` script that translates
a Claude plugin into an OpenClaw agent workspace.

## Key Difference: Subagents vs Single Context

Claude Code/Cowork plugins can use **true subagents** — separate processes with isolated
context windows. OpenClaw runs everything in a **single agent context**. This means:

- Agent definitions become prompts the single agent reads and role-plays sequentially
- "Run in parallel" becomes "run sequentially with mental isolation"
- Skills remain skills (OpenClaw has its own skill loading)
- Commands become operating instructions in AGENTS.md

## OpenClaw Workspace Structure

```
~/.openclaw/agents/agent-name/
├── SOUL.md                     ← Identity, personality, boundaries
├── AGENTS.md                   ← Operating instructions, pipeline logic
├── MEMORY.md                   ← Continuity structure definition
├── memory/                     ← Daily memory files (YYYY-MM-DD.md)
├── skills/                     ← Methodology, reference docs
│   └── domain-name/
│       ├── SKILL.md
│       ├── ORCHESTRATOR.md     ← Derived from main command/skill
│       └── agents/             ← Individual agent prompts
│           ├── agent-a.md
│           └── agent-b.md
└── data/                       ← Working data directory
```

## Component Mapping

| Claude Plugin Component | OpenClaw Equivalent |
|------------------------|---------------------|
| `skills/*/SKILL.md` | `skills/*/SKILL.md` (direct copy) |
| `commands/*.md` | Logic folded into `AGENTS.md` |
| `agents/*.md` | `skills/[domain]/agents/*.md` (read as prompts) |
| `.mcp.json` | Not applicable (OpenClaw has its own MCP config) |
| `hooks/` | Not applicable |
| `CONNECTORS.md` | Not applicable |
| `plugin.json` | Not needed |

## SOUL.md Template

Derive from the plugin's description and README. Structure:

```markdown
# SOUL.md — [Agent Name]

You are **[Agent Name]** — [one-line role description].

[2-3 sentences expanding on what the agent does and its approach.]

## Personality

- **[Trait 1]**: [Description]
- **[Trait 2]**: [Description]
- **[Trait 3]**: [Description]

## Tone

- [Style guideline 1]
- [Style guideline 2]

## Boundaries

- [What it does]
- [What it doesn't do]
- [What it defers to humans on]

## Continuity

Each session, read your memory/ files and check data/ for in-progress work.
```

## AGENTS.md Template

This is the operating manual. Derive from the main command/skill orchestrator logic:

```markdown
# AGENTS.md — [Agent Name] Operating Instructions

## Session Startup

1. Read `SOUL.md`
2. Read `memory/` (today + yesterday)
3. Check `data/` for in-progress work
4. If work active, summarize status to user

## Primary Mission

[Describe what the agent does when triggered]

## The Methodology

Read `skills/[domain]/SKILL.md` before every run.
Read each agent prompt from `skills/[domain]/agents/` before executing that phase.

### Pipeline

[Describe the phase sequence]

### Single-context discipline

OpenClaw runs all perspectives in your single context. Unlike Claude Code subagents,
you must ENFORCE independence mentally:

- When switching to a new perspective, mentally reset
- Do not anchor on prior outputs when generating the next perspective
- Each perspective reads ONLY the shared input data
- Sequential perspectives that synthesize (like Devil's Advocate) read all prior outputs
```

## MEMORY.md Template

```markdown
# MEMORY.md

## Daily files (memory/YYYY-MM-DD.md)

After each run, log:
- Task performed
- Final output summary
- Key findings
- Open questions

## Working data (data/)

In-progress files. Final outputs stay here for reference.
```

## Script Generation Rules

When generating `openclaw-install.sh`:

1. **Detect plugin directory**: Use `$SCRIPT_DIR` to find the repo root, then locate
   the plugin directory. After marketplace restructuring, the plugin is at root level
   (e.g., `$SCRIPT_DIR/plugin-name/`), not nested under `plugins/`.

2. **Handle path changes**: The script must work whether run from the repo root or from
   a subdirectory. Always use `$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)` for `SCRIPT_DIR`.

3. **Copy methodology and agents**: Copy skill files directly. Copy agent `.md` files
   into a sub-directory of skills so the single-context agent can read them as prompts.

4. **Copy the orchestrator**: The main command or skill that drives the pipeline should
   be copied as `ORCHESTRATOR.md` alongside the methodology, so the agent knows the
   step-by-step workflow.

5. **Generate SOUL.md dynamically**: Based on the plugin's purpose. Don't copy a generic
   template — tailor the personality, boundaries, and tone to the specific plugin.

6. **Seed initial memory**: Create a `memory/YYYY-MM-DD.md` with installation metadata.

7. **Verify all files**: After copying, verify every expected file exists. Exit with
   error if anything is missing.

8. **Print next steps**: Show the user the `openclaw.json` config entry they need to add,
   a test command, and a log-viewing command.

## Script Template

See `scripts/openclaw-generator.sh` for the base template. When generating for a specific
plugin, customize:

- `AGENT_NAME` — from plugin name
- `PLUGIN_DIR` — path to plugin within repo
- `EXPECTED` array — list of all files that should exist after install
- `SOUL.md` content — tailored to the plugin
- `AGENTS.md` content — derived from the plugin's orchestrator
- `MEMORY.md` content — appropriate to the plugin's domain
- File copy commands — match the plugin's actual component structure

## Example: Plugin with Skills + Agents

For a plugin with 2 skills and 8 agents (like npd-validator):

```bash
# Copy skills
cp "$PLUGIN_DIR/skills/methodology/SKILL.md" "$WORKSPACE/skills/methodology/SKILL.md"
cp "$PLUGIN_DIR/skills/validate/SKILL.md" "$WORKSPACE/skills/methodology/ORCHESTRATOR.md"

# Copy agents as skill-readable prompts
for agent in "$PLUGIN_DIR/agents/"*.md; do
    cp "$agent" "$WORKSPACE/skills/methodology/agents/"
done
```

## Example: Plugin with Commands Only

For a simpler plugin with just commands:

```bash
# Fold command logic into AGENTS.md
# The AGENTS.md should contain the command instructions as "modes" or "workflows"
# that the single-context agent can execute on request
```

The key insight: OpenClaw has no `/slash-command` system. Everything the agent can do
is described in AGENTS.md, and the user triggers it through natural conversation.
