## Description:

Helps developers, support teams, SaaS operators, and users turn vague errors into clearer messages that explain what failed, why it failed, and what action to take next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, SaaS operators, and users use this skill to rewrite or plan clearer error messages and troubleshooting responses. It helps produce tailored artifacts, reusable checklists, workflows, analysis, code changes, and verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad debugging, support, and productivity triggers may cause the skill to be selected more often than intended.

Mitigation: Narrow or disable implicit invocation when tight routing is required.

Risk: Generated error-message guidance may be misleading if the user provides incomplete logs, constraints, or product context.

Mitigation: Review suggested wording and actions against the actual failure mode before publishing or sending them to users.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/error-message-improver-100358)
- [Dify issue: agent_v2 standard docker deployment error](https://github.com/langgenius/dify/issues/39161)
- [AWS API VPC assignment platform issue](https://github.com/VladAdochitei/aws-api-vpc-assignment-platform/issues/8)
- [DBA Dash issue: Source IOStats](https://github.com/trimble-oss/dba-dash/issues/1981)
- [SegmentFault tag: error-messages](https://segmentfault.com/t/error-messages)
- [Hacker News: Ghostel.el](https://news.ycombinator.com/item?id=48905348)
- [Hacker News: A road to Lisp](https://news.ycombinator.com/item?id=48862125)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown or concise text with optional code blocks, templates, checklists, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no runtime tools, credentials, or external services are required by the artifact.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
