## Description:

Guides agents through installing, configuring, and troubleshooting the OpenClaw DingTalk connector for DingTalk bot messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chao980](https://clawhub.ai/user/chao980)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect OpenClaw to a DingTalk enterprise bot, configure AppKey and AppSecret credentials, and troubleshoot message delivery, authentication, version, stream connection, and port issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow asks users to install mutable external connector code.

Mitigation: Pin and verify the DingTalk connector and OpenClaw versions where possible before installation.

Risk: The setup flow stores DingTalk AppSecret credentials in a local OpenClaw configuration file.

Mitigation: Restrict ~/.openclaw/openclaw.json to the owning user, keep it out of repositories and support bundles, and rotate the AppSecret if exposure is suspected.

Risk: Global npm installation can broaden host-level impact if run with elevated privileges.

Mitigation: Avoid running global npm installs with elevated privileges unless the environment requires it and the package source has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chao980/skills/dingtalk-link-smb)
- [DingTalk OpenClaw connector documentation](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector)
- [DingTalk Open Platform](https://open-dev.dingtalk.com/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
