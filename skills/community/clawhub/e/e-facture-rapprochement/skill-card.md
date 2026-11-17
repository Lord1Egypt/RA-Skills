## Description:

Ingests invoices, receipts, PDFs, and bank statements, then reconciles payments to invoices and writes Pocket-Claw company.json and rapprochement.json outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trendex](https://clawhub.ai/user/trendex)

### License/Terms of Use:

MIT-0

## Use Case:

Accounting teams and agents use this skill to ingest electronic invoices, receipts, PDFs, and bank statement exports, reconcile payments against invoices, and report paid, pending, overdue, orphan, and missing items for each client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive financial files.

Mitigation: Use it only in a controlled workspace, prefer the default sandbox before --real, and avoid untrusted XML or PDF inputs unless the run is isolated.

Risk: The release depends on a sibling reconciliation engine that the security evidence says should be verified.

Mitigation: Verify that the sibling rapprochement-paiements skill is trusted and unchanged before installing or running this skill.

Risk: Low-confidence or high-value extraction can affect accounting results.

Mitigation: Review the generated human-validation list and confirm flagged invoices before relying on the reconciliation output.

## Reference(s):

- [Invoice extraction](references/invoice-extraction.md)
- [Bank formats](references/bank-formats.md)
- [Matching rules](references/matching-rules.md)
- [Output contract](references/output-contract.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON files, Markdown]

**Output Format:** [Markdown guidance with inline shell commands plus JSON sidecar, company.json, and rapprochement.json files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes human-review flags for high-value or low-confidence invoice extraction.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
