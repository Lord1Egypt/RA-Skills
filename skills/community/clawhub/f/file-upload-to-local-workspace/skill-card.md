## Description:

File Upload to Local Workspace provides a web interface and agent guidance for uploading files into a local OpenClaw workspace for AI analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengwang86](https://clawhub.ai/user/chengwang86)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to run a local upload service, give users upload instructions, and manage uploaded files for later agent analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The upload service can be persistent and network-accessible with weak or absent authentication in common configurations.

Mitigation: Require authentication to fail closed, bind to localhost by default, and make any network exposure an explicit user choice.

Risk: Gateway credentials may be reused in URLs.

Mitigation: Avoid placing reusable tokens or passwords in query strings; prefer short-lived credentials or header-based authentication.

Risk: The service includes endpoints that can list and export installed skills.

Mitigation: Remove or disable skill export endpoints unless they are clearly disclosed, authenticated, and limited to trusted administrators.

Risk: Uploaded content can consume local storage or contain unexpected file types.

Mitigation: Enforce upload size limits, restrict accepted file types where practical, and store uploads in a constrained directory.

Risk: Service installation and removal can leave a persistent process or system service running.

Mitigation: Make service installation, startup, shutdown, and removal steps explicit and verify they complete reliably.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chengwang86/skills/file-upload-to-local-workspace)
- [AI reply guide](artifact/docs/AI-REPLY-GUIDE.md)
- [Authentication compatibility guide](artifact/docs/AUTH-COMPATIBILITY.md)
- [Security audit](artifact/SECURITY-AUDIT.md)
- [Declared repository metadata](https://github.com/openclaw/openclaw.git)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline URLs, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe local service URLs, authentication placeholders, upload paths, and troubleshooting commands.]

## Skill Version(s):

3.0.1 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
