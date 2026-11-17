## Description:

Connects an agent in OpenClaw to a local FreeCAD session through CADPilot for CAD modeling and geometry checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeszeles](https://clawhub.ai/user/joeszeles)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect OpenClaw to a local FreeCAD session, create or inspect parts, check geometry, and export solids through CADPilot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Launching an unpinned CADPilot package through uvx may execute a version you have not reviewed.

Mitigation: Verify uvx and CADPilot come from trusted sources and consider pinning a known-good CADPilot version.

Risk: Remote exposure of FreeCAD's control interface could let other systems access the CAD session.

Mitigation: Keep the FreeCAD RPC server bound to 127.0.0.1 and the MCP connection on local stdio.

## Reference(s):

- [FreeCAD CADPilot release](https://clawhub.ai/joeszeles/skills/freecad-cadpilot)
- [CADPilot dependency](https://github.com/LBurny/cadpilot)
- [FreeCAD](https://www.freecad.org/)
- [uv tool documentation](https://docs.astral.sh/uv/guides/tools/)
- [OpenClaw](https://openclaw.ai/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and modeling results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report FreeCAD document or object names, geometry results, or errors; modeling requests can change the local FreeCAD session.]

## Skill Version(s):

1.0.1 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
