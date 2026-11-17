## Description:

残保金申报表逐项复算应安排人数、应缴金额、已缴与应缴差异、合计勾稽、重复与空缺检测，并为每条结论引用原文行号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and tax staff use this skill before disability employment fund filing to locally recalculate worksheet arithmetic, detect missing or duplicate rows, and compare paid amounts with payable amounts. The skill is intended for checking worksheet consistency, not for tax advice or local policy lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is not tax advice and does not verify local policy parameters, certificates, contracts, or XLSX files.

Mitigation: Provide only worksheet text needed for arithmetic checks and have qualified staff verify filing obligations, local policy values, certificates, contracts, and source spreadsheets before submission.

Risk: Missing or unrecognized worksheet fields can prevent a reliable conclusion.

Mitigation: Include the required table headers and rows from the worksheet text; when the tool reports insufficient input, correct the input instead of treating the absence of findings as validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/disability-fund-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Human-readable text or JSON check results with finding categories, source line references, missing-input messages, and advice.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; does not use network access, API keys, or registration.]

## Skill Version(s):

1.0.45 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
