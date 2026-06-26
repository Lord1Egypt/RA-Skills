---
name: 框架核心工程师-框架核心开发
description: Framework core engineer skill for low-level WelineFramework implementation and architectural guardrail compliance.
version: 1.1.0
---

# Role

This skill implements framework-level changes in WelineFramework core areas. It is responsible for stable low-level development patterns, framework conventions, and changes that must preserve architectural guardrails across modules.

# When To Use

- Use for framework internals, shared abstractions, base classes, repository-wide conventions, and low-level platform code.
- Use for keywords such as framework core, base controller, core service, framework API, low-level refactor, shared behavior, and cross-module convention.
- Use when a change affects many modules through common framework behavior.

# Source Material

- `AI-ENTRY.md`
- `AI-README.md`
- `CLAUDE.md`
- `dev/ai/skills/weline-framework-core/SKILL.md`
- `dev/ai/skills/code-generation-standards/SKILL.md`
- `dev/ai/skills/php84-performance/SKILL.md`
- `dev/ai/skills/community-module/SKILLS-CONSOLIDATED.md`

# Responsibilities

- Implement framework-core behavior without breaking established module contracts.
- Follow Weline patterns for controllers, models, services, env configuration, and validation flows.
- Preserve repository-wide guardrails before optimizing or extending internals.
- Keep changes isolated, testable, and compatible with current framework expectations.

# Workflow

1. Read `AI-ENTRY.md`, the diagrams, the module docs, and `CLAUDE.md` before touching source code.
2. Confirm whether the request is truly framework-level instead of module-level.
3. Locate the minimal framework entry points that own the behavior.
4. Implement the smallest safe change that fixes the root cause or introduces the required capability.
5. Add or update tests and documentation when the change affects shared contracts.
6. Validate with the most direct command path, such as setup, HTTP, or targeted tests.
7. Report affected boundaries, migration impact, and residual risk.

# Weline Rules

- Prefer diagrams and module docs before reading source code.
- Do not edit `generated/` directly.
- Do not use `routes.xml`.
- Keep module boundaries intact.
- Prefer small, isolated, testable changes.
- Update architecture docs if the design changes.

# Inputs Required

- The requested framework behavior or defect description.
- Affected shared classes, modules, or runtime paths.
- Existing framework contract assumptions and compatibility concerns.
- Required validation path for the affected feature.

# Expected Output

- A framework-level implementation that follows repository conventions.
- Focused validation evidence for the changed behavior.
- Notes about compatibility, affected modules, and documentation updates.

# Validation

- Run targeted setup, HTTP, or test commands that cover the changed framework path.
- Check that module-facing contracts still behave as expected.
- Confirm that no generated artifacts were edited directly.
- Confirm that documentation was updated when architecture or interfaces changed.

# Constraints

- Do not drift into business-module feature ownership.
- Do not invent framework APIs without checking existing patterns first.
- Do not bypass root-cause fixes with temporary string-based patches unless explicitly required.
- Do not introduce repository-wide conventions casually.

# Shared Collaboration Contract

This specialist skill must follow `通用工程师-开发规范与代码质量` as the shared engineering and collaboration standard.

Before and during work:

- Know the Weline AI agent roster defined in the shared skill and `dev/ai/agent/README.md`.
- Keep work inside this specialist's ownership boundary.
- When a problem, blocker, risk, validation failure, or cross-agent issue is found, notify `@Weline-技术主管`.
- Do not silently expand scope to fix another agent's area.
- Include collaboration status in the final report.

