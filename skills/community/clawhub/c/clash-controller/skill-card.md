## Description:

Manages Clash/mihomo proxy environments, including installation, proxy start and stop, subscription management, Web panel operations, Tun mode configuration, and kernel upgrades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kklldog](https://clawhub.ai/user/kklldog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to administer Clash/mihomo proxy environments through command-line guidance for installation, lifecycle control, subscriptions, Web UI access, Tun mode, and upgrades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide installation through an unverified remote installer.

Mitigation: Pin and verify the upstream installer source before execution, or use a reviewed local copy.

Risk: The skill can change high-impact host network settings, including system proxy and Tun mode behavior.

Mitigation: Require explicit user confirmation before enabling Tun mode, changing system proxy state, or running commands that need root privileges.

Risk: The skill can expose or alter Web UI and subscription settings.

Mitigation: Confirm intended Web UI exposure, rotate panel secrets when needed, and review subscription URLs before adding or updating them.

## Reference(s):

- [Clash Controller on ClawHub](https://clawhub.ai/kklldog/skills/clash-controller)
- [kklldog Publisher Profile](https://clawhub.ai/user/kklldog)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that change proxy, network, subscription, Web UI, Tun mode, or kernel settings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
