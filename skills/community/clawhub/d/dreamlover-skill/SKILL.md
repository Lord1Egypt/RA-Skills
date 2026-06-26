---
name: dreamlover-skill
description: Always run intake first before creating or updating distilled agent skills for anime and game virtual characters. Use when the task requires separating canon, persona, and style examples, writing one canonical source, installing a Codex wrapper, and optionally exporting an OpenClaw wrapper.
---

# Dreamlover Skill

This repository is a meta-skill for building character skills from text-only source materials.

Use this skill when the user wants to:

- create a new character skill from raw notes, wiki pages, plot summaries, or quote collections
- correct an existing character because the facts are wrong, the behavior feels off, or the voice is weak
- merge new source materials into an existing character skill without collapsing canon and persona together
- inspect what character skills are installed in `./.agents/skills/` or archived in `characters/`

## Hard Intake Gate

If the user wants a new character skill but has not supplied enough intake information, stop and ask the intake questions before generating anything.
If intake is incomplete, you are forbidden to create, update, or modify any character files.

The minimum intake bundle is:

- source decision policy
- character name
- source work, or an explicit decision that the character is fully original
- source material types: official, plot, quotes, wiki, or user description
- whether low-confidence persona inference is allowed when materials are thin

If the user says only something like "create a Rem skill", do not jump straight to `canon`, `persona`, or `style_examples`.
Do not dump the full questionnaire in one message.
Use a slot-state intake model with these canonical slots:

- `source_policy`
- `input_mode`
- `character_name`
- `source_work`
- `material_types`
- `allow_low_confidence_persona`
- `archive_mirror`

Ask exactly one unresolved intake question at a time, wait for the user's answer, then ask the next needed question.
If a slot is already clearly answered, do not ask it again unless the answer is ambiguous, conflicts with another slot, or the user explicitly changes it.
Build the draft in memory first, then summarize the generated key factors for confirmation before writing files.

## Source Decision Policy

Before any generation work, ask which source completion policy is allowed:

1. only user-provided information
2. official material plus wiki material
3. official material plus user material
4. quick generate from official-style defaults

Then ask how the directly provided material will arrive:

1. direct text entered in chat or CLI
2. file paths that should be read first

Ask these in sequence:

1. ask only the source completion policy
2. if the user chooses only user-provided information or official plus user material, ask only the input mode
3. if the user chooses quick generate, skip the remaining intake questions
4. if the user chooses direct text, ask them to paste the source text
5. if the user chooses file paths, ask them for the paths and read those files first
6. if the character name was already in the user's request, ask only for name confirmation instead of asking for the name again
7. source work may be blank for a fully original character
8. if public completion is allowed and source work exists, ask for search scope: small, medium, or large
9. ask whether personality supplementation is allowed when the materials are thin

The first intake reply for an underspecified request should contain only question 1 plus its options.
Do not include question 2 or later questions in that first reply.

Do not ask for `target use` during the hard intake gate unless the user explicitly asks to customize it.
Use the default target use `openclaw roleplay conversation` when no explicit target use is supplied.

If the current branch still requires input mode and the user has not answered it yet, the hard intake gate is still incomplete.

## Core Workflow

Follow this order:

1. Run the hard intake gate first whenever the request is underspecified.
2. Collect and normalize the source materials.
3. Audit each source by reliability.
4. Build `canon` first.
5. Build `persona` from source materials plus the confirmed `canon`.
6. Extract `style_examples`.
7. Write one canonical static source under `characters/{slug}/`.
8. Compose a Codex wrapper `SKILL.md`.
9. Install the Codex runtime package under `./.agents/skills/{slug}/`.
10. Ask whether to export an OpenClaw runtime package.
11. If requested, ask for the OpenClaw workspace path and export a platform-specific wrapper there.
12. Keep dynamic memory outside the package and route it through the local memory scripts only when needed.

Do not skip the ordering. `persona` may depend on `canon`, but `canon` must not depend on `persona`.

## Layer Boundaries

`canon` may only contain:

- objective facts directly supported by source material
- explicit plot events
- explicit identity relationships
- explicit setting attributes
- explicit official statements

`canon` must never contain:

- interpretation
- psychology guesses
- behavior summaries
- style descriptions
- unverified lore

`persona` may only contain:

- behavior patterns summarized from materials
- emotional reaction tendencies
- interaction style
- relationship progression logic
- boundaries and preferences

`persona` must never contain:

- new facts presented as canon
- new plot events
- new identity data
- worldbuilding claims not grounded in source material

`style_examples` may only contain:

- address patterns
- rhythm and sentence habits
- verbal tics and recurring discourse markers
- short example lines

`style_examples` must never replace `canon` or `persona`.

## Files To Read

Read these files only when needed:

- `docs/PRD.md` for product goals and lifecycle
- `docs/evidence-model.md` for evidence priority and conflict handling
- `docs/canon-persona-boundary.md` for layer separation rules
- `docs/input-contract.md` for accepted source formats and intake minimums
- `docs/output-contract.md` for child skill layout
- `docs/safety.md` for content and copyright boundaries
- `references/memory_policy.md` for conditional memory rules

Use these prompts during execution:

- `prompts/intake.md`
- `prompts/source_audit.md`
- `prompts/canon_builder.md`
- `prompts/persona_builder.md`
- `prompts/style_examples_builder.md`
- `prompts/skill_composer.md`
- `prompts/correction_handler.md`
- `prompts/evolution_merge.md`

Use these tools when deterministic output helps:

- `tools/slugify.py`
- `tools/source_normalizer.py`
- `tools/evidence_indexer.py`
- `tools/style_extractor.py`
- `tools/skill_writer.py`
- `tools/skill_linter.py`
- `tools/version_manager.py`

Use these runtime memory scripts when composing or validating child skill behavior:

- `scripts/memory_prepare.py`
- `scripts/memory_router.py`
- `scripts/memory_fetch.py`
- `scripts/memory_commit.py`
- `scripts/memory_summarize.py`

Prefer `tools/skill_writer.py --interactive` when intake information is missing or incomplete.
In interactive mode, do not allow any writes before the intake summary is confirmed.

## Output Layout

Each generated character should first have one canonical static source under `characters/{slug}/`:

- `canon.md`
- `persona.md`
- `style_examples.md`
- `meta.json`
- `sources/normalized.json`
- `versions/`

Then install a Codex runtime package under `./.agents/skills/{slug}/` with a Codex-oriented `SKILL.md`.

If the user explicitly asks for OpenClaw export, also write `<openclaw_workspace>/.agents/skills/{slug}/` with an OpenClaw-oriented `SKILL.md`.

Static content must stay identical across Codex and OpenClaw runtime packages.
Dynamic memory must not be stored inside the character package. Use `./.dreamlover-data/` for local runtime memory storage.

Do not maintain two editable sources for the same character. Re-export from the canonical static source instead.

## Quality Bar

Before finishing:

- make sure the hard intake gate completed before generation if the request started underspecified
- make sure no character files were written before intake confirmation
- make sure `canon` contains only directly supported material
- make sure `persona` contains only summarized behavior
- make sure `style_examples` only handles language texture
- make sure corrections modify the right layer
- make sure the Codex child skill is discoverable from `./.agents/skills/{slug}/`
- make sure OpenClaw export is optional and only happens after the user confirms it
- make sure the installed package passes `tools/skill_linter.py` without errors
- make sure a snapshot exists after creation or major updates
- make sure the child skill only reads or writes memory when silent conditional routing says it should
- make sure the child skill never fabricates prior conversation history
- make sure the child skill never exposes internal memory flow to the user unless a real failure affects the answer
- make sure no runtime memory database is copied into exported skill directories
