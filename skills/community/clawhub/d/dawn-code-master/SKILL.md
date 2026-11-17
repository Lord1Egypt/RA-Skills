---
name: dawn-code-master
description: >
  AI 写的代码一上生产就崩——不是它不会写，是没人给它立规矩。
  代码大师把「写、审、测、重构」的标准炼成一条硬规矩，整合 80k★ agent-skills、23k★ claude-skills 等顶级技能集，让每一行 AI 代码都过验收。
  触发词：写代码、修bug、代码审查、PR review、重构、设计评审、API设计、测试用例、spec 驱动开发。
metadata:
  version: 6.1.0
  sources:
    - focused-fix (alirezarezvani/claude-skills)
    - pr-review-expert (alirezarezvani/claude-skills)
    - spec-driven-workflow (alirezarezvani/claude-skills)
    - api-design-reviewer (alirezarezvani/claude-skills)
    - api-test-suite-builder (alirezarezvani/claude-skills)
    - self-eval — alirezarezvani/claude-skills
    - skill-tester (alirezarezvani/claude-skills)
    - mcp-server-builder (alirezarezvani/claude-skills)
    - e2e-skills (voidmatcha/e2e-skills)
    - avoid-ai-writing (conorbronsdon/avoid-ai-writing)
    - cc-skills-golang (samber/cc-skills-golang)
    - agentic-stack (codejunkie99/agentic-stack)
    - antigravity-skills (krishnakanthb13)
    - codebase-onboarding / migration-architect / ci-cd-pipeline-builder
    - performance-profiler / database-designer / sql-database-assistant
    - observability-designer / ship-gate / tech-debt-tracker
    - changelog-generator / dependency-auditor / git-worktree-manager
    - monorepo-navigator / rag-architect / agent-designer / agent-workflow-designer
    - dawn-code-master v4.0 (local)
    - agent-skills (addyosmani/agent-skills, 80k star)
    - yao-meta-skill (yaojingang/yao-meta-skill, 2.1k star)
    - ratel-ai/ratel (ratel-ai/ratel, 351 star)
    - context-engineering-kit (NeoLabHQ/context-engineering-kit, 1.3k star)
    - claude-skills (borghei/Claude-Skills, 411 star)
  dawn:
    requires:
      bins: [python, node, pwsh, git]
    permissions:
      - exec: [python, node, ruff, black, pytest, pwsh, git]
      - filesystem: [read/write workspace]
---

# Dawn Code Master v6.0

**50+ 顶级编码技能集成 + 全生命周期工作流 + 反合理化验证门禁。** 写代码、修bug、审PR、做设计，按这个来。

---

## 0. Skill Router

### Core Operating Behaviors

1. Surface Assumptions - Before implementing, explicitly state assumptions
2. Manage Confusion - Stop, name confusion, present tradeoff, wait for resolution
3. Push Back - Point out problems directly, quantify downsides, propose alternatives

### When to Use What

| Phase | Task | Skill |
|-------|------|-------|
| Define | Dont know what you want | interview-me |
| Define | Rough concept needs refining | [s2] Spec-Driven Dev |
| Plan | Have spec, need tasks | [s3] Planning |
| Build | Implementing code | [s4] Incremental Impl |
| Build | UI work | Frontend principles |
| Build | API work | [s16] API Design |
| Build | Need better context | [s6] Context Eng |
| Build | High stakes / unfamiliar code | [s7] Doubt-Driven |
| Verify | Writing/running tests | [s5] TDD |
| Verify | Bug fixing | [s8] Focused-Fix |
| Review | Reviewing code | [s9] PR Review |
| Review | Too complex | [s10] Code Simplification |
| Review | Security concerns | [s11] Security |
| Review | Performance concerns | [s12] Performance |
| Ship | Committing/branching | [s14] Git Workflow |
| Ship | CI/CD pipeline | [s15] CI/CD |
| Ship | Deploying/launching | [s13] Ship Gate |
| Maintain | Migration/deprecation | [s19] Migration |
| Maintain | Tech debt | [s20] Tech Debt |
| Docs | Writing docs/ADRs | Doc standards |
| Ops | Logs/metrics/alerts | [s18] Observability |

---

## 1. Coding Laws

**Pre-Commit Checklist:** syntax clean, tests pass, type hints, no bare except, no hardcoded secrets, f-string (not format()), pathlib (not os.path), docstrings, functions <= 30 lines.

**File Structure:** <= 300 lines per file, <= 30 lines per function, one thing per function.

**Error Handling:** async ops must have error handling, network requests must timeout, user input must be validated, external deps assumed to fail.

**Anti-Rationalization:**

| Rationalization | Reality |
|----------------|---------|
| "Write now, refactor later" | Later never comes. |
| "Just one line, no need to check" | Small diffs push files past boundaries. |
| "AI-generated code is probably fine" | AI code needs more scrutiny. |
| "Tests pass, it is good" | Tests dont catch architecture or security issues. |

---

## 2. Spec-Driven Development

**Law: NO CODE WITHOUT AN APPROVED SPEC.**

**9 Mandatory Sections:** Title/Metadata, Context, Functional Requirements (RFC 2119), Non-Functional Requirements, Acceptance Criteria, Edge Cases, API Contract, Data Model, Out of Scope.

**4-Phase Gated Workflow:** SPECIFY -> PLAN -> TASKS -> IMPLEMENT (each reviewed by human)

**Stop-and-Ask Rules:** Scope creep, >30% ambiguity, breaking changes, security implications, unknown performance.

**Anti-Rationalization:**
| Rationalization | Reality |
| "Clear requirements, no spec needed" | Clear reqs take 5 min. Unclear ones need it. |
| "Quick prototype first" | The prototype is the final product. |
| "Specs are too slow" | Specs save 10x refactoring time. |
| "I will document later" | Later never comes. |

---

## 3. Planning and Task Breakdown

Each task <= 30 min, independently testable, with clear AC. Slicing strategies: Vertical (preferred), Contract-First, Risk-First.

---

## 4. Incremental Implementation

**Cycle:** Implement -> Test -> Verify -> Commit -> Next slice

**Anti-Rationalization:** "Writing everything at once is faster" -> 500 lines untested = 10x debugging. "Just a few lines, no need to commit separately" -> atomic commits make rollback/review clean. "I will test later" -> never happens.

---

## 5. Test-Driven Development + E2E

**TDD Cycle:** RED (write failing test) -> GREEN (min code to pass) -> REFACTOR (clean up)

**Prove-It Pattern:** Write test reproducing bug (RED) -> Fix bug (GREEN) -> Write regression test -> Refactor

**E2E Silent-Pass Detection:** toBeDefined()/not.toBeNull() on Locator always passes. Use toBeVisible()/toHaveText().

**P0 Anti-patterns:** toBeDefined() on Locator, forgotten it.only, empty catch blocks, un-awaited async.

**Anti-Rationalization:** "Tests pass, it is good" -> tests dont catch architecture/security. "AI-generated code is fine" -> needs more scrutiny. "Write code first, add tests later" -> tests what code does, not what it should do.

---

## 6. Context Engineering

**From: ratel-ai/ratel (351 star) + NeoLabHQ/context-engineering-kit (1.3k star)**

**Core Principle: Progressive Disclosure** - Load only what each turn needs.

**Context Hierarchy:** 1. Rules Files (persistent) -> 2. Spec/Arch (per feature) -> 3. Source Files (per task) -> 4. Error Output (per iteration) -> 5. History (accumulates, compacts)

**Ratel-Style Catalog:** All skills in SkillCatalog, tools in ToolCatalog. Each turn loads only matching ones.

**Anti-Rationalization:** "All rules in system prompt" -> noise reduces accuracy. "Same project, no need to separate" -> different modules need different context. "Write rules once" -> projects evolve.

---

## 7. Doubt-Driven Development

**From: addyosmani/agent-skills -- doubt-driven-development**

A confident answer is not a correct one. For non-trivial decisions (branching logic, crossing boundaries, unverifiable assertions, irreversible blast radius).

**Doubt Cycle:** 1. CLAIM (write claim + why matters) -> 2. EXTRACT (isolate artifact) -> 3. DOUBT (fresh-context adversarial review) -> 4. RECONCILE (classify findings) -> 5. STOP (trivial findings, 3 cycles, or user override)

**Anti-Rationalization:** "This is obviously correct" -> hides most dangerous assumptions. "Tests pass" -> only cover known scenarios. "No time" -> doubt cycle is faster than debugging.

---

## 8. Bug Fixing (Focused-Fix)

**Law: NO FIXES WITHOUT SCOPE -> TRACE -> DIAGNOSE FIRST.**

**Phase 1: SCOPE** - Identify feature, find files, understand purpose.
**Phase 2: TRACE** - Map inbound dependencies (imports) and outbound (who imports this).
**Phase 3: DIAGNOSE** - Risk tags: HIGH (public API/DB schema/security), MED (internal module), LOW (isolated file).
**Phase 4: FIX** - Dependencies -> Types -> Logic -> Tests -> Integration. Fix one at a time, run tests after each.
**Phase 5: VERIFY** - Feature tests -> referencing tests -> full suite.

---

## 9. PR Review (5-Axis + Anti-Rationalization)

**From: addyosmani/agent-skills -- code-review-and-quality**

**Axis 1: Correctness** - Matches spec? Edge cases? Error paths? Tests pass?
**Axis 2: Readability & Simplicity** - Descriptive names? Straightforward flow? Logical organization? No clever tricks? Lines can be reduced? Abstractions earning complexity?
**Axis 3: Architecture** - Fits system design? Clean boundaries? No circular deps? Appropriate abstraction?
**Axis 4: Security** - Input validated? Secrets safe? Auth checked? SQL parameterized? XSS prevented?
**Axis 5: Performance** - N+1 queries? Large object allocations? Uncached hot paths?

**Output Format:** Blast radius, per-axis assessment, severity labels (CRITICAL/REQUIRED/NIT), verdict (Approve/Request changes).

**Anti-Rationalization:** 9-item table covering "It works, good enough", "I wrote it, I know it is correct", "Clean up later", "AI-generated code is fine", "Tests pass", "Refactor makes it cleaner", "Just a small addition", "Just a version bump".

---

## 10. Code Simplification

**From: addyosmani/agent-skills -- code-simplification**

**Principles:** Chestertons Fence, Rule of 500 (>500 lines = decompose), reduce complexity not relocate it.

**Checklist:** Dead code? Conditionals can be simplified? Duplicate code? Complex expressions named? Nesting flattened? Single responsibility? Abstraction worth it? More code deleted than added?

---

## 11. Security Hardening

**From: addyosmani/agent-skills -- security-and-hardening**

**OWASP Top 10 Prevention:** SQL injection, XSS, auth, authorization, sensitive data, config security, dependency scanning, logging.

**3-Tier Boundary:** External (untrusted, validate all) -> Service (semi-trusted, auth) -> Internal (trusted, business logic).

---

## 12. Performance Optimization

**From: addyosmani/agent-skills -- performance-optimization**

**Measure First, Optimize Second:** Baseline -> Hypothesize -> Validate -> Optimize -> Verify -> Repeat.

**Checklist:** N+1 queries? Repeated computation? Large objects? Sync blocking? Caching? Lazy loading? Bundle size? Indexes? Connection pool?

---

## 13. Ship Gate and Deployment

**From: addyosmani/agent-skills -- shipping-and-launch**

**Pre-Launch Checklist:** All tests pass, code review approved, no P0/P1 vulns, CHANGELOG updated, version bumped, DB migrations forward-compatible, rollback plan, monitoring configured, docs updated, performance baseline, feature flags, staged rollout plan.

---

## 14. Git Workflow and Versioning

**From: addyosmani/agent-skills -- git-workflow-and-versioning**

**Principles:** Trunk-based development, atomic commits, ~100 lines per PR, commit as save point.

**Convention:** <type>: <description> (feat/fix/refactor/chore/docs/test/ci)

**Anti-Rationalization:** "Commit first, organize later" -> commit history IS code history. "One PR for everything" -> no one reviews large PRs. "Long feature branch is fine" -> merge hell.

---

## 15. CI/CD Pipeline and Automation

**From: addyosmani/agent-skills -- ci-cd-and-automation**

**Stages:** Lint -> Type check -> Unit test -> Integration test -> Build -> Security scan -> Deploy

**Gates:** Lint 0 errors (block), Unit test 100% (block), Coverage >=80% (block), Security scan 0 critical (block), Build success (block).

---

## 16. API Design Review

**REST:** kebab-case plural nouns (/api/v1/users). HTTP methods: GET (retrieve), POST (create), PUT (replace), PATCH (partial), DELETE (remove).

**5-Dimension Score:** Consistency (30%), Documentation (20%), Security (20%), Usability (15%), Performance (15%).

---

## 17. Database Design

**Principles:** Plural table names, UUID PK, created_at/updated_at, soft delete optional, indexes on query conditions, explicit FKs, forward-compatible migrations.

**Performance Checklist:** Indexes used? N+1 queries? Reasonable joins? Cursor pagination? Correct transaction scope?

---

## 18. Observability Design

**Three Pillars:** Structured logging, business metrics (latency/error rate/throughput), distributed tracing.

**Health Endpoints:** GET /health (liveness), GET /health/ready (readiness), GET /health/debug (internal only).

---

## 19. Code Migration

**Strategies:** Direct replacement (high risk, small module), Parallel run (medium, need rollback), Gradual (low, large system), Abstraction layer (low, dual maintenance).

**Flow:** Inventory -> Impact analysis -> Compatibility layer -> Execute -> Verify -> Cleanup

---

## 20. Tech Debt Tracking

**Classification:** Architecture (HIGH), Code quality (MED), Testing (HIGH), Documentation (LOW), Infrastructure (MED).

**Entry Format:** Type, Location, Description, Impact, Estimate, Created.

---

## 21. De-AI-Writing Check

**Tier 1 (Always Flag):** leverage/use, utilize/utilize, implement/build, nevertheless/but, furthermore/and, commence/start, endeavor/try.

**Tier 2 (Cluster Flag):** robust/reliable, seamless/smooth, facilitate/help, granular/detailed, holistic/complete, ecosystem/system.

**Tier 3 (High Density):** cutting-edge/modern, state-of-the-art/best available, game-changer/big change.

**Detection Flow:** First pass (flag all Tier 1) -> Structure check -> Rhythm check -> Second pass -> Output

---

## 22. Self Evaluation

**Two-Axis:** Task Difficulty (Low/Medium/High) x Execution Quality (Poor/Adequate/Strong) -> Score 1-5.

**Forced Counter-Argument:** Before final score, write reasons for lower, reasons for higher, then resolve.

**Inflation Detection:** 4+ of last 5 same score -> flag inflation. 3 consecutive 4s -> stricter evaluation.

---

## 23. Language Quick Reference

**Python:** snake_case, type hints, pathlib, f-strings, try/except/raise.
**TypeScript:** camelCase, PascalCase for types, interfaces, async/await with try/catch.
**Go:** camelCase, capitalized exports, error wrapping with fmt.Errorf.%w.
**PowerShell:** Verb-Noun naming, CmdletBinding, ErrorAction Stop.

---

## Appendix: Quick Reference

### When to Use What

| Scenario | Use |
|----------|-----|
| Write new code | Spec-Driven -> Plan -> TDD -> Incremental Impl |
| Fix bugs | Focused-Fix 5-phase |
| Review PR | 5-Axis PR Review |
| Design API | API Design + Score |
| Write tests | TDD + E2E silent-pass detection |
| Migration | Migration flow |
| CI/CD | Pipeline stages |
| Database | Design principles |
| Release | Ship gate checklist |
| Tech debt | Debt tracking format |
| Self-eval | 2-axis scoring |
| De-AI-fy | Writing check |

### Never Do

1. Fix bugs without scoping first
2. Write code without spec
3. Merge without review
4. Commit without tests
5. Release without CHANGELOG
6. Change API without impact assessment
7. Dishonest self-eval
8. Ship without de-AI-fying