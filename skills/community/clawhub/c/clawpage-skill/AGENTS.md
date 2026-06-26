# Repository Guidelines

## Project Structure & Module Organization

This repo is a **Claude Code plugin** (with `.claude-plugin/plugin.json`). It contains only LLM-facing instructions; the executable runtime ships separately as the [`@clawpage.ai/cli`](https://www.npmjs.com/package/@clawpage.ai/cli) npm package.

- `.claude-plugin/plugin.json` — plugin manifest.
- `skills/clawpage-skill/SKILL.md` — top-level router for all workflows.
- `skills/clawpage-skill/<sub-skill>/SKILL.md` — operational sub-skills:
  `init`, `create-page`, `update-page`, `create-management-page`, `create-template`, `update-template`, `manage-data`, `manage-links`, `manage-blobs`, `view-stats`, `use-sdk`.
- `skills/clawpage-skill/references/` — shared docs (API quickref, prompt contracts, design guidelines) — read-only references for the LLM, not executed.
- **No `scripts/` or `templates/`** — those live in the npm package and are invoked via `npx -y @clawpage.ai/cli ...`. Never reintroduce them here.

## Path Conventions

- **Auth** — `~/.clawpage/keys.local.json` (auto-created by `npx -y @clawpage.ai/cli init`). Project-scoped `./keys.local.json` in cwd takes precedence.
- **Pages** — default `~/.clawpage/pages/<page-name>/` (bare-name input to `--page-dir`). Path-like input (`./...`, `~/...`, absolute) is honored as-is for project-scoped storage.
- **Skill install dir** — read-only. The plugin must never be configured to write into `~/.claude/plugins/cache/` or wherever the runtime puts the install. All page projects belong under `~/.clawpage/pages/` or user CWD.

## Build, Test, and Development Commands

- Dry-run a template bundle (no auth):
  ```bash
  npx -y @clawpage.ai/cli scaffold general_template /tmp/preview
  npx -y @clawpage.ai/cli publish --page-dir /tmp/preview --title "Preview" --dry-run
  ```
- Publish a page project:
  ```bash
  npx -y @clawpage.ai/cli publish --page-dir <page-name> --title "My Page"
  ```
- One-time auth setup (registers an account, writes keys.local.json):
  ```bash
  npx -y @clawpage.ai/cli init
  ```

## Coding Style & Naming Conventions

- SKILL.md files are the only code in this repo (markdown + YAML frontmatter). Keep frontmatter minimal: `name` + `description` are required.
- Use `kebab-case` for sub-skill directory names. Sub-skills must register under `skills/clawpage-skill/<name>/SKILL.md`.
- Refer to plugin-bundled docs as `${CLAUDE_SKILL_DIR}/references/<file>.md` (Claude Code resolves the variable). Never use `~/.claude/...` absolute paths.
- Refer to runtime invocations as `npx -y @clawpage.ai/cli <subcommand>` exclusively. Never reintroduce `node scripts/...` or `${CLAUDE_SKILL_DIR}/scripts/...` — those break Codex/Gemini and trigger Claude Code permission prompts.

## Clawpage Browser SDK (page-side JS)

- All page-side JS that hits Clawpage APIs (data tables, atomic incr, short links, stats, blobs, `/api/me`) MUST use the Browser SDK: `https://clawpage.ai/sdk.js` (IIFE) or `https://clawpage.ai/sdk.mjs` (ESM). Raw `fetch('/api/...')` in page HTML/JS is forbidden.
- CLI scope (`@clawpage.ai/cli`'s Node scripts) may keep using raw `fetch`/`curl` — the SDK is browser-targeted.
- Owner `sk_*` tokens must NEVER appear in **any** browser-shipped page JS — including pagecode-protected pages. Pagecodes are not a token container: they can be shared, the page source can be inspected via DevTools, and browser caches persist. The only acceptable contexts for an `sk_*` token are CLI invocations (`npx -y @clawpage.ai/cli ...`) and server-side processes you control.
- See `skills/clawpage-skill/use-sdk/SKILL.md`.

## Testing Guidelines

- No automated test framework. Use the cli's `--dry-run` for bundle validation.
- For template changes (in `@clawpage.ai/cli`'s `templates/` directory), run dry-run and confirm generated output is valid HTML.
- For sub-skill SKILL.md changes, smoke-test by loading the plugin (`claude --plugin-dir <path>`) and triggering the sub-skill on a real prompt.

## Commit & Pull Request Guidelines

- Conventional Commits: `feat`, `fix`, `chore`, `docs`, `refactor`, etc.
- Keep commits scoped to one sub-skill or one cross-cutting concern (`feat(plugin): ...`, `fix(skills/manage-data): ...`).
- PRs should include purpose, changed paths, and verification commands run.

## Security & Configuration

- Never commit `keys.local.json`. The skill creates it at `~/.clawpage/keys.local.json` (or `./keys.local.json` for project-scoped use).
- The runtime (`@clawpage.ai/cli`) handles token discovery; SKILL.md files should refer to it abstractly (`run npx -y @clawpage.ai/cli init` for first-time auth) rather than instruct the LLM to construct the token file by hand.
