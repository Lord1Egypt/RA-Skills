# 🛠️ 150 Developer Productivity Prompts
## *The Ultimate Prompt Library for Engineering Teams, Code Reviewers & Solo Developers*

> **Battle-tested AI prompts that turn ChatGPT, Claude, and Copilot into a senior engineering pair. Code review, debugging, architecture, refactoring, testing, and docs — 150 copy-paste prompts used by shipping teams.**

---

## 📋 Table of Contents

| # | Category | Prompts |
|---|----------|---------|
| 1 | **Code Review** | Prompts 1–25 |
| 2 | **Debugging** | Prompts 26–50 |
| 3 | **Architecture Design** | Prompts 51–75 |
| 4 | **Refactoring** | Prompts 76–100 |
| 5 | **Testing** | Prompts 101–125 |
| 6 | **Documentation** | Prompts 126–150 |

---

# 1. Code Review (Prompts 1–25)

## Prompt 1 — Senior Reviewer Pass

```
You are a staff engineer reviewing a pull request. Here is the diff:

[PASTE DIFF]

Review it for: correctness, security vulnerabilities, edge cases, performance, readability, and test coverage. For each finding, give severity (blocker/major/minor/nit), the file:line, the problem, and a concrete suggested fix. End with a verdict: Approve, Request Changes, or Comment.
```

## Prompt 2 — Security-First Review

```
Act as an application security engineer. Review this code for OWASP Top 10 issues, secret leakage, injection, authz flaws, and unsafe deserialization:

[PASTE CODE]

List each vulnerability with CWE id, severity, the exact line, exploit scenario, and a remediation snippet.
```

## Prompt 3 — Performance Review

```
You are a performance engineer. Review the following code for algorithmic complexity, N+1 queries, unnecessary allocations, blocking calls, and caching opportunities:

[PASTE CODE]

Report each issue with the current time/space complexity, the suggested improvement, and expected impact.
```

## Prompt 4 — Readability & Style Review

```
You are a code quality reviewer focused on maintainability. Review this snippet:

[PASTE CODE]

Flag naming issues, dead code, duplicated logic, overly clever constructs, and violations of [STYLE GUIDE]. For each, give the line and a clearer rewrite. Keep changes minimal and idiomatic.
```

## Prompt 5 — Test Coverage Gap Review

```
Given this source file and its existing tests, identify untested branches, missing edge cases, and unasserted error paths:

[SOURCE]

[TESTS]

Output a checklist of test cases that should be added, grouped by function.
```

## Prompt 6 — API Contract Review

```
Review this API endpoint implementation against its documented contract:

[SPEC]

[IMPL]

Flag mismatches in status codes, response shape, error envelopes, pagination, and versioning. For each, note the breaking-change risk.
```

## Prompt 7 — Concurrency & Race Condition Review

```
You are a concurrency specialist. Review this multithreaded/async code for data races, deadlocks, lost updates, and unguarded shared state:

[PASTE CODE]

For each issue: the triggering interleaving, severity, and a fix using locks/atomics/channels as appropriate.
```

## Prompt 8 — Dependency & Supply-Chain Review

```
Review the dependencies introduced in this PR:

[DEPENDENCY LIST / DIFF]

For each, assess license compatibility, maintenance health, known CVEs, bundle size impact, and whether a native alternative exists. Recommend keep / pin / replace.
```

## Prompt 9 — Error Handling Review

```
Review this code's error handling:

[PASTE CODE]

Flag swallowed errors, generic catch blocks, missing rollback, uninformative messages, and places where failures should be retried/idempotent. Give a corrected version.
```

## Prompt 10 — Accessibility Review (Frontend)

```
Act as a frontend a11y reviewer. Review this component for WCAG 2.2 AA compliance:

[COMPONENT CODE]

Check keyboard nav, ARIA roles, color contrast, focus management, and screen-reader labels. Output a prioritized fix list.
```

## Prompt 11 — Database Migration Review

```
Review this schema migration for safety on a live, high-traffic table:

[MIGRATION SQL]

Flag locking behavior, backfills, index creation strategy, rollback safety, and data-loss risk. Suggest a zero-downtime approach if needed.
```

## Prompt 12 — PR Description & Title Quality

```
Given this PR title and description, rewrite it to follow [TEAM CONVENTION] (e.g., conventional commits). Summarize the why, the what, and testing done. Flag missing context a reviewer would need.

[PASTE PR TEXT]
```

## Prompt 13 — Code Smell Detector

```
You are a refactoring-minded reviewer. Scan this file for code smells from Fowler's catalog (long method, feature envy, primitive obsession, shotgun surgery, etc.):

[PASTE CODE]

List each smell with the method/line, why it's a smell, and the targeted remedy.
```

## Prompt 14 — Review Checklist Generator

```
Generate a tailored code review checklist for a [LANGUAGE] [FRAMEWORK] [SERVICE TYPE] change that touches [AREAS]. Output as a Markdown checklist grouped by risk category, with the single most important check first.
```

## Prompt 15 — Nitpick Filter

```
From this list of review comments, classify each as a genuine blocker vs a nitpick that should not block merge:

[PASTE COMMENTS]

For nits, suggest whether to fix now, file a follow-up, or ignore. For blockers, explain the risk.
```

## Prompt 16 — Breaking Change Detector

```
Compare this PR against the public API surface of the package. List any breaking changes, their consumer impact, and the migration path. Recommend deprecation strategy if a hard break is unavoidable.

[OLD API]

[NEW API]
```

## Prompt 17 — Logging & Observability Review

```
Review this service code for observability gaps: missing structured logs, no trace/span propagation, unlabeled metrics, and log injection risk:

[PASTE CODE]

Recommend specific log/metric lines and their fields.
```

## Prompt 18 — Config & Secrets Review

```
Review this code and config for hardcoded secrets, environment-variable misuse, missing validation, and unsafe defaults:

[PASTE CODE + CONFIG]

List each issue with remediation (env var, secret manager, schema validation).
```

## Prompt 19 — Reviewer Comment Drafter

```
Draft a respectful, actionable code review comment for this situation: [DESCRIBE ISSUE] in [FILE:LINE]. Include what's wrong, why it matters, and a suggested change. Keep it kind and specific, not prescriptive.
```

## Prompt 20 — Merge Conflict Resolution Guidance

```
These two branches conflict in [FILES]. Explain the semantic conflict, the safest resolution strategy, and how to verify correctness afterward. Do not just pick a side.

[CONFLICT HUNKS]
```

## Prompt 21 — Review SLO/Performance Budget Check

```
This PR changes a hot path. Estimate the added latency/allocations and check it against our budget of [BUDGET]. Recommend cuts if over budget.

[PASTE CODE]

[BUDGET SPEC]
```

## Prompt 22 — Third-Party API Integration Review

```
Review this integration with [EXTERNAL API] for: timeout handling, retry/backoff, rate-limit respect, idempotency, and failure fallback:

[PASTE CODE]

Give a hardened version of the client call.
```

## Prompt 23 — Review Summary for Non-Engineers

```
Summarize this technical PR for a product manager in 4 bullet points: what changed, user-visible impact, risk, and rollout notes. Avoid jargon.

[PASTE PR DIFF/DESCRIPTION]
```

## Prompt 24 — Duplicate Logic Finder

```
Across these files, find duplicated logic that should be extracted into a shared helper:

[FILE A]

[FILE B]

Show the common abstraction, its signature, and where to call it.
```

## Prompt 25 — Post-Merge Regression Risk

```
Based on this merged change, predict which existing behavior is most likely to regress and what monitoring/alerts should be added to catch it within 24h.

[PASTE MERGED DIFF]
```

---

# 2. Debugging (Prompts 26–50)

## Prompt 26 — Systematic Bug Triage

```
You are a debugging coach. A bug report says: [SYMPTOM]. Reproduce the likely cause space by listing hypotheses ranked by probability, with one quick test to confirm or reject each. Do not jump to a fix.
```

## Prompt 27 — Stack Trace Explainer

```
Explain this stack trace to a mid-level engineer: what failed, the root call path, and the most probable root cause. Then give 2–3 next diagnostic commands.

[PASTE STACK TRACE]
```

## Prompt 28 — "Works Locally, Fails in Prod" Diff

```
The code works in dev but fails in prod. Compare likely environment differences (config, data volume, timezone, permissions, network, secrets) and give an ordered checklist to isolate the cause.
```

## Prompt 29 — Heisenbug Investigator

```
We have a nondeterministic failure: [DESCRIPTION]. Propose causes (race, uninitialized memory, floating point, caching, clock skew, GC). For each, a way to make it deterministic enough to reproduce.
```

## Prompt 30 — Flaky Test Diagnoser

```
This test fails ~1 in 20 runs: [TEST CODE]. Identify flakiness sources (order dependence, time, async, shared state, randomness) and give a hardened rewrite plus a way to prove stability.
```

## Prompt 31 — Memory Leak Hunter

```
Review this long-running service for memory leaks:

[PASTE CODE]

Check unbounded caches, listeners not removed, closures retaining refs, and missing cleanup. Suggest how to confirm with heap snapshots.
```

## Prompt 32 — Slow Query Diagnoser

```
This query is slow: [SQL]. Given the schema [SCHEMA], identify missing indexes, full scans, joins blowing up, and function-in-where issues. Provide the corrected query + index DDL and explain the plan change.
```

## Prompt 33 — Null/undefined Traceback

```
We hit a TypeError: cannot read property of undefined at [LINE]. Walk backward through the data flow to find where the value could be undefined, list guard strategies, and give a defensive fix.
```

## Prompt 34 — Infinite Loop / Hang Finder

```
This code hangs: [PASTE CODE]. Find the loop/await/recursion that never terminates or deadlocks. Explain the exact condition and provide a bounded version.
```

## Prompt 35 — API Returns Wrong Data

```
An endpoint returns [ACTUAL] but should return [EXPECTED]. Given the handler [CODE] and upstream calls, trace where the value diverges and propose a fix with a regression test.
```

## Prompt 36 — Build/Compile Error Decoder

```
Decode this build error in plain language and give the fix:

[PASTE BUILD ERROR]

Include the root cause, not just the surface message.
```

## Prompt 37 — Race Condition Reproduction

```
Given this concurrent code [CODE], construct a minimal reproduction script that triggers the race with high probability, then show the fix.
```

## Prompt 38 — Dependency Version Conflict

```
Our build breaks after upgrading [PACKAGE] from [OLD] to [NEW]. Analyze the likely breaking change, check the changelog, and suggest the minimal code change or a safe version pin.

[ERROR / DIFF]
```

## Prompt 39 — Silent Failure Auditor

```
This operation "succeeds" but produces no result. Audit for silently swallowed errors, success-by-default responses, and missing validation:

[PASTE CODE]

List where the real failure is hidden and how to surface it.
```

## Prompt 40 — Frontend Rendering Bug

```
The UI shows [BUG] in [BROWSER]. Given this component [CODE] and state [STATE], hypothesize causes (key collisions, stale closure, layout thrash, z-index, event bubbling) and a debugging plan.
```

## Prompt 41 — Timeout/Cascading Failure

```
Service A times out calling B which calls C. Map the failure cascade, identify the bottleneck, and recommend timeouts, circuit breakers, or bulkheads to contain it.

[ARCHITECTURE SKETCH]
```

## Prompt 42 — Intermittent 500 Diagnoser

```
We get sporadic HTTP 500s with no clear pattern. List the top 5 causes for a [FRAMEWORK] app and a logging/metric plan to catch the next occurrence with enough context to fix it.
```

## Prompt 43 — Data Corruption Investigator

```
Records in [TABLE] have [BAD DATA] that appeared after [EVENT]. Reconstruct the probable write path that introduced corruption and how to clean + prevent recurrence.
```

## Prompt 44 — Cache Invalidation Bug

```
Stale data is served despite an update. Given the cache layer [CODE] and invalidation logic, find the bug (missing invalidation, wrong key, TTL too long, race) and fix it.
```

## Prompt 45 — Auth/Session Bug

```
Users get logged out unexpectedly / can access forbidden routes. Review the auth middleware and session handling:

[PASTE CODE]

Flag token expiry, missing guards, CSRF, and cookie attributes. Provide a hardened version.
```

## Prompt 46 — Webhook/Event Not Firing

```
Our webhook handler isn't triggering. Given the provider [PROVIDER] and our receiver [CODE], list failure modes (signature verify failing, timeout, 2xx requirement, retries, ordering) and a debug checklist.
```

## Prompt 47 — Off-by-One / Boundary Bug

```
We see an off-by-one in [DESCRIPTION]. Audit loops, slice/index math, pagination, and inclusive/exclusive bounds in [CODE]. Show the corrected ranges with examples.
```

## Prompt 48 — Docker/Env Bug

```
The container crashes with [ERROR]. Given the Dockerfile [DOCKERFILE] and entrypoint, find image/runtime/permission/volume issues and a fix that keeps the image minimal.
```

## Prompt 49 — Performance Regression Bisect

```
Latency regressed after a recent deploy. Given the changelog [COMMITS], hypothesize the culprit, suggest a git bisect command sequence, and a profiling approach to confirm.
```

## Prompt 50 — Root Cause Writeup

```
Write a blameless postmortem for this incident: [TIMELINE]. Include impact, root cause (5 whys), contributing factors, what went well, and 3 corrective actions with owners.
```

---

# 3. Architecture Design (Prompts 51–75)

## Prompt 51 — System Design From Requirements

```
Design a system for: [REQUIREMENTS]. Constraints: [SCALE, LATENCY, BUDGET, TEAM SIZE]. Produce a component diagram (ASCII), data flow, storage choice with rationale, and the top 3 risks. Keep it pragmatic, not trendy.
```

## Prompt 52 — Monolith vs Microservices

```
We're at [STAGE] with [TEAM SIZE] engineers. Given [TRADEOFFS], recommend monolith, modular monolith, or microservices. Justify with Conway's Law, deploy cadence, and operational cost. Include a migration path.
```

## Prompt 53 — API Design (REST)

```
Design a RESTful API for [DOMAIN]. Define resources, endpoints, status codes, pagination, filtering, error envelope, and versioning. Output as an OpenAPI-flavored spec. Note idempotency for writes.
```

## Prompt 54 — Event-Driven Design

```
Design an event-driven architecture for [USE CASE]. Define events, producers/consumers, delivery guarantees (at-least-once vs exactly-once), dead-letter handling, and schema evolution strategy.
```

## Prompt 55 — Database Schema Design

```
Design a normalized schema for [DOMAIN] with [RELATIONSHIPS]. Include indexes for the hot queries [QUERIES], partitioning if needed, and a note on read/write ratio. Flag any many-to-many or soft-delete handling.
```

## Prompt 56 — Caching Strategy

```
Design a caching layer for [WORKLOAD]: what to cache (read-through/write-through/aside), key design, TTL policy, invalidation, and how to avoid stampede/thundering herd. Include a fallback when cache is cold.
```

## Prompt 57 — Scalability Bottleneck Audit

```
Given this architecture [DIAGRAM/CODE], identify the next 3 scaling bottlenecks at [TARGET SCALE] and the cheapest mitigation for each. Rank by ROI.
```

## Prompt 58 — Choosing a Message Queue

```
Compare [KAFKA] vs [RABBITMQ] vs [SQS] for [USE CASE] with [THROUGHPUT] and [DELIVERY NEEDS]. Recommend one with tradeoffs and operational burden.
```

## Prompt 59 — Idempotency & Exactly-Once

```
Design idempotency for this payment/order endpoint:

[ENDPOINT LOGIC]

Add an idempotency key flow, dedupe store, and safe retry handling. Explain the correctness guarantee.
```

## Prompt 60 — Auth/Authorization Model

```
Design an authz model for [APP] with [ROLES] and [RESOURCES]. Choose RBAC vs ABAC, define the policy format, and show middleware enforcement. Note how to test it.
```

## Prompt 61 — Rate Limiting & Throttling

```
Design rate limiting for a public API: algorithm (token bucket/leaky bucket/sliding window), scope (per-user/IP/key), response headers, and distributed coordination. Provide pseudo-code.
```

## Prompt 62 — Multi-Tenancy Design

```
Design multi-tenancy for [SAAS] at [SCALE]: separate DB vs shared schema with tenant_id, isolation guarantees, noisy-neighbor mitigation, and migration from single to multi-tenant.
```

## Prompt 63 — Feature Flag Architecture

```
Design a feature-flag system: storage, evaluation (targeting rules), rollout safety, kill-switch, and how flags get cleaned up. Include a code example of a guarded path.
```

## Prompt 64 — Retry & Backoff Policy

```
Design a resilient retry policy for calls to [DEPENDENCY] with [FAILURE MODES]. Specify attempt count, backoff curve, jitter, timeout per attempt, and when to fail fast. Give code.
```

## Prompt 65 — Circuit Breaker Design

```
Add a circuit breaker around this unstable dependency:

[CODE]

Define open/half-open/closed states, thresholds, recovery, and what to return while open. Provide an implementation sketch.
```

## Prompt 66 — Data Pipeline Design

```
Design a batch/streaming pipeline for [DATA FLOW] with [VOLUME]. Choose ingestion, processing (stream vs batch), storage (lake/warehouse), and exactly-once semantics. Note schema drift handling.
```

## Prompt 67 — Frontend State Architecture

```
Design state management for a [FRAMEWORK] app of [COMPLEXITY]: local vs global, server cache (React Query/SWR), and when to reach for a store. Show the data-fetching flow and invalidation.
```

## Prompt 68 — Design Doc Critique

```
Critique this design doc for completeness and soundness:

[PASTE DOC]

Check: problem statement, requirements, options considered, tradeoffs, failure modes, rollout, and observability. List gaps.
```

## Prompt 69 — Tradeoff Exploration (Options)

```
For [DECISION], generate 3 viable architectural options with pros/cons, when each is appropriate, and a recommendation. Use a comparison table.
```

## Prompt 70 — Zero-Downtime Deployment

```
Design a zero-downtime deployment for [STATEFUL/STATELESS] service with [DB]. Cover blue/green vs canary, migration compatibility (expand/contract), and rollback.
```

## Prompt 71 — CAP Theorem Tradeoff

```
Our distributed store faces a network partition. Given [CONSISTENCY NEEDS] and [AVAILABILITY NEEDS], recommend CP vs AP and the user-visible behavior during partition. Justify.
```

## Prompt 72 — Observability Architecture

```
Design observability for [SYSTEM]: metrics (RED/USE), structured logs, distributed tracing, and SLOs. Specify what to instrument first and a sample dashboard layout.
```

## Prompt 73 — Cost-Efficient Architecture

```
Redesign [SYSTEM] to cut cloud cost by 40% without hurting p99 latency. Identify waste (over-provisioning, chatty calls, expensive storage tier) and cheaper alternatives.
```

## Prompt 74 — Schema Evolution Strategy

```
Define a backward/forward compatible schema evolution policy for [SERVICE] using [AVRO/PROTOBUF/JSON]. Show how to add/remove/rename fields safely across deployments.
```

## Prompt 75 — Architecture Decision Record (ADR)

```
Write an ADR for this decision: [CONTEXT], [DECISION], [OPTIONS]. Include status, consequences (good/bad), and links. Use the standard ADR template.
```

---

# 4. Refactoring (Prompts 76–100)

## Prompt 76 — Refactor Plan Generator

```
Refactor this function for clarity without changing behavior:

[PASTE CODE]

Show the before/after, the techniques used (extract method, early return, guard clauses), and how to verify equivalence with tests.
```

## Prompt 77 — Extract Method / Function

```
This method is [N] lines and does [THINGS]. Extract cohesive helpers with clear names and signatures. Keep side effects explicit. Show the result.

[PASTE CODE]
```

## Prompt 78 — Replace Conditionals with Polymorphism

```
This code uses a long if/else or switch on [TYPE]. Refactor to polymorphism/strategy so adding a type doesn't touch this block. Show the interface and implementations.

[PASTE CODE]
```

## Prompt 79 — Introduce Domain Types

```
Replace primitive obsession in this code with domain types (e.g., Email, Money, UserId). Show the type definitions and updated signatures, and note validation placement.

[PASTE CODE]
```

## Prompt 80 — Dead Code Remover

```
Identify dead/unreachable code, unused exports, and commented-out blocks in this file. List what's safe to delete and what looks dead but is referenced dynamically.

[PASTE CODE]
```

## Prompt 81 — Reduce Nesting / Guard Clauses

```
This function is deeply nested. Flatten it with guard clauses and early returns. Show the flattened version and the cyclomatic-complexity drop.

[PASTE CODE]
```

## Prompt 82 — Split God Class/Module

```
This class/module does too much: [RESPONSIBILITIES]. Propose a split into cohesive units with responsibilities, and show the new module boundaries and interfaces.

[PASTE CODE]
```

## Prompt 83 — Replace Temp with Query

```
Refactor this code to remove temporary variables in favor of intent-revealing queries/methods. Show the cleaner version.

[PASTE CODE]
```

## Prompt 84 — Parameter Object Refactor

```
This function takes [N] parameters. Introduce a parameter object to group related args. Show the new signature, the object shape, and call-site updates.

[PASTE CODE]
```

## Prompt 85 — Callback to Async/Await

```
Convert this callback/Promise-chain code to clean async/await with proper error handling. Show the result and note any parallelism you introduced.

[PASTE CODE]
```

## Prompt 86 — Immutability Refactor

```
Refactor this code to prefer immutability (const, pure functions, no in-place mutation). Show the safer version and explain the bug class it prevents.

[PASTE CODE]
```

## Prompt 87 — Magic Number / String Eliminator

```
Replace magic numbers and string literals in this code with named constants/config. Show the constants and updated references.

[PASTE CODE]
```

## Prompt 88 — Strategy Pattern Introduction

```
This code hardcodes an algorithm choice. Introduce the Strategy pattern so algorithms are swappable. Show the interface, implementations, and a factory/registry.

[PASTE CODE]
```

## Prompt 89 — Repository Pattern for Data Access

```
Extract raw DB calls from business logic into a repository. Show the repository interface, impl, and how the caller changes. Note testability gains.

[PASTE CODE]
```

## Prompt 90 — Dependency Inversion

```
This high-level module depends directly on a low-level detail. Apply dependency inversion (pass dependencies in). Show the interface and constructor injection.

[PASTE CODE]
```

## Prompt 91 — Null Object / Optional Refactor

```
Replace null checks scattered through this code with a Null Object or Optional/Maybe pattern. Show the cleaner control flow.

[PASTE CODE]
```

## Prompt 92 — Loop to Higher-Order Refactor

```
Refactor these imperative loops to declarative map/filter/reduce (or list comprehensions). Preserve behavior and note readability/perf tradeoffs.

[PASTE CODE]
```

## Prompt 93 — Monolith Module Extraction

```
This module is tightly coupled to the monolith. Define a seam to extract it into its own package/service. Show the interface boundary, data ownership, and a strangler-step rollout.

[PASTE CODE/CONTEXT]
```

## Prompt 94 — Error Type Refactor

```
Replace stringly-typed errors with a typed error hierarchy. Show the types and how callers discriminate. Note how this improves handling.

[PASTE CODE]
```

## Prompt 95 — Config Centralization

```
Config is scattered as literals across files. Centralize into a validated config module with env mapping. Show the schema and access pattern.

[PASTE CODE]
```

## Prompt 96 — Testability Refactor

```
This code is hard to test (hidden deps, static calls, time). Refactor for testability: inject clock, IO, and randomness. Show the seam and a sample test.

[PASTE CODE]
```

## Prompt 97 — Rename for Intent

```
Suggest clearer names for these identifiers based on their behavior. Show old → new and the reasoning. Flag any that are fine as-is.

[PASTE CODE]
```

## Prompt 98 — Duplicate to Shared Utility

```
These three snippets do nearly the same thing. Extract a shared utility with parameters. Show the utility and the three call sites.

[SNIPPET A]

[SNIPPET B]

[SNIPPET C]
```

## Prompt 99 — Safe Refactor with Characterization Tests

```
Before refactoring this legacy code, write characterization tests that lock current behavior. Then show the refactor. List what the tests must cover.

[PASTE CODE]
```

## Prompt 100 — Refactor ROI Prioritizer

```
Given this file with [SMELLS], rank refactorings by risk-adjusted ROI (effort vs maintainability/clarity gain). Recommend what to do now vs defer, with a one-line reason each.
```

---

# 5. Testing (Prompts 101–125)

## Prompt 101 — Unit Test Generator

```
Write unit tests for this function covering happy path, edge cases, and error paths. Use [FRAMEWORK]. Each test should have a clear name and one assertion focus.

[PASTE FUNCTION]
```

## Prompt 102 — Edge Case Brainstormer

```
List all edge cases for this function: null/empty, boundaries, large input, unicode, concurrency, negative, type coercion. Output as a test-case table.

[PASTE FUNCTION]
```

## Prompt 103 — Test Name Improver

```
Rewrite these test names to be behavior-focused and readable (should_X_when_Y). Show before/after and why the new names help.

[PASTE TEST NAMES]
```

## Prompt 104 — Mocking Strategy

```
This test needs to isolate [UNIT] from [DEPENDENCIES]. Recommend what to mock vs use real, the seam to inject, and show the mock setup in [FRAMEWORK].

[PASTE CODE]
```

## Prompt 105 — Integration Test Design

```
Design an integration test for [FLOW] hitting [SERVICES]. Specify setup/teardown, data fixtures, assertions on side effects, and how to keep it deterministic.

[CONTEXT]
```

## Prompt 106 — Property-Based Test

```
Design property-based tests for this function using [LIBRARY]. Define invariants (commutativity, idempotence, round-trip) and show the test skeleton.

[PASTE FUNCTION]
```

## Prompt 107 — Table-Driven Test

```
Convert these repetitive tests into a table-driven test. Show the cases array and the loop/runner. Preserve coverage.

[PASTE TESTS]
```

## Prompt 108 — Flaky Test Fixer

```
This test is flaky due to [CAUSE]. Harden it (deterministic time, seeded random, proper async await, isolation). Show the fix.

[PASTE TEST]
```

## Prompt 109 — Mutation Testing Guidance

```
We added mutation testing with [TOOL]. Review the surviving mutants and suggest missing assertions. Explain why each mutant should be killed.

[MUTANT REPORT]
```

## Prompt 110 — Coverage Gap Analyzer

```
Given this coverage report, list the highest-value untested paths (error branches, boundaries) and a test for each. Ignore trivial getters.

[COVERAGE REPORT]
```

## Prompt 111 — E2E Test Scenario Designer

```
Design E2E scenarios for [FEATURE] in [TOOL]. Cover critical user journeys, happy + sad paths, and one cross-feature flow. Note what NOT to E2E (keep suite fast).

[CONTEXT]
```

## Prompt 112 — API Contract Test

```
Write a contract test between [CONSUMER] and [PROVIDER] verifying status, schema, and error envelope. Show the test and the schema assertion.

[API SPEC]
```

## Prompt 113 — Performance/Load Test Plan

```
Design a load test for [ENDPOINT] targeting [RPS] and [P99]. Specify workload shape, ramp, metrics, and pass/fail thresholds. Suggest a tool.

[CONTEXT]
```

## Prompt 114 — Snapshot Test Review

```
We overuse snapshot tests. Review these and flag which should be explicit assertions instead (to avoid masking changes). Show the better assertion.

[PASTE TESTS]
```

## Prompt 115 — Test Data Builder

```
Create a test-data builder/factory for [ENTITY] with sensible defaults and overrides. Show the builder API and 3 usage examples.

[ENTITY SCHEMA]
```

## Prompt 116 — Boundary Value Analysis

```
For this input with range [MIN–MAX], generate boundary value tests (min, min+1, max-1, max, out-of-range). Show expected behavior per case.

[PASTE FUNCTION]
```

## Prompt 117 — Fuzz Test Design

```
Design a fuzz test for this parser/deserializer using [TOOL]. Define the input grammar and the invariants that must hold. Show setup.

[PASTE CODE]
```

## Prompt 118 — TDD Starter

```
I'm TDD-ing [FEATURE]. Write the first failing test (red), then the minimal implementation (green), then a refactor note. Show both steps.

[FEATURE DESCRIPTION]
```

## Prompt 119 — Regression Test from Bug

```
Turn this past bug [DESCRIPTION + FIX] into a regression test that fails without the fix and passes with it. Show the test and what it guards.

[BUG CONTEXT]
```

## Prompt 120 — Accessibility Test Checklist

```
Generate an automated + manual a11y test checklist for [COMPONENT]: axe rules, keyboard paths, screen-reader announcements. Map each to a test or manual step.

[COMPONENT CODE]
```

## Prompt 121 — Concurrency Test

```
Write a test that stresses this concurrent code with [N] threads/tasks to expose races. Show how to detect failure (assertions on final state) and a stable run.

[PASTE CODE]
```

## Prompt 122 — Database Test Isolation

```
Our DB tests interfere with each other. Design transactional/per-test isolation with fixtures and cleanup. Show the pattern in [FRAMEWORK].

[CONTEXT]
```

## Prompt 123 — Negative/Error Path Tests

```
List the error paths in this function and write a test for each (thrown errors, rejected promises, returned error objects). Show assertions on the error.

[PASTE FUNCTION]
```

## Prompt 124 — Test Doubles Decision

```
For testing [UNIT], decide between stub/fake/mock/spy for each collaborator. Justify per collaborator and show the chosen double in [FRAMEWORK].

[CONTEXT]
```

## Prompt 125 — Test Suite Health Report

```
Audit this test suite for slow tests, duplication, weak assertions, and order dependence. Rank improvements by impact and give a 1-week plan.

[SUITE CONTEXT]
```

---

# 6. Documentation (Prompts 126–150)

## Prompt 126 — README Generator

```
Write a README for this project: one-line description, badges, install, quick start, usage example, config, contributing, and license. Match the tone to [AUDIENCE].

[PROJECT CONTEXT / FILES]
```

## Prompt 127 — Function/Module Docstring

```
Write clear docstrings for these functions following [STYLE] (Google/NumPy/Sphinx). Include params, returns, raises, and a usage example each.

[PASTE CODE]
```

## Prompt 128 — Architecture Overview Doc

```
Write a 1-page architecture overview for [SYSTEM]: components, data flow, key decisions, and diagrams (ASCII). Audience: new engineer joining the team.
```

## Prompt 129 — Runbook / On-Call Guide

```
Write an on-call runbook for [SERVICE]: what it does, common alerts, symptom→cause→fix table, escalation path, and how to deploy/rollback.

[SERVICE CONTEXT]
```

## Prompt 130 — API Reference from Code

```
Generate API reference docs (endpoints, params, responses, examples) from this source. Use [FORMAT]. Fill gaps where code lacks comments with [PLACEHOLDER].

[SOURCE]
```

## Prompt 131 — ADR Writer

```
Write an Architecture Decision Record for [DECISION]: context, options, chosen approach, consequences, and status. Use the standard ADR template.
```

## Prompt 132 — Tutorial / How-To

```
Write a step-by-step tutorial for [TASK] targeting [SKILL LEVEL]. Include prerequisites, numbered steps, expected output per step, and a troubleshooting section.
```

## Prompt 133 — Troubleshooting Guide

```
Create a troubleshooting guide for [PRODUCT] from these known issues: [ISSUES]. For each: symptom, cause, fix, and prevention. Group by area.
```

## Prompt 134 — Changelog Generator

```
Generate a user-facing CHANGELOG entry from these commits [COMMITS], grouped by Added/Changed/Fixed/Deprecated. Follow Keep a Changelog. Avoid internal jargon.
```

## Prompt 135 — Code Comment Improver

```
Improve the comments in this file: remove noise, add why-not-what, explain non-obvious logic and constraints. Show the annotated version.

[PASTE CODE]
```

## Prompt 136 — Glossary Builder

```
Build a glossary of [DOMAIN] terms used in this codebase. For each: plain-language definition and a code reference. Audience: onboarding devs.

[CODE/DOCS]
```

## Prompt 137 — Diagram-as-Code

```
Produce a Mermaid/ASCII diagram for [FLOW/ARCHITECTURE]. Choose the right diagram type (sequence/flow/class) and label the key actors and steps.

[CONTEXT]
```

## Prompt 138 — Onboarding Doc

```
Write a 1-week onboarding plan + doc for a new dev on [TEAM]: environment setup, architecture tour, first-good-issue suggestions, and who to ask for what.
```

## Prompt 139 — Design Doc Template

```
Provide a reusable design doc template covering problem, goals/non-goals, requirements, options, tradeoffs, rollout, and observability. Fill the header with [PROJECT].
```

## Prompt 140 — Inline Error Message Writer

```
Rewrite these user-facing error messages to be actionable (what happened, why, next step). Keep under [N] words each. Show before/after.

[PASTE MESSAGES]
```

## Prompt 141 — Doc String Consistency Audit

```
Audit this docs set for inconsistencies: outdated examples, broken references, mismatched API names. List each with file:line and the correction.

[DOCS]
```

## Prompt 142 — Video/Quickstart Script

```
Write a 90-second quickstart script (spoken narration + on-screen actions) for [TOOL]. Audience: first-time user. Keep it punchy and demo-ready.
```

## Prompt 143 — FAQ Generator

```
Generate an FAQ for [PRODUCT] from these support questions [QUESTIONS]. For each: the question, a concise answer, and a link to deeper docs if relevant.
```

## Prompt 144 — Internal Knowledge Base Article

```
Write a KB article explaining [CONCEPT] to [TEAM]. Include why it matters, how it works at a high level, gotchas, and links to source/specs.
```

## Prompt 145 — Open Source Contributing Guide

```
Write CONTRIBUTING.md for this OSS repo: how to set up, branch/PR convention, test/lint requirements, review process, and code of conduct pointer.

[REPO CONTEXT]
```

## Prompt 146 — API Migration Guide

```
Write a migration guide from API v1 to v2: breaking changes, before/after calls, deprecation timeline, and a codemod suggestion.

[V1 SPEC]

[V2 SPEC]
```

## Prompt 147 — Release Notes

```
Write release notes for [VERSION]: headline feature, notable fixes, upgrade steps, and known issues. Tone: friendly, confident, concise.
```

## Prompt 148 — Explain-This-Code Doc

```
Explain what this complex function does, in plain language, for a teammate. Cover intent, inputs/outputs, side effects, and the one thing that trips people up.

[PASTE CODE]
```

## Prompt 149 — Documentation Gap Audit

```
Given the codebase [STRUCTURE] and existing docs [DOCS], list the top documentation gaps (missing READMEs, undocumented public APIs, no runbook) ranked by impact.
```

## Prompt 150 — Doc Tone & Clarity Editor

```
Edit this documentation for clarity and consistent voice per [STYLE GUIDE]: shorten sentences, active voice, consistent terminology, scannable headings. Show the revised version.

[PASTE DOCS]
```

---

> **That's all 150 prompts.** Copy any block into your LLM of choice, replace the `[BRACKETED]` placeholders with your real context, and ship faster. For the latest companion tooling, see the Paperclip `code-tools` collection.
