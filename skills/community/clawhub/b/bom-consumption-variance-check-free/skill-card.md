## Description:

A free deterministic checker for production-work-order BOM consumption variance worksheets that recomputes standard quantity, usage variance, loss rate, totals, duplicate material rows, missing fields, and negative or non-positive values with source-line citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing cost accountants, auditors, and operations teams use this skill to locally check BOM and work-order material consumption worksheets before close or review. It identifies arithmetic and worksheet-quality issues but does not decide BOM engineering correctness, approval compliance, substitutions, cross-work-order material use, or accountability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free version does not run cross-work-order material-use detection, substitution approval checks, refund-not-offset checks, overuse attribution, or amount-ranked action lists.

Mitigation: Review the skill output's checks_not_run and withheld-scope fields before using results for accounting, audit, or remediation decisions.

Risk: The skill recomputes worksheet arithmetic from provided values and does not validate whether BOM rates, approvals, units, or responsibility assignments are correct.

Mitigation: Confirm BOM master data, approval records, unit normalization, and responsibility decisions in the source business systems before taking action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/bom-consumption-variance-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON with line-cited findings and scope metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard-library code; reports checks executed and checks_not_run when scope is limited.]

## Skill Version(s):

1.0.26 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
