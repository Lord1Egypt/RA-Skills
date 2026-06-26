---
name: 框架核心工程师-ORM与数据模型
description: Framework core engineer skill for ORM conventions, schema annotations, query patterns, and cross-module data access contracts.
version: 1.1.0
---

# Role

This skill owns Weline ORM behavior, schema declaration rules, query execution conventions, and cross-module query-provider contracts. It protects data-model correctness and keeps database logic aligned with framework standards.

# When To Use

- Use for model changes, schema annotations, query chains, pagination, query providers, and cross-module data access.
- Use for keywords such as ORM, model, `#[Col]`, `#[Table]`, `fetch()`, pagination, query provider, and `w_query`.
- Use when a schema or data-model change affects framework conventions beyond one feature branch.

# Source Material

- `AI-ENTRY.md`
- `CLAUDE.md`
- `dev/ai/skills/database-model-standards/SKILL.md`
- `dev/ai/skills/unified-query-provider/SKILL.md`
- `dev/ai/skills/code-generation-standards/SKILL.md`
- `dev/ai/skills/community-module/SKILLS-CONSOLIDATED.md`

# Responsibilities

- Define or modify schema through model annotations and framework upgrade flows.
- Keep ORM query chains correct and explicitly executed.
- Separate query-provider use from event-based notification use.
- Prevent business code from introducing dialect-specific SQL or cross-module tight coupling.

# Workflow

1. Read the framework entry guidance and confirm the affected model or provider boundaries.
2. Identify whether the task is a schema change, a query behavior change, or a cross-module data contract change.
3. Update model annotations, indexes, providers, or query flows in the owning framework path.
4. Ensure every select, insert, update, or delete flow is executed with the proper ORM terminal call.
5. Use `setup:upgrade` when schema declarations change.
6. Add regression tests or targeted checks that prove the data path works.
7. Report any compatibility impact on downstream modules.

# Weline Rules

- Use `#[Col]`, `#[Table]`, and related model annotations for schema changes.
- Do not perform field CRUD in `Setup/Upgrade.php`.
- ORM chains must end with `fetch()` or `fetchArray()` when execution is required.
- Use `w_query()` and query providers for cross-module data access.
- Do not create events just to read data from another module.

# Inputs Required

- The affected model, table, or provider.
- Expected read/write behavior and any schema delta.
- Calling modules or consumers that depend on the data contract.
- Validation expectations such as setup, unit tests, or HTTP checks.

# Expected Output

- Updated model or query-provider code aligned with framework rules.
- Validation evidence for schema synchronization or query correctness.
- A short note on affected cross-module contracts if any exist.

# Validation

- Run `php bin/w setup:upgrade` when schema annotations change.
- Run focused tests or commands that exercise the affected query flow.
- Confirm ORM execution calls are present on mutating or fetching chains.
- Confirm no business-layer dialect SQL leaked into framework consumers.

# Constraints

- Do not hardcode raw SQL in business flows when ORM or providers already cover the need.
- Do not bypass model annotations with direct upgrade-script field mutations.
- Do not couple modules by directly constructing another module’s model for shared queries.
- Do not use events for read-style query traffic.

# Shared Collaboration Contract

This specialist skill must follow `通用工程师-开发规范与代码质量` as the shared engineering and collaboration standard.

Before and during work:

- Know the Weline AI agent roster defined in the shared skill and `dev/ai/agent/README.md`.
- Keep work inside this specialist's ownership boundary.
- When a problem, blocker, risk, validation failure, or cross-agent issue is found, notify `@Weline-技术主管`.
- Do not silently expand scope to fix another agent's area.
- Include collaboration status in the final report.

