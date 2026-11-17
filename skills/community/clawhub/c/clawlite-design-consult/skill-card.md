## Description:

A product design consulting skill that clarifies project context, proposes coherent design-system decisions, can optionally research competitors, previews typography and color choices, and writes DESIGN.md plus a CLAUDE.md design section.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to establish or update a project design system through a guided consultation. It produces design rationale, visual direction, typography and color recommendations, optional preview HTML, and project-level design guidance files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The preview path may open a browser and load fonts from Google.

Mitigation: Review network and font-loading policy before using the preview path in restricted environments.

Risk: The final write step may create DESIGN.md and append design guidance to CLAUDE.md.

Mitigation: Review the resulting file diffs before relying on the guidance in future agent sessions.

Risk: Design proposals may introduce incorrect or misleading guidance into project design standards.

Mitigation: Have a human product or design owner review the recommendations before adopting them as project policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/x-rayluan/skills/clawlite-design-consult)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational guidance with Markdown documents, inline shell commands, and optional HTML preview code.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create DESIGN.md and append a design-system section to CLAUDE.md after user confirmation in the workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
