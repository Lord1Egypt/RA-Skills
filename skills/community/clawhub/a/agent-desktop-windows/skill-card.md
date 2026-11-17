## Description:

Guides agents using the agent-desktop CLI through Windows desktop automation capabilities, limitations, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lahfir](https://clawhub.ai/user/lahfir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this guide to automate Windows applications with agent-desktop, select supported desktop actions, and troubleshoot accessibility and permission boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notification, clipboard, screenshot, and UI tree output can expose sensitive information.

Mitigation: Treat captured desktop content as sensitive and limit its disclosure.

Risk: Headed actions can take the foreground and interact with the user's desktop.

Mitigation: Use headed actions only when foreground interaction is intended.

Risk: The cursor overlay may affect other users of a shared account or people sensitive to motion.

Mitigation: Leave the cursor overlay disabled in those environments.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lahfir/skills/agent-desktop-windows)
- [Chromium and Electron trees](artifact/references/chromium-and-electron.md)
- [Permissions and elevation](artifact/references/permissions-and-elevation.md)
- [Shell surfaces, notifications and cursor overlay](artifact/references/shell-and-overlay.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-specific agent-desktop guidance]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; skill frontmatter says 0.8.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
