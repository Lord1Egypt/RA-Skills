# Mapping patterns

These are illustrative only. Verify every path in the actual project before using it.

## Small project

Add a short Project map section to the existing entry point, linking its source entry point, tests and release guide. If the entry point is already small, stop there. Don't add three documents just to fill a template.

## Service with an oversized entry point (the common case)

A Node/TypeScript service with an account app and a staff console had a 39 KB `CLAUDE.md`, which is about 10,000 tokens loaded in every session. It held:
- a 100-line source tree
- the CI walkthrough
- an env-var table
- the production box layout
- a gotcha list
- the UI design rules

Adding maps on top of that file would have saved nothing on the always-loaded cost. The fix:

- `CLAUDE.md` went from 39 KB to 6.3 KB. It now holds the hard rules, workflow, commands, reflexes and the Project map, with its upkeep rules.
- `AGENTS.md` became a short pointer to the same routers.
- `docs/map/PRODUCT.md`, `OPERATIONS.md` and `DOCS.md` are task tables.
- `src/README.md`, `app/README.md` and `admin/README.md` replaced the source tree. The UI design rules moved into `app/README.md`, so they load only for UI work.
- The CI walkthrough, env vars, box layout and gotchas moved verbatim into `docs/guides/`.
- Six comments and scripts that said "see CLAUDE.md § …" were repointed.
- The no-loss check found a handful of dropped specifics (brand colour values, a service name, a git command). They were restored.

## WordPress plugins built with both Claude Code and Codex

A free plugin had a 36 KB `CLAUDE.md`. Its commercial add-on had a 20 KB one that sent every session on to read the free plugin's guide first. Codex saw neither, because neither repository had an `AGENTS.md`. The adoption:

- `AGENTS.md` became the one full guide (9.7 KB and 7.6 KB). `CLAUDE.md` became `@AGENTS.md` plus three Claude-only notes (repo skills, a push hook, a slash command).
- `includes/` and `modules/` ship to customers, so their routers live in `docs/map/PRODUCT.md`. `src/` and `tests/` are excluded from the zip, so they got their own README routers.
- `AGENTS.md` was added to `.distignore`. The add-on's allowlist packager already left it out.
- The add-on's guide links the free plugin's `AGENTS.md` for the shared rules rather than importing it, and restates only the hard rules both repositories share.
- The no-loss check caught a dropped binding rule, "apply the unslop skill to any text people read", before review.
- A local review before pushing caught what the no-loss check can't:
  - Guides had been appended to instead of merged into, which left two bundle sizes in one guide.
  - A push ban was enforced only by a Claude Code hook, and was never written for other agents.
  - A testing guide described a CI job that didn't exist; the old entry point had been the one correct statement of it.
  - Commit messages broke the repo's own "no AI mentions" rule.

## Monorepo

Give each package its own entry point and routers. The root entry point stays small: shared rules, plus a router table of packages that links each package's entry point and the shared operations map. Avoid one giant inventory of every file.

## Existing work

Check `git status` first and preserve unrelated changes. On a rerun, measure again, update the existing routers and report the change. Don't create a second set of maps.
