# Skill Structure

## SKILL.md Requirements

**Filename:** `SKILL.md` (uppercase)
**File Size:** Less than 200 lines

### YAML Frontmatter

```yaml
---
name: skill-name
description: Brief description of what this skill does and when to use it.
---
```

**Metadata Quality:** The `name` and `description` determine when the Agent uses the skill. Be specific about what the skill does and when to use it.

### Writing Style

- Use imperative/infinitive form (verb-first instructions)
- Use objective, instructional language
- Example: "To accomplish X, do Y" rather than "You should do X"

### Content Organization

1. Purpose of the skill (a few sentences)
2. When the skill should be used
3. How to use the skill (reference bundled resources)
4. Reference section pointing to `references/` files

## Bundled Resources

### Scripts (`scripts/`)

- Executable code for deterministic reliability
- Prefer Node.js or Python over Bash (better Windows support)
- Include `requirements.txt` for Python scripts
- Follow `.env` file precedence: `process.env` > `%USERPROFILE%\.agent\skills\${SKILL}\.env` > `%USERPROFILE%\.agent\skills\.env` > `%USERPROFILE%\.agent\.env` (adjust paths based on Agent framework)
- Create `.env.example` files
- Always write tests
- **Windows Note**: For shell scripts, use `.ps1` (PowerShell) or `.bat` files instead of `.sh` files

### Reference Files (`references/`)

- Documentation loaded on-demand
- Keep files <200 lines when possible
- Can reference other Markdown files or scripts
- Sacrifice syntax for brevity when necessary
- Avoid duplication with SKILL.md

### Assets (`assets/`)

- Files not loaded into context
- Used in Agent-generated output
- Examples: templates, images, icons, fonts, boilerplate code
