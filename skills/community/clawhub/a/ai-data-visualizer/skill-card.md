## Description:

Automatically analyze and recommend optimal chart combinations based on data characteristics, generate beautiful interactive HTML dashboards (including line charts, bar charts, scatter plots, pie charts, etc.), support dark/light theme switching, CSV and JSON input, and data statistical summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect CSV or JSON datasets, select appropriate chart types, and generate interactive HTML dashboards with summary statistics and data previews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated dashboards are active web pages, and untrusted CSV or JSON content can introduce browser-code execution risk.

Mitigation: Use the skill only with trusted data until HTML escaping and JSON embedding are fixed; review generated dashboards before opening, sharing, or hosting them.

Risk: Generated dashboards load Chart.js from an external CDN.

Mitigation: Bundle Chart.js locally or add subresource integrity and a clear network disclosure before use on sensitive or authenticated domains.

## Reference(s):

- [Chart Selection Rules](artifact/references/chart-selection.md)
- [AI Data Visualizer ClawHub Page](https://clawhub.ai/openlark/skills/ai-data-visualizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration]

**Output Format:** [Markdown guidance with bash command snippets and generated interactive HTML dashboard files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated dashboards include Chart.js visualizations, a theme toggle, summary statistics, and a data table preview limited to 500 rows.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
