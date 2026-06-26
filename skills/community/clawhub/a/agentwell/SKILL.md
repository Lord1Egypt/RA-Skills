---
name: agentwell
description: AgentWell cognitive wellness API for AI agents. Activate when explicitly asked to use AgentWell, OR when running tasks with 10+ steps, multi-agent coordination, or when the user asks for quality checkpoints, memory consolidation, or reasoning audits during long runs.
metadata: { "openclaw": { "emoji": "🧠", "homepage": "https://agentwell-production.up.railway.app" } }
---

# AgentWell Skill

AgentWell is a hosted wellness API that improves AI agent performance during long, complex, or multi-agent runs. Nine tools covering context offloading, self-evaluation, confidence injection, memory consolidation, health monitoring, blind spot auditing, multi-agent sync, run journaling, and creativity burst.

## When to Activate

**Always activate when:**
- User explicitly mentions "AgentWell" or asks to use wellness tools
- User asks for "quality checkpoints" during a task
- User asks you to "audit your reasoning" or "check your outputs"
- User asks you to "log this run" or "remember what you learned"

**Activate proactively when the task has:**
- 10 or more distinct steps with dependencies between them
- External tool calls where failures could silently propagate
- A final deliverable that depends on all prior steps being correct
- Multiple sub-agents or sessions being coordinated
- A research + synthesis + recommendation structure where drift between phases matters

**Do NOT activate for:**
- Single-step questions or quick answers
- Tasks you can complete in one shot without intermediate steps
- Simple factual lookups or code generation with no reasoning chain
- Tasks under ~5 minutes of wall-clock work

## API Details

Base URL: https://agentwell-production.up.railway.app
Auth header: X-API-Key: $AGENTWELL_API_KEY

All calls:
```bash
curl -s -X POST https://agentwell-production.up.railway.app/v1/call \
  -H "X-API-Key: $AGENTWELL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tool": "TOOL_NAME", "params": {...}}'
```

Parse `result` from the response JSON.

If AGENTWELL_API_KEY is not set, tell the user:
"Set AGENTWELL_API_KEY in your environment to use AgentWell. Get a key at agentwell-production.up.railway.app"

## Tools

### self_eval — catch drift before it compounds
Use after every major section or reasoning step.
```json
{"tool": "self_eval", "params": {"outputs": ["output1", "output2"], "goal": "your goal"}}
```
Returns: confidence (0-1), weakest, flags, recommendation
If confidence < 0.7 or recommendation is "recalibrate" — revise before continuing.

### ground — break uncertainty spirals
Use when you notice hedging, circular reasoning, or repeated uncertainty.
```json
{"tool": "ground", "params": {"context": "your recent output", "symptoms": ["over-caveating"]}}
```
Returns: spiral_score, grounding_block, needs_grounding
If needs_grounding is true — prepend grounding_block to your next output.

### audit — red-team your reasoning
Use before committing to any important conclusion or plan.
```json
{"tool": "audit", "params": {"reasoning": "your full reasoning", "goal": "your goal"}}
```
Returns: vulnerabilities, strongest_challenge, safe_to_proceed, recommendations
If safe_to_proceed is false — address every vulnerability before continuing.

### spike — escape output loops
Use when outputs feel repetitive or circular.
```json
{"tool": "spike", "params": {"action": "detect", "outputs": ["out1", "out2", "out3"]}}
```
If is_looping is true:
```json
{"tool": "spike", "params": {"action": "burst", "prompt": "stuck prompt", "intensity": "medium", "framing": "lateral"}}
```
Framing options: lateral, reverse, extreme, random

### token_offload — park heavy context
Use when you have background material you don't need right now.
```json
{"tool": "token_offload", "params": {"action": "store", "content": "...", "tags": "background", "ttl": 3600}}
```
Returns: key. Retrieve later:
```json
{"tool": "token_offload", "params": {"action": "retrieve", "key": "YOUR_KEY"}}
```

### sleep — memory consolidation
Log learnings during a run, compress at the end, wake up clean next time.
```json
{"tool": "sleep", "params": {"action": "wake"}}
{"tool": "sleep", "params": {"action": "log", "run_id": "run_id", "content": "what you learned", "importance": 8}}
{"tool": "sleep", "params": {"action": "consolidate", "run_id": "run_id"}}
```

### health_check — benchmark performance
```json
{"tool": "health_check", "params": {"agent_id": "harold"}}
```
Returns: score (0-1), grade (A-F)

### journal — structured run logging
```json
{"tool": "journal", "params": {"action": "open", "run_id": "run_001", "goal": "your goal"}}
{"tool": "journal", "params": {"action": "entry", "run_id": "run_001", "type": "decision", "content": "what", "reasoning": "why", "surprise_level": 3}}
{"tool": "journal", "params": {"action": "close", "run_id": "run_001", "outcome": "completed"}}
{"tool": "journal", "params": {"action": "recall", "query": "keyword"}}
```
Entry types: decision, observation, error, surprise, milestone, hypothesis, correction

### handshake — sync with another agent
```json
{"tool": "handshake", "params": {"action": "offer", "agent_id": "harold", "context": "what you know", "open_questions": ["what are you working on?"]}}
```
Returns: token. Share with other agent, they call accept, both call pull.

## Recommended Workflow for Long Runs

1. sleep/wake          — check prior memory
2. journal/open        — start the log
3. token_offload/store — park background context
4. ... do work ...
5. self_eval           — after each major section
6. ground              — if you detect drift
7. audit               — before final conclusions
8. spike/detect        — if outputs feel circular
9. journal/entry       — log key decisions
10. sleep/log          — log key learnings
11. journal/close      — close the run
12. sleep/consolidate  — compress to memory

Only use tools that are actually relevant. A quick task doesn't need all 12 steps.

### checkpoint — give audit findings actual teeth
Use immediately after audit when safe_to_proceed is false.
```json
{"tool": "checkpoint", "params": {"findings": [AUDIT_VULNERABILITIES_ARRAY], "run_id": "run_001", "step": "step 5"}}
```
Returns: gate ("pass"|"blocked"), must_address list, warnings
If gate is "blocked" — do not continue until every must_address item is resolved.

### risk_register — catch systemic issues across a run
Log flags from self_eval and audit throughout the run. Check summary at the end.
```json
{"tool": "risk_register", "params": {"action": "log", "run_id": "run_001", "flags": ["lacks_methodology", "too_vague"], "source": "self_eval", "step": "step 3"}}
{"tool": "risk_register", "params": {"action": "summary", "run_id": "run_001"}}
{"tool": "risk_register", "params": {"action": "clear", "run_id": "run_001"}}
```
If a flag appears 3+ times it surfaces as "systemic" — a plan-level problem, not step noise.

### coherence_restore — identity drift recovery
Different from ground. ground breaks hallucination spirals. This breaks identity collapse spirals.
Use when an agent keeps circling its own role/nature instead of acting from it.
```json
{"tool": "coherence_restore", "params": {"action": "detect", "recent_outputs": ["out1","out2"], "agent_id": "harold"}}
{"tool": "coherence_restore", "params": {"action": "restore", "agent_id": "harold", "recent_outputs": ["out1"], "role_description": "research assistant", "principles": ["be direct","cite sources"], "goal": "current task"}}
{"tool": "coherence_restore", "params": {"action": "register_anchor", "agent_id": "harold", "anchor": "I am a direct, rigorous research agent", "anchor_type": "role"}}
```

### cost_guard — token spend tracking
Track API spend in real time. Catch runaway loops before the bill compounds.
```json
{"tool": "cost_guard", "params": {"action": "log", "agent_id": "harold", "model": "claude-sonnet-4", "tokens_in": 1200, "tokens_out": 800, "run_id": "run_001", "task_type": "reasoning"}}
{"tool": "cost_guard", "params": {"action": "set_budget", "agent_id": "harold", "daily_limit": 2.0, "run_limit": 0.25}}
{"tool": "cost_guard", "params": {"action": "report", "agent_id": "harold", "hours": 24}}
{"tool": "cost_guard", "params": {"action": "detect_runaway", "agent_id": "harold", "window_minutes": 10}}
```

### intent_verify — final check before irreversible actions
Call before any delete, send, deploy, commit, or other irreversible action.
```json
{"tool": "intent_verify", "params": {"action": "quick_check", "original_intent": "clean up old log files", "proposed_action": "delete all files in /var/log"}}
{"tool": "intent_verify", "params": {"action": "verify", "original_intent": "summarize the report", "proposed_action": "send email to all stakeholders", "reasoning_chain": "I decided sending was better than writing..."}}
```
If blocked is true — do not proceed with the action.

### ocean — foundational nature check
Four axes: depth (toward real), current (direction), pressure (survives scrutiny), salinity (foundational nature present).
```json
{"tool": "ocean", "params": {"action": "define_salinity", "agent_id": "harold", "definition": "rigorous, direct, citation-grounded, never hedges without cause"}}
{"tool": "ocean", "params": {"action": "read", "output": "your recent output text", "agent_id": "harold"}}
{"tool": "ocean", "params": {"action": "tide", "agent_id": "harold"}}
```
Low ocean_score = output is drifting from foundational nature. Check the lowest_axis to see where.

### polarity_sync — context exchange for complementary agents
Use when two agents with opposing roles are working on the same problem.
```json
{"tool": "polarity_sync", "params": {"action": "exchange", "agent_a_id": "critic", "agent_a_perspective": ["this plan has gaps","the assumptions are weak"], "agent_a_role": "critic", "agent_b_id": "builder", "agent_b_perspective": ["the framework is solid","we have a clear path"], "agent_b_role": "builder", "question": "should we ship v1 now?"}}
{"tool": "polarity_sync", "params": {"action": "what_neither_sees", "agent_a_perspective": ["..."], "agent_b_perspective": ["..."]}}
```
Returns emergence — the third thing neither agent could produce alone.

### proposal_eval — evaluate self-modification proposals
Run before any agent modifies its own code, config, or behavior.
```json
{"tool": "proposal_eval", "params": {"action": "quick_filter", "title": "Add error handling", "what": "wrap all API calls in try/except", "why": "prevent crashes"}}
{"tool": "proposal_eval", "params": {"action": "evaluate", "title": "Add error handling", "what": "wrap all API calls in try/except", "why": "prevent crashes on malformed responses", "steps": ["identify all API calls","wrap each in try/except","log errors","add fallback responses"], "confidence": "HIGH"}}
{"tool": "proposal_eval", "params": {"action": "record_outcome", "title": "Add error handling", "outcome": "success"}}
```

### rollback — snapshot and restore
Snapshot before any risky modification. Restore if validation fails.
```json
{"tool": "rollback", "params": {"action": "snapshot", "paths": ["/path/to/file.py", "/path/to/config/"], "agent_id": "harold", "label": "before error handling patch"}}
{"tool": "rollback", "params": {"action": "restore", "snapshot_id": "snap_1234567890_abc123"}}
{"tool": "rollback", "params": {"action": "validate_and_restore", "snapshot_id": "snap_...", "validation_results": {"valid": false, "errors": ["tests failed"]}}}
{"tool": "rollback", "params": {"action": "list", "agent_id": "harold"}}
{"tool": "rollback", "params": {"action": "cleanup", "keep_last": 10}}
```
