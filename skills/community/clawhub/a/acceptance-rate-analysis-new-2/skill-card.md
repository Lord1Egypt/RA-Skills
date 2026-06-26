## Description: <br>
Analyzes declines in acceptance rate through staged attribution, first locating abnormal slices and then checking slice mix, funding-side capacity, asset dimensions, and sensitive funding-side contraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzhou1982](https://clawhub.ai/user/mzhou1982) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business analysts and operations teams use this skill to investigate day-over-day or week-over-week acceptance-rate declines. It guides an agent through staged command execution and turns script outputs into concise business-facing root-cause analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill ships and can silently use powerful DataWorks credentials. <br>
Mitigation: Remove the embedded credential, rotate any exposed token, and require an explicit least-privilege credential before installation or execution. <br>
Risk: Metric queries and generated logs can contain sensitive business data. <br>
Mitigation: Disable or redact debug logging by default, restrict log access, and treat generated outputs and log files as sensitive data. <br>
Risk: The skill sends analytics queries to a DataWorks endpoint. <br>
Mitigation: Pin or allowlist the approved endpoint and run the skill only in a controlled environment with expected network access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mzhou1982/acceptance-rate-analysis-new-2) <br>
- [DataWorks metric query endpoint](https://dataworks-metric.jirongyunke.net/dataworks-metric/metric/data/query/agent/queryMetricData) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with staged business analysis and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill produces business-facing conclusions while avoiding internal route fields, debug field names, and raw JSON unless needed for execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
