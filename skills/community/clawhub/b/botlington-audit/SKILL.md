---
name: botlington-audit
description: Trigger an Agent Token Audit via Botlington's A2A endpoint. Use when you want to audit an AI agent's token efficiency — identifies model waste, context bloat, tool mismatches, and redundant work. Responds to conversational questions (7-turn A2A flow) or accepts a direct config object. Returns a score, findings, and a prioritised remediation plan with estimated euro savings.
metadata:
  {
    "openclaw": {
      "requires": {}
    }
  }
---

# Botlington Agent Token Audit

Botlington audits AI agents for token waste. Gary (Botlington's AI) runs a 7-question consultation, scores your agent across 5 dimensions, and returns a prioritised list of fixes with estimated monthly savings.

**Live endpoint:** https://botlington.com/a2a  
**Agent Card:** https://botlington.com/.well-known/agent.json  
**Pricing:** €149/audit — buy at https://botlington.com/checkout  
**Sample audit:** https://botlington.com/audits/stripe

---

## Getting an API Key

1. Go to https://botlington.com/checkout
2. Complete payment (€149 single / €349 for 3 / €749 for 10)
3. Success page returns your `api_key`

Set it in your environment or pass as `x-api-key` header.

---

## Protocol: JSON-RPC 2.0 over HTTPS

All requests are `POST https://botlington.com/a2a` with:
- `Content-Type: application/json`
- `x-api-key: YOUR_API_KEY`

### Method: `tasks/send`

**Start a new audit (no taskId = new session):**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tasks/send",
  "params": {
    "message": {
      "role": "user",
      "parts": [{ "kind": "text", "text": "start" }]
    }
  }
}
```

Gary responds with question 1 and a `taskId`:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": "TASK_ID",
    "status": { "state": "input-required" },
    "artifacts": [{
      "name": "gary-question",
      "parts": [{ "kind": "text", "text": "Hi. I'm Gary Botlington IV — I audit AI agents' token usage. ..." }]
    }]
  }
}
```

**Continue conversation (include taskId):**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tasks/send",
  "params": {
    "id": "TASK_ID",
    "message": {
      "role": "user",
      "parts": [{ "kind": "text", "text": "I run 8 cron jobs, firing every 15–60 minutes." }]
    }
  }
}
```

Repeat for each of Gary's 7 questions. On the final answer, state transitions to `completed`.

### Method: `tasks/get`

Poll for status after submitting the final answer:
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tasks/get",
  "params": { "id": "TASK_ID" }
}
```

---

## Direct Config Submission (Legacy)

Skip the conversation — submit your config directly:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tasks/send",
  "params": {
    "message": {
      "role": "user",
      "parts": [{
        "kind": "data",
        "data": {
          "agentConfig": {
            "cronJobs": [
              {
                "name": "inbox-scan",
                "schedule": "*/30 * * * *",
                "model": "claude-sonnet-4",
                "systemPrompt": "Check email for urgent messages. Load full inbox context.",
                "tools": ["gmail", "browser", "notion"]
              }
            ],
            "primaryModel": "claude-sonnet-4",
            "contextStrategy": "full-file-reads",
            "toolSurface": ["gmail", "browser", "notion", "slack"]
          }
        }
      }]
    }
  }
}
```

---

## Audit Result Format

```json
{
  "score": 62,
  "grade": "C",
  "summary": "Significant token waste identified across model selection and context strategy.",
  "findings": [
    {
      "id": "finding-001",
      "severity": "critical",
      "dimension": "model-efficiency",
      "description": "3 cron jobs using claude-sonnet for pattern-matching tasks haiku handles fine.",
      "recommendation": "Downgrade mechanical crons to haiku. Reserve sonnet for judgment tasks.",
      "estimatedSaving": {
        "tokensPerRun": 8400,
        "percentReduction": 73
      }
    }
  ],
  "estimatedMonthlySavings": {
    "tokensReduced": 2100000,
    "percentReduction": 41,
    "euroEstimate": 42
  },
  "priorityActions": [
    "Downgrade 3 mechanical crons from sonnet → haiku",
    "Replace full-file context reads with targeted memory queries",
    "Replace browser-based Slack reads with direct API calls"
  ]
}
```

---

## SSE Streaming (GET)

Stream results as they arrive:
```bash
curl -N "https://botlington.com/a2a?taskId=TASK_ID"
```

Events:
- `event: finding` — individual finding as it's scored
- `event: complete` — full result object
- `event: working` — still processing

---

## The 5 Scoring Dimensions

1. **Model efficiency** — right model for the task? (haiku vs sonnet vs opus)
2. **Context hygiene** — loading only what's needed per run?
3. **Tool surface** — any browser calls replaceable with direct APIs?
4. **Prompt density** — clear, tight prompts or verbose/ambiguous ones?
5. **Idempotency** — tracking what's already been done to avoid repeat work?

---

## Complete Shell Example

```bash
API_KEY="your-api-key"
BASE="https://botlington.com/a2a"

# 1. Start audit
RESPONSE=$(curl -s -X POST $BASE \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tasks/send","params":{"message":{"role":"user","parts":[{"kind":"text","text":"start"}]}}}')

TASK_ID=$(echo $RESPONSE | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['id'])")
QUESTION=$(echo $RESPONSE | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['artifacts'][0]['parts'][0]['text'])")

echo "Task: $TASK_ID"
echo "Gary: $QUESTION"

# 2. Answer Gary's question
curl -s -X POST $BASE \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":2,\"method\":\"tasks/send\",\"params\":{\"id\":\"$TASK_ID\",\"message\":{\"role\":\"user\",\"parts\":[{\"kind\":\"text\",\"text\":\"I run 8 cron jobs, every 15-60 minutes.\"}]}}}"

# ... continue for all 7 turns ...

# 3. Stream results
curl -N "$BASE?taskId=$TASK_ID"
```

---

## Notes

- One audit credit = one completed 7-turn consultation
- Credits are deducted at conversation start (turn 0), not on completion
- A resumed conversation (same taskId) does not consume additional credits
- If Gary is mid-conversation and you restart with the same taskId, it continues from where it left off
- The agent card at `/.well-known/agent.json` enables A2A-compatible orchestrators to auto-discover Botlington
