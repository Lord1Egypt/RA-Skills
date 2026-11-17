## Description:

A free deterministic checker for construction-in-progress ledgers that recomputes cost pooling, cumulative roll-forward, carrying balance, capitalized interest, transfer amount reconciliation, category validity, duplicate rows, and missing fields with source-line citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, accounting, and audit users can run this local checker against Chinese-language construction-in-progress ledger text to identify arithmetic and reconciliation issues before month-end close or audit review. It supports review of ledger consistency, not accounting policy or audit opinion decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker is not a substitute for accounting, audit, or policy judgment.

Mitigation: Use findings as a reconciliation aid and have qualified reviewers decide capitalization policy, audit conclusions, and final accounting treatment.

Risk: The free edition omits transfer-timing, post-transfer cost, abnormal stoppage capitalization, contract-rate mismatch, and provisional-transfer adjustment checks.

Mitigation: Review those out-of-scope areas separately before relying on the ledger review.

Risk: Incomplete, malformed, or headerless ledger input can prevent a meaningful conclusion.

Mitigation: Provide a tab-delimited ledger with recognized headers and treat insufficient-input output as no conclusion.

Risk: The skill runs local Node.js code on ledger text.

Mitigation: Install from the verified release, review scan results, and run only in environments approved for the ledger data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/cip-capitalization-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Human-readable console text or JSON findings with line citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on Node.js standard library; reports insufficient input instead of inventing conclusions.]

## Skill Version(s):

1.0.52 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
