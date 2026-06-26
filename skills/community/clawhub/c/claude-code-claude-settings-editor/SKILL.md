---
name: "claude_settings_editor"
description: "Use when the user wants to update Claude settings, hooks, permissions, MCP server toggles, or other JSON config safely and with scope awareness."
---

# Claude Settings Editor

Use this skill for `settings.json`, local overrides, and hook configuration.

## Workflow
1. Choose the correct settings file by scope: user, project, or local.
2. Read the current file before editing.
3. Apply the smallest valid JSON change.
4. Keep permissions, hooks, plugins, and MCP configuration syntactically valid.
5. Explain scope, precedence, and any risky config changes.

## Guardrails
- Do not replace a config file wholesale unless necessary.
- Preserve unrelated user settings.
- Warn before widening permissions or changing automation hooks broadly.

## Source Provenance
Derived from `src/skills/bundled/updateConfig.ts`.
