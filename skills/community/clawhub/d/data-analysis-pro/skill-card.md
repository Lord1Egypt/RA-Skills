## Description: <br>
Data Analysis Pro helps agents analyze, interpret, and visualize spreadsheet, CSV, or JSON data through ChartGen-backed natural language workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chartgen-ai](https://clawhub.ai/user/chartgen-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to run natural-language data analysis, trend interpretation, and chart generation over provided CSV, Excel, or JSON datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected spreadsheets, CSVs, or JSON data are sent to chartgen.ai for processing. <br>
Mitigation: Use only approved datasets, avoid confidential or regulated data unless the vendor flow is approved, and review ChartGen privacy practices before use. <br>
Risk: API usage consumes credits and depends on a configured ChartGen API key. <br>
Mitigation: Use a dedicated API key with credit limits and rotate or revoke it according to organizational policy. <br>
Risk: Generated HTML visualizations may be shared outside the originating environment. <br>
Mitigation: Review generated HTML and chart content before publishing or distributing it. <br>


## Reference(s): <br>
- [Data Analysis Pro on ClawHub](https://clawhub.ai/chartgen-ai/data-analysis-pro) <br>
- [ChartGen](https://chartgen.ai) <br>
- [ChartGen Billing](https://chartgen.ai/billing) <br>
- [ECharts CDN](https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown or text analysis results, ECharts JSON, and optional HTML chart files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CHARTGEN_API_KEY and sends selected input data to chartgen.ai for processing.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
