## Description:

Guides an agent in setting up Blender MCP access for 3D modeling, scene inspection, rendering, and importing Poly Haven assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lusilong](https://clawhub.ai/user/lusilong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and 3D artists use this skill to configure an AI client to work with an open Blender session, inspect or render scenes, and find or import Poly Haven assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server's executable code was not included in this review, so installation requires trusting third-party code.

Mitigation: Verify the server before installation and pin a reviewed package version or Git commit in each client configuration.

Risk: Blender code execution runs with the user's account permissions, and untrusted project files may be unsafe to process.

Mitigation: Save project copies, use trusted scenes, and consider an isolated environment.

Risk: The Blender plugin socket has no authentication or encryption.

Mitigation: Keep port 9876 local and do not forward or expose it to a network.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/lusilong/skills/blender-mcp-plus)
- [Blender MCP plugin releases](https://projects.blender.org/lab/blender_mcp/releases)
- [Tool reference](artifact/references/tools.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Shell commands, Code]

**Output Format:** [Markdown with inline code and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task-oriented setup steps, tool-selection guidance, and safety notes.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
