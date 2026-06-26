## Description: <br>
Generates concise daily work reports for short-drama and AI comic teams, including workload, token usage, content progress, completed work, risks, and next-day tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elevenzhou](https://clawhub.ai/user/elevenzhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Short-drama and AI comic teams use this skill to turn session token usage and scoped production notes into a daily operating report. The report summarizes script, storyboard, video, publishing, collaboration, target-comparison, and risk information when those data are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The report may include information from named memory files that is not suitable for a daily team report. <br>
Mitigation: Keep the referenced memory files limited to report-appropriate production notes before invoking the skill. <br>
Risk: Generic daily-report or summary phrases may trigger the skill unintentionally. <br>
Mitigation: Invoke the skill explicitly when a short-drama production report is intended. <br>
Risk: Missing production data can make report metrics look complete when they are not. <br>
Mitigation: Follow the artifact guidance to mark unavailable values with a dash instead of leaving fields blank or inventing values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elevenzhou/eleven-daily-shortdrama-report) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance] <br>
**Output Format:** [Markdown daily report with concise sections and production metrics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses session token usage and scoped memory notes when available; unavailable fields are marked with a dash.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
