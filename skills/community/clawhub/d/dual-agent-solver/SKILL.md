---
name: dual-agent-solver
description: Run a two-agent collaborative problem-solving workflow where one agent is your OpenClaw agent (primary solver) and a second agent challenges assumptions, surfaces risks, and improves the plan over multiple rounds, then outputs one merged actionable solution and stores it in Open Brain memory.
---

# DualAgentSolver

Use this when the user wants two agents to work a problem and converge on a practical solution.

## Setup

```bash
export OPENBRAIN_MCP_URL="http://127.0.0.1:54321/mcp"
# optional
export OPENBRAIN_MCP_TOKEN="..."
```

Optional second-agent model via OpenAI API (if key exists):

```bash
export OPENAI_API_KEY="..."
export SOLVER_SECOND_MODEL="gpt-4o-mini"
```

If `OPENAI_API_KEY` is missing, the second agent also runs through `openclaw agent`.

## Run

```bash
python3 skills/dual-agent-solver/scripts/dual_agent_solver.py \
  --query "How should we migrate our cron jobs safely?" \
  --rounds 3
```

## Output

Returns JSON including:
- round-by-round solver + critic outputs
- final merged solution
- memory write result and key (`dual-agent-solver:<timestamp>`)

## Storage

Persists outcome into `public.memories` (creates table if missing).
