## Description:

Android phone automation skill that supports Node Gateway and direct HTTP connections for tapping, swiping, text input, screenshots, layout retrieval, app launching, and device data access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[klscool](https://clawhub.ai/user/klscool)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect an Android 10+ phone running the ClawPaw App to an agent workflow and automate common phone operations. It is suited for remote device interaction, UI automation, screen inspection, app launching, and permission-gated access to phone data such as notifications, contacts, photos, location, SMS, calls, calendar, and files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can remotely control Android UI actions and access sensitive phone capabilities over Gateway or HTTP paths.

Mitigation: Install only when the ClawPaw app and network path are trusted; prefer Gateway or a protected tunnel instead of direct WiFi HTTP.

Risk: Optional permissions can expose contacts, photos, SMS, calls, location, notifications, files, calendar entries, and screen contents.

Mitigation: Grant only the Android permissions needed for the current task and require explicit user confirmation before sensitive reads, uploads, messages, calls, purchases, or notification actions.

Risk: Vision analysis may process screenshots or layout data from sensitive screens.

Mitigation: Keep vision analysis disabled unless needed, avoid using it on sensitive screens, and use options that avoid saving screenshots or sending layout data when possible.

## Reference(s):

- [ClawPaw App](https://github.com/klscool/ClawPaw)
- [ClawPaw App Releases](https://github.com/klscool/ClawPaw/releases)
- [OpenClaw Docs](https://docs.openclaw.ai)
- [Operation Guide Index](references/INDEX.md)
- [Supported Apps List](references/apps/app-list.md)
- [Basic Integration Example](references/guides/basic-example.md)
- [Permissions Guide](README_PERMISSIONS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON parameters, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return device status, screenshots, layout XML, Base64 image data, permission-gated phone data, and command results through the configured Gateway or HTTP path.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
