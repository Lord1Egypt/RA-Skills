## Description:

A macOS platform guide for the agent-desktop CLI covering permissions, headed interactions, accessibility surfaces, notifications, Chromium and Electron apps, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lahfir](https://clawhub.ai/user/lahfir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this guide alongside the core agent-desktop skill to configure macOS permissions, automate desktop interfaces, and troubleshoot platform-specific behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Accessibility permission lets the launching app read and control desktop interfaces.

Mitigation: Grant it only to a trusted launcher and revoke it when automation is no longer needed.

Risk: The external agent-desktop runtime was not included in the documentation scan.

Mitigation: Assess the installed runtime separately before granting it desktop permissions.

Risk: Screenshot features require Screen Recording permission.

Mitigation: Enable Screen Recording only when using screenshots or screenshot session artifacts.

## Reference(s):

- [macOS troubleshooting](references/troubleshooting.md)
- [ClawHub release page](https://clawhub.ai/lahfir/skills/agent-desktop-macos)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
