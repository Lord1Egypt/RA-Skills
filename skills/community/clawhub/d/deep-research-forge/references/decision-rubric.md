# Decision Rubric

Use this file when the output must support an action: adopt, buy, learn, invest, copy, monitor, avoid, or continue researching.

## Verdicts

| Verdict | Use when | Required next step |
| --- | --- | --- |
| `GO` | upside is clear, risks are bounded, and evidence is strong enough for the user's stakes | act with named guardrails |
| `EXPERIMENT` | promise is plausible but the user's context needs proof | run a small test with success / fail criteria |
| `HOLD` | timing, maturity, budget, or missing evidence makes action premature | define what must change before reconsidering |
| `MONITOR` | category matters, but no immediate action is justified | watch specific signals on a cadence |
| `NO-GO` | risks or mismatch outweigh upside under current assumptions | avoid, or choose an alternative |

## Confidence Levels

- `high`: multiple independent strong sources, stable facts, low contradiction, clear fit to user's context.
- `medium`: enough evidence for a provisional call, but some facts are time-sensitive, indirect, or context-dependent.
- `low`: evidence is sparse, conflicting, stale, or mostly inferred. Prefer `EXPERIMENT`, `HOLD`, or `MONITOR`.

Do not use high confidence for volatile markets, unreleased products, unverified private claims, or user-specific decisions without user context.

## Decision Frame

Before recommending, name:

```text
Decision:
Stake:
User context:
Alternatives:
Default if we do nothing:
Evidence threshold:
```

If the user did not provide the context, state a reasonable default and mark it as an assumption.

## Reversal Conditions

Every decision brief needs at least one reversal condition:

- `GO` should change if a named risk appears.
- `EXPERIMENT` should change if the test misses defined success criteria.
- `HOLD` should change if the blocker is removed.
- `MONITOR` should change if a monitored signal crosses a threshold.
- `NO-GO` should change if the core mismatch is solved or the user's goal changes.

## Monitoring List

Keep monitoring lists short and inspectable:

- signal
- why it matters
- where to check
- review cadence
- threshold that changes the decision
