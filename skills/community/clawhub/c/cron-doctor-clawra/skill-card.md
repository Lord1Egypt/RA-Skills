## Description: <br>
Diagnose and triage cron job failures by checking job states, identifying error patterns, prioritizing by criticality, and generating health reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geq1fan](https://clawhub.ai/user/geq1fan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and system administrators use this skill to inspect cron configuration and recent cron logs, triage failed scheduled jobs, and produce a concise health report with suggested fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cron diagnosis can expose operational details from crontabs, logs, and generated health reports. <br>
Mitigation: Run it only on systems the user administers and review reports for sensitive operational information before sharing them. <br>
Risk: Some troubleshooting commands may require elevated reads of system cron files or logs. <br>
Mitigation: Approve sudo reads or manual script execution only when appropriate for the environment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/geq1fan/cron-doctor-clawra) <br>
- [Publisher profile](https://clawhub.ai/user/geq1fan) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and triage recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local cron health report under ~/workspace/reports when the user asks for diagnosis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
