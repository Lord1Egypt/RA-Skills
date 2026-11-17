## Description:

Turn product photos into textured GLB models with Easyrender's MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jorgerl02](https://clawhub.ai/user/jorgerl02)

### License/Terms of Use:

MIT

## Use Case:

External users can preview product photos as textured 3D models, approve credit-based builds, and resume renders while tracking a catalogue within a shared budget.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may not expect product photos to be sent to Easyrender for processing.

Mitigation: Explain the external upload before sending and use only photos the user provided or authorized.

Risk: The security assessment is incomplete because one local reference could not be resolved.

Mitigation: Resolve and review that reference before relying on the scan.

## Reference(s):

- [MCP contract and operational details](references/mcp.md)
- [Example workflows](references/workflows.md)
- [ClawHub skill page](https://clawhub.ai/jorgerl02/skills/easyrender-image-to-3d)

## Skill Output:

**Output Type(s):** [3D model files, Text]

**Output Format:** [GLB model plus a concise status and delivery summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Geometry is approximate; not dimensionally accurate CAD, room reconstruction, or photogrammetry.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
