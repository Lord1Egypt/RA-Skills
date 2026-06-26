# Effective Java Review Checklist

Use this checklist when reviewing or refactoring Java code. Start at the top and stop when you have enough high-value findings; avoid dumping every possible style preference.

## 1. Construction and Lifecycle

- Static factories: use when a name clarifies intent, instances are controlled or cached, return type can be an interface or subtype, or construction can hide complexity.
- Constructors: keep when arguments are few, required, and obvious; avoid telescoping constructors with many optional values.
- Builders: use for many optional parameters, cross-field validation, and readable call sites; keep the target object immutable when possible.
- Dependency injection: inject clocks, random sources, clients, repositories, configuration, and strategies; avoid global statics for variable resources.
- Resource cleanup: use try-with-resources for `AutoCloseable`; avoid finalizers and cleaners except as last-resort safety nets.
- Object churn: reuse expensive immutable objects; avoid accidental boxing and regex recompilation in hot paths.

## 2. Object Contracts

- `equals`: check reflexive, symmetric, transitive, consistent, and non-null behavior; avoid equality across incompatible subclasses.
- `hashCode`: update with every significant equality field; ensure equal objects have equal hashes.
- `toString`: include useful state for diagnostics without exposing secrets or unstable implementation details.
- `clone`: be skeptical; prefer copy constructors, static copy factories, or builders.
- `Comparable`: ensure ordering is consistent, transitive, and documented when inconsistent with `equals`.

## 3. Classes and Interfaces

- Visibility: make classes, constructors, methods, fields, and nested types as private or package-private as possible.
- Mutability: make fields `final` where practical; protect invariants; avoid leaking mutable internals.
- Defensive copies: copy incoming mutable values and outgoing mutable state at trust boundaries.
- Inheritance: prefer composition; if inheritable, document override hooks and self-use, or prohibit with `final` or private constructors.
- Interfaces: define behavior contracts; avoid constant interfaces; use skeletal implementations only when they reduce repeated correct code.
- Nested classes: make nested classes `static` unless they need the enclosing instance.

## 4. Generics and Type Safety

- Remove raw types and unchecked warnings at the source; do not suppress broad scopes.
- Prefer generic methods and classes over casts at call sites.
- Use bounded wildcards for flexibility: `? extends T` for producers, `? super T` for consumers.
- Prefer lists to arrays for generic element types; arrays are covariant and reified, generics are invariant and erased.
- Guard varargs with generics; use `@SafeVarargs` only when the method does not write into or expose the varargs array unsafely.
- Prefer type-safe heterogeneous containers when a map needs keys of different value types.

## 5. Enums and Annotations

- Replace integer or string constants with enums when the value set is known.
- Put behavior on enum constants when it removes switches scattered across the codebase.
- Use `EnumSet` and `EnumMap` instead of bit fields or ordinal-indexed arrays.
- Never persist or depend on enum ordinals; use stable names or explicit codes.
- Use annotations instead of naming conventions for framework hooks, tests, validation, or code generation metadata.

## 6. Lambdas and Streams

- Prefer lambdas for small behavior blocks; prefer method references only when they are clearer than lambdas.
- Keep stream pipelines side-effect-free, short, and readable.
- Do not force streams onto logic with early returns, checked exceptions, mutation-heavy accumulation, or complex branching.
- Use primitive streams to avoid boxing in numeric pipelines.
- Avoid parallel streams unless the data source, operation cost, splitting behavior, and collector semantics are proven suitable.

## 7. Methods and Defensive Programming

- Validate public parameters near method entry; validate private method assumptions with assertions when useful.
- Make method signatures explicit and small; avoid boolean parameters that hide modes when separate methods or enums are clearer.
- Return empty collections or arrays for no results; avoid `null` multi-value returns.
- Use `Optional` for optional return values judiciously; avoid fields, parameters, and collection elements of `Optional`.
- Document units, ownership, mutation, thread-safety, and exceptional behavior.
- Make defensive copies before validation when mutable inputs could be changed concurrently.

## 8. Exceptions

- Use exceptions for exceptional conditions, not normal loop or control flow.
- Use checked exceptions only for recoverable conditions the caller can handle.
- Preserve causes when translating exceptions.
- Fail atomically where practical: a failed operation should leave objects unchanged.
- Include useful failure-capture information in exception messages, without leaking secrets.
- Do not ignore exceptions; if suppression is intentional, document why.

## 9. Concurrency

- Prefer immutable objects and thread confinement before locks.
- Synchronize all access to shared mutable state, not just writes.
- Use `ExecutorService`, `CompletableFuture`, concurrent collections, atomics, locks, and synchronizers instead of manually managing threads when possible.
- Document thread-safety: immutable, thread-safe, conditionally thread-safe, not thread-safe, or thread-hostile.
- Avoid calling overridable or foreign methods while holding locks.
- Use lazy initialization only when needed; implement it with safe publication patterns.

## 10. Serialization

- Avoid Java native serialization for new APIs; prefer explicit formats.
- If serialization is required, define serialized form deliberately and treat it as a public API.
- Validate invariants during deserialization.
- Use defensive copies for mutable serialized components.
- Consider a serialization proxy for classes with invariants.
- Be cautious with `readObject`, `readResolve`, and `serialVersionUID`; mistakes become compatibility or security issues.

## Finding Template

```text
- [P1/P2/P3] Problem title (`File.java:line`): concrete impact.
  Effective Java lens: principle or item range.
  Fix: smallest safe change.
  Compatibility: note if public API or serialized form changes.
```
