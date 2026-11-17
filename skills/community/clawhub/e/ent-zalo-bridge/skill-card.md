## Description:

Guides deployment of a Zalo Bot webhook bridge for OpenClaw, including a Node.js receiver, HTTPS routing, service configuration, and webhook registration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinhbuiii](https://clawhub.ai/user/thinhbuiii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy a persistent receiver for Zalo Bot messages in OpenClaw and register its HTTPS webhook with Zalo.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing a persistent service and registering a webhook change the target machine and bot configuration.

Mitigation: Confirm authorization before running sudo, systemd, or setWebhook commands; run the service under a dedicated user.

Risk: Bot credentials and webhook message contents are sensitive.

Mitigation: Keep token and secret out of chat and logs, restrict the environment file, and control access to locally stored message logs.

## Reference(s):

- [ClawHub release listing](https://clawhub.ai/thinhbuiii/skills/ent-zalo-bridge)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with JavaScript, shell, and service configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes webhook setup and message-log verification guidance.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
