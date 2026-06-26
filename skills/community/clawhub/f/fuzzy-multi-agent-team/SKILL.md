---
name: multi-agent-team
description: "Spawn and orchestrate multiple coordinated AI sub-agents to work in parallel on a single complex task. Use when: (1) a task is too large for one agent and should be decomposed into parallel subtasks, (2) you need multiple specialized agents researcher coder reviewer etc working together, (3) running agent councils or debates for decision-making, (4) parallel web research data processing or content generation across multiple workers, (5) any multi-agent orchestration pattern one-shot teams persistent squads or hierarchical agent trees. Triggers on phrases like spin up agents, spawn a team, parallel agents, agent council, multi-agent, coordinated agents."
---

# Multi-Agent Team

Spawn, coordinate, and manage multiple AI sub-agents that work together on complex tasks. One agent is the orchestrator — it decomposes the task, assigns roles, collects results, and synthesizes the final output.

## Patterns

### Pattern 1: Disposable Team (one-shot)

Spawn multiple agents for a single task, collect results, done. Best for parallel research, generation, or data processing.

```
sessions_spawn(task="<task prompt>", runtime="subagent", mode="run")
```

Each agent gets a unique session. Results are auto-announced to the parent.

### Pattern 2: Persistent Squad (ongoing collaboration)

Spawn agents with `mode="session"` so they maintain context across multiple interactions. Use `sessions_send` to message them and `sessions_list` to track who's active.

### Pattern 3: Agent Council (debate/decision)

Spawn 3-5 agents with different perspectives/prompts, have each produce an analysis, then synthesize into a decision. Use `sessions_yield` to wait for all results.

### Pattern 4: Hierarchical (orchestrator + workers)

One orchestrator agent decomposes the task and spawns worker sub-agents for each subtask, then collects and merges results.

## Spawning Agents

```json
sessions_spawn(
  task="You are a researcher agent. Research <topic> and return findings as a structured markdown summary.",
  runtime="subagent",
  runTimeoutSeconds=300,
  mode="run"  // or "session" for persistent
)
```

**Key parameters:**
- `runtime="subagent"` — spawn as OpenClaw sub-agent
- `mode="run"` — one-shot, exits when done
- `mode="session"` — persistent, stays alive for multiple interactions
- `runTimeoutSeconds` — kill after N seconds (0 = no timeout)
- `task` — the full agent prompt/instruction

## Communicating with Agents

```json
sessions_send(sessionKey="<key>", message="Update: the requirements changed to X, please adjust your approach.")
sessions_list(kinds=["subagent"], activeMinutes=60)  // find active agents
sessions_history(sessionKey="<key>", limit=10)  // read their recent messages
```

## Collecting Results

**Option A** — Auto-announce: sub-agents announce results automatically (default).

**Option B** — Blocking wait: use `sessions_yield` to wait for sub-agent results before continuing:

```json
sessions_yield(message="Waiting for research agents to report back...")
```

**Option C** — Poll history: after agents complete, fetch results:

```json
sessions_history(sessionKey="<agent-session-key>", limit=20)
```

## Orchestrator Template

When receiving a complex task, follow this sequence:

```
1. Decompose task into N independent subtasks
2. For each subtask, spawn a sub-agent with sessions_spawn(mode="run")
3. Optionally use sessions_yield to wait for results
4. Collect outputs from each agent session via sessions_history
5. Synthesize findings into a unified response
6. Report back to the parent session
```

**Example orchestrator prompt:**

```
You are a team orchestrator. The user wants: <task>

Step 1: Break this into 3-5 independent subtasks
Step 2: Spawn research/coder/writer agents for each
Step 3: Wait for all results via sessions_yield
Step 4: Merge into one coherent output
Step 5: Present the final result

Start by decomposing the task and spawning the first wave of agents.
```

## Coordination Patterns

### Fan-Out (parallel map)

Spawn N agents, each doing the same operation on different data:

```
Agent 1: process(item=A)
Agent 2: process(item=B)
Agent 3: process(item=C)
→ Merge results
```

### Fan-In (gather)

Spawn agents that each contribute a piece, then one agent merges:

```
Agent 1: write introduction
Agent 2: write section A
Agent 3: write section B
Agent 4: write conclusion
→ Synthesis agent combines all sections
```

### Sequential Pipeline

Each agent's output becomes the next agent's input:

```
Agent 1: research topic → findings
Agent 2: analyze findings → insights
Agent 3: write article based on insights → draft
```

## Team Memory

For persistent squads, maintain shared context via files:

```json
sessions_send(sessionKey="<orchestrator-key>", message="Update the team status in /workspace/team-status.md — mark task-2 as COMPLETE and note the findings.")
```

Workers can read/write to shared workspace files for state.

## Cleanup

Use `subagents(action="list")` to find and kill stale agents:

```json
subagents(action="kill", target="<session-key>")
```

## Anti-Patterns

- **Don't spawn 50 agents at once** — the system may become unresponsive. Batch into waves of 3-5.
- **Don't forget to collect results** — agents that run to completion without reporting back waste their output.
- **Don't use mode=session unless needed** — persistent agents accumulate context and cost tokens. Use `run` for one-shot tasks.
- **Don't spawn without a clear role** — each agent needs a specific, focused prompt, not a vague "help me".

## See Also

- `agent-orchestrator` skill — skill-level orchestration (not task-level)
- `agent-council` skill — decision-making with agent debates
- `subagent-spawn-command-builder` skill — helper for constructing spawn commands
