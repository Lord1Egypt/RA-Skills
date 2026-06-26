# agentMemo Demo Scenarios — Before vs After

> 5 scenarios demonstrating visible improvements with agentMemo memory.
> Each scenario: Input → Baseline Output → agentMemo Output → Difference

---

## Scenario 1: Multi-Turn Context Retention

**Problem:** Agent forgets context from earlier in the conversation across sessions.

**Setup:**
- Turn 1 (Session A): User says "I'm working on the payment-service refactor, moving from Stripe v2 to v3 API"
- Turn 2 (Session B, 2 hours later): User asks "What was I working on?"

| | Baseline (Stateless) | agentMemo |
|---|---|---|
| **Input** | "What was I working on?" | "What was I working on?" |
| **Output** | "I don't have context about your recent work. Could you remind me?" | "You were working on the payment-service refactor, migrating from Stripe v2 to v3 API (stored 2h ago, score: 0.91)" |
| **Task Complete?** | ❌ No — requires user to repeat | ✅ Yes — recalls prior context |

**Why it matters:** In real agent workflows, sessions restart frequently (cron jobs, tool calls, errors). Without memory, every restart loses all context. agentMemo bridges sessions.

---

## Scenario 2: Repeated Preference Memory

**Problem:** User repeatedly tells the agent the same preferences.

**Setup:**
- Day 1: User says "Always use 4-space indentation in Python, and include type hints"
- Day 3: User asks agent to write a Python function

| | Baseline (Stateless) | agentMemo |
|---|---|---|
| **Input** | "Write a function to parse CSV files" | "Write a function to parse CSV files" |
| **Output** | ```def parse_csv(file):\n  data = []\n  ...``` (2-space indent, no type hints) | ```def parse_csv(file: str) -> list[dict]:\n    data: list[dict] = []\n    ...``` (4-space, typed) |
| **Correct?** | ❌ Ignores known preferences | ✅ Applies stored preferences |

**Why it matters:** Agents that forget preferences create friction. Users stop trusting them. Memory makes the agent feel "aware" and personalized.

---

## Scenario 3: Project Status Tracking

**Problem:** Agent can't continue where it left off yesterday.

**Setup:**
- Yesterday: Agent completed Steps 1-3 of a 5-step deployment pipeline
- Today: User says "Continue the deployment"

| | Baseline (Stateless) | agentMemo |
|---|---|---|
| **Input** | "Continue the deployment" | "Continue the deployment" |
| **Output** | "I don't see any active deployment. Want me to start from the beginning?" | "Resuming deployment from Step 4 (DB migration). Steps 1-3 (build, test, stage) completed yesterday at 16:42. Proceeding with Step 4..." |
| **Task Complete?** | ❌ Would redo steps 1-3 (wasted time + risk) | ✅ Picks up exactly where it left off |

**Why it matters:** Repeated work is expensive (compute, time, risk). For multi-step operations like deployments, re-running completed steps can be dangerous.

---

## Scenario 4: Cross-Session Decision Consistency

**Problem:** Agent gives contradictory answers across sessions.

**Setup:**
- Session 1: Team decided "Use gRPC for internal services, REST for external APIs"
- Session 2: User asks "Should the notification service use REST or gRPC?"

| | Baseline (Stateless) | agentMemo |
|---|---|---|
| **Input** | "Should the notification service use REST or gRPC?" | "Should the notification service use REST or gRPC?" |
| **Output** | "For a notification service, I'd recommend REST for its simplicity and wide adoption." (generic advice, ignores team decision) | "Per the architecture decision recorded on 2026-03-12: internal services should use gRPC. Since the notification service is internal, gRPC is the right choice. (decision score: 0.94)" |
| **Consistent?** | ❌ Contradicts prior team decision | ✅ Aligns with recorded decisions |

**Why it matters:** Inconsistent advice from agents undermines trust and creates technical debt. Memory ensures institutional knowledge persists.

---

## Scenario 5: Error Correction — Learn from Mistakes

**Problem:** Agent repeats the same mistake even after being corrected.

**Setup:**
- Turn 1: Agent incorrectly suggests "Set Redis TTL to 7200s"
- Turn 2: User corrects "No, 7200 caused stale cache. Use 3600s"
- Turn 3 (next day): Another query about Redis caching

| | Baseline (Stateless) | agentMemo |
|---|---|---|
| **Input** | "What Redis TTL should I use for the session cache?" | "What Redis TTL should I use for the session cache?" |
| **Output** | "A common Redis TTL for sessions is 7200s (2 hours)." (repeats the error) | "Redis TTL should be 3600s. Note: 7200s was previously tried but caused stale cache issues — corrected on 2026-03-14 (importance: 0.9)" |
| **Correct?** | ❌ Repeats known-bad advice | ✅ Applies correction, cites history |

**Why it matters:** This is the highest-value memory use case. Agents that learn from corrections become more reliable over time. Without memory, every session starts at zero trust.

---

## Summary

| Scenario | Baseline | agentMemo | Improvement |
|----------|----------|------------|-------------|
| Context Retention | ❌ Lost across sessions | ✅ Recalled with score | Session continuity |
| Preference Memory | ❌ Forgotten daily | ✅ Applied automatically | User trust |
| Project Tracking | ❌ Restart from zero | ✅ Resume from state | Time & safety |
| Decision Consistency | ❌ Generic/contradictory | ✅ Aligned with records | Technical consistency |
| Error Correction | ❌ Repeats mistakes | ✅ Applies corrections | Reliability growth |

**Bottom line:** agentMemo transforms agents from stateless tools into context-aware collaborators that improve over time.
