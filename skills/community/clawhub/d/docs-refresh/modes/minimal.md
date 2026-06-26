# Minimal Mode

Use this mode when the collector reports `doc_system_mode=minimal`, or when manual routing shows there is no split docs tree but the repository already has stable living docs.

The repository already has core living docs, but it has not yet split into a durable docs taxonomy.

## Focus

- Prefer updating the existing living docs first: `README.md`, `AGENTS.md`, `ARCHITECTURE.md`, and cross-cutting top-level docs such as `DESIGN.md`, `FRONTEND.md`, `PRODUCT_SENSE.md`, `RELIABILITY.md`, `SECURITY.md`, `PLANS.md`, or `QUALITY_SCORE.md`.
- Keep `AGENTS.md` small and navigational.
- Use `ARCHITECTURE.md` or another current-state doc for durable system truth that no longer belongs in the overview.

## Creation Rules

- Create the first domain-specific subtree only when it has earned a second durable page in that domain.
- When splitting for the first time, choose the subtree that matches the durable fact:
  - `docs/design-docs/` for design principles and architecture rationale
  - `docs/product-specs/` for product behavior and user-facing constraints
  - `docs/references/` for schemas, contracts, and protocol detail
  - `docs/generated/` for authoritative generated facts
  - `docs/exec-plans/` for versioned plans and debt tracking

## Working Rule

- A minimal repo should converge by strengthening its existing docs, not by exploding into a premature taxonomy.
- A repo can be `minimal` even if `AGENTS.md` is absent, as long as other durable current-state docs already exist.
