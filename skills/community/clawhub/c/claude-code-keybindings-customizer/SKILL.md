---
name: "keybindings_customizer"
description: "Use when the user wants to customize Claude Code keybindings, rebind shortcuts, add chords, or edit `~/.claude/keybindings.json` safely."
---


# Keybindings Customizer

Use this skill for shortcut rebinding, unbinding, or chord creation.

## Workflow
1. Read the current keybindings file first.
2. Merge changes instead of replacing the entire file.
3. Keep schema and docs fields intact.
4. Validate against reserved and non-rebindable shortcuts.
5. Explain any conflicts or terminal-level limitations.

## Guardrails
- Never overwrite the full file blindly.
- Preserve unrelated existing bindings.
- Flag OS or terminal-reserved shortcuts before saving.

## Example Requests
- Rebind the external editor shortcut.
- Add a chord to toggle todos without overwriting my keybindings file.

## Inputs
- Requested key changes
- Existing keybindings file
- OS or terminal constraints

## Outputs
- Merged keybinding config
- Conflict explanations

## Success Criteria
- The file was merged, not clobbered.
- Reserved shortcuts were handled correctly.
- Schema and docs fields remain intact.

## Non-Goals
- Whole-file replacement for a small binding change

## Source Provenance
Derived from `src/skills/bundled/keybindings.ts`.
