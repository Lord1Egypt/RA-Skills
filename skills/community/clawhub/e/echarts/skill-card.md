## Description:

Create Apache ECharts option JSON, standalone HTML chart pages, and export-ready chart artifacts from CSV, TSV, JSON tables, or existing option configs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to turn structured data or existing ECharts options into reviewable chart configs, standalone preview pages, and optional static image exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated chart pages contact public CDNs and execute the returned ECharts JavaScript.

Mitigation: Use a reviewed local ECharts bundle with --cdn, or avoid opening and rendering generated pages until the runtime source is pinned or bundled.

Risk: Sensitive or offline data may be reviewed in generated pages that depend on an external runtime source.

Mitigation: For sensitive or offline workflows, render only with a reviewed local or mirrored ECharts bundle.

## Reference(s):

- [Apache ECharts](https://echarts.apache.org/)
- [Chart Selection](references/chart-selection.md)
- [Option Patterns](references/option-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/jvy/skills/echarts)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands plus generated JSON, HTML, and optional PNG or SVG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts commonly include chart.option.json, chart.spec.json, chart.html, manifest.json, normalized data JSON, and optional exported images.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
