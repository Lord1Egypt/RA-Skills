# Hermes Alignment Notes

This skill borrows the useful parts of Hermes-style skill design without depending on Hermes internals.

## Reusable Ideas

- Keep `SKILL.md` as the trigger plus workflow entry point.
- Use progressive disclosure: keep the main skill concise and move detailed material into `references/`.
- Prefer reusable scripts for deterministic or repeatedly rewritten logic.
- Validate skills with both static checks and realistic task prompts.

## How To Apply That Here

- Put triggering language in frontmatter `description`.
- Put the main workflow near the top of `SKILL.md`.
- Add `agents/openai.yaml` when the host product benefits from UI metadata.
- Keep references one level away from `SKILL.md`; do not create deep documentation trees.
- Bundle tests for helper scripts so the skill can be evolved safely.

## Compatibility Mindset

For OpenClaw-like systems, favor portable files:

- `SKILL.md`
- optional `agents/openai.yaml`
- optional `scripts/`
- optional `references/`

Avoid relying on hidden runtime state or product-specific features unless the target environment explicitly supports them.
