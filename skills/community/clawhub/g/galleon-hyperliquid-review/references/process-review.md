# Process and incident review

Grade process before reading net PnL.

## Checks

| Control | Evidence |
|---|---|
| Complete immutable ticket | revision and digest |
| Current risk sign-off | live inputs and ticket expiry |
| Exact user approval | user-authored `approve <id>` after ticket |
| Single send | durable send ledger and nonce ownership |
| Client identity | unique client order ID per leg |
| Price and size bounds | approved fields versus submitted payload |
| Reconciliation | order, fills, position, balance agreement |
| Protection | valid reduce-only trigger throughout exposure |
| Limits | per-trade, total, correlated, daily, tier, and mode-specific |
| Incident handling | stopped adding risk, no blind retry, smallest containment |

## Grades

- `clean`: every required control present and no material mismatch.
- `minor break`: evidence or process defect that did not bypass authorization, exceed limits, duplicate exposure, or leave a position unprotected.
- `major break`: unapproved action, material ticket drift, duplicate send on an unknown result, limit breach, signer misuse, or unprotected exposure.

Outcome never changes the process grade.

## Incident review

Write a UTC timeline from durable records. State maximum exposure, liquidation buffer, protection state, what controls caught or missed, containment actions, and remaining uncertainty. Assign one corrective action with an owner and verification condition. Do not invent a root cause when evidence only supports a symptom.
