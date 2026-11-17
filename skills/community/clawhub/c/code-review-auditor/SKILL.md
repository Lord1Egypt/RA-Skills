---
name: code-review-auditor
description: Review codebases for bugs, security issues, architecture/SOLID problems, code smells, justified design-pattern opportunities, anti-patterns, performance, observability, testability, hotspots, and planned refactors without changing code during analysis.
metadata:
  short-description: Code review, security, architecture, smells, patterns, and refactor planning
---

# Code Review Auditor

Use this skill when the user asks for a code review, architecture review, security review, refactoring review, design-pattern assessment, hotspot analysis, or a planned fix/refactor workflow.

## Non-Negotiable Constraints

- Analysis modes never edit source code, tests, configuration, migrations, lockfiles, generated files, or infrastructure files.
- Refactoring and fixes must be planned before implementation. Create or update `review/<timestamp>/refactoring-plan.md` first, then wait for explicit user approval unless the user has already asked to implement that plan.
- Avoid overengineering. Recommend a pattern, abstraction, split, layer, or framework only when it reduces current or near-term complexity and is justified by evidence in the code.
- Every execution must end by creating a local review folder in the project being reviewed:

```text
review/YYYY-MM-DD_HH-mm-ss/
```

Use the local timezone for the timestamp. Include seconds. If two runs collide, append `-NN` while preserving the timestamp.

## Supported Modes

Choose the narrowest mode that satisfies the user request. If the user does not specify a mode, use `complete` for broad review requests and `diff` when the request clearly focuses on changed code.

- `complete`: full project review across all categories.
- `diff` or `changed`: review only changed files and relevant call sites.
- `security`: vulnerabilities, insecure defaults, secrets, authz/authn, injection, SSRF, deserialization, path traversal, dependency risk.
- `architecture`: module boundaries, layering, SOLID, coupling, cohesion, domain leakage, framework misuse.
- `smells`: maintainability problems and local code-quality issues.
- `patterns`: justified opportunities for Strategy, Factory, Adapter, Decorator, Chain of Responsibility, State, Specification, Repository, Unit of Work, Observer, or other patterns already aligned with the project.
- `performance`: hot paths, query behavior, memory, concurrency, IO, caching, serialization, batch size, retries, backpressure.
- `tests`: missing, weak, brittle, slow, flaky, low-signal, or over-mocked tests.
- `hotspots`: prioritize files by churn, complexity, ownership, risk, dependency fan-in/fan-out, and production criticality.
- `explain`: explain findings, risks, and tradeoffs without changing code.
- `fix`: propose and, only after approval, implement narrowly scoped fixes.
- `refactor`: propose and, only after approval, implement behavior-preserving refactors.
- `challenge`: critique an existing implementation or proposal, looking for hidden failure modes and unjustified complexity.

Read [workflows/modes.md](workflows/modes.md) when mode selection or mode-specific deliverables matter.

## Required Review Folder

At the end of every execution, write the review package using [templates/output-structure.md](templates/output-structure.md). At minimum include:

- `summary.md`
- `findings.md` or category files such as `security.md`, `architecture.md`, `bugs.md`, `code-smells.md`, `patterns.md`, `performance.md`, `testing.md`, and `observability.md`
- `hotspots.md`
- `metrics/score.md`
- `metadata.json`
- `refactoring-plan.md` when fixes, refactors, or material design changes are proposed

Use `scripts/create_review_run.py` to create the timestamped folder and seed the required files when helpful.

## Finding Contract

Each finding must include:

- stable ID within the execution
- file and line range
- category
- title and description
- evidence from the code
- impact
- severity
- confidence
- effort
- priority
- recommendation
- suggested example or refactoring sketch
- possible false-positive note

Use the models in [rules/scoring.md](rules/scoring.md) and the finding template in [templates/finding.md](templates/finding.md).

## Review Method

1. Identify the stack, framework, package manager, test tools, database layer, messaging systems, and deployment/infrastructure hints.
2. Read the changed files or representative architecture before judging. Prefer repository-local conventions over generic preferences.
3. Check category-specific rules from [rules/categories.md](rules/categories.md), then read only the relevant stack guide from `stacks/`.
4. Verify each important finding against actual code paths, tests, configuration, or runtime contracts when possible.
5. De-duplicate findings. Prefer one root-cause finding over many symptoms.
6. Record false-positive possibilities instead of overstating certainty.
7. Assign severity, confidence, effort, priority, and refactorability score consistently.
8. Write all review artifacts before responding to the user.

## Stack Guides

Read only the relevant guides:

- Java/Spring: [stacks/java-spring.md](stacks/java-spring.md)
- Node/TypeScript: [stacks/node-typescript.md](stacks/node-typescript.md)
- Kotlin: [stacks/kotlin.md](stacks/kotlin.md)
- Swift: [stacks/swift.md](stacks/swift.md)
- React: [stacks/react.md](stacks/react.md)
- Databases: [stacks/database.md](stacks/database.md)
- Kafka: [stacks/kafka.md](stacks/kafka.md)

## Output Tone

Be direct and evidence-led. Findings are not style opinions. Call out what can break, where, why it matters, and the smallest responsible improvement.
