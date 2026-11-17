## Description:

Desktop Guardian gives OpenClaw agents macOS GUI automation through Hammerspoon, including window queries, app and browser-tab management, dialog handling, keypresses, and desktop policy monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[s3rous](https://clawhub.ai/user/s3rous)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to let an OpenClaw agent inspect and manage a macOS desktop, enforce configurable cleanup policies, and alert when human attention is needed for dialogs or policy violations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and configures an always-on macOS desktop controller that can close apps, close browser tabs, and dismiss dialogs automatically.

Mitigation: Install only when that level of desktop automation is intended, review policy.yaml before enabling it, and adjust cleanup.enabled, cleanup.apps.action, browser actions, and dialogs.auto_dismiss before use.

Risk: The installer may modify Hammerspoon configuration, set up LaunchAgent persistence, and install unpinned dependencies.

Mitigation: Inspect the installer before running it, consider running the monitor manually first, and disable or remove persistence if continuous monitoring is not required.

Risk: Accessibility permission gives Hammerspoon broad control over the macOS GUI.

Mitigation: Grant Accessibility only in trusted environments, use the documented kill switch to stop actions quickly, and keep hardcoded protected-app and dialog safeguards enabled.

Risk: Chrome DevTools Protocol support can expose browser tab control to same-user local processes when enabled on localhost:9222.

Mitigation: Enable Chrome remote debugging only when tab-level monitoring is required and keep it limited to the local user trust boundary.

## Reference(s):

- [macOS Permissions for Desktop Guardian](references/macos-permissions.md)
- [Desktop Guardian Policy Configuration Guide](references/policies.md)
- [Hammerspoon Setup Guide](references/hammerspoon-setup.md)
- [Hammerspoon](https://www.hammerspoon.org/)
- [Desktop Guardian on ClawHub](https://clawhub.ai/s3rous/skills/desktop-guardian)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration examples, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide installation of local macOS automation components and policy files.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
