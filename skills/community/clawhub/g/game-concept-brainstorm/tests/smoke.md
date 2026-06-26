# Smoke Test

Bundle: `game-concept-brainstorm`
Version: `1.1.0`

## Prompt

Use `game-concept-brainstorm` on a fitting game-development task.

## Expected checks

- The agent recognizes the skill's stated purpose.
- The agent uses packaged references when `SKILL.md` points to `./shared/...`.
- The agent does not claim companion skills are bundled implicitly when they are separate installs.
- Companion skills referenced in this bundle: game-requirements-brainstorm, game-scope-profile, game-ux-flow-designer
