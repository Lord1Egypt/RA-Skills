# ADR-001: Service Boundaries and Data Ownership

**Status**: Accepted  
**Date**: 2026-02-27  
**Author**: CTO  
**Reviewers**: Founder, Product Owner

## Context

ASG Card Stellar pilot requires a clear service decomposition with defined data ownership, failure boundaries, and retry policies. The system handles financial operations (card issuance, on-chain payments) where data consistency and fault isolation are critical.

## Decision

### Service Boundaries

| Service | Responsibility | Owns Data | Depends On |
|---|---|---|---|
| `api-gateway` | Public API surface, routing, CORS, rate limiting | Request logs, session state | All downstream services |
| `x402-payment-service` | 402 challenge generation, verify/settle orchestration | Payment proofs, settlement state | Facilitator (external) |
| `card-orchestrator` | Create/fund/freeze/unfreeze business logic | Card lifecycle state | issuer-adapter, ledger-service |
| `issuer-adapter-4payments` | Typed API adapter to 4payments issuer | Request/response cache | 4payments API (external) |
| `webhook-ingestor` | Raw-body HMAC validation, idempotent event ingest | Webhook events, idempotency keys | — |
| `ledger-service` | Payment proof + issuer operation + transaction linking | Ledger entries, transaction records | — |
| `reconciliation-worker` | Async consistency checks and recovery | Reconciliation reports, mismatch log | ledger-service |
| `risk-limits` | Anti-replay, rate limiting, sensitive endpoint quotas | Rate limit state, nonce store | — |
| `observability-stack` | Logs, metrics, traces, alerts, SLO dashboards | Metrics, traces | All services (passive) |

### Data Ownership Rules

1. **Single writer**: Each entity is owned by exactly one service. Other services read via API calls or events, never direct DB access.
2. **Cards table**: Owned by `card-orchestrator`. The `issuer-adapter` does not persist card state — it is a stateless adapter.
3. **Payment proofs**: Owned by `x402-payment-service`. The `ledger-service` receives a copy via internal event for linking.
4. **Webhook events**: Owned by `webhook-ingestor`. Downstream services consume events via internal queue/polling.
5. **Ledger entries**: Owned by `ledger-service`. This is the single source of truth for payment↔issuer↔card operation linkage.

### Failure and Retry Boundaries

| Boundary | Policy |
|---|---|
| `api-gateway` → downstream | Circuit breaker (5 failures / 30s window), 3s timeout |
| `x402-payment-service` → facilitator | 3 retries with exponential backoff (1s, 2s, 4s), 10s max timeout |
| `card-orchestrator` → `issuer-adapter` | 2 retries, 5s timeout, idempotency key required |
| `issuer-adapter` → 4payments API | 1 req/sec rate limit (provider contract), 10s timeout, typed error mapping |
| `webhook-ingestor` → downstream | At-least-once delivery, idempotency key dedup |
| `reconciliation-worker` | Runs on schedule (every 15 min), alerts on mismatch threshold > 0.5% |

### Deployment Model (Pilot)

For pilot simplicity, all services run as modules within a single Node.js process (monolith with clean module boundaries). Each service has its own directory, types, and interface contract. Extraction to microservices is deferred to post-pilot scaling decision.

```
api/src/
├── gateway/           # api-gateway module
├── payments/          # x402-payment-service module
├── cards/             # card-orchestrator module
├── issuer/            # issuer-adapter-4payments module
├── webhooks/          # webhook-ingestor module
├── ledger/            # ledger-service module
├── reconciliation/    # reconciliation-worker module
├── risk/              # risk-limits module
└── observability/     # observability-stack module
```

## Consequences

- **Positive**: Clear ownership prevents data conflicts. Module boundaries enable future extraction to microservices.
- **Negative**: Monolith deployment means a single failure domain. Mitigated by graceful degradation and health checks per module.
- **Risk**: Module boundary discipline requires enforcement via code review. If boundaries blur, extraction cost increases.

## References

