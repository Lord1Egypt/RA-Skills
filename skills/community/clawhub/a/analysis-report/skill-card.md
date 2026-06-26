## Description: <br>
Orchestrates complete, structured data analysis reports by choosing report sections, delegating metric query, anomaly detection, attribution, and forecasting work to downstream skills, and weaving the results into a coherent narrative. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackyujun](https://clawhub.ai/user/jackyujun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, analysts, and business users use this skill when they need a one-time, multi-section business analysis report rather than a single metric lookup or isolated anomaly check. It acts as the report editor, confirming scope and structure, coordinating downstream analytical skills, and producing an executive-readable report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates analysis to downstream metric-query, anomaly-detection, metric-attribution, forecast-simulation, and document-conversion skills. <br>
Mitigation: Install and run it only in environments where those downstream skills are trusted and available. <br>
Risk: Generated reports and intermediate analytical results may contain sensitive business data. <br>
Mitigation: Review the requested report scope and handle generated content according to the organization’s data handling policies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackyujun/analysis-report) <br>
- [Publisher profile](https://clawhub.ai/user/jackyujun) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown report with structured sections, tables, summaries, findings, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request conversion to docx, pptx, or xlsx after Markdown generation by calling an appropriate document conversion skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
