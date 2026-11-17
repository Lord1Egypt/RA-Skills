## Description:

Data visualization with chart selection, color theory, and annotation best practices. Covers chart types (bar, line, scatter, heatmap), axes rules, and storytelling with data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

External users, developers, analysts, and content creators use this skill to choose appropriate chart types and produce clearer charts, dashboards, reports, presentations, infographics, and data stories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users toward a mutable remote installer for the inference.sh CLI.

Mitigation: Prefer a manual, version-pinned install path, inspect installer contents before running, and verify downloaded binaries against published checksums.

Risk: The skill uses external execution services for chart-generation examples.

Mitigation: Avoid sending private datasets, credentials, proprietary code, or sensitive business data through infsh app runs unless the service is trusted and credential storage is understood.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/okaris/skills/data-visualization-2)
- [inference.sh](https://inference.sh)
- [inference.sh CLI Installer](https://cli.inference.sh)
- [inference.sh CLI Checksums](https://dist.inference.sh/cli/checksums.txt)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Markdown with inline bash, Python, and HTML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to generate chart code or shell commands that call external inference.sh apps.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
