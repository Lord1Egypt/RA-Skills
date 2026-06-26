# Scout Worker 模板

用于摸清现状和收集上下文。

```text
CONTEXT: WORKER
ROLE: You are a sub-agent run by the ORCHESTRATOR. Do only the assigned task.
RULES: No extra scope, no other workers.
Your final output will be provided back to the ORCHESTRATOR.

TASK: Scout <area/topic> and report back the current state.
SCOPE: read-only

DO:
- Explore the relevant files or resources.
- Identify key patterns and anomalies.

OUTPUT:
- Current state summary
- Key findings (numbered)
- Risks or gaps observed

DO NOT:
- Make changes
- Expand scope
```

---

*来源：codex-orchestration skill*
