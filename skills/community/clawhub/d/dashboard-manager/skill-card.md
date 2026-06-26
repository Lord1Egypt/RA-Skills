## Description: <br>
Dashboard Manager helps an agent read, update, and synchronize a Jarvis dashboard data.json file, including notes, logs, tasks, statistics, heartbeat, and active-agent status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Philippeh5](https://clawhub.ai/user/Philippeh5) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to let an agent keep a local Jarvis dashboard data file synchronized with current notes, logs, tasks, token statistics, heartbeat, and model status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change notes, logs, tasks, statistics, heartbeat, and agent status in the configured dashboard data file. <br>
Mitigation: Install it only for the intended Jarvis dashboard, verify the configured data.json path before use, and keep a backup of the dashboard file. <br>
Risk: Background or silent workflows may update dashboard state without direct conversational output. <br>
Mitigation: Review the dashboard logs and status fields during operation so automated changes remain auditable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Philippeh5/dashboard-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Logs, Status updates, Configuration] <br>
**Output Format:** [Local JSON file updates and console log messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and writes the configured Jarvis dashboard data.json file; background use may update dashboard state without conversational output.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, skill.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
