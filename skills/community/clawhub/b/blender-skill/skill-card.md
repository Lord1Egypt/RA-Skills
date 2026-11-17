## Description:

Connect an agent to a running Blender instance through Blender MCP to inspect scenes, render images, search documentation, or run Blender Python code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taosiuman](https://clawhub.ai/user/taosiuman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Blender users use this skill to connect an agent to Blender for scene inspection, viewport screenshots, rendering, documentation lookup, and Python-based scene operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unpinned `uvx quick` reference flagged by ClawScan can make the resolved package version less predictable, and some local path-like references were not resolved during scanning.

Mitigation: Use an explicitly version-pinned package command and check referenced local files before following their instructions.

Risk: The Blender MCP code execution tool can run arbitrary Python through `bpy`, including operations that read, modify, or delete files and make network requests; this can also alter Blender project data.

Mitigation: Keep the server bound to localhost, review code before execution, prefer scoped tools where suitable, and back up important `.blend` files.

## Reference(s):

- [Blender MCP product page](https://www.blender.org/lab/mcp-server/)
- [Blender platform requirements](https://www.blender.org/download/requirements/)
- [Blender MCP tools](artifact/references/tools.md)
- [Blender MCP communication protocol](artifact/references/protocol.md)
- [Blender API compatibility notes](artifact/references/api.md)
- [Blender MCP troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Python code, Shell commands, Configuration instructions, Images]

**Output Format:** [Markdown guidance with Python, shell, JSON, and configuration examples; Blender tool results may be text, JSON, screenshots, or rendered image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Blender scene and the requested tool; render tools write image files to a path.]

## Skill Version(s):

3.7.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
