## Description:

Diagram Tool Pro generates and manages Mermaid, PlantUML, ASCII, and SVG diagrams, with batch generation, templates, version tracking, and export workflows for technical documentation teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation teams, and enterprise workflow maintainers use this skill to create, batch-generate, export, template, and version diagrams for technical documents, architecture reviews, teaching materials, and internal knowledge bases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad execution and write authority could affect files outside the intended diagram workflow.

Mitigation: Activate the skill only for explicit diagram or export requests, constrain writes to a chosen diagram output directory, and require approval for writes elsewhere.

Risk: Rendering workflows may run local Java, PlantUML, npm, npx, or Mermaid CLI commands.

Mitigation: Require approval before running rendering commands and prefer pinned, locally installed tools over ad hoc package execution.

Risk: Callback URLs and public PlantUML rendering can expose diagram content outside the local environment.

Mitigation: Require review for callback URLs and public rendering services, and prefer local rendering for sensitive diagrams.

Risk: Automatic diagram versioning can create repository commits without sufficient review.

Mitigation: Disable auto-commit by default or require manual confirmation before any commit is made.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/diagram-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, diagram source code, SVG/HTML file guidance, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Mermaid, PlantUML, ASCII, SVG, PNG/PDF/HTML export instructions, theme configuration, template structures, versioning guidance, and execution logs.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
