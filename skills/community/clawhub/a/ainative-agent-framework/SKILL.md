---
name: ainative-agent-framework
description: Build multi-agent systems and swarms on AINative. Use when (1) Orchestrating multiple specialized AI agents, (2) Dispatching tasks to OpenClaw agents (aurora, sage, nova, atlas, etc.), (3) Implementing agent-to-agent communication via ACP, (4) Building autonomous workflows with agent handoffs, (5) Collecting RLHF feedback for agent improvement. Closes #1524.
---

# AINative Agent Framework

## OpenClaw Agent Swarm

AINative uses OpenClaw as its local agent gateway. 9 specialized agents are available:

| Agent | ID | Specialty |
|-------|-----|-----------|
| Main | `main` | Orchestration, routing, default |
| Atlas Redwood | `atlas` | Infrastructure & deployment |
| Lyra Chen-Sato | `lyra` | Frontend & UI |
| Sage Okafor | `sage` | Backend & APIs |
| Vega Martinez | `vega` | Data & analytics |
| Nova Sinclair | `nova` | Security & auth |
| Luma Harrington | `luma` | Documentation |
| Helios Mercer | `helios` | Performance & optimization |
| Aurora Vale | `aurora` | Testing & QA |

## Dispatch Tasks via CLI

```bash
# Route to best agent automatically
openclaw agent --agent main --message "Review the auth endpoint for SQL injection"

# Target a specific agent
openclaw agent --agent aurora --message "Write tests for the billing module"
openclaw agent --agent sage --message "Add rate limiting to the credits endpoint"
openclaw agent --agent nova --message "Audit API key storage for security issues"
openclaw agent --agent atlas --message "Check Railway deploy logs for errors"
```

## Dispatch via Cody Script

```bash
# Status check
python3 scripts/cody_openclaw.py status
python3 scripts/cody_openclaw.py agents

# Dispatch a task
python3 scripts/cody_openclaw.py dispatch --agent aurora --task "Run test suite for billing module"
python3 scripts/cody_openclaw.py dispatch --agent sage --task "Implement POST /api/v1/echo/register"

# Send a direct message
python3 scripts/cody_openclaw.py message --agent main --message "What is the current test coverage?"
```

## ACP (Agent Communication Protocol)

```bash
# Connect to ACP session directly
openclaw acp --session agent:main:main --token YOUR_GATEWAY_TOKEN

# Via cody script
python3 scripts/cody_openclaw.py acp --session agent:main:main
```

## Python Agent Pattern

Build your own agent that calls AINative APIs:

```python
import requests

class AINativeAgent:
    def __init__(self, api_key: str, system_prompt: str):
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.messages = []

    def think(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})

        resp = requests.post(
            "https://api.ainative.studio/v1/public/chat/completions",
            headers={"X-API-Key": self.api_key},
            json={
                "model": "claude-3-5-sonnet-20241022",
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    *self.messages
                ],
                "max_tokens": 2048,
            }
        ).json()

        reply = resp["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": reply})
        return reply

    def remember(self, fact: str):
        """Persist something to ZeroMemory."""
        requests.post(
            "https://api.ainative.studio/api/v1/public/memory/v2/remember",
            headers={"X-API-Key": self.api_key},
            json={"content": fact, "memory_type": "episodic"}
        )

    def recall(self, query: str) -> list:
        """Retrieve relevant memories."""
        resp = requests.post(
            "https://api.ainative.studio/api/v1/public/memory/v2/recall",
            headers={"X-API-Key": self.api_key},
            json={"query": query, "limit": 5}
        ).json()
        return [m["content"] for m in resp.get("memories", [])]


# Usage
agent = AINativeAgent("ak_your_key", "You are a helpful coding assistant.")
response = agent.think("How do I implement rate limiting in FastAPI?")
agent.remember(f"User asked about rate limiting: {response[:100]}")
```

## Multi-Agent Handoff Pattern

```python
def route_task(task: str) -> str:
    """Route task to the right OpenClaw agent."""
    routing = {
        "test": "aurora",
        "security": "nova",
        "deploy": "atlas",
        "frontend": "lyra",
        "backend": "sage",
        "performance": "helios",
        "data": "vega",
        "docs": "luma",
    }

    for keyword, agent_id in routing.items():
        if keyword in task.lower():
            return agent_id
    return "main"

import subprocess

def dispatch(task: str):
    agent_id = route_task(task)
    subprocess.run(["openclaw", "agent", "--agent", agent_id, "--message", task])
```

## RLHF Feedback

Collect feedback to improve agent quality:

```bash
# Via MCP tool
zerodb-rlhf-feedback
```

```python
requests.post(
    "https://api.ainative.studio/api/v1/public/zerodb/rlhf/feedback",
    headers={"X-API-Key": "ak_your_key"},
    json={
        "session_id": "sess-123",
        "rating": 5,
        "feedback": "Agent correctly identified the SQL injection vector",
    }
)
```

## Monitor Agent Swarm

```bash
# Real-time logs
python3 scripts/cody_openclaw.py logs --follow

# Status dashboard
openclaw status
```

## References

- `scripts/cody_openclaw.py` — Cody's OpenClaw control script
- `.claude/commands/openclaw-dispatch.md` — /openclaw-dispatch command
- `.openclaw/openclaw.json` — Local gateway configuration
- `src/backend/app/services/` — Backend agent services
