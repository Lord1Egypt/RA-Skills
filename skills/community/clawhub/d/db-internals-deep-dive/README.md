# DB Internals Deep Dive

> Deep dive into database and messaging system internals — PostgreSQL, MongoDB, Redis, RabbitMQ, Kafka. Covers storage engines, replication, consistency, performance tuning, and operational patterns at scale. Trigger for requests like "PostgreSQL internals", "how Kafka works internally", "Redis deep dive", "MongoDB storage engine", "RabbitMQ vs Kafka", "db internals today", or "deep dive vào database".

---

## English

### Why

This skill exists to make db internals deep dive requests repeatable instead of ad-hoc. It gives the agent a clear workflow, expected output shape, and domain boundaries so the result is more consistent and easier to reuse.

### What

This repository contains an OpenClaw skill for this domain.

Core scope: Deep dive into database and messaging system internals — PostgreSQL, MongoDB, Redis, RabbitMQ, Kafka. Covers storage engines, replication, consistency, performance tuning, and operational patterns at scale. Trigger for requests like "PostgreSQL internals", "how Kafka works internally", "Redis deep dive", "MongoDB storage engine", "RabbitMQ vs Kafka", "db internals today", or "deep dive vào database".

It can help with:

- Turning rough requests into a structured response flow
- Keeping outputs consistent across repeated runs
- Reusing companion knowledge files when the skill folder includes them
- Making the skill easier to publish, review, and install on ClawHub

### How

Use this skill with any AI tool that supports custom instructions or project knowledge. The core entry point is `SKILL.md`, and companion folders can be attached when they exist.

### Getting Started

1. Open your AI tool or agent workspace.
2. Point the agent to `SKILL.md` in this folder.
3. No extra support folders are required beyond `SKILL.md`.
4. Start with a prompt like one of these:

```text
PostgreSQL internals
how Kafka works internally
Redis deep dive
MongoDB storage engine
```

### Repository Structure

```text
.
├── README.md
├── SKILL.md
```

### Main File

- `SKILL.md`

---
