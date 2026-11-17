## Description:

Programmatically controls Claude Code in visible macOS Terminal windows for command input, screenshots, session logging, and terminal management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melichar-m](https://clawhub.ai/user/melichar-m)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to launch Claude Code in a visible macOS Terminal session, send work requests, capture screenshots, and save session records for review or automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Terminal screenshots and saved session recordings can contain sensitive project, credential, or conversation data.

Mitigation: Store recordings and screenshots in protected locations, review them before sharing, and delete them when no longer needed.

Risk: Accessibility-driven Terminal control can approve trust prompts and send commands in a user's visible environment.

Mitigation: Use only on trusted project folders, verify the displayed prompt and path before approval, and grant the minimum macOS permissions required.

Risk: The security evidence reports shell and AppleScript interpolation risks for untrusted paths, task text, or screenshot locations.

Mitigation: Avoid untrusted inputs until the package escapes or isolates those values, and review generated commands before execution.

## Reference(s):

- [Claude Code Control on ClawHub](https://clawhub.ai/melichar-m/skills/claude-code-control)
- [melichar-m publisher profile](https://clawhub.ai/user/melichar-m)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Node.js API results with screenshot paths, JSON session recordings, and terminal-driven command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, Node.js 18 or newer, Claude Code authentication, and Accessibility permission for Terminal control.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
