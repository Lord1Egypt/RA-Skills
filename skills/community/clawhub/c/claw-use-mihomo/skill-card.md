## Description:

Manage mihomo proxy installation, subscription configuration, health monitoring, and automatic node switching for vmess, ss, trojan, and vless protocols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[4ier](https://clawhub.ai/user/4ier)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users use this skill to install and manage mihomo proxy configurations from subscription URLs or protocol links, monitor proxy health, and switch nodes when connectivity degrades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent privileged service setup can keep mihomo running beyond the initiating agent session.

Mitigation: Inspect created systemd or launchd service files before enabling them and document the manual removal steps for the target host.

Risk: Mutable binary downloads can change between installs.

Mitigation: Use a pinned, trusted package version and verify the downloaded mihomo binary before execution.

Risk: Subscription URLs and proxy controller data may expose sensitive proxy-management information.

Mitigation: Avoid pasting sensitive subscription URLs into logged agent sessions, bind the controller to loopback, and configure a controller secret.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/4ier/skills/claw-use-mihomo)
- [mihomod npm package](https://www.npmjs.com/package/mihomod)
- [mihomo project](https://github.com/MetaCubeX/mihomo)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create or update local proxy configuration, install a mihomo binary, and manage system services.]

## Skill Version(s):

0.2.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
