# First Principles Thinking -- Worked Examples

Four full-flow engineering examples. Each shows all phases the depth level
requires, so you can see what "good" looks like before emitting your own
artifact.

Examples are illustrative; numbers are plausible, not real.

---

## Example 1 -- Infrastructure (Standard): "Should we add a Redis cache?"

### Phase 1 -- Intake
> "You want to reduce API latency on the `/orders` endpoint, and your
> proposed approach is adding Redis. Is that right? -- Standard depth."

### Phase 2 -- Socratic
- *Evidence:* "What's current P99? What's the target? Have you profiled?"
- *Assumption probing:* "Why caching specifically, not query optimization?"
- *Alternative viewpoints:* "What if the slowness is the query plan, not absence of a cache?"
- *Implications:* "What's the invalidation strategy? What happens when the data goes stale?"

### Phase 3 -- Decomposition
**Ground Truths**
- `[TRUTH]` P99 must be < 200ms (SLA, contractual).
- `[TRUTH]` Current P99 is 800ms, measured.
- `[TRUTH]` Underlying data changes ~every 30 min.

**Unknowns**
- `[UNKNOWN]` Where in the 800ms is the time actually spent? (profile not yet run)

**Assumptions**

| Assumption                        | Category  | Challenge                                        | Verdict      |
|-----------------------------------|-----------|--------------------------------------------------|--------------|
| We need an external cache         | Technical | Bottleneck might be the query, not the absence of caching | Investigate |
| Redis is the right cache          | Technical | In-process memoization may suffice for this data size      | Investigate |
| All endpoints need caching        | Business  | Only 3 of 20 endpoints are actually slow                    | Discard      |

### Phase 5 -- Reconstruction
- **Path A -- Fix the query.** Add the missing index + eager-load the joined relation. 2 hours. Trivial reversibility.
- **Path B -- In-process memoization with 5-min TTL.** 1 hour. Limits: single-process; won't help horizontal scale.
- **Path C -- Redis with explicit invalidation on write.** 1-2 days incl. ops. Gives horizontal scale, adds operational surface.

### Recommendation
Start with **Path A** (profile, fix). If P99 is still > 200ms, escalate to
Path B. Only reach for Path C with evidence B is insufficient. Each step
is cheap and reversible; do them in that order.

### Verification
- **Falsifier:** If P99 is still > 200ms 48h after the Path A fix with no
  other regressions, Path A was insufficient.
- **Reversibility:** Path A trivially reversible; Path C is weeks of operational debt.

---

## Example 2 -- Architecture (Deep): "We need microservices"

### Phase 1 -- Intake
> "You want to break the monolith into microservices because the codebase
> is hard to work with. The outcome is 'teams ship independently without
> stepping on each other'. Is that right? -- Deep depth."

### Phase 2 -- Socratic
- *Clarification:* "What specifically is hard -- build times, merge conflicts, unclear ownership?"
- *Assumption probing:* "Does 'hard to work with' mean the *architecture* is wrong, or the *code* needs refactoring inside the current structure?"
- *Evidence:* "How many teams? How often do they block each other, measurably?"
- *Meta:* "Would a modular monolith solve the same problem without the operational cost of distributed systems?"

### Phase 3 -- Decomposition
**Ground Truths**
- `[TRUTH]` Two teams (Payments, Catalog) ship on different release cadences and block each other weekly.
- `[TRUTH]` Full-monolith deploy pipeline is 45 minutes.
- `[TRUTH]` Database already has clean domain boundaries (payments tables vs catalog tables; no cross-domain joins in the last 6 months).

**Unknowns**
- `[UNKNOWN]` Team size in 12 months. Changes whether "organizational scaling" pressure is real or projected.

**Assumptions**

| Assumption                              | Category   | Challenge                                                     | Verdict |
|-----------------------------------------|------------|---------------------------------------------------------------|---------|
| The entire monolith must be split       | Technical  | Only Payments and Catalog have genuine independence needs     | Discard |
| Microservices will make code clearer    | Technical  | They add network, tracing, and mesh complexity                | Discard |
| We need independent *deploy*            | Business   | We actually need independent *release cycles*; modular monolith + feature flags can deliver this | Modify |

### Phase 4 -- Inversion
| Failure mode                                         | Currently prevented? |
|------------------------------------------------------|----------------------|
| Distributed tracing gaps hide cross-service failures | No -- need observability investment before split |
| Team still blocks on a shared database               | Partial -- need schema ownership rules           |
| Ops complexity exceeds team capacity                 | No -- must gate on ops hiring                    |

### Phase 5 -- Reconstruction
- **Path A -- Extract Payments only.** Clear domain boundary, own tables, different release cadence. 2-3 weeks. Risk: one service boundary.
- **Path B -- Modular monolith.** Enforced module boundaries (package / build-module), independent CI per module, feature flags for release. 1-2 weeks. Risk: low; no new infra.
- **Path C -- Full microservices (5+ services, mesh, gateway).** 2-3 months. Risk: operational complexity for a team this size.

**Chesterton's Fence check:** The monolith exists because a 3-person team built the product fast. Conditions now: different (2 teams, different cadences). Conditions for *removing the monolith entirely*: not yet met (only 2 teams with real independence need).

### Recommendation
**Path B first** to capture 80% of the benefit at 10% of the cost. **Then Path A** if the Payments/Catalog cadence conflict still bites 3 months later. Path C is premature; microservices solve organizational scaling problems that are not present yet.

### Verification
- **Falsifier:** If Path B ships and the weekly block rate between Payments
  and Catalog hasn't dropped after 6 weeks, modularization was insufficient
  and the Path A extraction should start immediately.
- **Reversibility:** Path B fully reversible. Path A hard to reverse once
  tables are split. Path C effectively irreversible within the year.

---

## Example 3 -- Authentication (Standard): "Let's do OAuth2 + JWT"

### Phase 1 -- Intake
> "Outcome: authenticated access to an internal tool for ~200 employees.
> Proposed: OAuth2 with JWT. Standard depth."

### Phase 2 -- Socratic
- *Clarification:* "Federating identity with a third party, or internal only?"
- *Assumption probing:* "Why OAuth2? Do you need delegated authorization, or just authentication?"
- *Meta:* "What's the simplest mechanism that correctly verifies identity and controls access here?"

### Phase 3 -- Decomposition
**Ground Truths**
- `[TRUTH]` Single application, no third-party identity federation required.
- `[TRUTH]` ~200 known employees, managed set.
- `[TRUTH]` Single-server deployment, not distributed.
- `[TRUTH]` Session duration matches workday (~8h acceptable).

**Assumptions**

| Assumption                          | Category  | Challenge                                              | Verdict |
|-------------------------------------|-----------|--------------------------------------------------------|---------|
| Need OAuth2                         | Technical | OAuth2 is for *delegated authorization*; no federation here | Discard |
| JWT required for stateless auth     | Technical | Single server makes server-side sessions viable and simpler | Discard |
| Need refresh tokens                 | Technical | Workday-length sessions handled by plain timeout       | Discard |

### Phase 5 -- Reconstruction
- **Path A -- Server-side sessions + secure cookies.** ~100 LOC, no external deps, easy to debug. Limits: tied to one server.
- **Path B -- Custom token auth (no OAuth2 framework).** Stateless; works when you go multi-server. ~300 LOC. Limits: own the token lifecycle.
- **Path C -- Full OAuth2 + JWT + refresh.** Framework + ~1000 LOC. Federation-ready. Limits: massive overkill for this context.

### Recommendation
**Path A.** The ground truths (single app, single server, known users, workday sessions) eliminate every reason to reach for OAuth2. Revisit only if a third-party login or horizontal scaling becomes a `[TRUTH]`.

---

## Example 4 -- Database Selection (Standard): "Let's use PostgreSQL"

### Phase 1 -- Intake
> "Choosing a datastore for a new service; defaulting to PostgreSQL. Standard depth."

### Phase 2 -- Socratic
- *Clarification:* "What are your actual access patterns -- joins, key lookups, full-text?"
- *Assumption probing:* "Is PostgreSQL chosen because the data is relational, or because it's familiar?"
- *Evidence:* "Of the last 20 queries you'd write, how many are joins vs lookups by ID?"

### Phase 3 -- Decomposition
**Ground Truths**
- `[TRUTH]` Must persist across restarts.
- `[TRUTH]` Read P99 < 50ms.
- `[TRUTH]` ~100 writes/sec.
- `[TRUTH]` Mostly read, rarely updated.
- `[TRUTH]` ~90% of access is key-value lookup by ID; ~10% are small relational queries.

**Assumptions**

| Assumption                      | Category  | Challenge                                         | Verdict     |
|---------------------------------|-----------|---------------------------------------------------|-------------|
| Need an RDBMS                   | Technical | 90% of access is key-value; relational is overkill there | Investigate |
| Need SQL for querying           | Technical | The 10% relational queries are simple; could be app-side joins | Modify     |
| PostgreSQL is the safe default  | Historical| Safe, but may be over-provisioned for this workload | Investigate |

### Phase 5 -- Reconstruction
- **Path A -- Key-value store (DynamoDB / Redis with persistence).** Optimized for the 90% path. Sub-10ms reads. Limits: the 10% relational needs a second solution.
- **Path B -- PostgreSQL used primarily as KV.** Familiar, single system, JSONB for flexible rows. Paying RDBMS overhead for KV work, but one system to run.
- **Path C -- Hybrid: KV store + small PostgreSQL.** Best fit for both patterns, but two stores to maintain and consistency to reason about.

### Recommendation
**Path B** if the team already knows PostgreSQL well and meets the 50ms P99 under load test. Measure first. If PostgreSQL can't hold the latency target, move to Path A or C. Do not introduce a second datastore until measurement forces it.

### Verification
- **Falsifier:** Load test must show PostgreSQL can sustain 10k lookups/sec at P99 < 50ms. If not, Path B is out.
- **Reversibility:** Path B easy to reverse to Path C later. Path A hard to reverse once the data shape locks in.
