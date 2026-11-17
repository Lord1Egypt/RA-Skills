## Description:

Windows automation via the Clawdos API for screen capture, mouse and keyboard input, window management, file-system operations, and shell command execution from an agent-controlled Python CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danzig233](https://clawhub.ai/user/danzig233)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to control or inspect a Windows host from OpenClaw through a configured Clawdos service. It is suited for remote GUI automation, file operations inside the configured Windows root, and explicit shell-command workflows that require strong operator review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can provide full remote-control access to a Windows host, including shell execution and GUI input.

Mitigation: Install only when remote Windows control is intended, trust the Clawdos server, and require explicit review before shell or GUI actions are executed.

Risk: Non-local connections may use unsafe transport if HTTPS is not configured.

Mitigation: Use HTTPS for any non-local Clawdos connection and keep the API key narrowly scoped.

Risk: The advertised filesystem sandbox is not enforced by the client.

Mitigation: Ensure the server binds credentials to the intended filesystem root and do not rely on the client alone for filesystem isolation.

Risk: File deletion and file transfer actions can modify or expose host and agent data.

Mitigation: Confirm delete targets and transfer paths before use, and avoid uploading or downloading sensitive files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danzig233/skills/clawdos)
- [Publisher profile](https://clawhub.ai/user/danzig233)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save screenshots or binary file contents through explicit output paths; requires Clawdos service configuration and API-key environment variables.]

## Skill Version(s):

2.1.1 (source: server release metadata and OpenClaw frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
