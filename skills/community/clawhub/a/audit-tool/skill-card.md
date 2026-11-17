## Description:

Deep audit for installed ClawHub skills — usage analysis, permission review, conflict detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use Skill Auditor to review installed OpenClaw and ClawHub skills for usage, permissions, conflicts, and health, then plan cleanup or permission changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect local skill metadata and session or usage history, which can expose sensitive operational details.

Mitigation: Run it with a narrow time window and use aggregate usage data only when possible.

Risk: Generated cleanup scripts can uninstall, disable, or archive skills if executed without review.

Mitigation: Use dry-run cleanup first and review any generated shell script before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/audit-tool)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured Markdown report with optional shell cleanup script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include health scores, flags, conflict matrices, and dry-run cleanup commands.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
