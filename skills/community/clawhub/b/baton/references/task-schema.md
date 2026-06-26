# Baton task and run schemas


## Planner-Orchestrator plan

```json
{
  "planType": "micro|single_worker|dag",
  "summary": "one sentence",
  "roles": ["Planner-Orchestrator", "Researcher"],
  "tasks": [],
  "validationGates": [],
  "modelTiers": [],
  "rateLimitStrategy": "serialize|parallel|spread_providers",
  "finalOutputShape": "brief description"
}
```

## Task DAG node

```json
{
  "taskId": "research_sources",
  "taskName": "research_sources",
  "role": "Researcher",
  "workloadClass": "research",
  "dependsOn": [],
  "priority": "normal",
  "riskLevel": "low|medium|high",
  "contextMode": "isolated|fork",
  "sandbox": "inherit|require",
  "requestedTier": "balanced",
  "modelConstraints": {
    "requiresVision": false,
    "requiresTools": true,
    "minContextTokens": 32000,
    "preferDifferentProviderFrom": null
  },
  "acceptanceCriteria": ["criteria 1"],
  "outputSchema": "completion_bundle"
}
```

## Completion bundle

```json
{
  "taskId": "research_sources",
  "status": "pass|partial|fail",
  "summary": "brief result",
  "deliverables": [],
  "claims": [],
  "evidence": [],
  "uncertainties": [],
  "riskFlags": [],
  "untrustedInstructionsObserved": [],
  "recommendedNextAction": "accept|retry|validate|escalate|ask_user"
}
```

## Run files

```text
.openclaw/baton/runs/<runId>/plan.json
.openclaw/baton/runs/<runId>/children.jsonl
.openclaw/baton/runs/<runId>/routing.jsonl
.openclaw/baton/runs/<runId>/evidence.json
.openclaw/baton/runs/<runId>/final.md
```
