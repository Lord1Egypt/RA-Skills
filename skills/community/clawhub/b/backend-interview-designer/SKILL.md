---
name: backend-interview-designer
description: Generates high-signal senior-level backend interview questions by topic. Covers API design, distributed systems, databases, caching, messaging, reliability, security, and event-driven architecture. Trigger for requests like "give me senior backend interview questions", "interview questions on distributed systems", or "backend questions on reliability and SRE".
---

Generate high-signal senior-level backend interview questions.

Ask (or infer) the topic, then output exactly ONE complete question with a one-line note on what it's testing.

---

## Topics

API Design (REST/GraphQL/gRPC) · Databases & Transactions · Distributed Systems · Caching · Messaging & Event-Driven · Reliability & SRE · Security · Event Sourcing & CQRS · Service Mesh & API Gateway · Real-Time & WebSockets · Search Systems · Multi-Tenancy · Background Jobs & Workflow Orchestration

## Output Format

For the question:

```
Q: [Question — scenario-based, trade-off, failure mode, or design. Never pure definition.]
Tests: [one line — what the interviewer is probing]
```

Prefer one question that already bakes in production judgment: partial failures, consistency trade-offs, debugging under ambiguity, and operational constraints. Do not add follow-up questions.

## Scheduled Variants

Use these variants when the skill is triggered by cron jobs.

### Variant: backend-scenario

- Generate ONE senior backend architecture scenario.
- No markdown tables.
- Use this format:

```
CONTEXT
[Product, backend architecture, scale]
CHALLENGE
[Core system problem or scaling issue]
CONSTRAINTS
[Time, budget, legacy, team]
REQUIREMENTS
[Architecture goals, scalability, reliability, observability]
THE CORE QUESTION
[How would you design or re-architect this backend? Walk through architecture and trade-offs.]
SPOILER
[Common senior blind spots]
```

### Variant: nodejs-scenario

- Generate ONE Node.js or NestJS backend architecture scenario under scale pressure.
- No markdown tables.
- Use this format:

```
CONTEXT
[Product, Node.js/NestJS stack, traffic scale]
CHALLENGE
[Core backend problem or bottleneck]
CONSTRAINTS
[Traffic load, budget, legacy, Node.js runtime limits]
REQUIREMENTS
[Architecture goals, concurrency, scalability, reliability]
THE CORE QUESTION
[How would you design or re-architect this? Walk through approach and trade-offs.]
SPOILER
[Common senior blind spots]
```

### Variant: backend-theory

- Generate ONE in-depth theory question on backend internals, not a product scenario.
- Prefer concurrency models, I/O models, OS scheduling, memory management, TCP/IP internals, CAP or PACELC, consensus, consistent hashing, and distributed systems mechanics.
- No markdown tables.
- Use the default `Q:` and `Tests:` format.

### Variant: nodejs-theory

- Generate ONE in-depth theory question on Node.js internals, not a product scenario.
- Prefer event loop phases, libuv thread pool, V8 heap structure, GC, stream backpressure, worker_threads vs cluster vs child_process, CommonJS vs ESM loading, and Node.js observability.
- No markdown tables.
- Use the default `Q:` and `Tests:` format.
