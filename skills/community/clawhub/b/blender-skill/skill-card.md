## Description:

Connects an agent to Blender through MCP and guides a spec-driven art production workflow from scene work and modeling through export and quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taosiuman](https://clawhub.ai/user/taosiuman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and 3D artists use this skill to inspect and control Blender scenes, create production assets, prepare game-engine exports, and run asset quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Code run through Blender's MCP interface can execute Python with access to files and network resources, and can alter Blender project data.

Mitigation: Review code before execution, prefer scoped built-in tools where practical, and keep backups of important .blend files.

Risk: The release security assessment notes an unpinned tool reference and incomplete analysis.

Mitigation: Check the referenced tool's source and version before installation, and do not treat the assessment as a guarantee of safety.

## Reference(s):

- [Blender Lab MCP Server](https://www.blender.org/lab/mcp-server/)
- [Blender Lab MCP add-on release v1.0.3](https://projects.blender.org/lab/blender_mcp/releases/download/v1.0.3/mcp-1.0.3.zip)
- [Blender system requirements](https://www.blender.org/download/requirements/)
- [Blender Python API notes](artifact/references/api.md)
- [Art production pipeline](artifact/references/art-pipeline.md)
- [Asset quality checks](artifact/references/art-qa.md)
- [Export and optimization guidance](artifact/references/art-optimize-export.md)
- [Source material noted for art production guidance](https://github.com/arjun988/blender-skills)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance, Python code, shell commands, configuration snippets, and Blender project or export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions through Blender may change scene data or files; review code before execution and back up important projects.]

## Skill Version(s):

4.0.0 (source: SKILL.md frontmatter, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
