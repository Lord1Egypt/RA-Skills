## Description: <br>
fullask reports logistics index scores, industry rankings, trend analysis, abnormal indicators, and operational suggestions for a carrier and statistical date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a-vb](https://clawhub.ai/user/a-vb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized logistics operations users use this skill to query a carrier and statistical date, then summarize logistics index performance, ranking changes, pickup timeliness impact, and exception proportions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a logistics dashboard and named local spreadsheets that may contain sensitive operational data. <br>
Mitigation: Install and use it only when the agent is authorized to access the Jingwe logistics dashboard and the intended spreadsheet files. <br>
Risk: Recommendations depend on the fixed assumption that pickup timeliness is the main sub-indicator affecting ranking. <br>
Mitigation: Confirm that assumption and the selected date and carrier before relying on the operational recommendations. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report with logistics metrics, trend analysis, exception summaries, and operational recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires carrier name and statistical date as inputs; output includes score, industry average, ranking, seven-day trend, fixed pickup-timeliness sub-indicator, and exception category proportions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
