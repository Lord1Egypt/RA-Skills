## Description:

Multi-dimensional code audit skill that uses structured subagent delegation to review GitHub releases, pull requests, or codebases across security, concurrency, implementation logic, test quality, and simplicity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinghaojia](https://clawhub.ai/user/yinghaojia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to run structured code audits before merging or releasing code. It helps organize findings into verified severity, priority, risk, and fix guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow reads source code and may use multiple subagents during review, which can expose private code beyond the main session.

Mitigation: Confirm the review scope and data handling expectations before using it on private repositories or sensitive code.

Risk: Audit findings and fix recommendations may be incomplete, incorrect, or overly broad.

Mitigation: Require line-level evidence for each finding and have humans verify important remediation decisions before changing production code.

Risk: Critical findings can create release-blocking decisions if a single reviewer misclassifies severity.

Mitigation: Use the skill's Four-Eyes cross-verification process for Critical findings and escalate disputed findings to a human reviewer.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yinghaojia/skills/deep-code-review)
- [Audit Dimensions](references/audit-dimensions.md)
- [Four-Eyes Cross-Verification Protocol](references/four-eyes.md)
- [Output Format Specification](references/output-format.md)
- [Severity Classification Rubric](references/severity-rubric.md)
- [Subagent Audit Templates](references/subagent-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with structured findings, severity tables, priority matrix, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Chinese-formatted report sections and source file citations.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
