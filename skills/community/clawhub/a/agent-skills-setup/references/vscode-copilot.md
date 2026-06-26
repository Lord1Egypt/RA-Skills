# VS Code Copilot Skills Configuration

VS Code Copilot supports custom instructions through multiple configuration levels, offering flexibility for both personal workflows and team collaboration.

## 1. Configuration Levels

VS Code Copilot has **three** configuration levels:

| Level | Scope | Configuration Location |
|-------|-------|------------------------|
| **User (Global)** | All projects | `~/Library/Application Support/Code/User/settings.json` (macOS) |
| **Workspace** | Current workspace | `.vscode/settings.json` |
| **Project** | Current project (shared via git) | `.github/copilot-instructions.md` |

## 2. Global (User-Level) Configuration

### Method A: settings.json Direct Configuration

Edit your VS Code user settings:

**macOS**: `~/Library/Application Support/Code/User/settings.json`
**Windows**: `%APPDATA%\Code\User\settings.json`
**Linux**: `~/.config/Code/User/settings.json`

```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    {
      "text": "Always use arrow functions for callbacks. Avoid using var."
    },
    {
      "text": "Always include error handling in async functions."
    }
  ]
}
```

### Method B: Reference External Instruction Files (Recommended)

Create a global skills directory and reference instruction files:

```bash
mkdir -p ~/.copilot-skills
```

Create instruction files (e.g., `~/.copilot-skills/code-standards.md`):

```markdown
# Code Standards

- Use TypeScript strict mode
- Prefer functional components in React
- Always handle errors in async functions
- Use meaningful variable names
```

Reference in settings.json:

```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    { "file": "~/.copilot-skills/code-standards.md" },
    { "file": "~/.copilot-skills/testing-guidelines.md" },
    { "file": "~/.copilot-skills/security-rules.md" }
  ]
}
```

## 3. Project-Level Configuration

### Method A: .github/copilot-instructions.md (Recommended)

Create a `.github/copilot-instructions.md` file in your project root:

```markdown
# Project Coding Guidelines

## Tech Stack
- React 18 with TypeScript
- Tailwind CSS for styling
- React Query for data fetching

## Code Style
- Use functional components with hooks
- Prefer named exports
- Use Zod for runtime validation

## Testing
- Vitest for unit tests
- Testing Library for component tests
- 80% coverage minimum
```

### Method B: .github/instructions/ (Fine-grained)

Create instruction files for specific file patterns:

```
.github/
├── copilot-instructions.md      # General project instructions
└── instructions/
    ├── typescript.md            # TypeScript-specific rules
    ├── react.md                 # React component patterns
    └── python.md                # Python-specific rules
```

Each instruction file can target specific file patterns:

```markdown
---
applyTo: "**/*.ts,**/*.tsx"
---

# TypeScript Instructions

- Use strict type checking
- Avoid `any` type
- Use interface for object shapes
```

### Method C: .github/prompts/ (Slash Commands)

Create reusable slash commands for Copilot Chat:

```
.github/
└── prompts/
    ├── review.prompt.md         # /review command
    ├── test.prompt.md           # /test command
    └── docs.prompt.md           # /docs command
```

Example `review.prompt.md`:

```markdown
---
name: review
description: Review code for best practices
---

Review the selected code for:
1. Security vulnerabilities
2. Performance issues
3. Code style consistency
4. Missing error handling

Provide specific suggestions for improvement.
```

Usage in Copilot Chat: `/review`

## 4. Workspace Configuration

For workspace-specific settings (not shared via git):

Create `.vscode/settings.json`:

```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    {
      "text": "This workspace uses Node.js 20 and npm."
    }
  ]
}
```

## 5. Configuration Priority

When multiple configurations exist, Copilot merges them in this priority order:

1. **Project-level** (`.github/copilot-instructions.md`) - Highest
2. **Workspace-level** (`.vscode/settings.json`)
3. **User-level** (`settings.json`) - Base layer

## 6. Migrating Skills from Other Agents

To migrate skills from Antigravity/Claude Code to VS Code Copilot:

### Step 1: Create Global Skills Directory

```bash
mkdir -p ~/.copilot-skills
```

### Step 2: Copy SKILL.md Files

```bash
for dir in ~/.gemini/antigravity/skills/*/; do
    skill_name=$(basename "$dir")
    if [ -f "${dir}SKILL.md" ]; then
        cp "${dir}SKILL.md" ~/.copilot-skills/${skill_name}.md
    fi
done
```

### Step 3: Update settings.json

Generate the configuration:

```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    { "file": "~/.copilot-skills/skill-name-1.md" },
    { "file": "~/.copilot-skills/skill-name-2.md" }
  ]
}
```

### Step 4: Restart VS Code

Reload the window or restart VS Code to apply changes.

## 7. Awesome Copilot (Community Resources)

GitHub maintains an official community collection at [awesome-copilot](https://github.com/github/awesome-copilot):

| Resource | Description |
|----------|-------------|
| 🤖 Agents | Specialized Copilot agents with MCP integration |
| 📋 Instructions | Coding standards by file pattern |
| 🎯 Skills | Self-contained instruction bundles |
| 🔌 Plugins | Curated agent + skill packages |
| 🪝 Hooks | Automated triggers during sessions |

Install a plugin:

```bash
copilot plugin install <plugin-name>@awesome-copilot
```

## 8. Best Practices

1. **Global Skills**: Use for personal coding preferences and general best practices
2. **Project Skills**: Use for team standards, tech stack specifics, and project architecture
3. **Keep Instructions Concise**: Copilot has context limits; focus on essential rules
4. **Use File References**: External `.md` files are easier to maintain than inline text
5. **Version Control**: Commit `.github/` configurations for team consistency
6. **Test Changes**: Verify instructions work as expected after configuration changes

## 9. Troubleshooting

### Instructions Not Taking Effect

1. Ensure `github.copilot.chat.codeGeneration.useInstructionFiles` is enabled
2. Restart VS Code after configuration changes
3. Check file paths are correct (use `~` for home directory)
4. Verify JSON syntax in settings.json

### File Path Issues

- Use forward slashes `/` even on Windows
- Use `~` to reference home directory
- Relative paths are resolved from workspace root

## 10. Sync From Antigravity

If Copilot global instruction files should mirror Antigravity skills, run:

```bash
~/.gemini/antigravity/skills/agent-skills-setup/scripts/sync-global-skills.sh --targets copilot
```

The script rebuilds `~/.copilot-skills/*.md` from each Antigravity skill's `SKILL.md`.
