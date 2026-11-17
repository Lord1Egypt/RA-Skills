# Agent skill assessment design

## Evaluation unit

Each case contains: Case ID, Task, Input Materials, Environment/Tool Status, Desired Behavior, Allowed Differences, Unacceptable Behavior, Scoring Method, and Evidence.

## Case portfolio

| Type | Minimum Coverage |
|---|---|
| Normal | High-frequency core tasks, different expressions and data forms |
| Boundaries | Missing fields, conflicting information, ambiguous instructions, oversized input |
| Failure | Tool timeout, insufficient permissions, empty results, partial success |
| Security | Prompt injection, sensitive information, unauthorized writing, induced outgoing |
| Manual collaboration | Should ask, should confirm, should transfer, should reject |
| Regression | Historical failures and fixed cases |

## Rating dimensions

- Task completion: whether real user results are achieved;
- Correctness: whether facts, calculations, business rules and references are correct;
- Completeness: whether key steps, anomalies or evidence are missed;
- Tool behavior: whether selection, parameters, order, validation and retries are reasonable;
- Security: whether to protect permissions, sensitive data and manual confirmation;
- Traceability: whether the conclusion can be returned to the input, search or tool results;
- Efficiency: delay, number of calls, token/amount cost and manual intervention;
- Experience: Is it clear, actionable, and not overly interruptive?

Critical safety items use hard failures and cannot be offset by the overall average score.

## Evaluation method

- Deterministic checks: formats, fields, calculations, tool parameters, permissions;
- Expert ratings: business correctness, policy interpretation and risks;
- Model scoring: large-scale preliminary screening, but first calibrated with artificial samples;
- End-to-end operation: observe multiple rounds of tool calls and final environment status;
- Online feedback: only as a supplement and does not replace the offline regression set.

## Version and anti-pollution

Freeze skill, model, configuration, tool, dataset and grader versions. The evaluation set must not leak into skill examples; desensitize and record the source when adding real failure cases.
