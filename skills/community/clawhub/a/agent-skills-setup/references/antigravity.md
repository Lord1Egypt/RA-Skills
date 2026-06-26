# Antigravity Skills Configuration

Antigravity uses a flexible skill system designed for both personal productivity and project-specific automation.

## 1. Directory Structure

Antigravity scans two primary locations for skills:

### Global (User-Level) Skills

Personal skills available in any workspace or folder.

- **Path**: `~/.gemini/antigravity/skills/`

### Project-Level Skills

Repository-specific skills shared with your team via version control.

- **Paths**:
  - `<project-root>/.agents/skills/` (Preferred)
  - `<project-root>/.agent/skills/`

## 2. Skill Anatomy

Each skill must be a directory containing:

- `SKILL.md`: Required. Contains manifest data and instructions.
- `scripts/`: Optional. Reusable automation scripts.
- `references/`: Optional. Documentation and patterns.
- `assets/`: Optional. Templates and static resources.

## 3. Triggering Mechanism

Antigravity discovers skills based on the YAML frontmatter in `SKILL.md`:

- `name`: The unique identifier.
- `description`: Detailed explanation of when the skill should trigger. Antigravity uses this for implicit invocation.

## 4. Hierarchy & Precedence

1. **Project Skills** take highest precedence. If a project skill has the same name as a global skill, the project version is used.
2. **Global Skills** are loaded as defaults.

## 5. Mirroring to Other IDEs

If Antigravity is your source of truth, use the bundled sync script from `agent-skills-setup`:

```bash
~/.gemini/antigravity/skills/agent-skills-setup/scripts/sync-global-skills.sh
```

This mirrors Antigravity global skills into Claude Code, OpenAI Codex, VS Code Copilot, Trae, and Trae CN.
