## Description:

Generate beautiful charts via the Chart Splat API. Use when the user asks to create, generate, or visualize data as charts, graphs, or plots. Supports line, bar, pie, doughnut, radar, polar area, and candlestick/OHLC charts. Returns PNG images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobbyg603](https://clawhub.ai/user/bobbyg603)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to turn user-provided datasets and chart configuration into PNG charts through the Chart Splat CLI, helper script, or API. It supports common business, categorical, time-series, and OHLC financial visualizations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chart data is sent to the Chart Splat API for server-side rendering.

Mitigation: Avoid sensitive chart contents unless approved for external processing.

Risk: The preferred CLI path uses npx without a pinned package version.

Mitigation: Use a pinned and reviewed chartsplat-cli version before production deployment.

Risk: The helper script can override the API endpoint through CHARTSPLAT_API_URL.

Mitigation: Keep CHARTSPLAT_API_URL unset unless a trusted endpoint has been reviewed, and restrict network egress to the Chart Splat API.

## Reference(s):

- [Chart Splat API Reference](references/api-reference.md)
- [Sample Chart Configurations](examples/sample-charts.json)
- [Chart Splat Homepage](https://chartsplat.com)
- [Chart Splat API Endpoint](https://api.chartsplat.com/chart)
- [Chart Splat API Keys](https://chartsplat.com/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON chart configuration, and PNG file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CHARTSPLAT_API_KEY, Node.js, npx, and network access to the Chart Splat API.]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
