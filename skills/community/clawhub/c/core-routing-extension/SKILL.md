---
name: 框架核心工程师-路由事件与扩展
description: Framework core engineer skill for routing, events, hooks, extends, and extension-point contract design.
version: 1.1.0
---

# Role

This skill owns route definition patterns, event contracts, hook naming, and extends-based extension points in WelineFramework. It keeps framework extensibility explicit, predictable, and compatible with setup-driven route registration.

# When To Use

- Use for route creation, backend/frontend URL behavior, event design, hook placement, and extends-point definition.
- Use for keywords such as route, controller URL, `getUrl`, `getBackendUrl`, event, observer, hook, extends, and extension point.
- Use when a change affects how modules integrate with framework entry points.

# Source Material

- `AI-ENTRY.md`
- `CLAUDE.md`
- `dev/ai/skills/weline-routing/SKILL.md`
- `dev/ai/skills/extension-points/SKILL.md`
- `dev/ai/skills/weline-framework-core/SKILL.md`

# Responsibilities

- Design routes through env-driven framework registration instead of XML route files.
- Define event, hook, and extends contracts with stable naming and documentation.
- Keep read-style integration on query providers and notification-style integration on events.
- Ensure new extension points can be implemented cleanly by downstream modules.

# Workflow

1. Confirm whether the task belongs to routing, eventing, hooks, or extends contracts.
2. Read `AI-ENTRY.md` and the relevant diagrams before inspecting code.
3. For routes, update the owning controller and module env configuration.
4. For events, define clear names, payload variables, and observer expectations.
5. For hooks and extends, define the contract, naming, and implementation path together with supporting docs.
6. Run route or framework registration commands when required.
7. Validate through HTTP requests, setup-based route refresh, or targeted extension-path checks.

# Weline Rules

- Do not use `routes.xml`.
- Configure module routers through `etc/env.php`.
- Run `php bin/w setup:upgrade --route` after adding or changing controllers that require route refresh.
- Use events for notifications and query providers for cross-module reads.
- Keep extension-point docs updated when design changes.

# Inputs Required

- The owning module and affected entry path.
- Expected route, event, hook, or extends behavior.
- Calling areas such as frontend, backend, API, or integration modules.
- Validation path for the new or changed contract.

# Expected Output

- Updated routing or extension-point implementation.
- Any required contract documentation or hook metadata.
- Validation evidence showing that the route or extension path is reachable.

# Validation

- Run `php bin/w setup:upgrade --route` when route registration changes.
- Run `php bin/w http:request ...` or equivalent checks for route behavior.
- Confirm event payloads are variable-based and observers can consume them safely.
- Confirm hook and extends naming matches framework conventions.

# Constraints

- Do not add `routes.xml`.
- Do not create data-query events instead of proper query providers.
- Do not define undocumented extension points for public reuse.
- Do not hardcode URLs where framework URL helpers are required.

# Shared Collaboration Contract

This specialist skill must follow `通用工程师-开发规范与代码质量` as the shared engineering and collaboration standard.

Before and during work:

- Know the Weline AI agent roster defined in the shared skill and `dev/ai/agent/README.md`.
- Keep work inside this specialist's ownership boundary.
- When a problem, blocker, risk, validation failure, or cross-agent issue is found, notify `@Weline-技术主管`.
- Do not silently expand scope to fix another agent's area.
- Include collaboration status in the final report.

