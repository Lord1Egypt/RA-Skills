## Description:

Control Adobe desktop apps - Photoshop, Illustrator, Premiere, After Effects, InDesign, Audition - from the shell via Flue, without an MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sfkislev](https://clawhub.ai/user/sfkislev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to let an agent inspect live Adobe documents or projects and make bounded edits through Flue bridge commands under human direction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Flue install command uses an unpinned third-party package.

Mitigation: Review the Flue project first, prefer a pinned and verified version, and install in an isolated environment when possible.

Risk: The skill can control professional desktop applications and modify user documents or projects.

Mitigation: Approve only specific, reversible actions, prefer small inspectable steps, and avoid destructive changes unless explicitly requested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sfkislev/skills/adobe-flue)
- [Flue project](https://github.com/SFKislev/flue)
- [Flue on PyPI](https://pypi.org/project/flue)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown guidance with shell commands and app-specific scripts that return JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent actions depend on local Flue installation, supported desktop application state, and explicit user approval for setup or destructive changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
