## Description:

Control Blender from the shell via Flue - a Python bridge to bpy without an MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sfkislev](https://clawhub.ai/user/sfkislev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative technical users use this skill to let an agent inspect Blender scenes, run bounded bpy scripts, and make small user-directed edits through the local Flue bridge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release uses an external Flue package and setup command that should be reviewed before installation.

Mitigation: Inspect the Flue project, pin or verify the package version where practical, and require explicit user approval before running installation or setup commands.

Risk: Generated scripts can modify professional desktop software state.

Mitigation: Run with normal user privileges, keep edits small and inspectable, and only execute scripts that match the requested Blender task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sfkislev/skills/blender-flue)
- [Flue project](https://github.com/SFKislev/flue)
- [Flue on PyPI](https://pypi.org/project/flue)
- [FLUE.md](artifact/FLUE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides user-approved Blender automation and expects JSON results from the Flue bridge when commands are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
