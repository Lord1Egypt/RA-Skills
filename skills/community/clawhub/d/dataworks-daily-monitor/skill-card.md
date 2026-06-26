## Description: <br>
Monitors daily DataWorks task runs, summarizes success, failure, and running counts, and sends Feishu reports with failure alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexmayanjun-collab](https://clawhub.ai/user/alexmayanjun-collab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data engineers and operations teams use this skill to check the previous day's DataWorks task status, review failed tasks, and receive a daily Feishu report with alerts when failures are present. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses cloud credentials to read DataWorks task metadata. <br>
Mitigation: Configure a least-privilege RAM subaccount with only the DataWorks project and instance query permissions needed for monitoring. <br>
Risk: Failure details may be sent to a broad or unintended Feishu recipient. <br>
Mitigation: Confirm the Feishu recipient or webhook before enabling notifications, and avoid sending detailed error messages to broad chats unless approved. <br>
Risk: The daily schedule may continue sending reports after it is no longer needed. <br>
Mitigation: Enable the 9:00 daily schedule only when the operator knows how to disable or change it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alexmayanjun-collab/dataworks-daily-monitor) <br>
- [README](artifact/README.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style daily status report with environment variable configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include DataWorks task counts, failed task details, console links, Feishu notification text, and failure alerts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
