---
name: faas
description: Deep workflow for serverless workloads—event sources, IAM, cold start/latency, limits, observability, security, cost, and deployment patterns (functions, containers, step functions). Use when designing or debugging Lambda/Cloud Functions/Azure Functions/edge workers.
---

# Serverless (Deep Workflow)

Serverless shifts complexity to **permissions**, **quotas**, **observability**, and **state at the edges**. Guide the user to explicit trade-offs: simplicity vs cold starts, synchronous vs async, and **least privilege** IAM that is still operable.

## When to Offer This Workflow

**Trigger conditions:**

- Choosing between containers vs functions, or decomposing a service into functions
- Cold starts, timeouts, memory sizing, or concurrency throttling
- “Works locally, fails in Lambda”—IAM, VPC, DNS, or env differences
- Cost spikes, recursive invocation, or DLQ backlogs

**Initial offer:**

Use **six stages**: (1) workload fit & constraints, (2) triggers & contract, (3) IAM & networking, (4) runtime performance, (5) observability & ops, (6) cost & governance. Confirm **cloud** and **language/runtime**.

---

## Stage 1: Workload Fit & Constraints

**Goal:** Decide if **functions** are appropriate and what **boundaries** look like.

### Fit Criteria (heuristics)

- **Good**: event-driven, spiky traffic, small well-defined units, short execution, state externalized
- **Hard**: long CPU-heavy jobs, large in-memory state, strict low-latency p99 without provisioned concurrency, complex socket protocols

### Clarify

- **SLAs**: sync API vs async pipeline
- **Payload limits**, **execution time cap**, **tmp storage**
- **Stateful needs**: DB, queue, cache, workflow engine

**Exit condition:** Clear **yes/no/partial** with **escape hatch** (container, batch, ECS/Fargate, Step Functions).

---

## Stage 2: Triggers & Contract

**Goal:** Define **inputs**, **idempotency**, **retry semantics**, and **output side effects**.

### Map

- Triggers: HTTP, queue, schedule, object storage, streams, webhooks
- **At-least-once** delivery → **idempotent handlers** and dedupe keys
- **Partial failure** in batch: what gets retried vs poison messages

### Design

- **Event schema** versioning; backward-compatible consumers
- **DLQ** or failed-letter path with replay procedure

**Exit condition:** Written contract: **success criteria**, **retry policy**, **dead-letter ownership**.

---

## Stage 3: IAM & Networking

**Goal:** **Least privilege** that is debuggable; correct **VPC** when needed.

### IAM

- One role per function family; **resource-scoped** policies
- Avoid `*` actions on `*` resources except where cloud forces it—then narrow ASAP
- **Cross-account** and **KMS** decrypt permissions explicit

### Networking

- Public vs **VPC-attached** functions (cold start + ENI trade-offs)
- **Egress** for third-party APIs: NAT costs and security groups / NACLs
- **Private** API Gateway / internal ALB patterns if applicable

**Exit condition:** IAM policy review with **least privilege checklist**; network path diagram for dependencies.

---

## Stage 4: Runtime Performance

**Goal:** Meet **latency** and **throughput** within platform limits.

### Tactics

- **Memory** tuning: CPU scales with memory on many clouds—profile
- **Provisioned concurrency** / **min instances** for critical sync paths—cost trade-off
- **Connection reuse** (HTTP, DB) outside handler global where safe
- **Cold start**: trim dependencies, ARM Graviton if supported, lazy init discipline
- **Timeouts** set below client expectations; avoid infinite hangs

### Concurrency

- **Reserved concurrency** vs account limits; avoid starving other functions

**Exit condition:** Load test or trace evidence for **p95/p99**; documented **limits** and mitigations.

---

## Stage 5: Observability & Operations

**Goal:** **Debuggable** serverless—correlation across async hops.

### Practices

- **Structured logging** with request IDs; **PII** redaction
- **Tracing** (X-Ray, OpenTelemetry) across queue → function → DB
- **Metrics**: throttles, errors, duration, iterator age for streams
- **Alarms** on error rate, DLQ depth, duration approaching timeout

### Runbooks

- Replay DLQ safely (idempotency!)
- **Blue/green** or **canary** if using traffic shifting features

**Exit condition:** Dashboard + alerts + **on-call steps** for top failure modes.

---

## Stage 6: Cost & Governance

**Goal:** Predictable spend and **guardrails**.

### Levers

- Right-size memory; eliminate unnecessary VPC; async where sync not needed
- **Recursive patterns** and accidental infinite loops—billing alerts
- **Tagging** for cost allocation; budgets and anomaly detection

### Governance

- Approved **runtimes**; dependency scanning; org-level deny policies for public buckets, etc.

---

## Final Review Checklist

- [ ] Workload fit validated; boundaries documented
- [ ] Idempotency + DLQ + replay story clear
- [ ] IAM minimal; network path understood
- [ ] Latency/cold start addressed for critical paths
- [ ] Observability and alarms in place
- [ ] Cost and recursion risks acknowledged

## Tips for Effective Guidance

- Always state **at-least-once** and what breaks if handlers are not idempotent.
- When user says “Lambda slow,” separate **cold start** vs **downstream** vs **code**.
- Prefer **Step Functions / workflows** when logic is long-running branching—not nested Lambdas calling Lambdas ad hoc.

## Handling Deviations

- **“We only have one function”**: still document IAM, retries, and logs—future you will thank you.
- **Edge workers**: emphasize **CPU time limits**, **geography**, and **cache** semantics.
