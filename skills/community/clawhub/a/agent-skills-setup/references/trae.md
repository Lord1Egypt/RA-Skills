# Trae / Trae CN Skills Configuration

Trae is ByteDance's AI-native IDE, available in two versions:
- **Trae (International)**: Global version
- **Trae CN (China)**: Chinese domestic version with Doubao-1.5-pro and DeepSeek models

## 1. Directory Structure

### Global Skills (User-Level)

Personal skills available in any workspace.

| Version | Global Path |
|---------|-------------|
| **Trae (International)** | `~/.trae/skills/` |
| **Trae CN (China)** | `~/.trae-cn/skills/` |

### Project-Level Skills

Repository-specific skills shared with your team via version control.

| Version | Project Path |
|---------|--------------|
| **Trae (International)** | `./.trae/skills/` |
| **Trae CN (China)** | `./.trae/skills/` |

## 2. Skill Anatomy

Each skill must be a directory containing:

```text
<skill-name>/
├── SKILL.md (Required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions
├── scripts/ (Optional) - Executable automation
├── references/ (Optional) - Detailed docs and schemas
└── assets/ (Optional) - Templates and resources
```

## 3. Installation Methods

### Method A: Using skills CLI (Recommended)

The `skills` CLI tool from [skills.sh](https://skills.sh/) provides unified skill management:

```bash
# Install a skill globally
npx skills add https://github.com/vercel-labs/skills --skill find-skills -g

# Install to specific agent (Trae)
npx skills add https://github.com/vercel-labs/skills --skill find-skills -a trae

# List installed skills
npx skills list          # Project level
npx skills ls -g         # Global level

# Search for skills
npx skills find typescript

# Update all skills
npx skills update
```

**CLI Options:**

| Option | Description |
|--------|-------------|
| `-g, --global` | Install globally (user-level) |
| `-a, --agent <agents>` | Specify target agents (trae, claude-code, cursor, etc.) |
| `-s, --skill <skills>` | Specify skill names to install |
| `--all` | Install all skills to all agents |

### Method B: Manual Installation

Create the skill directory and copy SKILL.md:

```bash
# Trae (International)
mkdir -p ~/.trae/skills/my-skill
cp SKILL.md ~/.trae/skills/my-skill/

# Trae CN (China)
mkdir -p ~/.trae-cn/skills/my-skill
cp SKILL.md ~/.trae-cn/skills/my-skill/

# Project-level (both versions)
mkdir -p ./.trae/skills/my-skill
cp SKILL.md ./.trae/skills/my-skill/
```

### Method C: Via Trae IDE UI

1. Open Trae IDE
2. Navigate to **Skills Center** (技能中心)
3. Click **Import Skill** (导入技能)
4. Choose **Custom Import** and paste skill content

## 4. Triggering Mechanism

Trae discovers skills based on the YAML frontmatter in `SKILL.md`:

```yaml
---
name: my-skill
description: "Clear description of when this skill should be triggered. Include keywords, use cases, and scenarios."
---
```

- `name`: Unique identifier (use kebab-case)
- `description`: Primary trigger mechanism - be comprehensive and specific

## 5. Skill Design Best Practices

### 5.1 Metadata Design

```yaml
---
name: go-microservice-skeleton
description: "Generate production-ready Go microservice skeleton with Gin, zap, pprof, and graceful shutdown. Use when creating new Go services or setting up Go project structure."
---
```

### 5.2 Progressive Information Architecture

Keep SKILL.md under 500 lines. Split detailed content:

```text
my-skill/
├── SKILL.md           # Main content (entry point)
├── advanced.md        # Advanced features
├── api-reference.md   # API documentation
└── samples/           # Code examples
```

### 5.3 Workflow Definition

For complex tasks, define explicit workflows with checklists:

```markdown
## Workflow

Before execution, copy this checklist and mark each step:

- [ ] Step 1: Analyze requirements and constraints
- [ ] Step 2: Design solution architecture
- [ ] Step 3: Implement core functionality
  - (Feedback loop) If design issues found, return to Step 2
- [ ] Step 4: Write tests
- [ ] Step 5: Review and optimize
```

### 5.4 Script Reliability

When using executable scripts, prioritize robustness:

```bash
# Good: Explicit error handling
if [ ! -f "./config.yaml" ]; then
    echo "ERROR: Config file not found"
    echo "HINT: Run 'init-config.sh' to generate default config"
    exit 1
fi

# Good: Self-explanatory output
echo "[PASS] Node.js version: v18.20.0 (required: >=18.0.0)"
echo "[FAIL] Docker not running"
echo "  SUGGESTION: Start Docker Desktop"
```

## 6. Hierarchy & Precedence

1. **Project Skills** (`./.trae/skills/`) take highest precedence
2. **Global Skills** (`~/.trae/skills/` or `~/.trae-cn/skills/`) are loaded as defaults

If a project skill has the same name as a global skill, the project version is used.

## 7. Migrating Skills Between Agents

### From Antigravity to Trae

```bash
# Trae (International)
for dir in ~/.gemini/antigravity/skills/*/; do
    skill_name=$(basename "$dir")
    mkdir -p ~/.trae/skills/$skill_name
    cp -r "${dir}"* ~/.trae/skills/$skill_name/
done

# Trae CN (China)
for dir in ~/.gemini/antigravity/skills/*/; do
    skill_name=$(basename "$dir")
    mkdir -p ~/.trae-cn/skills/$skill_name
    cp -r "${dir}"* ~/.trae-cn/skills/$skill_name/
done
```

### From Trae CN to Antigravity

```bash
for dir in ~/.trae-cn/skills/*/; do
    skill_name=$(basename "$dir")
    mkdir -p ~/.gemini/antigravity/skills/$skill_name
    cp -r "${dir}"* ~/.gemini/antigravity/skills/$skill_name/
done
```

### From Trae CN to VS Code Copilot

```bash
# Create VS Code skills directory
mkdir -p ~/.copilot-skills

# Copy SKILL.md files
for dir in ~/.trae-cn/skills/*/; do
    skill_name=$(basename "$dir")
    if [ -f "${dir}SKILL.md" ]; then
        cp "${dir}SKILL.md" ~/.copilot-skills/${skill_name}.md
    fi
done
```

Then add to VS Code settings.json:

```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    { "file": "~/.copilot-skills/skill-name.md" }
  ]
}
```

## 8. Anti-Patterns to Avoid

| Anti-Pattern | Wrong Example | Correct Approach |
|--------------|---------------|------------------|
| Over-generalization | "Help me write code" | "Generate REST API with Express and TypeScript following team standards" |
| Missing boundaries | No failure conditions | Explicitly list "Reject if no package.json found" |
| Skipping steps | "Then optimize code" | "Step 3: Run golangci-lint, fix all error-level issues" |
| Vague output | "Give suggestions" | "Output format: [Severity] Location - Issue - Fix Example" |
| Context pollution | One skill for full-stack | Split into frontend-setup and backend-api skills |

## 9. Troubleshooting

### Skills Not Loading

1. Check directory structure: `ls -la ~/.trae-cn/skills/`
2. Verify SKILL.md has valid YAML frontmatter
3. Restart Trae IDE

### Wrong Skill Triggered

1. Make description more specific with keywords
2. Use unique skill names (kebab-case)
3. Check for naming conflicts between global and project skills

### CLI Installation Fails

1. Ensure Node.js 16+ is installed
2. Try manual installation method

## 10. Sync From Antigravity

If Trae and Trae CN should mirror Antigravity global skills, run:

```bash
~/.gemini/antigravity/skills/agent-skills-setup/scripts/sync-global-skills.sh --targets trae,trae-cn
```

This creates `~/.trae/skills/` if it does not already exist.
3. Check file permissions

## 10. Resources

- **Skills Directory**: [skills.sh](https://skills.sh/)
- **Awesome Copilot**: [github.com/github/awesome-copilot](https://github.com/github/awesome-copilot)
- **Trae Official Documentation**: Built-in IDE help
