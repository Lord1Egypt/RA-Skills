# Smoke Test

Bundle: `game-backend-selector`
Version: `1.1.1`

## Prompt

Use `game-backend-selector` on a fitting game-development task.

## Expected checks

- The agent recognizes the skill's stated purpose.
- The agent uses packaged references when `SKILL.md` points to `./shared/...`.
- The agent does not claim companion skills are bundled implicitly when they are separate installs.
- Companion skills referenced in this bundle: game-web-2d-specialist, game-web-3d-specialist
