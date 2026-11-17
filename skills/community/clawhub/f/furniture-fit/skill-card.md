## Description:

Assess whether furniture fits in a measured Pascal room or layout. Use this skill for sofa, table, bed, cabinet, appliance, staging, placement, collision, clearance, or rotated-footprint questions. Produce a tool-backed spatial report that distinguishes footprint fit from unsupported height, door-swing, assembly, and delivery-route claims, and return insufficient evidence when dimensions or scale are missing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aymericr](https://clawhub.ai/user/aymericr)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to assess furniture footprints, collisions, clearance, and related unsupported checks in measured Pascal rooms or layouts. It is suited for bounded read-only fit reports and authorized placement workflows that keep height, door swing, delivery route, and safety claims separate from footprint evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted Pascal use can involve project data, measurements, or a Pascal API key.

Mitigation: Use local mode when projects should remain on the user's machine; use PASCAL_API_KEY only for hosted projects and keep credentials out of project files, reports, prompts, screenshots, and URLs.

Risk: Placement, save, hosted-link, or separate workspace actions can change state or expose data if treated as implicit authorization.

Mitigation: Keep assessments read-only unless the user explicitly authorizes the specific mutation or hosted action, then validate and report the final project status.

Risk: A clear horizontal footprint can be mistaken for proof of height, delivery, door swing, mesh contact, safety, or code compliance.

Mitigation: Report only the checks supported by measured evidence; mark unsupported or unmeasured constraints as not checked or insufficient evidence and request the smallest decisive measurement.

Risk: Connected Pascal releases can expose different MCP tools or schemas than the reviewed source.

Mitigation: Inspect the active Pascal guide, tool list, and schemas before assessment, and use only advertised inputs and outputs.

## Reference(s):

- [Pascal MCP developer documentation](https://editor.pascal.app/docs/developers/mcp)
- [ClawHub skill page](https://clawhub.ai/aymericr/skills/furniture-fit)
- [Setup](references/setup.md)
- [Evidence Boundaries](references/evidence-boundaries.md)
- [Report Template](references/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with structured nextAction YAML and optional setup snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports distinguish checked footprint evidence from unsupported height, door swing, delivery route, mesh, safety, and code claims.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; source skill metadata version 0.1.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
