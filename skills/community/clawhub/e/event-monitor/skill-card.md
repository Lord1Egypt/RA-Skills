## Description: <br>
Predicts CPU spikes using Random Forest regressor, monitors system resources, saves metrics, and generates Excel reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ningtoba](https://clawhub.ai/user/ningtoba) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to collect local CPU and memory metrics, predict CPU behavior for the next 24 hours, save alerts, and generate spreadsheet reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local monitoring data can reveal process names, hostname, CPU and memory usage, timestamps, predictions, and alerts. <br>
Mitigation: Keep monitoring.db and system_report.xlsx private, delete old data when it is no longer needed, and review or pin Python dependencies before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ningtoba/event-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, configuration, text] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce local SQLite monitoring data, CPU prediction alerts, and Excel reports when the agent runs the bundled script.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
