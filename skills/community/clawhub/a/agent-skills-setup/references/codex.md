# OpenAI Codex Skills Configuration

OpenAI Codex requires a specific structure to enable full UI and implicit invocation features.

## 1. Directory Scopes

### Global Scope

- **Path**: `~/.codex/skills/`

### Project Scope

- **Path**: `<project-root>/.agents/skills/`

## 2. Components of a Codex Skill

Codex skills follow the standard structure but have one unique requirement for UI integration:

- `SKILL.md`: **Required**. Metadata (name/description) + Instructions.
- `agents/openai.yaml`: **Optional but Recommended**. Configures UI metadata and invocation policies.

## 3. The `agents/openai.yaml` File

This file must reside in an `agents/` subdirectory within the skill folder.

```yaml
interface:
  display_name: "Skill Proper Name"
  short_description: "Concise summary (25-64 chars)"
policy:
  allow_implicit_invocation: true # Default is true
```

## 4. Triggering and Discovery

- **Implicit**: Codex automatically matches the prompt against the `description` in `SKILL.md`.
- **Explicit**: Trigger via `$skill-name` or `/skills`.
- **Precedence**: Project skills override global skills.

## 5. Sync From Antigravity

If Codex should mirror Antigravity global skills, run:

```bash
~/.gemini/antigravity/skills/agent-skills-setup/scripts/sync-global-skills.sh --targets codex
```

The sync script preserves Codex internal `.system/` content while updating user-managed skills.
