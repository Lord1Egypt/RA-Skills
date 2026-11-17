## Description:

Controller-level Balance Sheet deep analysis from QuickBooks Online that pulls current and prior-period balance sheets, computes rolling averages, drills into material general-ledger changes, and generates a seven-tab Excel workbook with actionable findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting teams use this skill to produce monthly close balance sheet reviews, working-capital health checks, equity rollforward reconciliations, common-size analysis, and narratives for material balance changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles confidential QuickBooks financial data and may produce sensitive Excel workbooks and cache files.

Mitigation: Use it only in a trusted finance environment, restrict access to generated workbooks and cache files, and delete them when no longer needed.

Risk: QuickBooks Online access and local dependencies are required but not fully specified by the artifact.

Mitigation: Verify and pin the exact dependencies and QBO client before deployment, and limit QBO token scope to the minimum needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/samledger67-dotcom/skills/bs-deep-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides use of a QuickBooks Online balance sheet analysis pipeline that produces a seven-tab Excel workbook.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
