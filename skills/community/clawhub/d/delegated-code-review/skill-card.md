## Description:

Perform a single review with a fresh, read-only subagent, then verify findings and apply accepted fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wufei-png](https://clawhub.ai/user/wufei-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to delegate one focused code review, verify the reported findings, apply accepted fixes, rerun relevant tests, and summarize the outcome.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Accepted review findings may result in code changes.

Mitigation: Review the final summary, decisions, fixes, and test results before relying on the changes.

Risk: Delegated review findings may be incorrect or not worth acting on.

Mitigation: Verify each finding before accepting it, record rejected findings as not accepted with a reason, and rerun relevant tests after accepted fixes.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown review summary with findings, decisions, fixes, verification results, and remaining risks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include accepted code changes and test commands after the primary agent verifies review findings.]

## Skill Version(s):

0.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
