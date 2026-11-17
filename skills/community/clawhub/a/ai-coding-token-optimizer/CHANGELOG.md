# Changelog

## v1.2.0 — 2026-09-29

- Add an explicit, opt-in feedback handoff after each run.
- Provide a redacted result template for before/after sizes, approximate token change, validation and usefulness.
- Add GitHub issue-template guidance without collecting telemetry or uploading project data.
- Explain how users can optionally leave feedback on GitHub, ProSkills or ClawHub.

## v1.1.0 — 2026-09-28

- **Measure and slim the always-loaded entry point.** Record the bytes and estimated tokens of the always-loaded files. Keep the rules that bind every task, and move reference material verbatim into guides and routers. Report the before and after sizes.
- **Two-level routing.** `docs/map/` task tables, plus a README router beside each code area, which also carries that area's own rules.
- **An operations checklist** (`references/operations.md`) for CI triggers, what actually ships, rollback, health, config and secret names, and external services.
- **No-loss and link verification** (`references/verification.md`). Also repoints “see CLAUDE.md § …” references across the repository.
- **Proactive behaviour.** Adoption runs the full workflow. The upkeep rules written into the entry point keep later sessions maintaining the map, and agents offer the workflow when an entry point grows past its budget.
- **One guide for Claude Code and Codex.** The full guide lives in `AGENTS.md`, and `CLAUDE.md` imports it with `@AGENTS.md`, so both hosts load the same rules.
- **Per-host measurement.** Each host's always-loaded context is measured and reported separately.
- **Hardened verification snippets.** Measurement follows `@imports`. The no-loss check reads only tracked or unignored Markdown, compares links by resolved destination, and skips symlinks. The anchor check ignores headings inside code examples.
- **Shipped folders stay clean.** Routers never go inside folders that ship to users; those areas are routed from `docs/map/`, and new agent files go on the packaging exclude list.
- **Move, don't copy.** When the owning guide already covers a topic, only the missing facts are merged in. Rules enforced by a single tool's hook are written into `AGENTS.md` for everyone. Links into sibling repositories are reported as not checked.
- **Templates** for the entry point, maps and area READMEs (`references/templates.md`), and a worked example of a 39 KB → 6.3 KB entry point.

## v1.0.2 — 2026-09-20

- Make ProSkills the primary homepage with hosted instructions and release downloads.

## v1.0.1 — 2026-09-20

- Explain the repeated-file-discovery problem and concrete map structure.
- Make onboarding agent-neutral and GitHub link-first, with standalone fallback.
- Separate registry guidance and clarify ongoing maintenance and benefits.


## v1.0.0 — 2026-09-20

- Rebrand user-supplied Workspace Map as AI Coding Token Optimizer.
- Add one-line adoption and host-aware AGENTS.md/CLAUDE.md guidance.
- Preserve documentation-only scope, targeted reading and idempotent updates.
- Add MIT license, security boundaries, examples and release integrity files.
