# Contracts

## Repository Layout

- `SKILL.md`
- `AGENTS.md`
- `.agents/skills/`
- `docs/`
- `references/`
- `scripts/`
- `prompts/`
- `tools/`
- `versions/`
- `characters/`

## Tool Interfaces

- `python tools/slugify.py "<name>"`
- `python tools/source_normalizer.py --input <path> --type manual|wiki|quotes|plot --output <path>`
- `python tools/evidence_indexer.py --input <normalized.json> --output <indexed.json>`
- `python tools/style_extractor.py --input <path> --output <style.json>`
- `python tools/skill_writer.py --action create|update|list [--slug <slug>] --root <path> [--interactive] [--output-root <path>] [--install-scope codex|archive|both] [--openclaw-workspace <path>] [--target-use <text>] [--source-types <csv>] [--allow-low-confidence-persona yes|no] [--skip-lint]`
- `python tools/version_manager.py --action snapshot|rollback --slug <slug> --root <path> [--output-root <path>] [--scope codex|archive|both]`
- `python tools/skill_linter.py --slug <slug> --root <path> [--output-root <path>] [--scope codex|archive|both]`
- `python scripts/memory_prepare.py --character-slug <slug> --user-message <text> [--user-id <id>]`
- `python scripts/memory_router.py --character-slug <slug> --user-message <text> [--assistant-message <text>] [--phase pre|post] [--user-id <id>]`
- `python scripts/memory_fetch.py --character-slug <slug> --user-message <text> [--user-id <id>]`
- `python scripts/memory_commit.py --character-slug <slug> --user-message <text> [--assistant-message <text>] [--user-id <id>]`
- `python scripts/memory_summarize.py --character-slug <slug> [--user-id <id>] [--summary-threshold <n>]`

## Layer Contracts

- `canon` contains only directly supported facts and explicit official positions
- `persona` contains only summarized behavior and interaction logic
- `style_examples` contains only language texture and short examples

## Runtime Contract

- `characters/{slug}/` is the canonical static source for each generated character
- generated Codex child skills are installed to `./.agents/skills/{slug}/` by default
- OpenClaw export is optional and goes to `<openclaw_workspace>/.agents/skills/{slug}/` only when explicitly requested
- both runtime packages share the same static character files and differ only in the wrapper layer and runtime packaging
- `skill_writer.py` runs a post-write lint pass by default and returns lint results alongside package metadata
- `skill_writer.py --interactive` performs intake-first prompting and writes the intake bundle into `meta.json` and `sources/normalized.json`
- after interactive generation, the tool asks whether to export to an OpenClaw workspace
- the hard intake gate must complete and be confirmed before any character files are written
- the hard intake gate asks one unresolved question at a time instead of sending the entire checklist at once
- the intake state tracks canonical slots and must not re-ask slots that are already clearly resolved
- `target_use` defaults when omitted and is not a required intake question
- child skills use silent conditional memory preparation instead of reading or writing memory every turn
- local runtime memory lives under `./.dreamlover-data/` and must not be written into `SKILL.md`
- generated child `SKILL.md` files use OpenClaw-compatible front matter and declare `python3` when memory scripts are available
- when `python3` is unavailable, child skills fall back to no-memory mode rather than failing completely
- child skills must not expose internal memory checks to the user during normal conversation
- runtime exports must not copy `.dreamlover-data/` into skill directories
