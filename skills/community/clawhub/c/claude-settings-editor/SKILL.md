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

## Example Requests
- Update project hooks without breaking existing settings.
- Change Claude permissions and MCP toggles in the right settings file.

## Inputs
- Requested configuration change
- Desired scope
- Existing settings state

## Outputs
- Validated JSON config edits
- Scope explanation
- Risk notes for sensitive changes

## Success Criteria
- Only the intended file was changed.
- JSON remains valid.
- Unrelated settings were preserved.

## Non-Goals
- Blind full-file rewrites
- Silent permission broadening

## Source Provenance
Derived from `src/skills/bundled/updateConfig.ts`.
