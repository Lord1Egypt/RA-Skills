## Description:

Set up feelgoodbot file integrity monitoring and TOTP step-up authentication for macOS agents that need malware detection, tamper monitoring, security alerts, or OTP checks before sensitive actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kris-hansen](https://clawhub.ai/user/kris-hansen)

### License/Terms of Use:


## Use Case:

Developers and security-conscious agent operators use this skill to install and configure feelgoodbot on macOS for file integrity monitoring and TOTP step-up checks before sensitive agent actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path installs mutable remote code as a persistent daemon.

Mitigation: Review before installing, pin or verify the feelgoodbot version, and inspect the upstream project before running the setup script.

Risk: The setup path changes Clawdbot webhook configuration and enables local integration behavior.

Mitigation: Only enable Clawdbot hooks when this local integration is intended and trusted, and keep the generated hook token private.

Risk: Configuration files may contain sensitive local security state and webhook secrets.

Mitigation: Ensure the feelgoodbot configuration directory and config.yaml are private to the current user.

Risk: Step-up authentication does not protect actions until TOTP is enrolled and verified.

Mitigation: After setup, enroll and verify TOTP separately before relying on step-up protection for sensitive actions.

## Reference(s):

- [Feelgoodbot GitHub repository](https://github.com/kris-hansen/feelgoodbot)
- [ClawHub Feelgoodbot release page](https://clawhub.ai/kris-hansen/skills/feelgoodbot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes macOS setup steps, daemon commands, Clawdbot webhook configuration, and TOTP action checks.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
