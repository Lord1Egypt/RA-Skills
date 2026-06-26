## Description: <br>
Game server real-time monitoring: query TPS, online users, JVM heap from Scouter Collector; detect alerts; send notifications; generate reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freepengyang](https://clawhub.ai/user/freepengyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Game operations engineers use this skill to query Scouter Collector metrics for JVM-based game servers, identify TPS and heap alerts, inspect single-server health, and generate operational status reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can query operational game-server metrics from a configured Scouter Collector. <br>
Mitigation: Install it only in agent environments authorized for game operations monitoring and verify that SCOUTER_COLLECTOR_URL points to a trusted Collector. <br>
Risk: Recurring alert workflows may send operational data to Feishu or DingTalk webhooks. <br>
Mitigation: Review webhook destinations, cronjob prompts, alert frequency, and cooldown settings before enabling automated notifications. <br>
Risk: Collector responses provide object hashes that are later used in shell commands. <br>
Mitigation: Keep the documented hex validation for objHash values before using them in curl URLs. <br>


## Reference(s): <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Scouter Project](https://github.com/scouter-project/scouter) <br>
- [Quick Start](references/quickstart.md) <br>
- [Alert Workflow](references/alert-workflow.md) <br>
- [Port Notes](references/PORT_NOTES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with operational summaries, tables, and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Scouter Collector API queries, metric calculations, alert summaries, notification setup guidance, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
