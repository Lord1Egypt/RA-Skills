## Description:

Provides command-line investor suitability matching and illustrative large-transaction reporting-threshold checks for financial AI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and financial-institution reviewers use the CLI to screen investor/product risk grades and flag transactions above a sample reporting threshold. Results require review against applicable rules before use in compliance decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read, write, execution, and web access despite a local calculator workflow.

Mitigation: Review before installation and narrow or remove unnecessary tool permissions, especially WebFetch and Write.

Risk: Documentation describes compliance reports and audit logs that the included script does not write.

Mitigation: Do not assume records are created; verify logging requirements and document any separate storage process.

Risk: A fixed illustrative threshold and simplified suitability grades may not match applicable regulations.

Mitigation: Have qualified reviewers validate current jurisdiction-specific rules before relying on the results.

## Reference(s):

- [fin-reg-calc ClawHub release](https://clawhub.ai/zhaoxinghua09-cell/skills/fin-reg-calc)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Command-line text, or JSON with --json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports suitability and threshold results with an overall compliant flag; exits 0 for pass, 1 for flagged checks, or 2 for usage errors. The included script does not write reports or audit logs.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata; bundled frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
