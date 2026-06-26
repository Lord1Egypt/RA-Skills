# Claude Code Skills Configuration

Claude Code (CLI) uses a robust skill system to extend the base model's capabilities with procedural knowledge and custom tools.

## 1. Global vs Project Skills

### Global Skills (User Wide)

Stored in the user's home directory. Useful for "superpower" skills available everywhere.

- **Path**: `~/.claude/skills/`

### Project Skills (Repository Specific)

Stored in the project root. Essential for project-specific business logic, schemas, and workflows.

- **Path**: `<project-root>/.claude/skills/`

## 2. Configuration & Hierarchy

- **Precedence**: Project-level skills override global skills with the same name.
- **Triggering**: Managed via the `SKILL.md` frontmatter.
- **Structure**: Uses the standard standard skill structure (SKILL.md, scripts/, references/, assets/).

## 3. Installation Workflow

1. Create a subdirectory under the appropriate skills path.
2. Add a `SKILL.md` file with a descriptive name and trigger description in the frontmatter.
3. Reload or restart Claude Code session to pick up new skills.

## 4. Best Practices

- Keep `SKILL.md` concise.
- Move large schemas or documentation into `references/`.
- Use `scripts/` for deterministic logic.

## 5. Sync From Antigravity

If Claude Code should stay aligned with Antigravity global skills, run:

```bash
~/.gemini/antigravity/skills/agent-skills-setup/scripts/sync-global-skills.sh --targets claude
```

For a full multi-IDE sync, omit `--targets`.
