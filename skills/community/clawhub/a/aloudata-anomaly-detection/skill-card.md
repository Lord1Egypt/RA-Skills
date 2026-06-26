## Description: <br>
Detects anomalies in business metrics by delegating metric lookup to metric-query, building baselines, comparing current values, and returning structured normal, attention, or anomaly reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackyujun](https://clawhub.ai/user/jackyujun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business analysts and operations teams use this skill to check whether selected metrics, dimensions, or health-check scopes deviate from normal ranges. It is useful for metric health checks and batch anomaly scans before deeper attribution work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording can cause the agent to start anomaly checks for vague health-check requests before the user has named a concrete scope. <br>
Mitigation: Ask the user to confirm the metric area, dimensions, and time range before running broad scans. <br>
Risk: The skill delegates all metric data retrieval to metric-query, so results depend on that delegated skill being trusted and correctly permissioned. <br>
Mitigation: Use it only with a trusted metric-query skill and verify data-access permissions before deployment. <br>
Risk: Anomaly judgments can be misleading when baselines are weak, history is sparse, or thresholds are not appropriate for the metric. <br>
Mitigation: Show the baseline and threshold used in the report, prefer data-driven baselines when enough history exists, and clearly state when fallback thresholds are used. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jackyujun/aloudata-anomaly-detection) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown report with tables, concise findings, and optional Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include anomaly severity labels, baseline details, normal/abnormal summaries, and follow-up guidance for attribution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
