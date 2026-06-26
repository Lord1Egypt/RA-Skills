## Description: <br>
Powerful ECharts-based data visualization skill optimized for the Feishu (Lark) ecosystem, supporting multiple chart types and data sources, automatic chart recommendation, analysis reports, and high-definition PNG chart generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzzanezhou0829](https://clawhub.ai/user/zzzanezhou0829) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to turn tabular business data from Excel, CSV, Feishu Bitable, Feishu Sheet, Markdown tables, JSON, or pasted data into Feishu-ready ECharts visualizations and brief analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says user data is rendered in a headless browser that loads ECharts from a third-party CDN. <br>
Mitigation: Review before processing sensitive business data; use an isolated environment, vendor ECharts locally, or block external browser network access. <br>
Risk: The security review says marketplace crypto and purchase capability tags do not match the reviewed artifacts. <br>
Mitigation: Verify marketplace capability tags before deployment and do not grant unrelated permissions based only on the advertised tags. <br>


## Reference(s): <br>
- [ECharts chart configuration reference](references/echarts_config.md) <br>
- [Feishu ECharts card specification](references/feishu_card_spec.md) <br>
- [ECharts documentation](https://echarts.apache.org/) <br>
- [Pyppeteer documentation](https://pyppeteer.github.io/pyppeteer/) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [PNG chart files, Feishu card JSON, Markdown or text analysis, and command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate high-definition chart screenshots and optional Feishu interactive card JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog, artifact changelog released 2026-04-09) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
