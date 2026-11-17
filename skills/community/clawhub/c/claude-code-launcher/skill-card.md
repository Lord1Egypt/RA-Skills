## Description:

Launches Claude Code in a new Terminal window with Remote Control enabled, including project navigation, startup, activation, screenshots, and error recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qusaiisaleem](https://clawhub.ai/user/qusaiisaleem)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to start Claude Code sessions for a chosen project and enable Remote Control so the session can be accessed from another device.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote Control activation can expose a Claude Code session URL or QR code.

Mitigation: Use the skill only in trusted environments and share the session details only with intended devices or users.

Risk: The skill requires macOS screen and input automation permissions.

Mitigation: Grant Screen Recording and Accessibility permissions only after verifying the Peekaboo and Claude CLI installations.

Risk: Screenshots and launch logs are retained locally.

Mitigation: Review and clear stored screenshots and logs after use, especially when working in sensitive projects.

Risk: Terminal command construction around project paths can be unsafe for unusual directory names.

Mitigation: Run the skill only on trusted project paths and avoid paths with unusual shell characters.

## Reference(s):

- [Troubleshooting Claude Code Launcher](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/qusaiisaleem/skills/claude-code-launcher)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Text status messages with shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a locally stored screenshot path and Remote Control access details when activation succeeds.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
