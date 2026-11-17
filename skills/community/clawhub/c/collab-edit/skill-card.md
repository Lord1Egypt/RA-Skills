## Description:

Enable real-time collaboration by exposing a local collaborative editing tool via aitun tunnel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctz168](https://clawhub.ai/user/ctz168)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and AI agents use this skill to start a shared browser-based editor, notepad, document workspace, or whiteboard so a user and agent can collaborate in real time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote installer commands can execute code that has not been reviewed in the current workspace.

Mitigation: Avoid one-line remote installers and use pinned, verified packages where possible before running the collaboration tool.

Risk: A public tunnel can expose an unauthenticated browser editor to anyone with the shared URL.

Mitigation: Require authentication on shared editors, bind local services to 127.0.0.1 unless broader access is required, and close the tunnel when the session ends.

Risk: A shared editing workspace can expose sensitive local files or project content.

Mitigation: Restrict the shared workspace to non-sensitive files and treat the public tunnel URL as a secret.

## Reference(s):

- [AiTun homepage](https://aitun.cc)
- [ClawHub skill page](https://clawhub.ai/ctz168/skills/collab-edit)
- [ClawHub listing](https://clawhub.ai/ctz168/collab-edit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and collaboration links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public tunnel URLs and process cleanup commands for the active collaboration session.]

## Skill Version(s):

1.0.6 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
