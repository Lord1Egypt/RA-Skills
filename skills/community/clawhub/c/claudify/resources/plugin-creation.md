# Plugin Creation Guide

Guide for open-source plugin distribution.

## Naming Restrictions

**IMPORTANT**: Marketplace names cannot impersonate official Anthropic/Claude marketplaces.

Reserved patterns (will be rejected):
- Names containing "official", "anthropic", or "claude" in official-sounding combinations
- Examples: `claude-plugins`, `anthropic-official`, `official-claude-tools`

Valid names:
- `es6kr-plugins`
- `mycompany-tools`
- `awesome-cc-plugins`

## Marketplace Structure

A marketplace is a repository containing multiple plugins.

```
marketplace-repo/                    # e.g., es6kr-plugins (NOT claude-plugins)
├── .claude-plugin/
│   └── marketplace.json            # Required: marketplace metadata
├── plugins/                        # Plugins folder
│   ├── code-quality/               # Individual plugin
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── agents/
│   │   ├── skills/
│   │   ├── commands/
│   │   └── README.md
│   └── another-plugin/
├── external_plugins/               # External plugin references (optional)
└── README.md
```

## marketplace.json Structure

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "marketplace-name",
  "description": "Marketplace description",
  "owner": {
    "name": "[Collect via AskUserQuestion]",
    "email": "[Collect via AskUserQuestion]"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "description": "Plugin description",
      "version": "1.0.0",
      "author": {
        "name": "[Same as owner or specify separately]",
        "email": "[Same as owner or specify separately]"
      },
      "source": "./plugins/plugin-name",
      "category": "productivity",
      "homepage": "https://github.com/owner/repo/tree/main/plugins/plugin-name"
    }
  ]
}
```

## Individual Plugin Structure

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json                 # Plugin metadata (optional)
├── agents/                         # Agent files
│   └── agent-name.md
├── skills/                         # Skill folders
│   └── skill-name/
│       └── SKILL.md
├── commands/                       # Slash commands
│   └── command-name.md
├── hooks/                          # Hook config (optional)
│   └── hooks.json
└── README.md                       # Plugin description
```

## Categories

| Category | Description |
|----------|-------------|
| `development` | Dev tools, LSP, SDK |
| `productivity` | Workflow, commit, PR |
| `testing` | Testing, E2E |
| `security` | Security checks |
| `learning` | Educational, explanatory |
| `database` | DB integration |
| `deployment` | Deployment |
| `monitoring` | Monitoring |
| `design` | Design |

## Metadata Collection

Collect via **AskUserQuestion** when creating marketplace:

```json
{
  "questions": [
    {
      "question": "Enter marketplace owner information",
      "header": "Owner",
      "options": [
        {"label": "Enter manually", "description": "Provide name and email"},
        {"label": "Use existing", "description": "Reuse previously entered info"}
      ],
      "multiSelect": false
    }
  ]
}
```

Additional items (if Other selected):
- Owner/author name
- Email address
- GitHub repository URL

## Workflow

### 1. Create Marketplace Repository

```bash
# Create with ghq
ghq create github.com/username/marketplace-name

# Create basic structure
cd $(ghq root)/github.com/username/marketplace-name
mkdir -p .claude-plugin plugins
```

### 2. Write marketplace.json

Create `.claude-plugin/marketplace.json` after collecting metadata.

### 3. Add Plugins

```bash
# Create new plugin directory
mkdir -p plugins/plugin-name/{agents,skills,commands}

# Copy existing automation
cp ~/.claude/agents/agent-name.md plugins/plugin-name/agents/
cp -r ~/.claude/skills/skill-name/ plugins/plugin-name/skills/
```

### 4. Generalize

When converting personal automation to open source:

- [ ] Remove hardcoded paths (e.g., `/Users/john/` → relative paths)
- [ ] Remove personal info (e.g., IP addresses, domains, names)
- [ ] Make configurable via environment variables
- [ ] Update description to be universal
- [ ] Write English README (for international distribution)

### 5. Write README

Include `README.md` for each plugin:
- Plugin description
- List of included agents/skills/commands
- Usage examples
- Configuration (if any)

### 6. Test

```bash
# Test local plugin installation
claude /install-plugin /path/to/plugins/plugin-name
```

### 7. Deploy

1. Push marketplace repository to GitHub
2. Visit claudemarketplaces.com
3. Request marketplace registration
4. Approval after review

## Official Marketplace Reference

Check official plugin marketplace structure:
- Location: `~/.claude/plugins/marketplaces/claude-plugins-official/`
- Repository: `anthropics/claude-plugins-official`

## Local Development Location

Develop directly in marketplaces folder:
- `~/.claude/plugins/marketplaces/marketplace-name/`

Then add via Claude Code:
```bash
~/.claude/plugins/marketplaces/marketplace-name
```

## License Considerations

### Using external code

When incorporating code from other projects:

1. **Check the license** of the source project
2. **BSD 3-Clause** (e.g., PyTorch): Can use with MIT, but must include BSD notice in the file
3. **MIT/Apache**: Generally compatible, include attribution

Example BSD notice in file:
```markdown
<!--
This file is derived from:
https://github.com/org/repo/path/to/file
Copyright (c) [Year] [Contributors]
Licensed under BSD 3-Clause License
SPDX-License-Identifier: BSD-3-Clause
-->
```

### Plugin dependencies

**Currently not supported.** Each plugin is independent.

Workaround for complementary plugins:
- Document in README that another plugin is recommended
- Name plugins to show relationship (e.g., `commit-reviewer` vs official `code-review`)
- Explain differences from similar official plugins
