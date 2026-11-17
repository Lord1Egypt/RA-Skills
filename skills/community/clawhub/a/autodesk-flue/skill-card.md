## Description:

Control Autodesk desktop apps - 3ds Max and friends - from the shell via Flue, without an MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sfkislev](https://clawhub.ai/user/sfkislev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical artists use this skill to let an agent inspect live Autodesk 3ds Max scenes, run small scripts, and make bounded edits through Flue while the human remains the driver.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on installing and setting up an unpinned external Flue package that can add files and desktop application integrations.

Mitigation: Review the package and source before installing, prefer a pinned version or isolated environment, and approve setup only after understanding the added integrations.

Risk: The skill can execute scripts inside professional desktop applications and may alter active scenes or documents.

Mitigation: Use small, inspectable steps, inspect the live application state first, and require explicit user approval before destructive or broad edits.

Risk: Operational behavior depends on local Flue documentation and adapters that may differ from the release artifact.

Mitigation: Treat installed Flue documentation as operational reference only after installation is approved, and keep actions scoped to the specific app and document requested by the user.

## Reference(s):

- [Flue GitHub repository](https://github.com/SFKislev/flue)
- [Flue PyPI package](https://pypi.org/project/flue)
- [ClawHub skill page](https://clawhub.ai/sfkislev/skills/autodesk-flue)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and app-specific script examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON-oriented bridge commands for inspecting or changing live desktop application state.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
