## Description:

Configures OpenClaw-CN browser modes for openclaw or chrome profiles and helps troubleshoot browser connection issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yishanjiu-3386](https://clawhub.ai/user/yishanjiu-3386)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw-CN users use this skill to configure openclaw or chrome browser profiles, restart the gateway, start browser sessions, and troubleshoot browser connection failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested edits can change OpenClaw-CN browser configuration and affect browser startup behavior.

Mitigation: Review proposed openclaw.json changes before applying them and keep a copy of the last working configuration.

Risk: Chrome mode can rely on an existing Chrome login session.

Mitigation: Confirm that sharing the current Chrome session is intended, or use openclaw mode for a more isolated browser profile.

Risk: Frequent switching between browser modes may disrupt saved login state.

Mitigation: Choose one browser profile for routine use and avoid unnecessary mode changes after login.

## Reference(s):

- [Browser Config on ClawHub](https://clawhub.ai/yishanjiu-3386/skills/browser-config)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the openclaw-cn binary; chrome mode may rely on an existing Chrome login session.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
