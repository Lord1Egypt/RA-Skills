---
name: effective_java
description: Review, refactor, and explain Java code using distilled Effective Java principles for API design, immutability, generics, enums, streams, exceptions, concurrency, and serialization.
---

# Effective Java

## Core Stance

Use this skill as an Effective Java design and review lens, not as a rigid style guide. Prefer APIs that are simple, type-safe, immutable where practical, composition-friendly, well-documented at boundaries, and hard to misuse.

Do not reproduce book text. Paraphrase the principles, explain tradeoffs, and cite item numbers only as navigation aids when helpful.

## Workflow

1. Classify the task: new API design, code review, refactor, bug fix, performance pass, or teaching/explanation.
2. Load `references/review-checklist.md` for reviews, refactors, or whenever code is provided.
3. Load `references/item-map.md` when the user asks for item-level mapping, broad Effective Java coverage, or a learning summary.
4. Inspect the public contract first: construction, mutability, equality, generics, exceptions, threading, serialization, and compatibility.
5. Prioritize recommendations by semantic risk before style: correctness, API safety, encapsulation, maintainability, then performance.
6. If editing code, make the smallest change that preserves existing behavior and public compatibility unless the user explicitly asks for an API redesign.

## Default Review Order

- **Correctness**: broken invariants, resource leaks, equality/hash violations, unsafe publication, races, swallowed exceptions.
- **API design**: confusing construction, boolean traps, excessive overloads, raw types, wildcard misuse, checked exceptions that are not recoverable.
- **Encapsulation**: exposed mutable state, public fields, inheritance without contracts, mutable static state, missing defensive copies.
- **Type safety**: unchecked casts, heap pollution, arrays mixed with generics, int constants where enums fit.
- **Clarity**: stream/lambda overuse, unclear method references, unnecessary cleverness, duplicated construction logic.
- **Performance**: avoid premature tuning; flag avoidable object churn, boxing, synchronization bottlenecks, and inappropriate parallel streams only after semantics are sound.

## High-Value Heuristics

- Prefer named static factories when names, caching, subtype returns, or instance control improve the API; keep constructors when the simple shape is clearer.
- Use builders for constructors with many optional parameters; validate invariants in one place before object publication.
- Prefer dependency injection over hard-coded singletons or static utilities for resources that vary or need testing.
- Favor immutability, minimize visibility, and make defensive copies at trust boundaries.
- Prefer composition over inheritance unless inheritance is deliberately designed, documented, and tested.
- Eliminate raw types; use bounded wildcards with PECS: producers `extends`, consumers `super`.
- Use enums instead of integer or string constants; use `EnumSet` and `EnumMap` for enum-keyed collections.
- Use lambdas and streams for clear transformations; keep complex control flow, checked exceptions, and stateful logic out of streams.
- Validate parameters at boundaries; return empty collections or arrays instead of `null` for multi-value returns.
- Use checked exceptions only for conditions callers can reasonably recover from; otherwise prefer unchecked exceptions with useful messages.
- Treat concurrency as a correctness concern: prefer immutability, executors, concurrent collections, and explicit thread-safety documentation.
- Avoid Java serialization for new designs; if forced to support it, validate invariants and consider the serialization proxy pattern.

## Response Patterns

For code review, answer with prioritized findings:

```text
- [P1] Title (`Path.java:line`): explain the concrete risk.
  Effective Java lens: item family or principle.
  Change: concise, actionable fix.
```

For refactoring, explain the chosen item families, apply a focused patch, then list behavior and compatibility assumptions plus validation performed.

For teaching, group principles by problem type and include small original examples rather than long quotes from the book.

## Guardrails

- Preserve public API compatibility unless the user explicitly asks for breaking changes.
- Do not turn every class immutable, every constructor into a builder, or every loop into a stream; justify each recommendation by context.
- Do not add frameworks or large abstractions when a Java language or library feature solves the problem.
- Call out uncertainty when source context is missing, especially around concurrency guarantees, serialization compatibility, and external API contracts.
