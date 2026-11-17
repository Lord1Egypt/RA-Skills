## Description:

Checks copied export tax refund declaration and supporting-document tables for refund recalculation, totals reconciliation, declaration and invoice matching, rate consistency, missing documents, and source-line-cited findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External export tax refund preparers and reviewers use this skill before filing to check tabular declaration and document data for arithmetic mismatches, duplicate or mismatched identifiers, rate inconsistencies, and missing supporting-document status fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The output can be mistaken for legal, tax authority, or filing eligibility guidance.

Mitigation: Use it only for local consistency checks on copied export tax refund tables, review checks_not_run, and have a qualified reviewer confirm tax-rate, classification, and filing decisions.

Risk: The free version does not run cross-month or cross-enterprise ledger checks, exchange-rate recalculation, invoice-basis comparison, or incomplete-document-in-period checks.

Mitigation: Treat checks_not_run as required review scope and do not rely on a clean result for those excluded checks.

Risk: Incomplete or unrecognized input may otherwise create false confidence.

Mitigation: Provide the full table including headers; when materials are insufficient, the skill should be treated as having made no finding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/export-tax-refund-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON with findings, scope, checks_not_run, summary verdict, and source line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local consistency checks on user-provided copied tables; insufficient input produces no conclusion.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
