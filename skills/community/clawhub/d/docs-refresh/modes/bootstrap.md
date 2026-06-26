# Bootstrap Mode

Use this mode when the collector reports `doc_system_mode=bootstrap`, or when manual routing shows there is no split docs tree and no stable docs system beyond `README.md` or a few incidental docs.

The repository does not have a real docs system yet. Grow one in phases instead of generating a full scaffold on first contact.

## Focus

- Create or update `README.md` as the living overview when the repository has no better current-state document yet.
- Create `AGENTS.md` as the map when the repository needs a stable navigation entry point for future agents.
- Create `ARCHITECTURE.md` only when the codebase already has multiple durable domains, subsystems, or cross-cutting operational behavior that no longer fits cleanly inside `README.md`.

## Placement Rules

- Prefer the smallest durable foundation over a full docs tree.
- Treat the OpenAI-like docs layout as the eventual target shape, not day-one output.
- Keep `AGENTS.md` short and navigational even during bootstrap.
- Do not create `docs/` subtrees just because the repository is new.

## Growth Triggers

- Create `docs/design-docs/` when stable design principles or architecture rationale need more than one durable page.
- Create `docs/product-specs/` when user-facing flows or product constraints have split beyond overview docs.
- Create `docs/references/` when schemas, provider contracts, protocol details, or LLM-oriented references need their own reference pages.
- Create `docs/generated/` only when generated facts are treated as authoritative repository outputs.
- Create `docs/exec-plans/` when plans, progress logs, or debt tracking are versioned as first-class artifacts.

## Working Rule

- Bootstrap should leave the repository with a minimal map and a living overview, not an empty cathedral of placeholder directories.
- Missing `AGENTS.md` is normal here. It is not, by itself, a repair signal.
