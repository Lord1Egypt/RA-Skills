# =============================================================================
# Domain-Driven Design — Project Scaffold
# =============================================================================
#
# Tactical DDD patterns: value objects, entities, aggregates,
# repositories, domain events, and domain services.
#
# Usage:
#   Copy this directory as your project starting point.
#   Replace the example Order aggregate with your own bounded context.
#
# Core Principles:
#   - Entities have identity, value objects have equality by content
#   - Aggregates are consistency boundaries — all changes through the root
#   - Repositories exist for aggregate roots only
#   - Domain events decouple aggregates and bounded contexts
#
# =============================================================================

## Directory Structure

```
src/
├── domain/                         # Core domain model
│   ├── aggregates/                 # Aggregate roots with their children
│   │   ├── order.aggregate.ts      # Example: Order aggregate root
│   │   └── order-item.entity.ts    # Child entity (managed by Order)
│   ├── entities/                   # Standalone entities (if any)
│   │   └── customer.entity.ts
│   ├── value-objects/              # Immutable domain concepts
│   │   ├── money.value-object.ts   # Example: Money value object
│   │   ├── order-id.value-object.ts
│   │   ├── email.value-object.ts
│   │   └── quantity.value-object.ts
│   ├── events/                     # Domain events (past tense)
│   │   ├── order-submitted.event.ts # Example: OrderSubmitted event
│   │   └── order-cancelled.event.ts
│   ├── services/                   # Domain services (cross-aggregate logic)
│   │   └── pricing.service.ts
│   ├── repositories/               # Repository interfaces (ports)
│   │   └── order.repository.ts
│   └── errors/                     # Domain-specific errors
│       └── domain.errors.ts
│
├── application/                    # Application services (use cases)
│   ├── submit-order.use-case.ts
│   ├── cancel-order.use-case.ts
│   └── event-handlers/             # React to domain events
│       ├── send-confirmation.handler.ts
│       └── update-inventory.handler.ts
│
├── infrastructure/                 # Technical implementations
│   ├── persistence/                # Repository implementations
│   │   └── prisma-order.repository.ts
│   ├── messaging/                  # Event bus implementation
│   │   └── event-dispatcher.ts
│   └── composition-root.ts        # Dependency wiring
│
└── main.ts                         # Entry point
```

## Customize

1. **Identify your aggregates** — What are your consistency boundaries?
2. **Define value objects** — What concepts need validation and immutability?
3. **Model aggregate roots** — All external access goes through the root
4. **Define domain events** — What happenings need to propagate?
5. **Create repository interfaces** — One per aggregate root
6. **Implement application services** — Orchestrate aggregates and services

## Key Rules

- Aggregates reference other aggregates by **ID**, not by object
- All changes to an aggregate go through the **aggregate root**
- Repository interfaces are in `domain/` — implementations in `infrastructure/`
- Domain events are collected during mutation, published after persistence
- Value objects are **immutable** — operations return new instances
- One repository per **aggregate root** — child entities saved through parent
