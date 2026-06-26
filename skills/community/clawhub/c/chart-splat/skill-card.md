## Description: <br>
Generate beautiful charts via the Chart Splat API. Use when the user asks to create, generate, or visualize data as charts, graphs, or plots. Supports line, bar, pie, doughnut, radar, polar area, and candlestick/OHLC charts. Returns PNG images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bobbyg603](https://clawhub.ai/user/bobbyg603) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use Chart Splat to turn user-provided datasets and chart configuration into PNG chart files through the Chart Splat CLI, helper script, or API. It is suited for line, bar, pie, doughnut, radar, polar area, candlestick, and OHLC chart generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chart data and configuration are sent to Chart Splat's remote API for rendering. <br>
Mitigation: Do not submit secrets, regulated data, or confidential business datasets unless external processing by Chart Splat is approved by the organization. <br>
Risk: The skill requires a CHARTSPLAT_API_KEY for API access. <br>
Mitigation: Store the API key in agent environment configuration, scope it to Chart Splat, and rotate or revoke it if exposure is suspected. <br>
Risk: Generated chart files can be misleading if labels, datasets, or OHLC values are incorrect. <br>
Mitigation: Validate source data and ensure labels and data arrays match before sharing generated PNG outputs. <br>


## Reference(s): <br>
- [Chart Splat API Reference](references/api-reference.md) <br>
- [Sample chart configurations](examples/sample-charts.json) <br>
- [Chart Splat homepage](https://chartsplat.com) <br>
- [Chart Splat ClawHub listing](https://clawhub.ai/bobbyg603/chart-splat) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration that produces PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npx, network access to api.chartsplat.com, and CHARTSPLAT_API_KEY. Default chart output is chart.png unless another output path is supplied.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
