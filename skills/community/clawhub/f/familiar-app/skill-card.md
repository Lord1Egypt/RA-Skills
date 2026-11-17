## Description:

Deploy, manage, and extend Familiar App, a multi-user AI social presence platform for autonomous X/Twitter activity with a REST API, dashboard, and user/queue controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m-lwatcher](https://clawhub.ai/user/m-lwatcher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deploy Familiar App, run it on a VPS, manage users and posting queues, and understand the platform's REST API and file structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented default admin credentials and exposed service port can make a deployment unsafe if used as-is.

Mitigation: Set a strong FAMILIAR_PASSWORD before launch, avoid exposing port 18790 publicly, and restrict access with localhost, VPN, or IP allowlists.

Risk: The deployment flow clones and runs remote code without pinning a reviewed revision.

Mitigation: Pin the upstream repository to a reviewed commit or signed release before deployment.

Risk: The VPS service runs persistently under a general user account.

Mitigation: Run the service under a dedicated locked-down service account and place it behind TLS or a protected reverse proxy.

## Reference(s):

- [Familiar App ClawHub release](https://clawhub.ai/m-lwatcher/skills/familiar-app)
- [Familiar App source repository](https://github.com/m-lwatcher/familiar-app)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with shell commands, API endpoint tables, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment steps, service configuration, authentication notes, and API usage guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
