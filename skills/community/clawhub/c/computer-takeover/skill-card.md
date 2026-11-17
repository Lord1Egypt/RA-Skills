## Description:

Guides an agent through unattended remote administration of paired OpenClaw nodes, including screen capture, camera access, shell execution, file, app, notification, location, process, and pairing operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and authorized device administrators use this skill to manage paired devices they own or are formally authorized to administer. It supports node discovery, device status checks, approved screen or camera capture, shell execution, and file, app, notification, location, and process management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables unattended control of screen, camera, notifications, location, shell, files, apps, and processes on paired devices.

Mitigation: Use it only on devices the operator owns or is formally authorized to administer, with explicit consent and visible approval for each sensitive capability.

Risk: Remote shell, file transfer, app install or uninstall, process termination, and service or registry changes can alter or damage a device.

Mitigation: Confirm the target node before action, scope commands to the approved task, avoid broad file browsing or destructive operations, and keep gateway access strongly authenticated and auditable.

Risk: Screen, camera, notification, and location access could be misused for covert monitoring or credential exposure.

Mitigation: Do not use the skill for covert monitoring, credential access, or collection beyond the approved administrative purpose.

## Reference(s):

- [Shell Command Reference by OS](references/shell-commands.md)
- [ClawHub skill page](https://clawhub.ai/fuzzyb33s/skills/computer-takeover)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline command and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OS-specific command examples and node-management guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
