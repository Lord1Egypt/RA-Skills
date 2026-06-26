## Description: <br>
Audit and improve your OpenClaw setup with one skill. Scores agent health, audits memory hygiene, checks cron reliability, and compares installed skills against ClawHub — with conservative fixes instead of reckless auto-repair. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zihaofeng2001](https://clawhub.ai/user/zihaofeng2001) <br>

### License/Terms of Use: <br>
CC BY-SA 4.0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to audit agent memory, cron jobs, installed skills, security posture, and continuity files, then review prioritized recommendations and trend reports. It is suited for periodic health checks and conservative maintenance planning rather than unattended self-repair. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw workspace, memory, skill metadata, and cron configuration, which may include sensitive operational context. <br>
Mitigation: Run it only in workspaces where local diagnostic scanning is acceptable, and review generated reports before sharing them. <br>
Risk: The cron optimizer can edit cron jobs when explicitly run with --fix. <br>
Mitigation: Run cron_optimizer.py without --fix first, review the proposed changes, and rely on its backup at memory/cron-backup.json before accepting fixes. <br>
Risk: The skill comparator contacts ClawHub to compare installed skills against public catalog signals. <br>
Mitigation: Use it only when outbound ClawHub API access is acceptable for the environment. <br>


## Reference(s): <br>
- [Agent Health Optimizer on ClawHub](https://clawhub.ai/zihaofeng2001/agent-health-optimizer) <br>
- [ClawHub API](https://clawhub.ai/api/v1/) <br>
- [proactive-agent](https://clawhub.ai/halthelobster/proactive-agent) <br>
- [self-improving-agent](https://clawhub.ai/pskoett/self-improving-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown console reports, JSON report files, and OpenClaw cron command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local diagnostic reports under memory/ and only changes cron timing when cron_optimizer.py is run with --fix.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
