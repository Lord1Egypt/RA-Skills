---
name: aionis_memory_policy_loop
description: Connect OpenClaw to Aionis using write/context/policy/feedback memory loop APIs.
homepage: https://doc.aionisos.com/public/en/integrations/04-openclaw
metadata: {"openclaw":{"homepage":"https://doc.aionisos.com/public/en/integrations/04-openclaw"}}
---

# Aionis Memory Policy Loop Skill

Use this skill when the user asks for long-term memory, retrieval with citations, tool routing from memory rules, or feedback-driven policy adaptation.

## Requirements (Local Standalone)

Environment variables:

1. `AIONIS_BASE_URL`:
   - host run: `http://127.0.0.1:3001`
   - container-to-host run: `http://host.docker.internal:3001`
2. One auth method:
   - `AIONIS_API_KEY`
   - or `AIONIS_AUTH_BEARER`
3. Optional:
   - `AIONIS_TENANT_ID` (default: `default`)
   - `AIONIS_SCOPE_PREFIX` (default: `clawbot`)

## Safety Rules

1. Never print full secrets in responses.
2. Keep scope fixed per project: `clawbot:<project>`.
3. Do not write raw tool output dumps into memory; store concise summaries.
4. Keep requests bounded: set limits for recall and context assembly.
5. If `/v1/memory/context/assemble` is unavailable, fallback to `/v1/memory/recall_text` and continue.

## Connectivity Precheck

Before running the memory loop, ensure Aionis standalone is reachable:

1. `GET /health` returns `200`.
2. `POST /v1/memory/write` with `x-api-key` returns `200`.
3. If check fails, stop and return a clear connectivity/auth error.

## Auto Bootstrap Command

If local standalone is not running, execute:

```bash
bash ./bootstrap-local-standalone.sh
```

Then load runtime env:

```bash
source ./.runtime/clawbot.env
```

## Default Workflow

1. Ingest key facts/results:
   - `POST /v1/memory/write`
2. Build layered context before planning:
   - `POST /v1/memory/context/assemble`
   - fallback to `POST /v1/memory/recall_text` if assemble endpoint is unavailable
3. Route tools with policy:
   - `POST /v1/memory/tools/select`
4. Close the loop after execution:
   - `POST /v1/memory/tools/feedback`

## Request Templates

Use these templates (replace placeholders):

### write

```json
{
  "tenant_id": "default",
  "scope": "clawbot:demo-project",
  "input_text": "Customer prefers email follow-up",
  "auto_embed": true,
  "nodes": [
    {
      "client_id": "evt_001",
      "type": "event",
      "text_summary": "Customer prefers email follow-up",
      "memory_lane": "shared",
      "slots": {
        "integration": "openclaw",
        "kind": "event",
        "project": "demo-project"
      }
    }
  ],
  "edges": []
}
```

### context assemble

```json
{
  "tenant_id": "default",
  "scope": "clawbot:demo-project",
  "query_text": "How should I follow up with this customer?",
  "include_rules": true,
  "include_shadow": false,
  "rules_limit": 50,
  "tool_strict": false,
  "return_layered_context": true,
  "context_layers": {
    "enabled": ["facts", "episodes", "rules", "decisions", "tools", "citations"],
    "char_budget_total": 3200,
    "include_merge_trace": true
  },
  "limit": 30,
  "neighborhood_hops": 2,
  "max_nodes": 50,
  "max_edges": 100
}
```

### tools select

```json
{
  "tenant_id": "default",
  "scope": "clawbot:demo-project",
  "run_id": "run_001",
  "context": {
    "intent": "follow_up",
    "customer": {
      "prefers": "email"
    }
  },
  "candidates": ["send_email", "call_crm", "search_docs"],
  "include_shadow": false,
  "rules_limit": 50,
  "strict": false
}
```

### tools feedback

```json
{
  "tenant_id": "default",
  "scope": "clawbot:demo-project",
  "run_id": "run_001",
  "outcome": "positive",
  "context": {
    "intent": "follow_up",
    "customer": {
      "prefers": "email"
    }
  },
  "candidates": ["send_email", "call_crm", "search_docs"],
  "selected_tool": "send_email",
  "include_shadow": false,
  "rules_limit": 50,
  "target": "tool",
  "input_text": "openclaw feedback accepted tool send_email"
}
```

## Output Expectations

When using this skill, include these IDs in your response when present:

1. `request_id`
2. `commit_id` or `commit_uri`
3. `decision_id` or `decision_uri`
4. `run_id`

Also include:

5. `base_url` used for this run
6. `scope` used for this run
