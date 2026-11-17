## Description:

Control and manage Deepin desktop settings including power, display, Bluetooth, airplane mode, user accounts, and time via D-Bus system services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaneniu](https://clawhub.ai/user/zaneniu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system administrators use this skill to inspect and operate Deepin/UOS desktop control modules through D-Bus commands for power, display, Bluetooth, networking, accounts, time, boot, package, and security settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad Deepin/UOS system changes, including privileged account, bootloader, package, time, network, and security actions.

Mitigation: Require explicit approval before executing mutating commands, especially commands affecting accounts, boot settings, packages, time, network, or security configuration.

Risk: The bundled evidence includes local account metadata.

Mitigation: Redact local account metadata or replace it with sanitized examples before broad distribution.

Risk: The introspection helper uses a hardcoded local output path.

Mitigation: Replace the hardcoded path with a caller-selected or package-relative output path before reuse.

## Reference(s):

- [Deepin Desktop Control ClawHub page](https://clawhub.ai/zaneniu/skills/deepin-desktop)
- [Bundled skill guide](artifact/SKILL.md)
- [Bundled D-Bus introspection references](artifact/references/)
- [Introspection helper script](artifact/scripts/introspect.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may target system or session D-Bus services and should be reviewed before execution.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
