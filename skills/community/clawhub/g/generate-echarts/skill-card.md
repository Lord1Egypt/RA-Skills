## Description:

MCP ECharts is a chart-generation skill that uses Apache ECharts-style options and chart-specific parameters to create visualizations through the XiaoBenYang remote API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to generate ECharts visualizations such as line, bar, pie, radar, scatter, sankey, funnel, gauge, treemap, sunburst, heatmap, candlestick, boxplot, graph, parallel-coordinate, and tree charts. The skill routes user requests to chart-specific API calls and returns the API result for presentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chart data is sent to XiaoBenYang's remote API.

Mitigation: Avoid sensitive chart inputs unless this external data flow is acceptable for the deployment.

Risk: The service API key is stored in a local .env file in plaintext.

Mitigation: Keep .env out of source control and use safer secret storage where available.

Risk: Server security evidence notes mismatched school-search and MinIO packaging details.

Mitigation: Review the installed skill behavior and documentation before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/generate-echarts)
- [Publisher profile](https://clawhub.ai/user/alinklab)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, API calls]

**Output Format:** [Agent-readable summaries of JSON API responses, with chart outputs requested as PNG, SVG, or ECharts option JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key. Custom ECharts options must be valid non-empty JSON strings.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
