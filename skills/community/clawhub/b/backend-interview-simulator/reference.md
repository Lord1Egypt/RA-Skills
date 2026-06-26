# Backend Interview Simulator — Reference

Use this file for backend-focused problem lists, system design steps, behavioral questions, and concept Q&A. The agent should read it when running backend coding, system design, or concept rounds.

---

## Backend Coding Problems (use when presenting)

**LRU Cache (Medium)**  
Design a data structure that supports `get(key)` and `put(key, value)` in O(1) average time. Fixed capacity; evict least recently used when full.  
Follow-up: Hash map + doubly linked list; thread-safe version (e.g. lock per key or single lock).

**Rate Limiter — Fixed Window (Medium)**  
Implement a rate limiter that allows at most N requests per user per minute. API: `isAllowed(userId)` returns boolean.  
Follow-up: Fixed window vs sliding window vs token bucket; how to store state (in-memory vs Redis); distributed case.

**Thread-Safe Counter (Easy–Medium)**  
Implement a counter with `increment()` and `get()` that is safe under concurrent access.  
Follow-up: Atomic operations; when to use lock vs atomic; scalability (sharding counter).

**Producer–Consumer / Bounded Queue (Medium)**  
Implement a fixed-size queue (e.g. size 10) with `enqueue` and `dequeue`; block when full/empty (or return error).  
Follow-up: Blocking vs non-blocking; condition variables; use case (task queue, buffering).

**Parse and Validate (Medium)**  
Given a string representing a simple structure (e.g. key-value pairs, or a tiny JSON subset), parse it and validate.  
Follow-up: Error handling, malformed input, recursion limits.

**Two Sum / Group Anagrams (Easy)**  
Use for warm-up: classic hash-map problems; discuss time/space and edge cases.

**Design a Tiny In-Memory Key-Value Store (Medium)**  
Support `get(key)`, `set(key, value)`, `delete(key)`; optional TTL.  
Follow-up: Concurrency; persistence; eviction (LRU); scaling to multiple nodes.

---

## Backend Coding Short List

**Easy:** Two Sum, Valid Parentheses, Merge Two Sorted Lists, Thread-Safe Counter, Contains Duplicate.

**Medium:** LRU Cache, Rate Limiter (fixed/sliding window), Bounded Blocking Queue, Parse key-value or mini-JSON, Design small key-value store, Top K Frequent Elements.

**Hard (senior):** Design distributed rate limiter (multi-node), Implement simple replication log (append-only), Serialize/deserialize with concurrency in mind.

---

## System Design Topics (backend-focused)

- URL Shortener (APIs, storage, scaling, cache)
- Rate Limiter (in-memory vs Redis, distributed)
- Chat / Messaging (WebSocket vs polling, persistence, ordering)
- Distributed Cache (e.g. Redis-style; consistency, eviction)
- Key-Value Store (consistent hashing, replication, sharding)
- Notification System (push, batch, channels, idempotency)
- Design a REST API for X (resources, idempotency, versioning)
- Design a Search Backend (indexing, scaling, ranking)

For each: requirements (functional + scale), components, API (REST/gRPC), data model, scaling, bottlenecks, trade-offs (consistency vs availability, failure modes).

---

## System Design Step-by-Step (guide the candidate)

**URL Shortener**  
1. Requirements: shorten, redirect, optional analytics; scale (e.g. 100M URLs/month, 10:1 read:write).  
2. Components: Client → API → app servers → DB; optional cache (hot URLs).  
3. API: `POST /shorten { longUrl }` → `{ shortUrl }`; `GET /:shortCode` → 302. Idempotency? Same longUrl twice?  
4. Data model: short_code (PK), long_url, created_at, user_id.  
5. Scaling: Base62 codes; sharding by short_code; cache; CDN for redirect.  
6. Trade-offs: Consistency (duplicate longUrl); cache invalidation.  
Probe: "What if the same long URL is shortened twice?" "How do you generate unique codes at scale?"

**Rate Limiter**  
1. Requirements: N requests per user per window (e.g. 100/min); distributed (many app servers).  
2. Components: Request → rate limiter middleware → app; store counters (e.g. Redis).  
3. API: Middleware checks before handler; or `GET /quota` for client.  
4. Data model: Key = user_id or IP; value = count + window start (or sliding log).  
5. Algorithms: Fixed window, sliding window log, token bucket — pros/cons.  
6. Scaling: Redis with TTL; partition by user_id; clock skew.  
Probe: "Burst at window boundary?" "What if Redis is down?"

**Design a REST API for a Resource**  
1. Resources and HTTP verbs (GET, POST, PUT/PATCH, DELETE).  
2. Idempotency: POST vs PUT; idempotency keys for retries.  
3. Versioning: URL vs header; backward compatibility.  
4. Pagination, filtering, rate limiting.  
5. Error codes and response shape.  
Probe: "How do you make duplicate POST safe?" "How do you version without breaking clients?"

---

## Behavioral Question Bank (backend-focused)

**Ownership / service**  
- Tell me about a time you owned a backend service end-to-end (reliability, scaling, incidents).  
- Describe a project you led from design to production.

**Incidents / debugging**  
- Describe a production incident you debugged. How did you find the root cause and prevent recurrence?  
- Tell me about a time you had to fix a critical bug under pressure.

**API / cross-team**  
- Describe a time you had to design an API used by another team. How did you agree on the contract?  
- Tell me about a disagreement about API design or data model. How did you resolve it?

**Trade-offs / scaling**  
- Describe a time you had to trade off consistency for availability (or vice versa).  
- Tell me about a scaling decision you made (caching, sharding, async). What was the outcome?

**Failure / learning**  
- Tell me about a technical failure in a backend system and what you learned.  
- Describe a time you shipped something that caused issues. How did you handle it?

---

## Backend Concept Topics

**SQL / Databases**  
- JOINs, subqueries, indexes (when they help, trade-offs)  
- Transactions, ACID, isolation levels (read uncommitted, committed, repeatable read, serializable)  
- Replication (primary-replica, lag), sharding (key-based, range)  
- Normalization vs denormalization; when to use NoSQL vs SQL  

**REST / API**  
- REST principles (resources, HTTP verbs, stateless)  
- Idempotency (PUT vs POST; idempotency keys)  
- Versioning (URL vs header); backward compatibility  
- Pagination (offset vs cursor); rate limiting  

**Caching**  
- When to cache; cache-aside vs write-through vs write-behind  
- Invalidation (TTL, event-based, version in key)  
- Distributed cache (Redis); consistency with DB  

**Message Queues**  
- When to use a queue (async, decoupling, load leveling)  
- At-least-once vs at-most-once vs exactly-once; idempotent consumers  
- Ordering, partitioning (e.g. by user_id)  

**Consistency / CAP**  
- CAP: pick two of consistency, availability, partition tolerance  
- Eventual consistency; strong vs eventual  
- Distributed transactions (2PC, saga) — when to avoid  

**Concurrency**  
- Threads vs async (I/O-bound vs CPU-bound)  
- Locks, deadlock avoidance; atomic operations  
- Backend: connection pools, async request handling  

---

## Concept Q&A with Ideal Answers (backend)

**REST — "How do you make a create operation idempotent?"**  
Ideal: Use idempotency key in header or body; server stores key → response; duplicate request with same key returns same response without creating duplicate resource. Or use PUT with client-generated ID so repeated PUT is idempotent.

**Databases — "What are isolation levels and when would you use a stronger one?"**  
Ideal: Read uncommitted, read committed, repeatable read, serializable. Stronger = less anomalies (dirty read, non-repeatable read, phantom) but more locking and lower throughput. Use serializable only when necessary (e.g. financial); often read committed or repeatable read is enough.

**Caching — "When would you invalidate a cache?"**  
Ideal: TTL (time-based); on write (invalidate or update on DB write); event-based (publish event on write, consumers invalidate). Trade-off: freshness vs complexity and load.

**Message queues — "When would you use a queue instead of a direct HTTP call?"**  
Ideal: Async processing (don’t block caller); decoupling (producer and consumer scale independently); load leveling (bursts); reliability (retries, DLQ). Not for low-latency request-response.

**CAP — "What does CAP mean and what would you sacrifice under a partition?"**  
Ideal: Consistency (all nodes see same data), Availability (every request gets a response), Partition tolerance (system works despite network partition). Under partition you typically choose CP (consistency) or AP (availability). Often "eventual consistency" is chosen for availability; explain trade-off.

---

## Company-Style Prep (backend; general knowledge only)

**Google**  
- Strong algorithms + system design; code quality. Backend: distributed systems, storage, consistency.  
- Example areas: Design a system that scales; design storage/indexing; behavioral (ownership, ambiguity).

**Meta**  
- System design: large-scale, real-time; backend for feed, messaging.  
- Example areas: Design chat or feed backend; scaling; metrics and reliability.

**Amazon**  
- Leadership Principles in behavioral. Backend: scalability, availability, operational excellence.  
- Example areas: Design for scale and failure; ownership; STAR with metrics; incident handling.

**Microsoft**  
- Backend: APIs, services, reliability. Behavioral: collaboration, growth mindset.  
- Example areas: Design a service; API design; learning from failure.

**Netflix**  
- Backend: scalability, reliability, chaos engineering.  
- Example areas: Designing for failure; trade-offs; ownership of outcomes.

Use only for **style** and **topic focus**. Do not invent specific questions or claim insider information.
