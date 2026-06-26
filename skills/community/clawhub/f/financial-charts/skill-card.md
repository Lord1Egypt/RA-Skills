## Description: <br>
根据财务数据生成精美的ECharts HTML图表页面，支持折线图、饼图、柱状图、K线图等 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[novaair026-dev](https://clawhub.ai/user/novaair026-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users can use this skill to turn financial datasets and chart preferences into polished HTML visualizations for trend, composition, comparison, relationship, and candlestick-style financial analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated chart HTML loads ECharts from a public CDN when opened. <br>
Mitigation: Avoid highly sensitive financial data unless you review the generated output, use a locally bundled ECharts copy, or open the file in a restricted or offline environment. <br>
Risk: The skill writes local HTML files from user-provided financial data. <br>
Mitigation: Review generated files before sharing or opening them in a less trusted environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/novaair026-dev/financial-charts) <br>
- [Publisher profile](https://clawhub.ai/user/novaair026-dev) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands, Guidance] <br>
**Output Format:** [HTML file with supporting shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated chart pages load ECharts from jsDelivr when opened unless the output is modified to use a local ECharts copy.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
