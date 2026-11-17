## Description:

A free local checker for Chinese export-rebate document consistency tables that recomputes row arithmetic, verifies totals, detects duplicates and blanks, and cites source rows for each finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, accounting, and export operations teams use this skill to locally pre-check Chinese export-rebate consistency tables before filing, reconciliation, or month-end review. It is a consistency checker, not tax or legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill checks table consistency only and does not provide tax or legal advice.

Mitigation: Use it as a pre-check and have qualified tax or compliance personnel review filing decisions and legal interpretations.

Risk: The free release performs only the listed checks and omits additional full-version checks.

Mitigation: Review the listed withheld checks before relying on the output for a complete reconciliation workflow.

Risk: Insufficient or malformed input causes the tool to withhold conclusions rather than certify consistency.

Mitigation: Provide the table with headers and required fields, and treat an insufficient-input response as no determination.

Risk: The checker is Chinese-language and domain-specific.

Mitigation: Use it only with reviewers who understand the language, field names, and export-rebate table context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chenqg618/skills/export-rebate-doc-consistency-check-free)
- [Publisher Profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable text or JSON results with cited source rows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; no network, registration, API key, or call limit is described. Insufficient input returns missing requirements instead of a pass/fail conclusion.]

## Skill Version(s):

1.0.62 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
