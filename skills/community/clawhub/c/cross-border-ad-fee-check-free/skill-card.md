## Description:

A local checker for cross-border ecommerce settlement statements and advertising fee bills that recalculates commissions, ad fees, net settlement amounts, totals, duplicate rows, and missing required fields with source-line evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External finance, operations, and ecommerce store users use this skill during periodic platform reconciliation to check settlement statement and advertising fee bill arithmetic before acting on discrepancies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker may be mistaken for a contract, platform policy, or back-office validation tool.

Mitigation: Use it only for the arithmetic and table-consistency checks it explicitly lists; review contracts, platform terms, and source platform records separately.

Risk: Settlement and advertising fee bill text can contain sensitive commercial data.

Mitigation: Run the local Node-based checker only in an environment approved for that data, and avoid sharing input files or generated findings outside the reconciliation workflow.

Risk: The skill is mainly Chinese-language, which can lead to misuse by reviewers who do not understand the input requirements or limitations.

Mitigation: Have a Chinese-reading reviewer confirm required columns, findings, and stated limitations before using outputs for operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/cross-border-ad-fee-check-free)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Human-readable terminal text or JSON when the --json option is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include severity, category, source line, message, advice, and source basis; insufficient input returns missing fields instead of conclusions.]

## Skill Version(s):

1.0.8 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
