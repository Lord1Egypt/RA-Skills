## Description:

Powerful ECharts-based data visualization skill optimized for the Feishu (Lark) ecosystem, supporting 12+ chart types, 6+ data sources, automatic chart recommendation, automatic analysis reports, and high-definition PNG charts for Feishu display.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzzanezhou0829](https://clawhub.ai/user/zzzanezhou0829)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business users use this skill to turn Excel, CSV, Feishu Bitable, Feishu Sheet, Markdown table, JSON, or pasted tabular data into ECharts visualizations and concise analysis reports for Feishu conversations, documents, and wiki pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chart rendering loads ECharts from an external CDN, which may expose chart data or create a dependency on remote JavaScript.

Mitigation: Vendor and verify the ECharts asset locally, or use the skill only with data that is acceptable to process through a remote chart-library CDN.

Risk: The renderer launches a browser without sandboxing and may download browser or Python dependencies at runtime.

Mitigation: Run the skill in an isolated environment, pin and verify dependencies and browser downloads, and restrict file and network access to the selected input and output paths.

## Reference(s):

- [ECharts configuration reference](references/echarts_config.md)
- [Feishu ECharts card specification](references/feishu_card_spec.md)
- [ECharts](https://echarts.apache.org/)
- [Pyppeteer](https://pyppeteer.github.io/pyppeteer/)
- [Feishu Open Platform](https://open.feishu.cn/)
- [ClawHub skill page](https://clawhub.ai/zzzanezhou0829/skills/data-analysis-for-feishu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and generated PNG, JSON, and text output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate high-definition PNG charts, Feishu-compatible ECharts card JSON, and optional analysis text files.]

## Skill Version(s):

1.0.0 (source: server release metadata and CHANGELOG, released 2026-04-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
