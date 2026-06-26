# Changelog

## v0.7

- changed generation output to one canonical static source under `characters/{slug}/`
- made Codex the default runtime install target under `./.agents/skills/{slug}/`
- added optional OpenClaw export to `<openclaw_workspace>/.agents/skills/{slug}/`
- kept static role files shared across Codex and OpenClaw while allowing platform-specific `SKILL.md` wrappers
- copied only runtime scripts into exported packages and kept `.dreamlover-data/` out of skill directories
- added export metadata fields such as `canonical_source`, `export_targets`, `generated_for`, and `openclaw_exported_at`

## v0.6

- updated generated child skills to use OpenClaw-oriented front matter and runtime wording
- added OpenClaw Python requirement metadata for child skills that use conditional memory scripts
- kept conditional memory routing while adding explicit no-memory fallback when `python3` is unavailable
- updated README and contracts to distinguish the generator skill from OpenClaw-loadable child skills
- changed hard intake from checklist-style prompting to one-question-at-a-time branching
- removed `target use` from the required intake questions and default it when omitted

## v0.5

- added conditional local memory scripts: `memory_router`, `memory_fetch`, `memory_commit`, and `memory_summarize`
- introduced local SQLite memory storage under `./.dreamlover-data/`
- updated generated child `SKILL.md` files to use memory gates instead of always-on memory
- added `references/memory_policy.md` to define what can be remembered and when memory calls are allowed

## v0.4

- upgraded intake from a soft recommendation to a hard no-write gate
- added source decision policy and input mode prompts to interactive intake
- required confirmation of the intake summary before any files are created or modified
- persisted source decision metadata into `meta.json` and `sources/normalized.json`

## v0.3

- added intake-first generation rules to the top-level skill and intake prompt
- added `tools/skill_writer.py --interactive` for CLI question-driven creation
- persisted interactive intake answers into `meta.json`, `sources/normalized.json`, and generated layer files
- updated contracts and README examples to show `/skills` plus `$slug` after generation

## v0.2

- switched generated child skills to Codex-installable output under `./.agents/skills/{slug}/`
- kept `characters/{slug}/` as an archive mirror instead of the only output location
- added `tools/skill_linter.py` for package validation
- made `tools/skill_writer.py` preserve existing content during updates and normalize duplicate sections
- made `tools/skill_writer.py` run post-write linting by default
- required child `SKILL.md` front matter for discoverable roleplay skills

## v0.1

- initialized repository structure
- defined canon, persona, and style_examples boundaries
- added prompt guides for intake, audit, building, correction, and merge
- added deterministic helper tools for first-pass workflows
- defined character package layout and version snapshot behavior
