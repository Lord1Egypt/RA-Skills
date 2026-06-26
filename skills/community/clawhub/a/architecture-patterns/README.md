# Architecture Patterns

Backend architecture patterns for building maintainable, testable systems: Clean Architecture, Hexagonal Architecture, and Domain-Driven Design.

## What's Inside

- Decision Framework — which pattern for which situation
- Clean Architecture — layers (entities, use cases, interface adapters, frameworks), dependency rule, implementation examples
- Hexagonal Architecture (Ports & Adapters) — ports as interfaces, adapters as swappable implementations
- Domain-Driven Design — value objects, aggregates, domain events, repository pattern
- Directory Structure for layered architecture
- Entity, Port, Use Case, and Adapter implementation patterns (Python)
- Testing Benefits — mock adapters for easy unit testing

## When to Use

- Designing new backend systems from scratch
- Refactoring monoliths for better maintainability
- Establishing architecture standards for teams
- Creating testable, mockable codebases
- Planning microservices decomposition

## Installation

```bash
npx add https://github.com/wpank/ai/tree/main/skills/backend/architecture-patterns
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/backend/architecture-patterns .cursor/skills/architecture-patterns
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/backend/architecture-patterns ~/.cursor/skills/architecture-patterns
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/backend/architecture-patterns .claude/skills/architecture-patterns
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/backend/architecture-patterns ~/.claude/skills/architecture-patterns
```

## Related Skills

- `architecture-decision-records` — Document architecture decisions made using these patterns
- `microservices-patterns` — Distributed system patterns that build on these foundations
- `service-layer-architecture` — Controller-service-query layered architecture

---

Part of the [Backend](..) skill category.
