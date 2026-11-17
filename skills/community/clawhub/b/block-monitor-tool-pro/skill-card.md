## Description:

内容验证网关专业版 helps agents perform enterprise content moderation, policy checks, batch validation, real-time blocking, audit reporting, and REST API integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, enterprise content safety teams, and workflow operators use this skill to evaluate content, manage moderation policies, process batches, trigger real-time blocking or alerts, and produce audit-oriented results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run a REST API and expose moderation results.

Mitigation: Use authentication, HTTPS, trusted callback destinations, and restricted bind addresses before use with real user content.

Risk: The skill may handle sensitive personal data during moderation and audit logging.

Mitigation: Define a retention policy, limit audit-log access, and avoid storing unnecessary personal data.

Risk: Webhook or callback behavior can send content or findings outside the intended environment.

Mitigation: Review webhook and callback destinations and allow only trusted endpoints.

Risk: The artifact does not fully clarify whether content is sent to an external LLM or service.

Mitigation: Clarify data flow before deployment and disable or restrict external service calls unless approved.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/thcjp/skills/block-monitor-tool-pro)
- [Detailed examples](references/detail.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON result examples and inline Python or shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured moderation results with status, data, execution log, and error fields.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
