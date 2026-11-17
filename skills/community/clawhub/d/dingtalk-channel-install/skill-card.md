## Description:

Installs and configures the OpenClaw DingTalk channel, including the @soimy/dingtalk plugin, DingTalk client credentials, and robot connection setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[k55k32](https://clawhub.ai/user/k55k32)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect OpenClaw to DingTalk for two-way messaging by installing the DingTalk channel plugin and updating OpenClaw channel configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default DingTalk configuration allows all sources and opens both direct-message and group policies.

Mitigation: Use an explicit DingTalk allowlist and restrict direct-message and group policies to the minimum needed audience.

Risk: The installation flow installs @soimy/dingtalk without a pinned version.

Mitigation: Pin the @soimy/dingtalk plugin version and review changes before upgrading.

Risk: DingTalk client secrets may be exposed through command-line entry or broadly readable OpenClaw configuration files.

Mitigation: Protect the OpenClaw config file, avoid exposing secrets in shell history, and rotate the DingTalk client secret if it may have been exposed.

## Reference(s):

- [DingTalk Open Platform](https://open.dingtalk.com/)
- [OpenClaw DingTalk Channel Documentation](https://github.com/soimy/openclaw-channel-dingtalk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and a Python installation script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes required DingTalk Client ID and Client Secret inputs plus optional robot, enterprise, card template, message type, restart, and config path settings.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
