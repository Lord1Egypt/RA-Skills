# AgentMFA Error Handling

## Tool call outcomes

| Status | Meaning | Action |
|--------|---------|--------|
| `approved` | Human approved with biometrics | Proceed; log the `code` as proof |
| `rejected` | Human rejected | Abort the action; inform the user |
| `expired` | Request timed out | Abort; treat as rejected |

## Rules

- Never proceed without `"status": "approved"`
- Never retry a rejected request automatically — only the human can re-initiate
- Never reuse a `code` — each approval generates a unique one-time approval code
