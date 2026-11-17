## Description:

A local Chinese-language checker that recalculates bank loan interest and repayment schedule rows, verifies totals, detects duplicates, blanks, placeholders, and negative values, and cites source lines for each finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and cashier teams use this skill during monthly close, reconciliation, or review workflows to check copied or exported Chinese bank loan interest and repayment schedule tables. It is intended as a local table arithmetic and reconciliation aid, not as a legal, tax, contract, LPR, or accounting judgment tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free edition does not perform excluded loan, contract, LPR, accounting, tax, or legal judgments.

Mitigation: Use the output as table-level arithmetic and reconciliation guidance only, and route contract, LPR, accounting, tax, and legal decisions to qualified reviewers.

Risk: Copied or exported table text that lacks required headers or rows cannot support a conclusion.

Mitigation: Provide the full bank loan interest and repayment schedule table, including headers, and treat insufficient-input responses as no conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/bank-loan-interest-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text summary or JSON result with executed checks, withheld checks, findings, scope, summary, and out-of-scope notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite input line numbers; insufficient input returns missing-field guidance instead of a positive or negative conclusion.]

## Skill Version(s):

1.0.53 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
