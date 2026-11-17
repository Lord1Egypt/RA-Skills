## Description:

Control Assimilate Live FX / SCRATCH — professional color grading, compositing, and virtual production software — via MCP. 88 tools across 14 categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ergopooka](https://clawhub.ai/user/ergopooka)

### License/Terms of Use:


## Use Case:

Developers and media-production operators use this skill to connect an AI assistant to Assimilate Live FX or SCRATCH through MCP for project navigation, media import, color grading, playback, rendering, output setup, snapshots, and file-management workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an unpinned npm MCP server.

Mitigation: Pin assimilate-mcp to a reviewed version where possible and review the package before production installation.

Risk: The skill can perform high-impact Assimilate operations such as importing media, changing grades, configuring outputs, and starting renders.

Mitigation: Run with least privilege and require explicit confirmation before edit, output, import, or render actions.

Risk: The skill may use ASSIMILATE_KEY to authorize access to the target Live FX or SCRATCH server.

Mitigation: Protect ASSIMILATE_KEY as a secret and avoid exposing it in shared configuration or logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ergopooka/skills/assimilate-mcp)
- [GitHub Repository](https://github.com/amac-roguelabs/assimilate-mcp)
- [npm Package](https://www.npmjs.com/package/assimilate-mcp)
- [Assimilate REST API](https://github.com/Assimilate-Inc/Assimilate-REST)
- [Assimilate Inc](https://assimilateinc.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include MCP server configuration and natural-language guidance for invoking Assimilate MCP tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
