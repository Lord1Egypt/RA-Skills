---
name: code-unit-test
description: Compare the current Git branch against master/main, identify newly added or changed code paths, and produce simulated unit-test-style case tables without generating test code. Use when the user asks for "代码单元测试", "模拟单元测试", "对新增代码做参数模拟", "比较当前分支和 master 的区别", or wants result tables showing inputs, calculated outputs, true/false returns, exceptions, or entity/object results for branch changes.
---

# 代码单元测试

## Overview

Use this skill to review branch changes like a lightweight unit-test designer: read the diff, understand the changed logic, choose representative inputs, mentally execute the code, and report the expected result table. Do not create unit test files unless the user explicitly asks for code generation.

## Workflow

1. Determine the comparison base.
   - Prefer `master` if it exists locally or as `origin/master`.
   - Fall back to `main` or `origin/main` only when `master` is unavailable.
   - Use the merge-base form for branch work: `git diff <base>...HEAD`.

2. Inspect the changed files and hunks.
   - Start with `git status --short`, `git branch --show-current`, and `git diff --stat <base>...HEAD`.
   - Read only the changed files and directly related methods/classes needed to understand behavior.
   - Separate production code changes from tests, formatting, generated files, config-only changes, and unrelated dirty worktree changes.

3. Decide the service scope before simulating cases.
   - If the current directory is a single service, or the diff only touches one recognizable service/module, proceed directly.
   - If the repository is a multi-service workspace and the diff touches multiple services/modules, ask the user which services need simulated unit-test analysis before continuing.
   - Identify services/modules from changed path prefixes, Maven/Gradle modules, service directories, application entry points, or existing repo conventions.
   - If the current directory is inside one service in a larger workspace and the diff is limited to that service, treat it as single-service.
   - Do not ask when the service scope is clear from the current directory and changed files.

4. Identify units and executable paths.
   - Treat each changed method, branch condition, lambda expression, parser, validator, mapper, or service decision as a unit.
   - Include interactions with helper methods, DTO/entity fields, enums, nullability, collection sizes, numeric/string boundaries, and exception paths.
   - If behavior depends on external services, database, cache, RPC, HTTP, or time, model those dependencies as input assumptions instead of executing them.

5. Generate simulated cases.
   - Cover normal path, boundary values, empty/null inputs, invalid inputs, duplicate/conflicting values, feature flags/config values, and exception-triggering inputs.
   - Prefer cases that directly exercise newly added or modified lines.
   - Keep cases concrete: name parameter values, object fields, mocked dependency returns, and expected side effects.
   - For Java services, preserve the user's minimal-change preference: analyze changed behavior without suggesting broad refactors unless needed to explain a risk.

6. Mentally execute and verify.
   - Trace the exact control flow for each case.
   - Compute expected scalar values, boolean returns, thrown exception types/messages when knowable, returned entity/DTO field values, list/map contents, and state changes.
   - Mark any result as "需要确认" only when the code depends on unknown runtime data that cannot be inferred locally.

7. Report in Chinese unless the user requests another language.
   - Lead with the comparison base, service scope, changed files, and units covered.
   - Provide tables grouped by changed unit.
   - Add risk notes for uncovered paths, ambiguous assumptions, or cases where true runtime behavior may differ from static simulation.

## Output Format

Use compact Markdown tables. Include these columns when applicable:

- `序号`
- `变更点/方法`
- `模拟输入`
- `依赖/前置条件`
- `执行路径`
- `预期结果`
- `结果类型`
- `覆盖的新增代码`
- `备注`

For `结果类型`, use one of:

- `计算结果`
- `返回 true`
- `返回 false`
- `抛出异常`
- `实体类结果`
- `集合/Map 结果`
- `状态变更`
- `无返回值`

## Case Selection Rules

Prefer fewer high-signal cases over exhaustive tables. A good default is 3-8 cases per changed unit, expanding only when the logic has many branches.

Always include:

- One representative success case.
- One boundary or empty-value case.
- One invalid or exception case when the code can throw.
- One case for each newly added branch condition.
- One case for each changed return shape or entity field assignment.

## Validation Boundaries

Do not claim the table is a replacement for automated unit tests. State clearly that the output is a static/simulated unit-test analysis unless commands were actually run.

If compiling or running tests is useful, follow the Java service validation strategy from the user's instructions: choose the smallest meaningful compile/test command for low-risk single-service changes, and explain why broader validation was or was not run.

## Example User Requests

- `用代码单元测试检查当前分支相对 master 的新增代码`
- `比较当前分支和 master，给新增逻辑模拟参数并输出结果表`
- `不要写单测代码，只帮我列出这些改动的输入和预期输出`
- `对这个分支新增方法做 true/false、异常、实体返回结果模拟`
