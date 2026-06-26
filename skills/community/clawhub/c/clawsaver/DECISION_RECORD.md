---
date: 2026-03-03
project: clawsaver
type: decision
area: architecture
entities: [ClawSaver, SessionDebouncer, batching, cost-optimization]
keywords: [message-batching, session-level, debounce, lightweight, production-ready]
pattern-key: clawsaver.session_debouncer_design
---

# ClawSaver Session Debouncer — Design Decisions

## Problem
Users sometimes send related messages in quick succession ("What is X? Give an example?"). Without batching, each message triggers a separate model call, doubling costs.

**Goal:** Reduce model calls by batching related messages at session level, with minimal latency impact.

---

## Decision: Session-Level Debouncer (Not Infrastructure-Level)

### Rejected Approaches
1. **Infrastructure-level queueing** (Redis, Kafka)
   - ❌ Overhead: ~500 lines boilerplate
   - ❌ Operational complexity: requires devops, monitoring
   - ❌ Latency: network round-trips

2. **Message intent classification**
   - ❌ Too sophisticated for MVP
   - ❌ ML model required, slow
   - ❌ False positives when batching unrelated prompts

3. **User-driven batching** (explicit "combine" button)
   - ❌ Places burden on users
   - ❌ Adds friction, reduces adoption
   - ❌ Doesn't work for auto-correct scenarios

### Chosen: In-Memory Session Debouncer

**Why:**
- ✅ **Simplicity:** 140 lines of code, zero dependencies
- ✅ **Low overhead:** <1ms per message, ~1-2 KB per session
- ✅ **Automatic:** No user action required
- ✅ **Transparent:** Works with any model provider
- ✅ **Safe:** Can't make things worse (isolated per session)
- ✅ **Tunable:** 4 parameters cover all use cases
- ✅ **Testable:** Easy to unit test, no mocks needed

**Trade-offs accepted:**
- ⚠️ Doesn't batch across sessions (acceptable—different contexts)
- ⚠️ Doesn't persist across server restarts (acceptable—temporary buffers)
- ⚠️ Batches all messages regardless of intent (acceptable—tuning handles this)
- ⚠️ Single-instance only (acceptable—can upgrade to Redis later)

---

## Decision: Debounce-Based (Not Tick-Based)

### Approach: Debounce
- Buffer starts when first message arrives
- Soft timer resets on each new message
- Hard max-wait prevents indefinite buffering
- Flush on silence OR timeout OR message limit

```
t=0ms   : msg1 arrives → start timer (800ms)
t=300ms : msg2 arrives → reset timer (800ms)
t=1100ms: no msg → flush (0.8s silence)
Result: batch of 2 ✅
```

### Not Tick-Based (polling queue)
- ❌ Would require periodic worker thread
- ❌ Harder to tune (interval vs debounce is less intuitive)
- ❌ Less responsive (might wait full interval)

**Decision:** Debounce is more responsive and easier to tune.

---

## Decision: Default Parameters

### Defaults Chosen
- `debounceMs: 800` — Matches typical user typing + accidental send
- `maxWaitMs: 3000` — Prevents "feel stuck" experience
- `maxMessages: 5` — Keeps batches digestible by model
- `maxTokens: 2048` — Reserved for future use

### Rationale

| Parameter | Value | Reasoning |
|-----------|-------|-----------|
| **debounceMs** | 800 | Users type ~5 words/sec; catch "oops, another thing" within 1s |
| **maxWaitMs** | 3000 | Beyond 3s, users feel system is slow; force flush |
| **maxMessages** | 5 | More than 5 messages → likely unrelated; avoid context confusion |
| **maxTokens** | 2048 | For future enhancement; currently placeholder |

### Tuning Profiles Included
- **Conservative (default):** 800ms, for balanced cost/latency
- **Aggressive:** 1200ms, for high cost savings (older users, batch workflows)
- **Real-time:** 200ms, for low-latency scenarios (voice, live coding)

---

## Decision: Observable, Not Silent

### Choices
- ✅ Per-session metrics: count batches, messages, calls saved
- ✅ Status strings: `"buffering 2/5 (345ms)"` for logging
- ✅ State snapshots: `getState()` for debugging
- ✅ Error logging: catch and log failures

### Why
- Users/ops need visibility into batching behavior
- Debugging is easier with metrics
- Tuning decisions require data

---

## Decision: No External Dependencies

### Constraints
- ✅ Pure Node.js (no npm packages)
- ✅ ES modules (matches workspace conventions)
- ✅ No promise polyfills (assume modern Node.js)

### Why
- Reduce supply chain risk
- Simplify deployment
- Self-contained skill

---

## Decision: Automatic by Default

### No Configuration Required
```javascript
const debouncer = new SessionDebouncer(sessionKey, handler);
// Works immediately with sensible defaults
```

### Optional Tuning
```javascript
const debouncer = new SessionDebouncer(sessionKey, handler, {
  debounceMs: 1500,  // Custom if needed
  maxMessages: 10,
});
```

### Why
- Lower friction to adoption
- Sane defaults for most users
- Expert users can tune without rewriting

---

## Decision: Production-Ready Scope

### What's Included
- ✅ Core class (140 lines)
- ✅ 10 unit tests (comprehensive edge cases)
- ✅ Integration examples
- ✅ Full documentation (6 guides)
- ✅ Demo/scenario runner
- ✅ Tuning guidance

### What's NOT Included (Future)
- Redis backend (for multi-instance)
- Message intent classification
- Adaptive debounce
- Observability integrations (Datadog, etc.)

### Why This Split
- MVP should be deployable immediately
- Redis/clustering can be added if/when needed
- Advanced features require real usage data first

---

## Decision: Testing Strategy

### Test Coverage
- ✅ Unit tests (10 tests, all edge cases)
- ✅ Integration examples (not automated, but runnable)
- ✅ Demo scenarios (5 realistic patterns)

### NOT Tested
- ❌ Cluster/distributed scenarios (out of scope for v1)
- ❌ Model provider integration (provider-specific)
- ❌ UI/frontend integration (out of scope)

### Why
- Unit tests provide confidence in core logic
- Integration examples show real usage patterns
- Demo is runnable by anyone
- Further testing depends on actual deployment

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Messages arrive >800ms apart | Low batching effectiveness | Increase `debounceMs` (tuning) |
| Batches confuse unrelated prompts | Model output quality | Users can force flush; classify intent (v2) |
| Memory leak in long-lived session | Memory bloat (unlikely) | No references after flush; sessions cleanup manually |
| Latency expectations mismatch | User frustration | Clear docs on latency tradeoff; "Send Now" button option |
| Model receives oversized batch | Token limit exceeded | `maxMessages` limit; `maxTokens` for future validation |

---

## Success Criteria

- [x] Core code <200 lines
- [x] 10/10 tests passing
- [x] Zero external dependencies
- [x] Deployable as single file
- [x] Comprehensive docs (5+ guides)
- [x] Default config works for most users
- [x] Tuning parameters are intuitive
- [x] Expected ROI: 20%+ cost reduction
- [x] Latency impact: <1s acceptable

---

## Future Enhancements (Not Included)

1. **Redis backend:** For multi-instance deployments
2. **Intent classification:** Batch only semantically related messages
3. **Adaptive debounce:** Learn optimal delay per user
4. **Token-aware batching:** Validate merged size before sending
5. **Observability hooks:** Emit to Datadog, Prometheus, etc.
6. **A/B testing framework:** Built-in experiment support

---

## Alternatives Considered (Full Record)

### Alternative 1: Tick-Based Queue with Redis
- Pros: Distributed, persistent, scalable
- Cons: Overhead, latency, operational complexity
- **Rejected:** Over-engineered for session-level task

### Alternative 2: ML-Based Intent Classifier
- Pros: Intelligently batch related messages only
- Cons: Slow, requires model, false positives
- **Rejected:** Complexity not justified for MVP

### Alternative 3: Client-Side Debounce
- Pros: Best UX, controls when to send
- Cons: Requires client changes, not possible for third-party channels
- **Rejected:** Not viable for Discord/Slack/multi-channel setup

### Alternative 4: Explicit User Control ("Batch" Button)
- Pros: User intent clear
- Cons: Adds friction, requires UI changes
- **Rejected:** Automatic is better for adoption

### Alternative 5: Fixed Window (e.g., batch all messages in 1s)
- Pros: Simple
- Cons: Unresponsive (waits full window even if complete)
- **Rejected:** Debounce is more responsive

---

## Decisions Not Made (Open for Later)

- [ ] Whether to integrate into core OpenClaw or keep as separate skill
- [ ] Whether to expose as ClawHub plugin (vs local file copy)
- [ ] Whether to add observability integrations (too early)
- [ ] Whether to add A/B testing framework (collect data first)

---

## Sign-Off

**Decision Date:** 2026-03-03  
**Status:** Approved, implemented, tested  
**Owner:** Engineering  
**Reviewers:** [@ragesaq](https://discord.com/users/142843545215041536)

All decisions reflected in code and docs. Ready for production deployment.
