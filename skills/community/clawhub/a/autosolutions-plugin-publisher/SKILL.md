---
name: plugin-publisher
description: >
  End-to-end plugin creation and publishing for Claude Code, Cowork, and OpenClaw.
  Handles the full lifecycle: design the plugin, scaffold it in the correct Anthropic
  marketplace format, generate an OpenClaw install script, create or connect to a GitHub
  repo, push it, and package a .plugin file for direct Cowork installation.
  
  Use this skill whenever the user says "create a plugin", "publish a plugin",
  "make a marketplace plugin", "push plugin to GitHub", "package a plugin",
  "turn this into a plugin", "make this installable", "publish to marketplace",
  or wants to convert existing skills/agents/workflows into a distributable plugin.
  Also trigger when the user asks to "update my plugin repo", "restructure my plugin",
  or "add a new plugin to my marketplace". Even if they just say "plugin" in the
  context of creating or distributing something, this skill is probably what they need.
---

# Plugin Publisher

Create, package, and publish Claude plugins that work across Claude Code, Cowork desktop,
and OpenClaw — with correct Anthropic marketplace structure and GitHub integration.

## Why This Matters

Plugins that don't follow the exact Anthropic marketplace directory convention won't install
correctly in Cowork. The marketplace system expects a specific layout — this skill encodes
that layout so you never have to guess. It also generates OpenClaw compatibility automatically,
so every plugin you create works in both ecosystems.

## Quick Reference: What Goes Where

```
marketplace-repo/                      ← GitHub repo (one per marketplace)
├── .claude-plugin/
│   └── marketplace.json               ← Catalog listing all plugins in this marketplace
├── my-plugin/                         ← Plugin dir AT REPO ROOT (not nested!)
│   ├── .claude-plugin/
│   │   └── plugin.json                ← Plugin manifest
│   ├── skills/
│   │   └── skill-name/SKILL.md        ← Skills (triggered automatically)
│   ├── commands/
│   │   └── command-name.md            ← Slash commands (invoked explicitly)
│   ├── agents/
│   │   └── agent-name.md              ← Subagent definitions
│   ├── .mcp.json                      ← MCP server connections (optional)
│   ├── CONNECTORS.md                  ← Tool-agnostic placeholders (optional)
│   └── README.md
├── another-plugin/                    ← Additional plugins in same marketplace
│   └── ...
├── openclaw-install.sh                ← Generated OpenClaw deployer
└── README.md                          ← Marketplace-level documentation
```

**Critical rule**: Each plugin directory lives at the REPO ROOT, not nested under `plugins/`.
The `marketplace.json` source path is `"./my-plugin"`, never `"./plugins/my-plugin"`.
This matches how Anthropic's own `knowledge-work-plugins` marketplace works.

Read `references/marketplace-structure.md` for the complete format specification before
creating any files.

## Workflow

### Phase 1: Understand What We're Building

Determine the scope through conversation:

1. **What does this plugin do?** — Get a clear description of the plugin's purpose.
2. **What components does it need?** — Skills, commands, agents, hooks, MCP servers?
3. **Is this a new marketplace or adding to an existing one?** — Check if the user already
   has a marketplace repo on GitHub.
4. **Who's the audience?** — Internal use only, or shared publicly? This affects whether
   to use `~~placeholder` connectors.

If the user already has skills, agents, or workflows in this session or in files, offer to
convert them directly rather than starting from scratch.

### Phase 2: Scaffold the Plugin

Create all files in a working directory, following this exact order:

#### 2a. Plugin manifest

Write `.claude-plugin/plugin.json`:
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "What it does in one sentence",
  "author": {
    "name": "Author Name",
    "url": "https://example.com"
  },
  "homepage": "https://github.com/owner/repo",
  "license": "MIT",
  "keywords": ["relevant", "keywords"]
}
```

Name rules: kebab-case, lowercase, hyphens only, no spaces.

#### 2b. Skills

Each skill is a directory with a `SKILL.md` file. Skills trigger automatically when Claude
detects a matching user request.

```yaml
---
name: skill-name
description: >
  Third-person description with trigger phrases.
  "When the user asks to X, Y, or Z, use this skill."
---
```

Body: imperative instructions, under 3,000 words. Use `references/` for detailed content.

#### 2c. Commands

Each command is a `.md` file with optional YAML frontmatter. Commands are invoked explicitly
by the user (e.g., `/plugin-name:command`).

```yaml
---
description: Short description (under 60 chars)
allowed-tools: Read, Write, Edit, Bash, WebSearch
argument-hint: [concept-description]
---
```

Body: directives FOR Claude to follow. Use `$ARGUMENTS` for user input.

#### 2d. Agents

Each agent is a `.md` file with YAML frontmatter. Agents are subagent definitions that run
in isolated context windows.

```yaml
---
name: agent-name
description: When to use this agent, with <example> blocks
model: sonnet
allowed-tools: Read Write WebSearch WebFetch
---
```

Body: system prompt for the subagent.

#### 2e. MCP Servers (if needed)

Write `.mcp.json` at plugin root. Use `${CLAUDE_PLUGIN_ROOT}` for local paths.
Use `${ENV_VAR}` for secrets. Document required env vars in README.

#### 2f. CONNECTORS.md (if sharing externally)

Only create this if the plugin references external tools by category (`~~chat`, `~~project tracker`).

#### 2g. README.md

Write a plugin-level README covering: overview, components, setup, usage.

### Phase 3: Create the Marketplace Wrapper

Wrap the plugin in a marketplace structure. Read `references/marketplace-structure.md` for
the exact `marketplace.json` format.

Write `.claude-plugin/marketplace.json` at the repo root:
```json
{
  "name": "marketplace-name",
  "owner": { "name": "Owner Name", "email": "email@example.com" },
  "metadata": { "description": "What this marketplace offers", "version": "1.0.0" },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugin-name",
      "description": "Plugin description",
      "version": "1.0.0",
      "author": { "name": "Author Name" },
      "homepage": "https://github.com/owner/repo",
      "license": "MIT",
      "keywords": ["keyword1", "keyword2"],
      "category": "category-name",
      "tags": ["tag1", "tag2"]
    }
  ]
}
```

Write a marketplace-level README.md covering:
- What plugins are available
- Install instructions for Cowork, Claude Code, and OpenClaw
- Repo structure diagram
- How the plugin works (architecture overview)

### Phase 4: Generate OpenClaw Compatibility

Every plugin gets an `openclaw-install.sh` at the repo root. Read
`references/openclaw-template.md` for the template and adaptation rules.

The script translates the Claude plugin structure into an OpenClaw agent workspace:
- Skills → `skills/` directory
- Agents → agent prompts inside `skills/[methodology]/agents/`
- Commands → incorporated into AGENTS.md operating instructions
- SOUL.md → personality, boundaries, tone (derived from plugin description)
- AGENTS.md → operating instructions, pipeline logic
- MEMORY.md → continuity structure

Key adaptation: OpenClaw runs everything in a single context window. Agent prompts that
assume independent subagent execution need a "mental isolation" discipline section.

### Phase 5: Push to GitHub

Check if a repo already exists or create a new one:

**If the user has `gh` CLI available (Claude Code / local terminal):**

```bash
# Create new repo
gh repo create owner/repo-name --public --description "Description" --clone
cd repo-name

# ... copy all files ...

git add -A
git commit -m "Initial release: plugin-name marketplace v1.0.0"
git push origin main
```

**If in Cowork (no git access):**

Prepare all files in the outputs directory and generate a PowerShell script the user
can run locally. The script should:

1. Clone or create the repo
2. Copy/restructure files
3. Commit with a descriptive message
4. Stop before pushing (let user review)
5. Print the `git push` command to run

Always detect the user's OS (check for Windows paths, PowerShell indicators) and generate
the appropriate script format (`.ps1` for Windows, `.sh` for Mac/Linux).

**If adding to an existing marketplace repo:**

1. Clone the existing repo
2. Add the new plugin directory at root level
3. Update `marketplace.json` to add the new plugin entry
4. Update the marketplace README
5. Commit and push

### Phase 6: Package as .plugin File

Create a `.plugin` file (a zip) for direct Cowork installation:

```bash
cd /path/to/plugin-dir
zip -r /tmp/plugin-name.plugin . -x "*.DS_Store"
cp /tmp/plugin-name.plugin /path/to/outputs/
```

Always create the zip in `/tmp/` first, then copy to outputs. The `.plugin` file renders
as an interactive card in Cowork where the user can browse files and install with one click.

### Phase 7: Present Everything

Deliver to the user:
1. The `.plugin` file for immediate Cowork installation
2. The push script (if in Cowork) or confirmation that the repo is pushed (if in Claude Code)
3. Install instructions for all three platforms:
   - **Cowork**: drag the .plugin file, or `/plugin marketplace add owner/repo`
   - **Claude Code**: `/plugin marketplace add owner/repo` then `/plugin install name@marketplace`
   - **OpenClaw**: `git clone` + `bash openclaw-install.sh`

## Adding a Plugin to an Existing Marketplace

When the user already has a marketplace repo and wants to add a new plugin:

1. Clone the existing repo
2. Create the new plugin directory at root level
3. Add the plugin entry to the existing `marketplace.json` plugins array
4. Generate/update the OpenClaw install script to handle the new plugin
5. Update the marketplace README with the new plugin
6. Commit, push, and package

## Converting Existing Work to a Plugin

When the user says "turn this into a plugin" or has skills/agents/workflows already built:

1. Identify all components in the current session or provided files
2. Map them to plugin component types (skills → skills/, agents → agents/, etc.)
3. Ensure frontmatter follows the correct schema (read `references/marketplace-structure.md`)
4. Wrap in marketplace structure
5. Proceed with Phase 5-7

## Updating an Existing Plugin

When the user wants to update a published plugin:

1. Clone the marketplace repo
2. Make the changes to the plugin files
3. Bump the version in both `plugin.json` and `marketplace.json`
4. Commit with a descriptive message noting the changes
5. Push and re-package the .plugin file

## Validation Checklist

Before declaring done, verify:

- [ ] `plugin.json` has `name` field (kebab-case)
- [ ] `marketplace.json` has correct `source` path (`"./plugin-name"`, not nested)
- [ ] Plugin directory is at repo root, not under `plugins/`
- [ ] All skills have `name` and `description` in frontmatter
- [ ] All agents have `name`, `description`, and `model` in frontmatter
- [ ] All commands have `description` in frontmatter
- [ ] README exists at both marketplace and plugin level
- [ ] OpenClaw install script references correct paths
- [ ] `.plugin` file contains all expected files
- [ ] No hardcoded absolute paths (use `${CLAUDE_PLUGIN_ROOT}` for intra-plugin refs)
