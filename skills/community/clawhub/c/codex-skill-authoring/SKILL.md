---
name: codex-skill-authoring
version: 1.0.0
description: Create, edit, and package new AgentSkills. Use when asked to create a skill, build a skill, author a skill, or when需要对技能进行创建、打包或审核。Triggers on phrases like "create a skill", "author a skill", "build a skill", "package a skill", "审核技能", or any request to make a new skill from scratch. Supports Chinese and English requests.
---

# Skill Authoring

Create modular, self-contained skills that extend agent capabilities.

## The 6-Step Workflow

```
1. Understand → 2. Plan → 3. Init → 4. Edit → 5. Package → 6. Iterate
```

## Step 1: Understand the Skill

Ask clarifying questions if needed. Understand:
- What functionality should this skill support?
- What are concrete usage examples?
- What should trigger this skill?

**When to skip**: When usage patterns are already clear.

## Step 2: Plan Reusable Contents

Identify what to bundle:
- **scripts/** — Executable code (Python/Bash) for deterministic tasks
- **references/** — Documentation to load when needed
- **assets/** — Files used in output (templates, icons)

## Step 3: Initialize the Skill

Always use `init_skill.py` — never create manually:

```bash
python3 <skill-creator>/scripts/init_skill.py <name> --path <output-dir> --resources scripts,references,assets
```

Example:
```bash
python3 /usr/local/lib/node_modules/openclaw/skills/skill-creator/scripts/init_skill.py my-skill --path /var/root/.openclaw/workspace/skills --resources scripts,references
```

## Step 4: Edit the Skill

### SKILL.md Structure

```markdown
---
name: skill-name
description: Clear description of what it does AND when to trigger it. Include Chinese triggers too.
---

# Skill Name

## Quick Start

## Details...
```

### Naming Rules
- Lowercase, hyphens only
- Under 64 characters
- Verb-led preferred (e.g., `pdf-edit`, `list-skills`)

### Key Principles
- **Concise**: Only add what the model doesn't already know
- **Progressive disclosure**: Keep SKILL.md lean, put details in `references/`
- **Imperative mood**: Use "do this" not "does this"

## Step 5: Package the Skill

```bash
python3 <skill-creator>/scripts/package_skill.py <path/to/skill-folder>
```

Output: `.skill` file (zip format).

**Validation runs automatically before packaging.**

## Step 6: Iterate

Test with real tasks, gather feedback, improve.

## Skill Template

```
skill-name/
├── SKILL.md           # Required: name + description + instructions
├── scripts/           # Optional: executable code
├── references/        # Optional: load-as-needed docs
└── assets/            # Optional: output files
```

## Quick Reference

| Resource | When to Use |
|----------|-------------|
| `scripts/` | Same code rewritten repeatedly |
| `references/` | Large docs the model should read on demand |
| `assets/` | Templates, images, boilerplate |

**Keep SKILL.md under 500 lines.** Move details to `references/`.
