## Description:

Claw Use lets AI agents read and control authorized physical devices over HTTP using a unified cu CLI for perception, input, navigation, app launch, and audio output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[4ier](https://clawhub.ai/user/4ier)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to connect an agent to authorized devices for UI inspection, input actions, screenshots, notifications, app navigation, and multi-device control through the Claw Use protocol.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote device control can expose private data or perform unintended actions on a real device.

Mitigation: Use only owned or authorized devices, review commands before execution, and require explicit confirmation before screenshots, notification reads, message typing, credential flows, payment flows, or unlocking.

Risk: Network-exposed control endpoints and tokens can allow unauthorized device access.

Mitigation: Keep endpoints off public networks, prefer private network access such as Tailscale, and protect and rotate tokens.

Risk: Automatic unlock behavior can bypass expected user review before sensitive device actions.

Mitigation: Disable or gate unlock flows unless the user explicitly approves the operation and the target device is authorized.

## Reference(s):

- [Claw Use skill page](https://clawhub.ai/4ier/skills/claw-use)
- [Claw Use Android API details](https://github.com/4ier/claw-use-android#api-details)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that interact with real devices and private on-device data; user authorization and review are required before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
