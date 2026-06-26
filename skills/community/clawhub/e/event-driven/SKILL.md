---
name: event-driven
description: Deep event-driven architecture workflow—events vs commands, ordering and idempotency, sagas, outbox pattern, observability, and failure modes. Use when designing async systems, event buses, or refactoring synchronous chains.
---

# Event-Driven Architecture

Event-driven design trades **tight coupling** for **asynchronous** workflows—and introduces **ordering**, **duplicates**, **schema evolution**, and **distributed tracing** challenges.

## When to Offer This Workflow

**Trigger conditions:**

- Replacing long chains of synchronous HTTP calls
- Adopting Kafka, Pub/Sub, EventBridge, NATS, etc.
- Need for sagas, compensating transactions, or cross-service workflows

**Initial offer:**

Use **six stages**: (1) identify events, (2) contracts & versioning, (3) delivery semantics, (4) orchestration vs choreography, (5) observability, (6) failure & replay). Assume at-least-once delivery unless proven otherwise.

---

## Stage 1: Identify Events

**Goal:** Distinguish **domain events** (facts that happened) from **commands** (requests). Assign owning bounded context per event type.

**Exit condition:** Event catalog: name, schema, producers, consumers, SLAs.

---

## Stage 2: Contracts & Versioning

**Goal:** Schema registry or equivalent; backward-compatible evolution; consumers ignore unknown fields; deprecation policy for old versions.

---

## Stage 3: Delivery Semantics

**Goal:** Partition keys for per-entity ordering; idempotent consumers; dedupe keys when exactly-once illusion is needed.

---

## Stage 4: Orchestration vs Choreography

**Goal:** Central orchestrator (saga coordinator) vs decentralized choreography—trade visibility vs coupling.

### Practices

- Transactional outbox when DB write and event publish must align

---

## Stage 5: Observability

**Goal:** Correlation ids on events; traces spanning HTTP → broker → consumer; lag and DLQ depth metrics.

---

## Stage 6: Failure & Replay

**Goal:** Dead-letter queues, replay tooling, poison message handling, and idempotent replays.

---

## Final Review Checklist

- [ ] Event inventory with clear ownership
- [ ] Versioned contracts and compatibility rules
- [ ] Idempotent consumers; partition strategy documented
- [ ] Saga/outbox where transactional consistency required
- [ ] Tracing and replay operationalized

## Tips for Effective Guidance

- Choreography can hide flows—document critical sequences as diagrams.
- Pair with **message-queues** and **idempotency** for implementation detail.

## Handling Deviations

- Low volume: start with a simple queue before full Kafka topology.
