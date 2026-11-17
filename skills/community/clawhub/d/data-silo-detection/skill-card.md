## Description:

Detects and maps data silos in construction organizations to identify disconnected data sources, duplicate data, and integration opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Construction data teams, analysts, and developers use this skill to analyze user-provided source inventories or project data for isolated systems, domain disconnects, duplicate entities, data-flow gaps, and integration priorities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide more construction project data than is needed for a silo analysis.

Mitigation: Provide only the project files, source inventories, or parameters intended for analysis.

Risk: Optional exports can contain project-sensitive findings or source names.

Mitigation: Treat exports as user-directed outputs and review destination paths and report contents before sharing.

## Reference(s):

- [DataDrivenConstruction homepage](https://datadrivenconstruction.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Structured text and Markdown reports with Python code patterns and optional CSV, Excel, or JSON exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided construction data; optional exports are user-directed.]

## Skill Version(s):

2.1.0 (source: server release metadata; artifact/claw.json lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
