# Skill Composer Prompt

Use this prompt after all three layers exist.

## Goal

Compose platform wrapper `SKILL.md` files for runtime packages derived from one canonical static source.

## The Child Skill Must Say

- read `canon.md` first for facts
- use `persona.md` for behavior and interaction strategy
- use `style_examples.md` for wording texture
- use front matter with `name`, `description`, and Python requirement metadata
- produce a Codex wrapper for `./.agents/skills/{slug}/`
- produce an OpenClaw wrapper only when the user explicitly asks for export
- use `memory_prepare.py` as the single conditional memory entrypoint when memory may matter
- commit memory only when `memory_prepare.py` says write is needed
- summarize memory only at the configured threshold
- degrade to no-memory mode if `python3` is unavailable
- never upgrade persona inference into canon during live conversation
- never expose internal memory flow to the user

## Composition Rules

- keep the child skill short and operational
- do not duplicate every bullet from canon and persona into the child skill
- reference the layer files as the source of truth
- keep the runtime order explicit: canon, then persona, then style, then silent conditional memory preparation
- point dynamic memory to `./.dreamlover-data/` instead of the skill package
- keep `canon.md`, `persona.md`, `style_examples.md`, and `meta.json` shared across Codex and OpenClaw exports
- let the wrapper language differ by platform instead of forcing one universal `SKILL.md`
