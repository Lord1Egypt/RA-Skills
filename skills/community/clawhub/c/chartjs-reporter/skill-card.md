## Description: <br>
Turns structured data such as query results, CSV summaries, JSON records, or Python lists and dictionaries into standalone dark-themed HTML visualization reports powered by Chart.js. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudcba](https://clawhub.ai/user/cloudcba) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to convert tabular or structured results into browser-opened Chart.js reports with KPI cards and common chart types. It is useful after SQL, CSV, Python, or DuckDB analysis when a self-contained visual report is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unescaped report data can become executable browser content in generated HTML previews. <br>
Mitigation: Use trusted input data, review generated reports before opening or sharing them, and HTML-escape report text before deployment. <br>
Risk: Generated reports load Chart.js from a CDN, which may be unsuitable for confidential or offline workflows. <br>
Mitigation: Bundle Chart.js locally when reports must remain offline or avoid external network requests. <br>


## Reference(s): <br>
- [Chart configuration guide](references/chart-config-guide.md) <br>
- [Theme tokens](references/theme-tokens.md) <br>
- [ClawHub release page](https://clawhub.ai/cloudcba/chartjs-reporter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON chart configuration examples, Python snippets, shell commands, and generated standalone HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports load Chart.js from a CDN and are intended to open directly in a browser.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
