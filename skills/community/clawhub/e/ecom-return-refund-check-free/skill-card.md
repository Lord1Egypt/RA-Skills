## Description:

Checks copied e-commerce return/refund and restock sheets for five deterministic consistency issues, citing source row numbers for each finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce finance, accounting, and warehouse teams use this skill during reconciliation, month-end close, or inventory review to check copied return/refund sheets for refund amount, document-pairing, restock quantity, status/payment, and missing-field issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copied return/refund spreadsheets may contain sensitive business or order data.

Mitigation: Run the checker locally and avoid sharing inputs externally; the security evidence describes local deterministic execution without hidden network behavior.

Risk: The free release only runs five checks and excludes cross-store or cross-period ledgers, recovery lists, and variance attribution.

Mitigation: Use the output scope and checks-not-run fields to confirm what was executed, and do not treat omitted checks as completed.

Risk: The skill checks spreadsheet consistency but does not decide refund policy, legal, tax, audit, ERP, inventory, quality-inspection, or fee-rule correctness.

Mitigation: Treat findings as reconciliation flags and confirm policy decisions and source-system records before taking business action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/ecom-return-refund-check-free)
- [ClawHub publisher profile: chenqg618](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Human-readable text or JSON result with findings, summary, scope, and exit status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source row numbers; insufficient input returns missing requirements without conclusions.]

## Skill Version(s):

1.0.5 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
