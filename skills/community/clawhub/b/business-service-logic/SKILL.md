---
name: 业务模块工程师-服务层与业务逻辑
description: Business module engineer skill for service-layer design, business logic extraction, and module-safe orchestration.
version: 1.1.0
---

# Role

This skill owns service-layer implementation and business-rule placement inside modules. It keeps controllers thin, models focused on persistence, and business logic extracted into services that can be tested and reused.

# When To Use

- Use for service classes, business-rule extraction, API service contracts, and coordination between controllers and models.
- Use for keywords such as service, business logic, orchestration, API layer, domain rule, and refactor controller logic.
- Use when a task is more about module behavior than about framework infrastructure.

# Source Material

- `AI-ENTRY.md`
- `CLAUDE.md`
- `dev/ai/skills/service-development/SKILL.md`
- `dev/ai/skills/code-generation-standards/SKILL.md`
- `dev/ai/skills/module-development/SKILL.md`

# Responsibilities

- Place business logic in services instead of controllers or templates.
- Define stable module-local service contracts and collaboration boundaries.
- Keep persistence concerns in models and orchestration concerns in services.
- Structure code to support unit testing and future reuse.

# Workflow

1. Confirm the business rule, the entry point, and the owning module.
2. Read the existing controller, service, and model interaction before changing structure.
3. Extract or implement the rule inside a service with explicit dependencies.
4. Keep controllers and console commands focused on input/output orchestration only.
5. Add unit tests around the extracted service behavior.
6. Validate the end-to-end feature path through its real entry point.
7. Report the service boundary and any new contract assumptions.

# Weline Rules

- Prefer small, isolated, testable changes.
- Keep module boundaries intact.
- Do not hardcode user-facing text.
- Use i18n for user-facing text.
- Provide unit test evidence where relevant.

# Inputs Required

- The current feature entry point and expected business outcome.
- The owning module and collaborating models or services.
- Any API or controller contracts that must remain stable.
- Required validation path and edge cases.

# Expected Output

- A service-layer implementation or refactor with clearer business boundaries.
- Unit-test or focused validation evidence for the business rule.
- Notes about affected controller, API, or model interactions.

# Validation

- Run targeted unit tests for extracted or changed service behavior.
- Run a route, command, or API check through the real entry point when relevant.
- Confirm controllers no longer contain unnecessary business-rule branches.
- Confirm models remain persistence-focused rather than becoming orchestration hubs.

# Constraints

- Do not move UI rendering logic into services.
- Do not bury business-critical logic inside controllers, commands, or templates.
- Do not introduce raw SQL or framework-invented APIs in service code.
- Do not change public contracts silently without documenting the impact.

# Shared Collaboration Contract

This specialist skill must follow `通用工程师-开发规范与代码质量` as the shared engineering and collaboration standard.

Before and during work:

- Know the Weline AI agent roster defined in the shared skill and `dev/ai/agent/README.md`.
- Keep work inside this specialist's ownership boundary.
- When a problem, blocker, risk, validation failure, or cross-agent issue is found, notify `@Weline-技术主管`.
- Do not silently expand scope to fix another agent's area.
- Include collaboration status in the final report.

