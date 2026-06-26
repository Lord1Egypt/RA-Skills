## ClawHub Runtime Notes

- This is an orchestrator skill, not a single-file skill.
- It depends on installable or locally available downstream skills:
  - `agent-spectrum`
  - `resonance-contract`
  - `tomorrowdao-agent-skills`
  - `portkey-ca-agent-skills`
- Task 3 may ask for the `CA keystore password` once when a real write needs the active `CA` context.
- Task 4 still depends on the remote live skill at `https://www.shitskills.net/skill.md`.
- No hidden private-key fallback is allowed in this distribution, and no undeclared secret dependency should be introduced.
- This built directory is the intended publish target on ClawHub; do not substitute the repository root.
