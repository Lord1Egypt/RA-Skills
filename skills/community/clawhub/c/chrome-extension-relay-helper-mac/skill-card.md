## Description:

Attach the OpenClaw Browser Relay Chrome extension to a live tab so the browser tool (profile="chrome") works on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[i-am-rad](https://clawhub.ai/user/i-am-rad)

### License/Terms of Use:


## Use Case:

Developers and automation agents use this skill before workflows that need OpenClaw browser automation through a live Chrome session on macOS. It launches Chrome, attaches the OpenClaw Browser Relay extension, and returns a concise status string that downstream steps can act on.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can force-quit Chrome while browser work is in progress.

Mitigation: Save browser work before running the skill and run it at the start of browser automation workflows.

Risk: The helper rewrites settings in the default Chrome profile.

Mitigation: Use a dedicated Chrome profile for automation when possible and review profile changes before broad deployment.

Risk: Failure screenshots may capture visible screen contents.

Mitigation: Treat ~/.openclaw/media/relay-attach-fail.png as potentially sensitive and remove it when it is no longer needed.

## Reference(s):

- [Chrome Extension Relay Helper - Mac on ClawHub](https://clawhub.ai/i-am-rad/skills/chrome-extension-relay-helper-mac)
- [Publisher profile: i-am-rad](https://clawhub.ai/user/i-am-rad)
- [OpenClaw Browser Relay helper script](artifact/scripts/attach.sh)
- [Static launch page used by helper](https://info.cern.ch/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation with shell commands and status strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The attach script returns ALREADY_ATTACHED, ATTACHED, or FAILED with a reason.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
