## Description:

Helps users set up and troubleshoot an OpenClaw DingTalk enterprise internal bot channel with plugin installation, Stream mode configuration, gateway restart, and message-delivery checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaoyunhao0107](https://clawhub.ai/user/shaoyunhao0107)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect OpenClaw to DingTalk enterprise internal bots, configure required DingTalk credentials, validate gateway status, and troubleshoot plugin or messaging failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup asks users to install an unpinned third-party DingTalk plugin.

Mitigation: Review the plugin source and install a pinned, trusted version where possible.

Risk: DingTalk Client Secret values may be exposed through command-line use or local OpenClaw configuration.

Mitigation: Avoid passing secrets on the command line, restrict permissions on ~/.openclaw/openclaw.json, and rotate any example-looking secret if it was ever real.

Risk: The optional automation path modifies OpenClaw configuration and restarts the gateway.

Mitigation: Back up the OpenClaw configuration before running automation and review the resulting channel settings before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shaoyunhao0107/skills/dingtalk-setup)
- [DingTalk Plugin Repository](https://github.com/soimy/openclaw-channel-dingtalk)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [DingTalk Open Platform](https://open.dingtalk.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands and JSON or PowerShell configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes manual setup steps, optional automation guidance, verification checks, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
