## Description: <br>
Monitors Alibaba DataWorks task runs, analyzes failures and runtime anomalies, classifies alerts by severity, and prepares daily operational reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexmayanjun-collab](https://clawhub.ai/user/alexmayanjun-collab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data platform operators and engineers use this skill to check DataWorks task status, review failures and runtime anomalies, classify alerts, and generate daily operational reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DataWorks credentials and project configuration may be exposed or granted broader access than the monitoring task requires. <br>
Mitigation: Confirm the DataWorks project scope, use a dedicated read-only access key, and store secrets outside source files. <br>
Risk: Task logs and failure details may contain sensitive identifiers, SQL fragments, tokens, or internal URLs before LLM analysis or external posting. <br>
Mitigation: Redact sensitive values from logs and reports before sending them to an LLM or Feishu. <br>
Risk: Recurring cron runs, sub-agent execution, or Feishu notifications can create autonomous monitoring and message delivery without the intended audience or cadence. <br>
Mitigation: Approve the exact Feishu webhook or channel and enable cron or sub-agent runs only when recurring autonomous monitoring is intended. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/alexmayanjun-collab/dataworks-smart-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and text reports with JSON report artifacts and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include DataWorks task summaries, severity levels, Feishu notification text, and cron configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
