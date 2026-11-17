## Description:

Reconciliation Report Analysis Expert - Parses ONLY local Settlement Detail report files (SETTLEMENT_DETAIL_*.csv / .xlsx) for settlement amount validation, fee analysis, and reconciliation knowledge Q&A.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antom-tech](https://clawhub.ai/user/antom-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Merchants, finance operators, and support teams use this skill to analyze local Antom Settlement Detail report files, validate settlement amounts, review fees, and answer reconciliation questions. It is limited to settlement and payment-processing reconciliation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote rules and knowledge documents can change after package review and influence analysis behavior.

Mitigation: Deploy only where access to marmot-cloud CDN is acceptable, and review remote-document behavior before using the skill for sensitive reconciliation decisions.

Risk: Merchant financial report files may contain sensitive payment and settlement data.

Mitigation: Run the skill in a constrained environment with appropriate data-handling controls for merchant financial files.

Risk: Large or untrusted XLSX inputs can create resource or parsing risk.

Mitigation: Avoid untrusted oversized XLSX files and require users to provide only expected Settlement Detail CSV or XLSX exports.

Risk: The skill can present update prompts that lead to administrative commands.

Mitigation: Treat update instructions as administrative actions and verify them before running.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/antom-tech/skills/antom-reconciliation-expert)
- [Antom Reconciliation Rules](https://cdn.marmot-cloud.com/page/antom_bill_reconciliation_doc/rules/)
- [Antom Reconciliation Wiki](https://cdn.marmot-cloud.com/page/antom_bill_reconciliation_doc/wiki/)
- [Filter DSL Schema](artifact/scripts/core/dsl_schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured analysis summaries, with optional code, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include settlement validation results, fee summaries, reconciliation explanations, rejection guidance for unsupported files, and update instructions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
