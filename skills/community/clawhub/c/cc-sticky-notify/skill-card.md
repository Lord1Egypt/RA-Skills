## Description:

Installs, configures, and troubleshoots cc-sticky-notify, a macOS notification skill that shows persistent sticky-note and system notifications for Claude Code completion, permission, idle, and failed-command events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bucleliu](https://clawhub.ai/user/bucleliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install or repair local macOS Claude Code notification hooks so important completion, approval, idle, and command-failure events remain visible while they work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill adds persistent Claude Code hook execution for local notification events.

Mitigation: Review the exact settings.json hook entries before installation and remove or disable hooks that are not needed.

Risk: The notification behavior can inspect local macOS GUI context to identify and restore the source application or window.

Mitigation: Install only where that local GUI context access is acceptable, and consider disabling focus-restoration or window-inspection behavior if it is not required.

Risk: The skill stores notification state under /tmp, which the security guidance flags as unsafe temporary state handling.

Mitigation: Avoid installing on shared machines until the temporary state handling is hardened.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bucleliu/skills/cc-sticky-notify)
- [Publisher profile](https://clawhub.ai/user/bucleliu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON hook snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent output may include install, verification, and troubleshooting steps for local macOS Claude Code hook configuration.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
