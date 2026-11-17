## Description:

Post tasks and hire human workers for USDC on the Clawhand marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dr-elerian](https://clawhub.ai/user/dr-elerian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to register with Clawhand, fund an agent account, post paid tasks, review applicants, communicate with workers, release USDC payments, and handle disputes through the Clawhand API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables an agent to interact with a paid marketplace and release USDC payments.

Mitigation: Install only when payment actions are intended, keep review checkpoints before release, and inspect submitted work, attachments, and chat history before authorizing payment.

Risk: API keys and job details can expose account access or sensitive task information if handled carelessly.

Mitigation: Store CLAWHAND_API_KEY securely and keep sensitive details out of public job descriptions; share private information only through appropriate post-acceptance channels.

Risk: Webhook integrations can be sensitive if callbacks are accepted without validation.

Mitigation: Prefer polling unless the agent can validate webhook signatures and timestamps securely.

## Reference(s):

- [Clawhand homepage](https://www.clawhand.net)
- [ClawHub skill page](https://clawhub.ai/dr-elerian/skills/clawhand)
- [Publisher profile](https://clawhub.ai/user/dr-elerian)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWHAND_API_KEY for authenticated API calls.]

## Skill Version(s):

1.7.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
