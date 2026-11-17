## Description:

Provides an OpenClaw web interface for uploading, downloading, listing, deleting, and packaging files in a local workspace for agent-assisted file analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengwang86](https://clawhub.ai/user/chengwang86)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to move files into a local workspace through a browser UI so an agent can inspect documents, screenshots, logs, code, or installed skill packages. It is intended for local workspace file handling rather than cloud storage or public file sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates a persistent network-facing upload and download service.

Mitigation: Review before installing on shared, routed, or production machines; bind the service to localhost by default and expose it only through an explicitly approved network path.

Risk: Authentication can fail open when no gateway token is available.

Mitigation: Require authentication to be configured before startup and fail closed when no token or password is present.

Risk: Secrets are passed in URL query strings.

Mitigation: Use a dedicated service token and prefer header-based authentication so credentials are less likely to appear in browser history, logs, or referrers.

Risk: Uploads may be accepted without an enforced server-side size limit.

Mitigation: Set and enforce upload size limits before accepting request bodies.

Risk: Persistent startup may be enabled during installation.

Mitigation: Make persistent service installation an explicit opt-in and document how to disable or remove it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chengwang86/skills/file-transfer-thru-local-workspace)
- [ClawHub publisher profile](https://clawhub.ai/user/chengwang86)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with URLs, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The installed service also produces JSON API responses and downloaded files in the local workspace.]

## Skill Version(s):

3.1.1 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
