---
name: dual-agent-debate
description: Run a structured 2-agent debate loop between ChatGPT (OpenAI API) and the user's own thoughts retrieved from Supabase Open Brain via MCP, iterating up to 3 rounds (or until semantic agreement), then write the final outcome back to Open Brain. Use when user asks to compare/pressure-test an idea against prior thoughts or memory.
---

# DualAgentDebate

Execute `scripts/dual_agent_debate.py` to run the debate loop.

## Setup

Set required environment variables:

```bash
export OPENBRAIN_MCP_URL="http://127.0.0.1:54321/mcp"
# optional if MCP is protected
export OPENBRAIN_MCP_TOKEN="..."
```

Optional: if you want direct OpenAI API mode, set:

```bash
export OPENAI_API_KEY="..."
```

If `OPENAI_API_KEY` is not set, the script uses `openclaw agent` (OAuth-backed local setup) for debate responses.

Optional tool/model overrides (defaults shown):

```bash
export OPENBRAIN_CONTEXT_TOOL="search_docs"
export OPENBRAIN_SQL_TOOL="execute_sql"
export DEBATE_MODEL="gpt-4o-mini"
```

## Run

```bash
python3 skills/dual-agent-debate/scripts/dual_agent_debate.py \
  --query "Should I migrate this service to Supabase edge functions?"
```

Optional explicit thoughts:

```bash
python3 skills/dual-agent-debate/scripts/dual_agent_debate.py \
  --query "Should we launch this feature now?" \
  --thoughts "My concern is reliability and on-call burden." \
  --rounds 3 \
  --agreement-threshold 0.9
```

## Behavior

1. Pull context from Open Brain MCP (`OPENBRAIN_CONTEXT_TOOL`).
2. Pull related prior thoughts from `public.thoughts` via MCP `execute_sql` unless `--thoughts` is provided.
3. Ask ChatGPT to debate the query using context and thoughts.
4. Compute semantic similarity (OpenAI embeddings) between ChatGPT reply and thoughts.
5. Repeat up to 3 rounds or stop early on agreement threshold.
6. Persist full outcome into `public.memories` via MCP `execute_sql`.

## Notes

- If your Open Brain MCP uses different tool names or argument schemas, set the tool env vars accordingly.
- The script uses MCP `tools/call` JSON-RPC shape; point `OPENBRAIN_MCP_URL` at your MCP HTTP endpoint.
