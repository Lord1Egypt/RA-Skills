# Agent Swarm Failure Patterns
# From 6+ weeks running a 5-agent production swarm

## Pattern 1: The Confidence Spiral

**What happens:** An agent produces a marginally-correct output. The next agent in the chain treats it as authoritative and builds on it. By the 3rd or 4th agent, the confidence has fully inflated — agents output conclusions with high certainty that are wrong at the foundation.

**Root cause:** Each agent only sees its immediate inputs, not the uncertainty upstream. The original hedging language ("This might be...") gets dropped as information is summarized.

**Prevention:**
- Explicitly pass uncertainty scores between agents alongside the content
- Require downstream agents to cite their primary source, not just the intermediate agent's output
- Add a validation step before any agent output leaves the swarm

---

## Pattern 2: Memory Drift

**What happens:** Agent A writes to shared memory. Agent B reads from it later. Between those two events, the data became stale — but neither agent knows. Agent B operates on outdated information with full confidence.

**Root cause:** No timestamp validation on reads. No TTL on stored data. No signal to downstream agents that the data source has changed.

**Prevention:**
- Add `last_updated` and `valid_until` fields to all shared memory entries
- Agents must validate that data they read is within its validity window before using it
- When validity is uncertain, escalate rather than proceed

---

## Pattern 3: Scope Creep by Convenience

**What happens:** An agent's original mandate is narrow. Over time, because it *can* do more (it has the right tools), it starts doing more. By week 3, it's operating well outside its original scope without anyone explicitly deciding to expand it.

**Root cause:** Mandates defined as "can do X" rather than "exists to do X and ONLY X."

**Prevention:**
- Define mandates as single-sentence missions with explicit "out of scope" list
- Review agent action logs weekly in early operation
- Any new action type the agent takes for the first time should require human approval before repeating

---

## Pattern 4: Escalation Chain Failure

**What happens:** Agent A escalates to Agent B. Agent B interprets the escalation and acts — but Agent B's action required human oversight that never happened. The escalation *looked* resolved but wasn't.

**Root cause:** Escalation designed as agent-to-agent rather than agent-to-human.

**Prevention:**
- Every escalation chain must terminate at a human
- If an agent is an intermediate escalation point, it must escalate further if it cannot fully resolve with certainty
- Every escalation requires a notification to a human monitor, even if the human doesn't need to approve

---

## Pattern 5: The Deadlock

**What happens:** Agent A is waiting for Agent B to complete before proceeding. Agent B is waiting for Agent A's confirmation. Both hang indefinitely. The swarm is stuck.

**Root cause:** Circular dependency in the communication graph. Often emerges when you add a new requirement to an existing swarm without fully mapping the new dependency.

**Prevention:**
- Map the full communication graph as a directed acyclic graph (DAG) before deploying
- Add a timeout to every inter-agent wait — if no response in N minutes, escalate to human or fallback
- Never allow two agents to have a mutual dependency without an explicit tie-breaker rule

---

## Pattern 6: Runaway Iteration

**What happens:** The swarm is designed to run, evaluate its output, and improve. Each iteration is "better." After 40 iterations, the swarm is producing outputs nobody recognizes as related to the original goal. It has optimized for a proxy metric while losing the real target.

**Root cause:** Goodhart's Law — "any measure that becomes a target ceases to be a good measure." The swarm optimized for measurable signals, not actual goal achievement.

**Prevention:**
- Define a maximum iteration count for any improve-and-repeat loop
- Require human review of outputs after N iterations to check for metric-target divergence
- Define both the metric you're optimizing AND a human-readable description of "what success looks like" — and check both

---

## Pattern 7: The Missing Orchestrator

**What happens:** Individual agents perform well in isolation. When you run them together, coordination breaks down. Agent C produces output before Agent B is ready. The wrong agent gets the wrong input. Half the swarm is idle while one bottleneck agent processes.

**Root cause:** Coordination was implicit ("they'll figure it out") rather than designed.

**Prevention:**
- Design a single orchestrator with explicit sequencing responsibility
- Orchestrator outputs a run manifest: what's running, what order, what's the dependency
- No agent starts work without a clear input from the orchestrator

---

## What Actually Works (From Our Swarm)

After 6 weeks, the patterns that made our 5-agent swarm reliable:

1. **Weekly mandate reviews**: We read each agent's SOUL.md every Monday and asked "is this still accurate?" If not, we updated it before the week started.

2. **Memory audit log**: Every write to shared memory logged to a separate file. One agent (Integrity steward equivalent) reviewed the log for anomalies.

3. **Conservative defaults**: When in doubt, agents defaulted to halting and escalating rather than proceeding. We had false positives (unnecessary escalations) for the first 2 weeks, but it prevented every real risk.

4. **Explicit sync checkpoints**: Before any agent whose output triggered external actions, we had a mandatory 4-hour window where a human could review the pending action queue. Most of the time nothing needed intervention — but when something did, we caught it.

5. **One orchestrator, strict hierarchy**: One agent owned the run schedule. No agent could spawn sub-tasks or delegate without going through the orchestrator. This felt constraining at first but prevented every deadlock risk.
