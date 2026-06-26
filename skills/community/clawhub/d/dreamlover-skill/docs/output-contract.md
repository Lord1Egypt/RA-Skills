# Output Contract

## Character Package Layout

Each generated character now has one canonical static source under `characters/{slug}/`.

The canonical source contains:

- `canon.md`: factual layer
- `persona.md`: behavioral layer
- `style_examples.md`: wording layer
- `meta.json`: character metadata
- `sources/normalized.json`: normalized source bundle or merge result
- `versions/`: character-level snapshots

Codex is the primary installed runtime target and is written to `./.agents/skills/{slug}/`.

OpenClaw is an optional export target and is only written when the user explicitly chooses an OpenClaw workspace.
That export goes to `<openclaw_workspace>/.agents/skills/{slug}/`.

Each runtime package contains:

- `SKILL.md`: platform-specific wrapper
- `canon.md`
- `persona.md`
- `style_examples.md`
- `meta.json`
- `sources/normalized.json`
- `versions/`
- `runtime/`: copied local memory scripts needed by the wrapper

Dynamic memory is out-of-band and must not be written into the package files.
Local runtime memory should live under `./.dreamlover-data/`.

Interactive creation should persist the intake answers into:

- `meta.json`
- `sources/normalized.json`
- the generated `canon.md`, `persona.md`, `style_examples.md`
- the child wrapper `SKILL.md`

Generated packages should also satisfy these lint expectations:

- no missing required files
- no duplicate required section headers
- no cross-layer section headers mixed into the wrong file
- child `SKILL.md` contains YAML front matter with `name` and `description`
- child `SKILL.md` contains OpenClaw-compatible metadata for Python-backed memory scripts
- published packages should not keep raw `TODO` placeholders

## Canon Sections

`canon.md` should use these sections:

- `## Basic Identity`
- `## Setting Attributes`
- `## Key Plot Events`
- `## Confirmed Relationships`
- `## Official Statements And Notes`

## Persona Sections

`persona.md` should use these sections:

- `## Behavior Patterns`
- `## Emotional Tendencies`
- `## Interaction Style`
- `## Relationship Progression`
- `## Boundaries And Preferences`

## Style Sections

`style_examples.md` should use these sections:

- `## Address Patterns`
- `## Rhythm And Sentence Shape`
- `## Verbal Tics`
- `## Short Example Lines`

## Metadata

`meta.json` should at least include:

- `slug`
- `character_name`
- `source_work`
- `target_use`
- `source_types`
- `allow_low_confidence_persona`
- `source_decision_policy`
- `input_mode`
- `search_scope`
- `archive_mirror`
- `source_paths`
- `layout_version`
- `created_at`
- `updated_at`
- `primary_path`
- `archive_path`
- `install_scope`
- `canonical_source`
- `export_targets`
- `generated_for`
- `openclaw_exported_at`

## Child Skill Rule

The platform wrapper `SKILL.md` must tell the runtime:

- read `canon.md` first for facts
- use `persona.md` for behavior and interaction strategy
- use `style_examples.md` for wording texture
- only call `runtime/memory_prepare.py` when the latest turn suggests memory may matter
- use returned `memory_context` only when `memory_prepare.py` says read is needed
- call `runtime/memory_commit.py` only when `memory_prepare.py` says memory write is needed
- call `runtime/memory_summarize.py` only when the summarization threshold is reached
- never invent prior chat history when no relevant memory exists
- never upgrade persona inference into canon during conversation
- include YAML front matter with `name` and `description`
- include OpenClaw-compatible front matter for Python requirements, for example `metadata: {openclaw: {requires: {bins: [python3]}}}`
- make `description` explicit that the skill is for Codex or OpenClaw roleplay / answering in the character's voice
- keep `canon.md`, `persona.md`, `style_examples.md`, and `meta.json` identical across exported runtime packages
- only let platform differences live in `SKILL.md` and copied runtime scripts
- be directly discoverable from `./.agents/skills/{slug}/` for Codex, and from `<openclaw_workspace>/.agents/skills/{slug}/` for OpenClaw exports
- degrade to no-memory mode when `python3` is unavailable instead of failing the whole skill
- never expose internal memory checks to the user unless a real failure affects the reply
- not copy `.dreamlover-data/` or any other runtime memory database into the exported package
