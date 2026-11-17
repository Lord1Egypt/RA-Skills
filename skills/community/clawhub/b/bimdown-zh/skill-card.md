## Description:

BimDown 中文 guides agents through creating, editing, validating, rendering, querying, and optionally publishing BimDown BIM projects using CSV/SVG files and the bimdown CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[novashang](https://clawhub.ai/user/novashang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and BIM practitioners use this skill to have an agent create BimDown projects, model buildings from briefs or drawings, run quantity and model checks, and produce validated BIM data and previews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for an unpinned global npm install of bimdown-cli.

Mitigation: Install only after explicit user approval, and prefer a pinned local or sandboxed installation.

Risk: The skill includes a direct ZIP download-and-unzip workflow for shared projects.

Mitigation: Review downloaded archive contents before extraction and unpack into an isolated project directory.

Risk: Publishing sends project names, geometry, rooms, materials, notes, CSV/SVG, GLB files, and metadata to a public sharing service.

Mitigation: Treat publish links as public, check for sensitive project data, and obtain explicit user authorization before the first publish.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/novashang/skills/bimdown-zh)
- [BIM Modeling SOP](references/bim-modeling.md)
- [Building Design SOP](references/building-design.md)
- [BimDown project repository](https://github.com/NovaShang/BimDown)
- [BimClaw publish API endpoint](https://bim-claw.com/api/shares/publish)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated BimDown CSV/SVG project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the bimdown CLI; optional publishing uploads project archives to BimClaw only after user authorization.]

## Skill Version(s):

1.4.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
