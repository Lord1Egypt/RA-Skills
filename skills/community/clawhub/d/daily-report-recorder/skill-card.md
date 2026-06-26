## Description: <br>
Daily Report Recorder records, polishes, and archives user-provided work updates into same-day Markdown daily reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bounding-elk](https://clawhub.ai/user/bounding-elk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and team members use this skill to turn daily work notes, troubleshooting records, meeting notes, and follow-up plans into concise internal status reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Daily reports may contain sensitive work details or credentials if the user includes them in prompts. <br>
Mitigation: Avoid entering secrets or sensitive internal details unless /data/reports/daily is approved for that content, and review generated reports before official submission. <br>
Risk: Optional scheduled prompts may create recurring report activity that users did not intend. <br>
Mitigation: Enable the cron schedule only when recurring report prompts are desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bounding-elk/daily-report-recorder) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown daily report file with a brief text confirmation and summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates /data/reports/daily/YYYY-MM-DD.md and adds Asia/Shanghai timestamps to submitted work items.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
