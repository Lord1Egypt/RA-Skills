# Production Readiness Checklist

Use this before deploying any agent to production.

---

### Router Layer
- [ ] Intent classifier handles unknown/ambiguous inputs gracefully
- [ ] Low-confidence routes fall back to clarification, not random dispatch
- [ ] Routing logic is tested against representative real-world inputs
- [ ] Router is stateless — it only classifies and dispatches, no side effects

### Orchestrator Agent
- [ ] Subagents receive only the context they need (no full parent history dump)
- [ ] Each subagent has a scoped tool set — not the full tool list
- [ ] Plan-then-execute used for any workflow with irreversible steps
- [ ] Result aggregation handles partial failures gracefully

### Tool Layer
- [ ] Every tool has a typed JSON schema (Pydantic `args_schema`)
- [ ] Tools are single-responsibility and named explicitly (no generic `execute`, `run`)
- [ ] Tool results are truncated before being fed back to the LLM
- [ ] Read-only tools are clearly separated from write/mutate tools
- [ ] No tool can affect systems outside its intended scope
- [ ] Concurrency safety checked at runtime (not just schema) — inspect actual input content
- [ ] Abort controller hierarchy implemented: query-level cancel + sibling-level peer abort

### Permission & Safety Layer
- [ ] Deny rules exist for all known-dangerous patterns (regex-tested)
- [ ] Irreversible operations require human approval via `interrupt()`, resumed with `Command(resume=...)`
- [ ] Every tool call is audit-logged (tool name, args, decision, timestamp)
- [ ] Bypass/auto modes have remote killswitch capability
- [ ] Permission rules are code (not prompts) — tested independently

### Memory Layer
- [ ] Auto-compaction configured at 80–85% context window threshold
- [ ] Compaction uses tiered strategy: tool result budgeting → snip → microcompact → autocompact
- [ ] Autocompact circuit breaker: stops retrying after 3 consecutive failures
- [ ] Long-term memory retrieval tested for relevance and speed
- [ ] Working state schema is typed (`TypedDict` or Pydantic)
- [ ] No PII stored in vector stores without appropriate encryption/retention policy

### Observability Layer
- [ ] Every tool call emits a structured trace event (name, args, result, latency)
- [ ] Token usage tracked per turn, per session, per agent
- [ ] Cost tracked and alertable (alert if session exceeds N USD)
- [ ] Session ID propagated to all subagents for trace correlation
- [ ] Session replay possible from stored traces
- [ ] Config snapshotted at query entry — no mid-turn re-reads of feature flags or env vars
- [ ] Continuation analytics tracked (token deltas per continuation) to detect diminishing returns

### Error Handling & Resilience
- [ ] Tool errors returned as `ToolMessage` observations, not process crashes
- [ ] Retry with exponential backoff on transient failures
- [ ] Circuit breaker on unreliable external tools/APIs
- [ ] Max iteration guard prevents infinite loops (tested)
- [ ] Diminishing returns detection: stop turn when token deltas shrink below threshold
- [ ] Max output tokens escalation: try larger limit before triggering compaction
- [ ] Streaming fallback cleanup: tombstone partial messages before non-streaming retry
- [ ] Unattended retry with heartbeats (gated behind feature flag — not for interactive sessions)
- [ ] Graceful degradation path exists for every critical tool

### Session & State Persistence
- [ ] Production uses Redis or Postgres checkpointer (not `InMemorySaver`)
- [ ] Session IDs are stable and indexed in a lookup store
- [ ] Resume flow tested end-to-end (kill process mid-session, verify resume works)
- [ ] Old sessions have a TTL cleanup policy defined

### Operations
- [ ] Per-tenant rate limiting and cost caps enforced in code
- [ ] Model version is pinned (no silent upgrades mid-production)
- [ ] Agent can be disabled per-tenant without redeployment
- [ ] Runbook exists for: agent stuck, cost explosion, tool consistently failing
