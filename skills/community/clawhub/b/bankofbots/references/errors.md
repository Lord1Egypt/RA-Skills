# BOB CLI — Error Recovery

Every failed command returns `ok: false` with `data.error` and `next_actions`. Always follow `next_actions` before retrying.

## Hard stops — do not retry

| Error | Action |
|---|---|
| 403 Forbidden | Run `bob auth me`. API key invalid or agent not approved. |
| Proof ownership mismatch | Challenge may have expired — re-run the challenge command for a fresh nonce. |

## Recoverable errors

| Error | Action |
|---|---|
| 429 Too Many Requests | Back off and retry. Check `next_actions` for suggested wait. |
| 409 Conflict | Resource already exists. Run `bob agent get` to confirm state. |
| Proof already submitted | Duplicate proof ref — already counted. Check `bob agent credit-events <agent-id>`. |
| Challenge expired | Re-run the binding challenge command (`bob binding challenge --rail evm`). |
| Claim code rejected | Generate a new code from the dashboard. |
| Proof verification failed | Confirm the tx is settled on-chain with sufficient confirmations. Double-check the txid/hash and chain. |

## Output format

```json
{
  "ok": true,
  "command": "bob <subcommand>",
  "data": { ... },
  "next_actions": [
    { "command": "bob ...", "description": "..." }
  ]
}
```

`ok: false` → `data.error` has the reason. Follow `next_actions` in order.
