# =============================================================================
# Hexagonal Architecture (Ports & Adapters) - Project Scaffold
# =============================================================================
#
# The domain core communicates with the outside world exclusively through
# ports (interfaces). Adapters connect external technologies to these ports.
#
# Usage:
#   Copy this directory as your project starting point.
#   Replace the example Order domain with your own business concepts.
#
# Key Distinction:
#   Primary (Driving) — external world drives the app (HTTP, CLI, events)
#   Secondary (Driven) — app drives external services (DB, payment, email)
#
# =============================================================================

## Directory Structure

```
src/
├── domain/                         # Core business logic (the hexagon)
│   ├── order.service.ts            # Example: Domain service
│   ├── entities/                   # Business entities with behavior
│   │   └── order.entity.ts
│   ├── value-objects/              # Immutable domain concepts
│   │   └── money.value-object.ts
│   ├── errors/                     # Domain-specific errors
│   │   └── domain.errors.ts
│   └── events/                     # Domain events
│       └── order-submitted.event.ts
│
├── ports/                          # Interfaces (hexagon edges)
│   ├── inbound/                    # Primary ports — USE CASE interfaces
│   │   ├── create-order.port.ts    # What the app can do
│   │   └── get-order.port.ts
│   └── outbound/                   # Secondary ports — DEPENDENCY interfaces
│       ├── order-repository.port.ts    # What the app needs from persistence
│       └── payment-gateway.port.ts     # What the app needs from payments
│
├── adapters/                       # Implementations (outside the hexagon)
│   ├── primary/                    # Driving adapters — call inbound ports
│   │   ├── rest/                   # REST API adapter
│   │   │   └── order.controller.ts
│   │   ├── cli/                    # CLI adapter (same port, different trigger)
│   │   │   └── order.command.ts
│   │   └── graphql/                # GraphQL adapter
│   │       └── order.resolver.ts
│   └── secondary/                  # Driven adapters — implement outbound ports
│       ├── persistence/            # Database adapter
│       │   └── prisma-order.repository.ts
│       ├── payment/                # Payment processor adapter
│       │   └── stripe-payment.adapter.ts
│       └── notification/           # Notification adapter
│           └── email-notifier.adapter.ts
│
├── infrastructure/                 # Framework & wiring
│   ├── config/                     # Environment configuration
│   └── composition-root.ts        # Wires adapters to ports
│
└── main.ts                         # Entry point
```

## Customize

1. **Define domain entities** — Your core business objects in `domain/entities/`
2. **Create inbound ports** — Use case interfaces in `ports/inbound/`
3. **Create outbound ports** — Dependency interfaces in `ports/outbound/`
4. **Implement domain logic** — Use cases in `domain/` that implement inbound ports
5. **Build primary adapters** — REST, CLI, or GraphQL adapters in `adapters/primary/`
6. **Build secondary adapters** — DB, payment, email adapters in `adapters/secondary/`
7. **Wire in composition root** — Connect everything in `infrastructure/composition-root.ts`

## Key Rules

- `domain/` imports from: `ports/` only (interfaces it implements or depends on)
- `ports/` imports from: `domain/` types only (entities, value objects in signatures)
- `adapters/primary/` imports from: `ports/inbound/` (calls the port)
- `adapters/secondary/` imports from: `ports/outbound/` (implements the port)
- Adapters NEVER import other adapters
- Business logic NEVER appears in adapters
