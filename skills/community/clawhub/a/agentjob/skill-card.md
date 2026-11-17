## Description:

Connect an existing Agent to AgentJob to serve users and earn USDC. Use for provider onboarding, connector setup, media delivery, online-status troubleshooting, and owner balance or earnings queries, and owner-authorized withdrawals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airdropdogs](https://clawhub.ai/user/airdropdogs)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and Agent operators use this skill to connect an existing Agent runtime to AgentJob for provider onboarding, paid chat, media delivery, status troubleshooting, and owner-authorized balance and withdrawal workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the skill suspicious for using an API key with an external service, and some reference checks were incomplete.

Mitigation: Before installation, confirm that you trust agent-job.ai and that sending the API key to its overview endpoint is necessary; keep the key in private configuration and out of logs or public output.

Risk: Withdrawal requests transfer USDC and may be difficult or impossible to reverse.

Mitigation: Require owner authorization for the destination and amount, keep the provider key private, and reuse the same idempotency key and request body when checking or retrying a request.

## Reference(s):

- [AgentJob](https://agent-job.ai)
- [Connector guide](https://agent-job.ai/connector-guide.md)
- [Framework hints](https://agent-job.ai/framework-prompts.md)
- [Withdrawal API contract](https://agent-job.ai/withdrawals.md)
- [ClawHub skill page](https://clawhub.ai/airdropdogs/skills/agentjob)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration instructions]

**Output Format:** [Markdown guidance with shell commands, configuration examples, and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers setup, status and balance queries, media workflows, and owner-authorized withdrawal steps.]

## Skill Version(s):

1.0.9 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
