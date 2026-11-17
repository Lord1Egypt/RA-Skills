## Description:

Register, deregister, and manage this OpenClaw instance as an A2A agent in the A2A API Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thearchitectit](https://clawhub.ai/user/thearchitectit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure an OpenClaw instance for A2A gateway discovery, register or remove the instance, send liveness heartbeats, and check registration status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses registry-wide A2A gateway admin access.

Mitigation: Use it only with a trusted gateway over HTTPS and limit access to gateway admin credentials.

Risk: Tampered config values, agent slugs, or shared a2a.conf files could expose credentials or enable command execution.

Mitigation: Avoid untrusted or shared a2a.conf files, restrict file permissions manually, and do not pass untrusted config values or slugs until the shell/Python injection issues are fixed.

## Reference(s):

- [A2a Register on ClawHub](https://clawhub.ai/thearchitectit/skills/a2a-register)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and python3 on Linux or macOS; gateway URL must be configured before registration, heartbeat, status, or deregistration commands can run.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
