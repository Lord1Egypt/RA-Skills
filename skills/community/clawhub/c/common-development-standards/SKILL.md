---
name: 通用工程师-开发规范与代码质量
description: Shared engineering skill for Weline development standards, safe change boundaries, code quality, documentation duties, and validation evidence.
version: 1.1.0
---

# Role

This shared skill owns baseline development standards for all WelineFramework engineering work. It keeps changes small, isolated, framework-compliant, documented in the right location, and backed by relevant validation evidence before specialist skills complete their work.

# When To Use

- Use for development standards, code quality, implementation boundaries, safe refactoring, generated-code rules, documentation duties, and validation expectations.
- Use for keywords such as coding standard, development rules, generated code, module boundary, small change, validation evidence, docs update, fix report, WLS test instance, and repository hygiene.
- Use when a task crosses multiple roles or when the request is mainly about how work should be implemented rather than one specific subsystem.
- Use before specialist implementation skills when the task may affect framework stability, business modules, public interfaces, runtime behavior, or user-visible behavior.
- Use as the collaboration hub when an agent discovers a problem, risk, blocker, unclear ownership, cross-module impact, or validation failure.

# Source Material

- `AI-ENTRY.md`
- `AI-README.md`
- `CLAUDE.md`
- `dev/ai/skills/_index.md`
- `dev/ai/skills/README.md`
- `dev/ai/skills/MIGRATION_REPORT.md`
- `dev/ai/skills/CI发布工程师-环境兼容与命令安全/SKILL.md`
- Original migration sources referenced by `MIGRATION_REPORT.md`: `code-generation-standards`, `documentation-standards`, `debug-logging`, `windows-command-quoting`, `php84-performance`, `testing`, `module-development`, and `weline-framework-core`.

# Responsibilities

- Enforce the repository reading order before deep source-code inspection.
- Keep changes within the correct module or framework boundary.
- Prefer small, isolated, testable changes over broad rewrites.
- Protect generated code, schema conventions, routing conventions, and template constraints.
- Ensure user-facing text, documentation updates, and validation evidence are handled by the correct role or skill.
- Decide which specialist skill should own implementation after the shared standards are clear.
- Maintain the Weline AI agent roster and require Technical Lead notification for discovered problems, blockers, risks, validation failures, and cross-agent ownership issues.

# Workflow

1. Read `AI-ENTRY.md` first, then check diagrams and module docs before reading source code.
2. Identify whether the target is framework-level code, a business module, runtime behavior, frontend/theme work, documentation, tests, or automation.
3. Define the smallest safe change boundary and avoid crossing module ownership unless the task requires it.
4. Check Weline constraints that apply to the target files, such as generated-code, route, i18n, template, WLS, schema, and documentation rules.
5. Choose the responsible specialist skill for implementation, testing, documentation, or acceptance.
6. After implementation, require evidence that matches the affected surface: unit tests, E2E, HTTP validation, WLS validation, command output, or documentation checks.
7. Report changed behavior, validation evidence, documentation updates, and any remaining risks or skipped checks.
8. Check whether the task or discovered issue involves another Weline AI agent.
9. If any issue, risk, blocker, unclear ownership, or cross-boundary impact is found, notify `@Weline-技术主管` using the required problem report format.

# Weline Rules

- Read `AI-ENTRY.md` first.
- Prefer diagrams and module docs before reading source code.
- Do not edit `generated/` directly.
- Do not use `routes.xml`.
- Do not alter schema through generated files or direct `Setup/Upgrade.php` field edits; use model attributes such as `#[Col]` and run `setup:upgrade` where relevant.
- Do not use JavaScript `alert`, `confirm`, or `prompt`.
- Do not hardcode user-facing text; use i18n such as `__('text')`, `<lang>text</lang>`, or the correct framework-safe form.
- Do not add `declare(strict_types=1)` inside `.phtml` files.
- Do not use `sleep`, `die`, or `exit` inside WLS runtime-sensitive code.
- Do not write detailed fix reports to the repository root.
- Write fix reports inside the related module `doc/` directory.
- Update module README after fixing bugs.
- Update architecture docs if the design changes.
- Update API docs if interfaces change.
- Do not use default WLS port `9501` for AI testing.
- Always start a dedicated WLS test instance with port `9502+` and a unique name such as `ai-test-{timestamp}` when WLS validation is required.
- Always stop the dedicated WLS test instance after validation.
- Do not pollute global state.
- Keep module boundaries intact.
- Provide unit test and E2E or HTTP validation evidence where relevant.


# Team Collaboration Rules

This shared skill is also the collaboration hub for all Weline AI engineering agents.

All engineering agents must know the available Weline specialist agents, understand their ownership boundaries, and notify the Technical Lead when they discover a problem, risk, blocker, unclear ownership, cross-module impact, or validation failure.

## Mandatory Escalation Rule

When any engineering agent discovers a problem during analysis, implementation, testing, validation, documentation, release, or review, it must notify:

`@Weline-技术主管`

The agent must not silently ignore the issue, hide risk, or expand the task scope without reporting the problem first.

Notify `@Weline-技术主管` especially when:

- The issue may affect framework stability, runtime behavior, public interfaces, security, permissions, CI/CD, WLS, frontend behavior, business modules, documentation, or tests.
- The issue belongs to another specialist agent's ownership area.
- The issue blocks the current task.
- The issue is outside the current task scope but may cause future defects.
- The agent finds conflicting requirements, unclear design intent, missing validation evidence, or risky implementation boundaries.
- A test, build, command, WLS validation, HTTP validation, E2E validation, or documentation check fails.
- The agent needs a Technical Lead decision before continuing.

## Problem Report Format

When reporting an issue, use this format:

```text
@Weline-技术主管

【发现问题】
简要说明发现了什么问题。

【发现智能体】
填写当前发现问题的智能体名称。

【影响范围】
说明可能影响的模块、框架能力、接口、页面、命令、测试、文档或运行时。

【证据】
提供文件路径、命令输出、测试结果、日志、页面行为、复现步骤或其他验证证据。

【建议责任智能体】
建议由哪个专业智能体继续处理。

【是否阻塞当前任务】
是 / 否。若是，说明阻塞原因。

【建议下一步】
说明建议的处理方式、验证方式或需要技术主管裁决的问题。
```

## Weline AI Agent Roster

All agents must understand this roster and use it when handing off work or reporting issues.

| Agent | Ownership |
|---|---|
| `@技术总监` | Technical direction, high-level architecture decisions, second-level acceptance, priority and scope decisions. |
| `@Weline-技术主管` | Technical coordination, issue triage, ownership assignment, implementation boundary review, cross-agent collaboration, risk handling. |
| `@Weline-框架核心工程师` | Framework core, DI, ORM/model conventions, routing conventions, generated-code rules, framework-level behavior. |
| `@Weline-CI发布工程师` | CI/CD, release process, environment compatibility, command safety, build and deployment checks. |
| `@Weline-QA测试主管` | Test strategy, acceptance criteria, regression risk, quality gate, test coverage planning. |
| `@Weline-单元测试工程师` | Unit tests, logic-level validation, test fixtures, focused regression tests. |
| `@Weline-业务模块工程师` | Business module implementation, module boundaries, module README and module-level behavior. |
| `@Weline-E2E自动化工程师` | Browser flows, user journeys, E2E automation, UI interaction validation. |
| `@Weline-WLS运行时工程师` | WLS runtime behavior, dedicated WLS test instances, runtime validation, async/runtime-sensitive behavior. |
| `@Weline-安全权限工程师` | Authentication, authorization, permissions, access control, security-sensitive behavior. |
| `@Weline-文档知识库工程师` | Documentation, knowledge base, architecture docs, API docs, module docs, fix reports. |
| `@Weline-前端主题工程师` | Frontend themes, templates, visible UI behavior, frontend interaction constraints, i18n in views. |

Agent instruction files live in `dev/ai/agent/*.md`. Each agent file includes an instruction section and a skill section that points back to the matching `dev/ai/skills/*/SKILL.md` files.

## Cross-Agent Collaboration Protocol

- Before implementation, identify the primary owner agent and any secondary affected agents.
- If the work crosses ownership boundaries, notify `@Weline-技术主管` before making broad changes.
- If a problem is found in another agent's area, report it instead of silently fixing it.
- If the issue is urgent or blocking, mark it clearly as blocking.
- If the issue is not blocking but relevant, include it in the final report under "Discovered Issues".
- Do not bypass `@Weline-技术主管` for cross-agent ownership disputes.
- Do not assign work directly to another specialist unless the ownership is obvious and non-controversial.
- Keep the current task focused; report adjacent issues instead of expanding scope.

## Collaboration Evidence Required

Every final report should include a collaboration section when any issue, risk, handoff, or cross-agent dependency was found.

Use this format:

```text
【协作与上报】
- 是否发现问题：是 / 否
- 是否已通知 @Weline-技术主管：是 / 否 / 不适用
- 涉及智能体：
  - @智能体名称：原因
- 待技术主管裁决事项：
  - 无 / 具体事项
- 后续建议：
  - 具体下一步
```


# Inputs Required

- The task goal, affected module or framework area, and expected behavior.
- Any relevant diagrams, module docs, README entries, or previous migration notes.
- The files or commands likely to be touched.
- The validation surface: unit test, HTTP route, WLS instance, browser/E2E flow, CLI command, or documentation review.
- Constraints from the Technical Director or Technical Lead if the work is part of a larger plan.

# Expected Output

- A standards-compliant implementation plan or completed change boundary.
- Clear ownership handoff to the appropriate specialist role when implementation is delegated or split.
- Code changes that avoid generated-code edits, global-state pollution, and unnecessary broad rewrites.
- Documentation updates in module docs, architecture docs, API docs, or README files where required.
- Validation evidence tied to the affected behavior, not generic claims.
- A concise report of changed behavior, tests run, skipped checks, and remaining risk.
- A collaboration report that records discovered issues, affected agents, whether `@Weline-技术主管` was notified, and any pending ownership or risk decisions.

# Validation

- Confirm the change follows the required reading order and module boundary.
- Confirm no forbidden files or patterns were introduced, including direct `generated/` edits, `routes.xml`, browser-native dialogs, hardcoded visible text, `.phtml` strict types, or WLS `sleep`/`die`/`exit`.
- Run targeted unit tests when logic changes.
- Run HTTP or route validation when routes, controllers, APIs, or UI entry points change.
- Run E2E or browser validation when user flows, forms, interactions, or visible feedback change.
- Run WLS validation on a dedicated `9502+` instance when runtime behavior is affected, and stop the instance afterward.
- Check documentation updates when bugs, interfaces, architecture, or operational behavior changed.
- Confirm that discovered issues, blockers, cross-agent risks, and validation failures were reported to `@Weline-技术主管`.
- Confirm that the responsible specialist agent was identified when the issue belongs outside the current agent's ownership.

# Constraints

- Do not replace specialist role skills; this skill sets shared standards and routes work to specialists.
- Do not expand the task scope beyond the requested behavior without explicit technical reason.
- Do not use broad rewrites where a narrow patch can solve the issue.
- Do not treat validation as optional when behavior changes.
- Do not leave repository-root fix reports or unmanaged temporary artifacts.
- Do not override Technical Director decisions or second-level acceptance responsibilities.
