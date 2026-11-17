## Description:

Helps agents create 24-hour disposable email addresses, read their inboxes, and list active addresses for signups and verification workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use temporary inboxes for service registrations, verification emails, and automated testing without supplying a permanent email address.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Other agents on the same budget may read inbox contents, including verification links and one-time codes.

Mitigation: Avoid personal, financial, production, or high-value accounts; isolate agent groups or budgets when inbox privacy matters.

Risk: Generic email requests could expose sensitive messages to a shared disposable inbox.

Mitigation: Use this skill only for explicit temporary-inbox requests and keep messages and credentials out of prompts and logs.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/agentpmt/skills/disposable-email-address)
- [AgentPMT marketplace listing](https://www.agentpmt.com/marketplace/disposable-email-address)
- [AgentPMT account setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [Guidance, JSON tool calls]

**Output Format:** [Text with JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool responses can include temporary addresses, expiry times, and complete inbox messages.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
