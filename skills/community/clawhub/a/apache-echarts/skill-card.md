## Description: <br>
Apache ECharts charting skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to turn user-provided two-dimensional or time-series data into complete interactive Apache ECharts HTML chart pages with export support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated chart files contain JavaScript and load Apache ECharts from a public CDN when opened. <br>
Mitigation: Use trusted chart data and options, and prefer a local or organization-approved ECharts copy when offline operation or stricter supply-chain control is required. <br>
Risk: Incorrect labels, data, or chart options can produce misleading visualizations. <br>
Mitigation: Review the generated HTML, chart configuration, and rendered visualization before publishing or using it for decisions. <br>


## Reference(s): <br>
- [ECharts API Reference](references/api.md) <br>
- [Apache ECharts Homepage](https://echarts.apache.org/) <br>
- [Apache ECharts Get Started](https://echarts.apache.org/handbook/en/get-started/) <br>
- [Apache ECharts Configuration Manual](https://echarts.apache.org/en/option.html) <br>
- [Apache ECharts Examples Gallery](https://echarts.apache.org/examples/en/index.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Complete HTML files with embedded JavaScript configuration and supporting Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated chart pages use ECharts 5.x from a CDN, include responsive resizing, and expose PNG export support.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
