## Description:

A bridge between AI and building data. Read & create BIM exactly like writing code. Execute architectural design, or just model your own house!

This skill is ready for commercial/non-commercial use.

## Publisher:

[novashang](https://clawhub.ai/user/novashang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, architects, engineers, and external agents use this skill to create, inspect, validate, render, and share BimDown BIM projects from design briefs or existing plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the bimdown-cli package and may require installation before use.

Mitigation: Use a pinned or project-local bimdown-cli install when stronger supply-chain control is required, and confirm the binary before invoking BimDown workflows.

Risk: The optional publish flow uploads BIM project files and returns a public-by-link share URL.

Mitigation: Publish only with explicit user consent and only when project files, geometry, room names, materials, notes, and GLB meshes can be shared publicly by link.

## Reference(s):

- [BIM Modeling SOP](artifact/references/bim-modeling.md)
- [Building Design SOP](artifact/references/building-design.md)
- [BimDown GitHub repository](https://github.com/NovaShang/BimDown)
- [BimClaw publish API endpoint](https://bim-claw.com/api/shares/publish)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and BIM CSV/SVG code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local BimDown project files and may optionally publish a project after explicit user consent.]

## Skill Version(s):

1.4.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
