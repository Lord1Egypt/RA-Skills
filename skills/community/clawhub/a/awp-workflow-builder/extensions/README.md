# AWP Skill Extensions

Extensions customize the AWP base skill for specific domains, platforms, or
organizational requirements.  They work like class inheritance: the base skill
(`skill/SKILL.md`) defines the protocol and generation process; an extension
overrides or extends specific parts without rewriting the whole skill.

## How It Works

```
skill/SKILL.md                  <-- Base skill (protocol + generation)
       |
       +-- adapters/            <-- Platform layer  (HOW agent.py is written)
       |     standalone.md
       |
       +-- extensions/           <-- Domain layer    (WHAT gets generated)
             financial.md
             devops.md
             your-custom.md
```

An AI assistant loads the files in order:

1. **Base skill** (`SKILL.md`) -- protocol rules, generation phases, templates
2. **Adapter** (`adapters/*.md`) -- platform-specific agent.py generation
3. **Extension** (`extensions/*.md`) -- domain overrides, extra rules, templates

The extension can override any part of the base skill.  When there is a
conflict, the extension wins -- just like a subclass method overrides the
parent.

## Extension Format

Every extension file follows this structure:

```markdown
# AWP Extension: {Name}

## Extends

base: skill/SKILL.md
adapter: skill/adapters/{platform}.md    # optional, default: standalone

## Description

{What this extension does and when to use it.}

## Defaults

{Override default values from the base skill.}

defaults:
  compliance_level: L3
  model: anthropic/claude-sonnet-4
  execution_mode: parallel

## Required Agents

{Agents that MUST be present in every workflow built with this extension.}

agents:
  - id: {agent_id}
    role: {role}
    description: {what it does}
    tools: [tool.a, tool.b]

## Required Output Fields

{Fields that MUST appear in every agent's output.contract,
 in addition to the base `confidence` field.}

fields:
  - name: {field_name}
    type: {type}
    description: {description}
    required: true

## Additional Rules

{Domain-specific rules on top of R1-R24.}

- **{ID}:** {rule description}

## Constraints

{Hard limits or policies.}

- denied_tools: [shell.execute, file.write]
- required_memory_tiers: [long_term, daily_log]
- min_compliance: L3

## Additional Templates

{Extra template files or overrides.}

templates:
  - file: SYSTEM_PROMPT_PREFIX.md
    inject: prepend                        # prepend | append | replace
    content: |
      {markdown content injected into every agent's system prompt}

  - file: output_fields.yaml
    description: Extra output contract fields added to every agent

## Additional Skills

{Project-level skills automatically included.}

skills:
  - name: {skill_name}
    content: |
      {skill content in markdown}

## Additional Tools

{Custom MCP tools automatically included.}

tools:
  - fqn: {namespace.action}
    description: {what it does}
    template: |
      {Python code for the tool}
```

## How an AI Uses an Extension

When a user says "build me a financial workflow", the AI:

1. Loads `SKILL.md` (base generation process)
2. Loads the adapter (e.g., `adapters/standalone.md`)
3. Loads the extension (e.g., `extensions/examples/financial.md`)
4. Merges the instructions:
   - Base rules R1-R24 apply
   - Extension rules (F1, F2, ...) apply additionally
   - Extension defaults override base defaults
   - Required agents from the extension are added to the graph
   - Required output fields are added to every contract
   - Constraints restrict what the AI can generate
   - Additional templates are injected into generated files
   - Additional skills are placed in `{workflow}/skills/`
   - Additional tools are placed in `{workflow}/mcp/`
5. Generates the workflow following all combined rules

## Composition

Extensions can reference other extensions for composition:

```markdown
## Extends

base: skill/SKILL.md
also:
  - extensions/examples/financial.md     # inherit financial rules
```

When composing, rules and constraints are **additive** (union of all rules),
defaults use **last-wins** (later extension overrides earlier), and
required agents are **merged** (union, no duplicates by id).

## Creating Your Own Extension

1. Copy `extensions/examples/financial.md` as a starting point
2. Adjust the sections to your domain
3. Place the file in `extensions/` (or any path the AI can read)
4. Tell the AI: "Use the {name} extension when building this workflow"

The AI will read your extension file alongside the base skill and apply
all overrides and additions automatically.
