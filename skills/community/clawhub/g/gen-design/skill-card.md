## Description:

Gen Design helps agents generate traceable system design documents from a PRD or clear requirements through interactive technology selection, architecture design, API design, data modeling, integration design, and deployment planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lf951515851](https://clawhub.ai/user/lf951515851)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use Gen Design after a PRD or requirements description is available to produce a complete system design document. The generated design covers technical stack choices, architecture, modules, required data-flow and integration points, APIs, data models, and deployment planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can hand off to validation after generating a design document without clear affirmative consent.

Mitigation: Require explicit user confirmation before invoking /validate, and review the generated docs/design file before using it for downstream task generation.

Risk: The skill writes generated design documents into docs/design/.

Mitigation: Review the target path and generated Markdown before accepting changes in a repository.

## Reference(s):

- [ClawHub Gen Design skill page](https://clawhub.ai/lf951515851/skills/gen-design)
- [README.md](artifact/README.md)
- [prompt.md](artifact/prompt.md)
- [design-template.md](artifact/design-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown file written to docs/design/YYYY-MM-DD-{project-name}-design.md, with Mermaid diagrams, tables, API specifications, data models, and deployment notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PRD or clear requirements and asks the user to confirm technology choices before generating the design document.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
