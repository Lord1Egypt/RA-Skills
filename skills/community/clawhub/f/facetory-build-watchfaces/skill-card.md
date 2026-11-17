## Description:

Uses Facetory's local MCP server to help agents inspect, create, edit, validate, save, and export Xiaomi watchface projects, including normal and AOD themes, data bindings, local assets, layer order, templates, and export troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sakurakilove](https://clawhub.ai/user/sakurakilove)

### License/Terms of Use:

MIT-0

## Use Case:

Watchface designers and developers use this skill when they want an agent to operate an active Facetory project through the local MCP server, review planned edits, validate normal and AOD themes, and prepare Xiaomi, Redmi, or Mi Band exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent can plan edits, saves, reviews, and exports against the active Facetory watchface project.

Mitigation: Read the current document version before each workflow, review plan summaries and validation results before applying changes, apply each approved plan only once, and export only after validation.

Risk: Some asset workflows may require copying files into Facetory's private Android application directory.

Mitigation: Prefer non-root paths; when root access is necessary, require fresh explicit approval for each command and state the source, destination, overwrite behavior, and risk before execution.

Risk: AOD image masks or export metadata can pass ordinary review but still fail device-specific Xiaomi export checks.

Mitigation: Validate normal and AOD themes separately, inspect warnings, confirm AOD images use alpha-only visible pixels, and reread the document version after UI metadata changes.

## Reference(s):

- [Facetory MCP workflow reference](references/mcp-workflow.md)
- [Facetory development pitfalls](references/pitfalls.md)
- [ClawHub skill page](https://clawhub.ai/sakurakilove/skills/facetory-build-watchfaces)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline commands and MCP workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces plans and instructions for operating Facetory through its local MCP server; the diagnostic script performs read-only MCP health checks.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
