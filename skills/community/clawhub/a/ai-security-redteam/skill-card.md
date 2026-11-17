## Description:

Guides authorized AI security assessments with attack-surface checklists, defensive red-team test cases, vulnerability grading, report templates, and remediation advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Developers and security teams use this skill to plan authorized AI red-team assessments, draft defensive test cases, prioritize findings, and prepare remediation and retest reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Red-team cases or prompts could be applied to systems without permission.

Mitigation: Require written authorization and use generated cases only for defensive testing within the approved scope.

Risk: Broad security-related trigger words may load the skill for unrelated security discussions.

Mitigation: Confirm the request is an authorized AI security assessment before applying the skill.

Risk: OWASP mappings in the bundled guidance may become outdated.

Mitigation: Check the current OWASP guidance before relying on specific mappings or issuing findings.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/ai-security-redteam)
- [AI security risk overview](references/01-AI安全风险全景.md)
- [Red-team testing workflow](references/02-红队测试流程.md)
- [Reporting and remediation](references/08-报告与修复.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Human-readable text and Markdown report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primarily Chinese; local CLI provides checklists, test cases, grading, report templates, and fixes.]

## Skill Version(s):

1.1.0 (source: ClawHub release; bundled skill identifies 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
