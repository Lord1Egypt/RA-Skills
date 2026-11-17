## Description:

ClawMobile helps agents configure and drive Android automation workflows through AutoX.js, including workflow execution, task recording, API calls, and membership-aware feature checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miyan1221](https://clawhub.ai/user/miyan1221)

### License/Terms of Use:

MIT

## Use Case:

Developers, QA engineers, and RPA operators use this skill to automate Android app interactions, record repeatable workflows, and invoke an AutoX.js HTTP API from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The device-control API uses weak public defaults and may be exposed broadly on port 8765.

Mitigation: Replace the default token, bind the service to localhost where possible, and avoid exposing port 8765 beyond localhost or an encrypted tunnel.

Risk: Remote access over plaintext HTTP can expose automation commands and device state.

Mitigation: Do not use plaintext HTTP for remote access; use a protected local connection or encrypted tunnel.

Risk: Recording screenshots and UI trees may capture sensitive app or user data.

Mitigation: Use recording only on Android devices and apps you control, review captured artifacts, and avoid recording sensitive screens.

Risk: Android automation can execute unintended interactions if workflows are wrong or run against the wrong app or device.

Mitigation: Review workflows before installation and execution, confirm the target device and app, and run validation checks before deployment.

## Reference(s):

- [ClawMobile ClawHub release](https://clawhub.ai/miyan1221/skills/clawmobile)
- [Publisher profile](https://clawhub.ai/user/miyan1221)
- [ClawMobile documentation](https://docs.clawmobile.com)
- [AutoX.js documentation](https://autoxjs.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, shell, JSON, and YAML snippets; may also propose API calls and task definitions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on local Android device state, AutoX.js availability, ADB connectivity, and configured API credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, CHANGELOG, README, and skill module)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
