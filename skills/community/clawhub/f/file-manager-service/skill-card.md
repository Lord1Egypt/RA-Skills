## Description:

File Manager Service starts and controls a local file-management service for browsing, editing, uploading, downloading, searching, moving, deleting, and annotating files in an OpenClaw projects directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lengyhua](https://clawhub.ai/user/lengyhua)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to start a local web interface and CLI for managing files under ~/.openclaw/workspace/projects. It supports day-to-day project file browsing, editing, search, upload, download, directory notes, and service status operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated file-management endpoints can read, write, upload, move, and delete project files.

Mitigation: Run only in a trusted local environment and avoid shared or exposed networks until authentication and CSRF protection are added.

Risk: The web service is reported to bind to all network interfaces.

Mitigation: Bind the service to localhost before use on shared, VPN, container, or otherwise reachable networks.

Risk: Security evidence reports upload path validation and web UI XSS issues.

Mitigation: Fix path validation and sanitize rendered user-controlled content before using the service with untrusted files or notes.

Risk: Dependency installation is documented with unpinned Flask and requests packages.

Mitigation: Pin, vendor, or otherwise review dependencies before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lengyhua/skills/file-manager-service)
- [Publisher Profile](https://clawhub.ai/user/lengyhua)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, endpoint descriptions, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start or stop a background local web service and may perform file read, write, upload, download, move, and delete operations through CLI or HTTP endpoints.]

## Skill Version(s):

1.1.3 (source: server release metadata, package.json, README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
