---
name: deerflow
description: "Deep research and async task execution via DeerFlow LangGraph engine. Submit multi-step research tasks through a lightweight API-only Docker deployment (no frontend). Triggers: /deerflow, deep research, async research, deerflow."
version: 1.1.3
license: mit-0
metadata:
  openclaw:
    requires:
      bins: [python3]
      anyBins:
        - git         # Required only for initial DeerFlow deployment (optional)
        - docker      # Required only for initial DeerFlow deployment (optional)
      env:
        - DEERFLOW_URL
        - DEERFLOW_LANGGRAPH
        - DEERFLOW_ASSISTANT_ID
        - DEERFLOW_MODEL
        - DEERFLOW_RECURSION
    os: [linux, darwin]
---

# DeerFlow Integration

## What This Skill Does

DeerFlow is a LangGraph-based deep research engine that chains web search, reasoning, and synthesis into structured reports. This skill provides OpenClaw integration for **submitting and monitoring** research tasks against a running DeerFlow API.


**Runtime contract**: The skill itself runs entirely locally (python3 only) and communicates with DeerFlow over HTTP. It does not install or run any external Docker images — those are operated independently by the user as the DeerFlow host.

**This skill does NOT** install DeerFlow or manage its services. It assumes a DeerFlow instance is already running and reachable.

## Prerequisites

> ⚠️ **External dependency — your DeerFlow host.** DeerFlow itself runs as a separate service on your infrastructure (or a VPS). Its Docker images are maintained by the [bytedance/deer-flow](https://github.com/bytedance/deer-flow) project. Review their security posture before deployment.


### Required at runtime

| Binary | Purpose | Notes |
|--------|---------|-------|
| `python3` | Run `submit_task.py` / `check_status.py` | Declared in skill metadata |

### Required only for initial DeerFlow deployment (one-time setup)

| Binary | Purpose | Notes |
|--------|---------|-------|
| `git` | Clone the DeerFlow repository | Not needed once DeerFlow is deployed |
| `docker` | Run DeerFlow services | Not needed once DeerFlow is running |

If DeerFlow is already running somewhere (yours, a colleague's, or a cloud instance), skip straight to [Quick Start](#quick-start) — no git/docker needed.

## Deploying DeerFlow (if you don't have one)

> 🔴 **Security note:** The following steps pull Docker images and run services from the `bytedance/deer-flow` GitHub repository. You are responsible for reviewing those images and configurations before running them in your environment.

### 1. Clone and configure

```bash
git clone https://github.com/bytedance/deer-flow.git
cd deer-flow
cp .env.example .env
```

Edit `.env` with your model API keys:

```bash
# Required: at least one LLM provider
OPENAI_API_KEY=sk-...
# Or MiniMax
MINIMAX_API_KEY=...
MINIMAX_API_BASE=https://api.minimax.com

# Optional: Tavily for web search
TAVILY_API_KEY=tvly-...
```

### 2. Start API-only services

```bash
# No nginx, no frontend — just gateway + langgraph
docker compose up -d deer-flow-gateway deer-flow-langgraph
```

Verify:

```bash
curl http://localhost:2024/openapi.json | head   # should return OpenAPI spec
curl http://localhost:8001/health               # should return 200
```

### 3. Test with a manual task

```bash
curl -X POST http://localhost:2024/threads \
  -H "Content-Type: application/json" \
  -d '{}'
# Returns: { "thread_id": "..." }
```

Then submit a task:

```bash
curl -X POST http://localhost:2024/threads/{thread_id}/runs \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "lead_agent",
    "input": {
      "messages": [{
        "type": "human",
        "content": [{ "type": "text", "text": "Your research query here" }]
      }]
    },
    "config": {
      "recursion_limit": 200,
      "configurable": {
        "model_name": "minimax-m2.7",
        "thinking_enabled": true,
        "is_plan_mode": false,
        "subagent_enabled": false
      }
    }
  }'
# Returns: { "run_id": "..." }
```

Poll for completion:

```bash
curl http://localhost:2024/threads/{thread_id}/runs/{run_id}
```

When status = `success`, fetch results:

```bash
curl http://localhost:2024/threads/{thread_id}/history
```

## Quick Start

```
/deerflow <research topic>
```

Example: `/deerflow Analyze the Chinese AI companion market`

The skill returns a `thread_id` and `run_id` for status tracking.

## Architecture

This skill targets the **minimal API-only DeerFlow deployment**. Only two services are relevant to this skill:

| Service | Port | Role |
|---------|------|------|
| `deer-flow-gateway` | 8001 | Business logic & channel glue |
| `deer-flow-langgraph` | 2024 | Core agent orchestration (the only endpoint this skill calls) |

## Model Configuration

Set `model_name` in the `configurable` block:

| Model | Config Value | Notes |
|-------|-------------|-------|
| MiniMax M2.7 | `minimax-m2.7` | Default, reasoning-capable |
| MiniMax M2.5 | `minimax-m2.5` | Lighter alternative |
| Kimi | `kimi` | Requires DeerFlow `.env` to have Kimi credentials |

Set `thinking_enabled: true` to enable extended chain-of-thought reasoning (recommended for research tasks).

## Skill Scripts

This skill includes two helper scripts in `scripts/`:

### submit_task.py

```bash
cd ~/.openclaw/workspace/skills/deerflow
python3 scripts/submit_task.py "Your research topic"
# Returns thread_id and run_id
```

### check_status.py

```bash
python3 scripts/check_status.py <thread_id> <run_id>
# Polls until completion, then prints the full report
```

## OpenClaw Tool Injection

The skill is auto-injected into OpenClaw as the `deerflow` tool. OpenClaw agents call it directly when the user triggers the keyword.

## Resource Comparison

| Deployment | Services | RAM Est. | Use Case |
|-----------|----------|----------|----------|
| **API-only (this skill)** | gateway + langgraph | ~2 GB | Self-hosted agents, VPS |
| Full stack | + nginx + frontend | ~4+ GB | Team shared UI |

## Troubleshooting

### LangGraph returns 404

Verify the container is healthy:
```bash
docker ps | grep langgraph
curl http://localhost:2024/openapi.json
```

### Task hangs or returns "error" status

Check LangGraph logs:
```bash
docker logs deer-flow-langgraph --tail 50
```

### Model API errors

Ensure credentials in DeerFlow's `.env` are valid and the `model_name` in your request matches a configured provider.

## File Structure

```
skills/deerflow/
├── SKILL.md           # This file
└── scripts/
    ├── submit_task.py  # Submit a research task
    └── check_status.py # Poll and retrieve results
```
