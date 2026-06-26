---
name: agent-init
description: Initialize or update AGENTS.md/CLAUDE.md for a project. Use this skill whenever the user wants to create, initialize, generate, setup, or update a project-level AGENTS.md or CLAUDE.md file. Triggers on requests like "initialize AGENTS.md", "create CLAUDE.md", "generate project doc for AI", "setup agent guidelines", "create project rules", or any mention of AGENTS.md/CLAUDE.md creation or initialization.
---

# Agent Init

Two-phase workflow for generating a comprehensive AGENTS.md (or updating an existing CLAUDE.md) for any project:
1. **Phase 1** — Run `/init` to produce raw project intelligence
2. **Phase 2** — Restructure that output into the 9-section universal template, adapting all tech-specific references to what the project actually uses

## Why This Structure

A well-structured AGENTS.md is the "onboarding doc" for AI agents. The 9-section template ensures every agent gets consistent context: what the project is, how to build and run it, what conventions to follow, and where to find deeper docs. Raw `/init` output tends to be uneven — it lists files well but misses conventions, workflows, and cross-references. Phase 2 fixes that.

---

## Phase 1: Base Analysis

Run `/init` in the project root. This analyzes the codebase and writes a preliminary CLAUDE.md.

- If a CLAUDE.md or AGENTS.md already exists, `/init` incorporates existing content
- The output is a starting point — expectations: file tree, dependency list, build file detection
- Do not skip this phase even if the project looks simple; the analysis provides useful raw material

## Phase 2: Restructure into Universal Template

Read the CLAUDE.md that `/init` produced, then rewrite it into the target AGENTS.md following the template below.

### Information Sources (use all three)

1. **From `/init` output** — file tree, dependencies, detected frameworks
2. **From project inspection** — read key config files, source layouts, existing docs to verify and supplement
3. **From inference** — conventions implied by the stack (e.g., Maven → `mvn test`, npm → `npm test`)

### Core Principle

**Adapt the template to the project, not the project to the template.** If the template says "Spotless" but the project uses ESLint, write ESLint. If the template assumes a backend but the project is frontend-only, merge the architecture sections.

### Target Filename

- `AGENTS.md` already exists → update it in-place
- Only `CLAUDE.md` exists → update it in-place (preserve filename to avoid breaking existing references)
- Neither exists → create `AGENTS.md`

### Language

Match the language of the project's existing documentation (README, comments). For Chinese projects, write in Chinese. When uncertain, default to Chinese.

### When Information Is Missing

Mark genuinely unavailable sections with `<!-- TODO: 待补充 — <reason> -->`. Never fabricate doc links, command names, or conventions. An honest TODO is better than a wrong instruction.

---

## 9-Section Universal Template

### 1. 项目概述 (Project Overview)

One paragraph: what the project does, the detected tech stack (real frameworks, not template placeholders), and repository structure (monorepo with subproject list, or single-project with key directories).

**Fill from:** README, package.json/pom.xml/build.gradle, top-level directory listing.

### 2. 快速命令 (Quick Commands)

Quick-reference table:

| 操作 | 命令 |
|------|------|
| 构建 | (from Makefile / package.json scripts / mvnw / gradlew) |
| 启动 | (dev server or application start command) |
| 测试 | (test runner command) |
| 格式化 | (formatter command, or "N/A") |
| Lint | (linter command, or "N/A") |

**Environment variables** (only if the project uses them): document `~/.<project>_env` or `.env` file loading priority. If the project has no env file convention, skip this subsection entirely.

**Fill from:** `package.json` scripts, `Makefile`, `pom.xml` plugins, `build.gradle` tasks, CI workflow files.

### 3. 后端架构 (Backend Architecture)

If the project has no backend: rename to "项目架构" and describe the single codebase.

- **ASCII package tree** — indent-based tree of key source directories (not every file, just meaningful packages)
- **Package annotations** — one-line purpose comment per package
- **Core subsystems** — 2-3 sentences each for major modules (auth, data layer, API, etc.)
- **Pointer:** `→ 详见 docs/architecture.md` only if that file exists

**Fill from:** `/init` file tree + spot-reading key source files in each package.

### 4. 前端架构 (Frontend Architecture)

If the project has no frontend, omit this section entirely.

- **Tech stack:** framework, state management, build tool (detected, not assumed)
- **Routing scheme:** file-based or config-based, with an example route
- **API layer:** how the frontend calls the backend (axios instance, base URL config, error interceptor)
- **Component library:** which UI library is used (or "无，使用原生组件")
- **Pointer:** `→ 详见 docs/design-docs/frontend-architecture.md` only if that file exists

**Fill from:** `package.json` dependencies, grep for router setup and API client initialization.

### 5. 关键约定 (Key Conventions)

Bullet list of **enforced** conventions. Each convention must be **verifiable in the codebase** — search for the actual pattern, don't copy from the template blindly.

Template examples (replace with detected equivalents):

- Error handling: search for custom exception base classes (`BusinessException`, `AppException`, etc.). If found → document. If the project throws raw `RuntimeException` → note that as a finding, not a convention.
- Response wrapping: search for `ApiResponse`, `R`, `Result<T>`, or global response advice/controller. If a unified wrapper exists → document it.
- Layering rules: check for ArchUnit tests, `lint-arch` Makefile targets, or package structure conventions that enforce layer boundaries. If none → omit.
- Code style: detect from `.editorconfig`, `.prettierrc`, `checkstyle.xml`, `spotless` config, `.eslintrc`. Document the actual tooling.
- Auth: detect JWT, session, OAuth2 from code. Document the actual mechanism.

**Every convention needs a doc link** (only if the doc exists):
```
→ 详见 docs/conventions/<topic>.md
```

### 6. 本地开发及验证流程 (Local Development)

Complete "edit → build → start → verify" loop:

```
1. 改 (Edit)   — source directories to modify
2. 构建 (Build) — exact command
3. 启动 (Start) — how to start the dev server
4. 验证 (Verify) — curl example or browser URL
```

Include (if applicable):
- **Token acquisition** — how to get an auth token for API testing
- **Log paths** — where application logs are written
- **Pointer:** `→ 详见 docs/design-docs/api-verification.md` only if that file exists

**Fill from:** README, CONTRIBUTING.md, docker-compose.yml. Construct a realistic curl example based on an actual API route found in the code.

### 7. 质量检查 (Quality Checks)

Single line listing available check commands:
```
make lint-arch / make lint-format / make format / make build / make test
```
Replace with the project's actual equivalents. If no formal checks exist, list the closest equivalents (e.g., `npm run lint && npm test && npm run build`).

### 8. 参考项目约定 (Reference Projects)

If the project references sibling repos or template projects for conventions, list them with priority rules. If none exist, omit this section entirely.

### 9. 文档导航 (Document Navigation)

Index table of existing detailed docs, grouped by category:

| 类别 | 文档路径 | 说明 |
|------|---------|------|
| architecture | docs/architecture.md | 架构设计 |
| design-docs | docs/design-docs/* | 设计文档 |
| conventions | docs/conventions/* | 编码约定 |

**Fill from:** Glob for `docs/**/*.md`, `ref-*/`, and any `*.md` files outside the root. Only include files that actually exist — never fabricate paths.

---

## Preserving Existing Content

If the project already has a hand-written CLAUDE.md or AGENTS.md, `/init` incorporates it. During Phase 2:

- Preserve hand-written insights that can't be discovered from code (historical context, team decisions, gotchas)
- Reorganize them into the matching template section
- Don't discard content just because it doesn't fit neatly — add it to the most relevant section, or create an additional subsection

## Verification Checklist

After writing, verify:
1. Every command in section 2 actually runs (at minimum, confirm the build and test commands work)
2. Every file path in section 9 exists on disk
3. Every convention in section 5 is observable in the codebase
4. No fabricated doc links or guessed commands

## Self-Evolution Mechanism

After each execution of this Skill:

1. Evaluate whether the output achieved the intended goal: **pass / fail**.
2. If it fails, reflect on the cause of failure and append a “failure case + improvement suggestion” to `diary/YYYY-MM-DD.md`.
3. If a certain improvement suggestion is repeatedly mentioned in the most recent three executions, refine it into a formal rule and submit a PR to modify this `SKILL.md`.
