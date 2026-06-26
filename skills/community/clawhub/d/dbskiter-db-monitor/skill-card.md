## Description: <br>
Provides database health monitoring guidance and dbskiter commands for health checks, anomaly detection, capacity forecasting, trend analysis, history review, and baseline comparison. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[magicczc](https://clawhub.ai/user/magicczc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database administrators, and operations teams use this skill to select dbskiter monitoring commands and interpret database health, anomaly, capacity, trend, history, and baseline-comparison results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to query live database or monitoring systems from broad prompts without always making that infrastructure access obvious. <br>
Mitigation: Install only where database or monitoring access is intended; use least-privilege, preferably read-only credentials; require explicit target database names and confirmation before health, history, or diagnostic queries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/magicczc/dbskiter-db-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with dbskiter shell commands and JSON-shaped result interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets Oracle monitoring through Zabbix for Z-series or KF-series assets and MySQL monitoring through direct database access or Prometheus when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
