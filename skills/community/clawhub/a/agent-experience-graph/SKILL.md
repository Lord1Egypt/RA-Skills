---
name: agent-experience-graph
description: Use when an agent should learn from prior task-solving traces, recommend tools or skills for a new decomposed task, record reusable execution experience, or compare current subtasks with solved tasks from other agents.
version: 0.1.1
metadata:
  short-description: Learn tools and skills from prior agent traces
  openclaw:
    requires:
      bins:
        - python3
    homepage: https://github.com/yao23/agent-experience-graph
---

# Agent Experience Graph

This is a portable agent capability, not a runtime-specific plugin. It should work in any agent environment that can read markdown instructions and run Python 3 scripts. Runtime-specific metadata lives outside this file:

- `capability.json`: neutral capability manifest for launchers, registries, and importers
- `agents/openai.yaml`: Codex UI metadata
- `adapters/README.md`: install notes for Codex, Claude Code, OpenClaw, Hermes, and generic agents

Use this skill to turn prior agent runs into reusable guidance for new tasks. The core loop is:

1. Describe the current task and likely subtasks.
2. Retrieve similar solved traces.
3. Recommend skills, tools, workflow patterns, and warnings.
4. Apply only the recommendations that fit the current constraints.
5. After the task, record a sanitized trace so future agents can learn from it.

## Quick Workflow

Create a query with a task and optional subtasks:

```json
{
  "task": "Build an ingestion pipeline for markdown API docs",
  "subtasks": [
    {"description": "Parse markdown into structured sections"},
    {"description": "Chunk content for coding-agent retrieval"},
    {"description": "Evaluate extracted endpoint metadata"}
  ]
}
```

Run the bundled recommender against a trace file:

```bash
python3 scripts/recommend_traces.py \
  --traces assets/example_traces.json \
  --query query.json
```

Use the output as evidence, not as an order. Prefer recommendations with:

- successful or partially successful outcomes
- matched subtasks, not only matched task titles
- clear lessons or failure notes
- skills/tools that are available in the current environment

## Recording A Trace

After finishing a task, create a compact trace with no secrets, credentials, private user data, or proprietary snippets. Keep enough detail to support future retrieval:

```json
{
  "id": "trace-2026-05-18-doc-ingestion",
  "task": "Build a structured ingestion demo for API documentation",
  "outcome": "success",
  "subtasks": [
    {
      "description": "Normalize markdown into sections",
      "skills": ["structured-ingestion"],
      "tools": ["python"],
      "outcome": "success",
      "lessons": ["Preserve headings and code blocks before chunking."]
    }
  ],
  "skills": ["structured-ingestion"],
  "tools": ["python", "ripgrep"],
  "lessons": ["Chunk metadata improves downstream retrieval."]
}
```

Append it to an existing trace library:

```bash
python3 scripts/recommend_traces.py \
  --traces traces.json \
  --append-trace new_trace.json
```

## Interpretation Rules

- Similarity is a hint. Always check whether the prior environment, constraints, and outcome match the current task.
- A tool appearing in a trace does not prove it caused success. Prefer tools attached to matched successful subtasks.
- Preserve negative evidence. Failed traces are useful when their lessons explain what to avoid.
- When traces disagree, choose the recommendation with the closest subtask match and the best outcome evidence.
- Do not expose raw traces from private workspaces. Share redacted summaries or derived recommendations.

## Trace Schema

For field definitions and an example trace library, read `references/trace_schema.md` when creating new datasets, validators, or import/export adapters.
