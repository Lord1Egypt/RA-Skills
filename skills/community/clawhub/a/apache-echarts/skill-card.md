## Description:

Apache ECharts charting skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to turn two-dimensional or time-series data into interactive ECharts HTML chart files with chart-type selection and PNG export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can embed untrusted chart content into executable browser code.

Mitigation: Review generated HTML before opening or sharing it, especially when chart data or titles came from an untrusted source; prefer safe serialization of chart options and escaped titles.

Risk: Opened charts load ECharts from jsDelivr.

Mitigation: Use the CDN only where external script loading is acceptable, or replace it with an approved local or pinned dependency source before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/openlark/skills/apache-echarts)
- [Apache ECharts Homepage](https://echarts.apache.org/)
- [ECharts API Reference](references/api.md)
- [Apache ECharts Getting Started](https://echarts.apache.org/handbook/en/get-started/)
- [Apache ECharts Configuration Manual](https://echarts.apache.org/en/option.html)
- [Apache ECharts Examples Gallery](https://echarts.apache.org/examples/en/index.html)

## Skill Output:

**Output Type(s):** [Code, Files, Guidance]

**Output Format:** [Complete HTML file with embedded JavaScript and chart configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated charts load ECharts 5.x from jsDelivr and include responsive resizing, PNG export, and console export helpers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
