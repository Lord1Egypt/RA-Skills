## Description:

Use the ntfy CLI to publish or schedule notifications, send attachments, subscribe or poll topics, run notification hooks, and administer ntfy servers, users, ACLs, tokens, tiers, or web push.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanjelin](https://clawhub.ai/user/lanjelin)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to manage notifications and authorized server administration through an installed ntfy CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notifications or credentials may reach an unintended or public topic or server.

Mitigation: Confirm the destination and use HTTPS with a dedicated account or token restricted to the required topics; avoid public topics for sensitive messages.

Risk: Notification handlers, streaming subscriptions, and persistent services can execute commands or remain active.

Mitigation: Require explicit authorization before enabling handlers or persistent processes, and use finite polling when practical.

Risk: Server administration can change users, access controls, tokens, or service configuration.

Mitigation: Confirm the intended local server and obtain explicit authorization before administrative changes.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lanjelin/skills/claw-ntfy)
- [Server-resolved source repository](https://github.com/Lanjelin/openclaw-ntfy)
- [ntfy installation](https://docs.ntfy.sh/install/)
- [ntfy publishing documentation](https://docs.ntfy.sh/publish/)
- [ntfy CLI subscription configuration](https://docs.ntfy.sh/subscribe/cli/)
- [OpenClaw skills configuration and sandbox guidance](https://docs.openclaw.ai/tools/skills-config)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Text or Markdown with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands depend on the installed ntfy CLI and the authorized server, topic, and credentials.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
