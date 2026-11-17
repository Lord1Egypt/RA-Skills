## Description:

Guides agents through ClawPaw Android setup and phone control, including APK installation, permission grants, SSH tunnel and ADB verification, MCP configuration, and step-by-step phone interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzliu888](https://clawhub.ai/user/wzliu888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and end users use this skill to set up ClawPaw for Android and let an agent perform phone workflows such as opening apps, tapping controls, typing text, taking screenshots, checking device state, and troubleshooting connectivity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad remote control over an Android phone, including screen interaction, location, notifications, camera, microphone, keyboard input, and real-world app actions.

Mitigation: Install and run it only for intended phone-control workflows, review proposed actions before execution, and disable TCP ADB or remote access when finished.

Risk: Credentials such as the ClawPaw UID and secret are used in shell commands and configuration and could be exposed through shell history or local config files.

Mitigation: Avoid placing secrets directly in shell history, restrict access to local configuration, rotate exposed secrets, and review credential handling before deployment.

Risk: The security evidence flags insecure curl usage and recommends reviewing backend trust before use.

Mitigation: Remove curl -k/--insecure usage, verify TLS behavior, and review the ClawPaw backend trust model before relying on the workflow.

## Reference(s):

- [ClawPaw Phone Control on ClawHub](https://clawhub.ai/wzliu888/skills/clawpaw-phone-control)
- [ClawPaw Service](https://www.clawpaw.me)
- [ADBKeyboard Releases](https://github.com/nicso/ADBKeyboard/releases)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, API calls]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, and step-by-step phone-control actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or request review of screenshots, phone state, location, notification summaries, and other device-derived information during workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
