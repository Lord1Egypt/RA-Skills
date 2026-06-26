# =============================================================================
# Clean Architecture - Project Scaffold
# =============================================================================
#
# Directory structure implementing Uncle Bob's Clean Architecture
# with TypeScript. Dependencies always point inward.
#
# Usage:
#   Copy this directory as your project starting point.
#   Replace the example User entity and CreateUser use case
#   with your own domain concepts.
#
# Dependency Rule:
#   domain ← use-cases ← adapters ← infrastructure
#   Inner layers NEVER import from outer layers.
#   Inner layers define interfaces. Outer layers implement them.
#
# =============================================================================

## Directory Structure

```
src/
├── domain/                     # Layer 1: Enterprise Business Rules
│   ├── entities/               # Business objects with behavior
│   │   └── user.entity.ts      # Example: User entity
│   ├── value-objects/           # Immutable, identity-less types
│   │   └── email.value-object.ts
│   ├── interfaces/             # Ports (repository contracts, service contracts)
│   │   └── repository.interface.ts
│   ├── errors/                 # Domain-specific error classes
│   │   └── domain.errors.ts
│   └── events/                 # Domain events
│       └── user-created.event.ts
│
├── use-cases/                  # Layer 2: Application Business Rules
│   ├── create-user.use-case.ts # Example: Create user use case
│   ├── get-user.use-case.ts
│   └── dtos/                   # Request/Response data transfer objects
│       └── user.dto.ts
│
├── adapters/                   # Layer 3: Interface Adapters
│   ├── controllers/            # HTTP/GraphQL request handlers
│   │   └── user.controller.ts  # Example: Express controller
│   ├── repositories/           # Persistence implementations
│   │   └── prisma-user.repository.ts
│   ├── presenters/             # Response formatters
│   │   └── user.presenter.ts
│   └── mappers/                # Entity ↔ persistence model mapping
│       └── user.mapper.ts
│
├── infrastructure/             # Layer 4: Frameworks & Drivers
│   ├── config/                 # Environment, app configuration
│   ├── database/               # Database connection, migrations
│   ├── http/                   # Express/Fastify app setup, middleware
│   └── composition-root.ts     # Wires all dependencies together
│
└── main.ts                     # Entry point — starts the application
```

## Customize

1. **Replace example entities** — Change `user.entity.ts` to your domain
2. **Add value objects** — Create types for Email, Money, UserId, etc.
3. **Define repository interfaces** — One per aggregate root in `domain/interfaces/`
4. **Create use cases** — One class per application operation in `use-cases/`
5. **Implement adapters** — Wire controllers and repositories in `adapters/`
6. **Set up composition root** — Connect everything in `infrastructure/composition-root.ts`

## Key Rules

- `domain/` imports from: nothing (zero external dependencies)
- `use-cases/` imports from: `domain/` only
- `adapters/` imports from: `use-cases/` and `domain/`
- `infrastructure/` imports from: everything (outermost layer)
- Never import framework packages (express, prisma, etc.) in `domain/` or `use-cases/`
