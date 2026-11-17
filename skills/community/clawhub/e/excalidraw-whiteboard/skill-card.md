## Description:

Start, reopen, read, and edit local Excalidraw whiteboards with the user during project design discussions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimjeffers](https://clawhub.ai/user/jimjeffers)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers collaborate with users on local, editable system diagrams and project whiteboards, then export the finished scenes and previews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation downloads and builds a pinned community runtime.

Mitigation: Review and trust the runtime and dependencies before running setup.

Risk: Active board servers have no authentication.

Mitigation: Keep servers bound to loopback and do not expose or forward their ports.

Risk: Board content remains on local disk across sessions.

Mitigation: Avoid secrets on shared boards unless local persistence is acceptable.

Risk: Simultaneous browser and agent edits can conflict.

Mitigation: Coordinate editing turns and save a snapshot before substantial changes.

## Reference(s):

- [Whiteboard on ClawHub](https://clawhub.ai/jimjeffers/skills/excalidraw-whiteboard)
- [Skill homepage](https://github.com/jimjeffers/excalidraw-whiteboard-skill)
- [Community Excalidraw runtime](https://github.com/yctimlin/mcp_excalidraw)
- [Drawing commands](references/drawing.md)
- [Session operations](references/operations.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Markdown chat guidance and exported .excalidraw scenes with PNG previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Editable local boards persist across sessions; exports are explicit copies.]

## Skill Version(s):

0.1.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
