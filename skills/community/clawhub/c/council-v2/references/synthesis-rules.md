# Council v2 Mechanical Synthesis Rules

These rules are the protocol. The synthesizer narrates the result; it does not invent one.

## Rule 1 — Majority vote decides
- `approve = 1.0`
- `approve_with_conditions = 0.5`
- `reject = 0.0`
- Highest mechanically supported outcome wins.

Example:
- approve, approve, reject = 2.0 / 3 reviewers → `approve`

## Rule 2 — Critical finding auto-block
Any reviewer can block approval by raising a `critical` finding.

Example:
- 4 approves, 1 reject with critical secret-exposure finding → `blocked`

## Rule 3 — Conditional votes count as half
Conditionals are not full approval.

Example:
- approve, approve_with_conditions, reject = 1.5 points / 3 reviewers → `approve_with_conditions`

## Rule 4 — Splits default conservative
Ambiguous splits resolve to the more conservative result.

Example:
- 2-2-1 in Full Council does not become approval by rhetoric; it resolves to `approve_with_conditions` or `reject` depending on the split shape.

## Rule 5 — Anti-consensus check on unanimous decisions
Unanimity is a signal, not proof. The synthesis must state the strongest serious counterargument.

Example:
- 5 approves → still surface the best case against approval and explain why it lost.

## Rule 6 — Raw outputs shown on Full Council
On Full Council runs, operator sees the original reviewer verdicts alongside synthesis.

Example:
- Final output includes each role, model alias, verdict, confidence, and summary.

## Rule 7 — Synthesizer does not vote on Full Council
The synthesizer may assemble and narrate the result but cannot add an extra vote in Full Council mode.

Example:
- 5 reviewer outputs in, synthesis happens afterward. No sixth vote appears.

## Rule 8 — Minority reports always preserved
If one or more reviewers dissent from the mechanical outcome, the strongest dissent must be carried forward.

Example:
- 4 approve, 1 reject → include the reject reviewer’s best argument in `minority_report`.

# Edge Cases

## 2-2-1 split
Typical example:
- 2 approve
- 2 reject
- 1 approve_with_conditions

Mechanical reading:
- approve points = 2.5 / 5
- no clear majority
- conservative default applies → `approve_with_conditions` if fixable, otherwise `reject`

## All conditional
Example:
- 3 x approve_with_conditions

Mechanical reading:
- 1.5 / 3
- not a clean approval
- result = `approve_with_conditions`

## Mixed verdicts
Example:
- approve, approve_with_conditions, approve_with_conditions, reject

Mechanical reading:
- 2.0 / 4
- result = `approve_with_conditions`

## Critical plus approval majority
Example:
- approve, approve, approve, reject with critical

Mechanical reading:
- vote looks favorable
- critical auto-block overrides → `blocked`
