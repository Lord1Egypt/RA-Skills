## Description:

Finance LITE helps agents perform basic financial ratio analysis, DuPont decomposition, and cash-flow structure analysis from provided financial statement data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze supplied financial statements for solvency, profitability, ROE drivers, cash-flow health, and basic improvement suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marked the release suspicious because the read-only finance-analysis skill also describes command execution, file writing, external APIs, and API keys.

Mitigation: Review carefully before installing and treat the skill as read-only finance-analysis guidance; remove or tightly scope unrelated command, API, credential, and file-writing language before broad deployment.

Risk: Financial conclusions can be misleading when source statements are incomplete, unaudited, or mapped incorrectly.

Mitigation: Require complete statement inputs where possible, state missing data and assumptions in outputs, and have finance-qualified reviewers verify conclusions before decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/accounting-and-finance-free)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with calculation tables, ratio explanations, health assessments, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on user-provided financial statement data and do not include real-time market analysis.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
