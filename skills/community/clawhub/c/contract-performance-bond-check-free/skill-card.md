## Description:

A local Chinese-language checker for performance bond and guarantee ledgers that recalculates row amounts, total rows, duplicates, blanks, and negative amounts with source-cited findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, treasury, and reconciliation staff use this skill during monthly close, account reconciliation, or ledger inventory to check performance bond and guarantee ledgers for arithmetic and table-consistency issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake arithmetic and table-consistency results for legal, banking, or compliance verification.

Mitigation: Treat the output as ledger consistency assistance and verify legal, banking, contract, and compliance questions through the responsible reviewer or institution.

Risk: Input ledgers may contain sensitive commercial or financial data.

Mitigation: Provide only the ledger files intended for checking and run the packaged local checker; server security evidence reports no network access or persistence.

Risk: The free release omits several checks, including over-refund, guarantee expiry, negative guarantee balance, deposit-ratio, and zero-deposit fee checks.

Mitigation: Review the reported checks_not_run scope and avoid relying on this free release for omitted checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/contract-performance-bond-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON check results from a local Node.js runner]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows; when required ledger fields are missing, the skill reports insufficient input instead of drawing a conclusion.]

## Skill Version(s):

1.0.61 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
