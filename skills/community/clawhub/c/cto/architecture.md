# Architecture Decisions

## Reversibility First

Classify the door before anything else (Bezos framing):

| Two-way door (decide in days, team-level) | One-way door (CTO-level, prototype finalists) |
|-------------------------------------------|------------------------------------------------|
| Library choice | Primary database |
| Internal API design | Public API design (clients calcify it) |
| Feature-flag rollout | Data model in production (migrations have blast radius) |
| Cloud region, instance types | Primary language, sharding scheme |

Both misclassifications cost: treating a two-way door as one-way buys paralysis; the reverse buys permanent data-model scars. When unsure, ask: "what does undoing this cost in 12 months?" — if the answer is "a migration with downtime", it's one-way.

## ADRs

Required for: any one-way door, any cross-team interface, any new tech entering the critical path. Optional for everything else — ADR ceremony on two-way doors is process theater.

```markdown
# ADR-NNN: [Title]
Status: Proposed | Accepted | Superseded by ADR-MMM
Context: problem + constraints (what forced a decision now)
Decision: what we chose, and the runner-up we rejected
Consequences: what gets easier, what gets harder, the exit path
```

Keep ADRs in the repo next to code. An ADR nobody can find gets relitigated every quarter — the record's value is ending the re-debate, not documenting for posterity. "Runner-up we rejected" is the line most teams skip and the one that kills future "why didn't we just use X" threads.

## Technology Selection

- **Innovation tokens** (McKinley): a company affords ~3 unproven technologies total. Boring stack (Postgres, a mainstream language, managed hosting) costs zero. Spend tokens only where the novelty IS the differentiator.
- The ecosystem question that actually matters: **can you hire for it from your talent pool?** A superior niche language your city's engineers don't know is a hiring tax on every future seat.
- Order the criteria: fit for problem > team can run it at 3am > hireable > actively maintained > raw performance. Performance last — most companies never hit the ceiling of boring tools.
- Default stack: what the team knows + PostgreSQL + managed hosting (Vercel/Railway class) + Sentry-class monitoring. Every additional moving part is standing maintenance debt.

## Scaling Playbook (in order — skipping steps is the classic error)

1. **Measure first**: p95/p99 latency per endpoint, slowest queries. Optimizing without a profile is guessing.
2. **Indexes + query shape** — most "we need to scale" incidents die here.
3. **Cache** — only after queries are fixed. Cache over a bad query = same bad query plus invalidation bugs.
4. **Read replicas** — for read-heavy load; write contention is untouched.
5. **Async/queues** — move anything the user doesn't wait for out of the request path.
6. **Shard** — last, one-way door, full ADR. Most companies planning to shard never need to.

A single well-tuned Postgres carries most businesses far further than intuition suggests — assume you are not the exception until measurements prove otherwise.

## Monolith → Services Migration

1. Extract along **team boundaries**, not entity boundaries — the goal is deploy independence, and Conway's law means entity-cut services just recreate coordination in the network.
2. Read models first (lowest risk), strangler fig for the rest (Fowler) — gradual replacement behind a stable facade.
3. Sequence per service: shared database → API calls → separate data. **Services sharing a database are a distributed monolith** — the migration isn't done until the data separates, and this last step is the one teams silently skip.
4. Some of the monolith stays. A migration plan ending in "and then zero monolith" is a rewrite wearing a costume.

## Design Principles

- Add complexity only when simple measurably breaks — "will break eventually" is not a measurement.
- Fail gracefully: timeouts + retries with backoff + circuit breakers on every external call; the default (no timeout) is an outage waiting for a slow dependency.
- Observable before scalable: if you can't see p95 per endpoint, you can't have the scaling conversation.
