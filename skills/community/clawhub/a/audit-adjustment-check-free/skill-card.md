## Description:

A free deterministic checker for audit adjustment reconciliation tables that recalculates row arithmetic, totals, duplicates, blanks, placeholders, and negative amounts with source-backed findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and audit teams use this skill during year-end audit adjustment reconciliation to check pasted audit adjustment tables for arithmetic balance, column totals, duplicate rows, missing values, placeholders, and negative amounts. It returns findings tied to source lines and withholds conclusions when required table content is missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide sensitive finance or audit table content.

Mitigation: Run the checker in a trusted local environment and keep input files local, consistent with the security evidence that found no network use.

Risk: The checker covers internal arithmetic and table consistency only, not accounting treatment or audit advice.

Mitigation: Review the Chinese-language findings carefully and have accounting or audit professionals assess treatment, disclosure, materiality, and policy questions.

Risk: The free edition omits some checks that are explicitly listed as not executed.

Mitigation: Review the listed omitted checks and use manual review or the appropriate complete workflow for those out-of-scope items.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/audit-adjustment-check-free)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries and optional JSON findings from a local Node.js checker]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source lines; insufficient input returns missing fields instead of a conclusion.]

## Skill Version(s):

1.0.58 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
