## Description: <br>
Audit AI agent cron jobs for token cost risks, model-switch loops, and session isolation failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pouria3](https://clawhub.ai/user/pouria3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit OpenClaw cron jobs, diagnose unexpected token cost spikes, and identify model-switch or session-isolation failures before they become runaway retry loops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a user-controlled destructive step to remove an offending cron job. <br>
Mitigation: Confirm the exact cron job ID and save the job definition or relevant logs before running cron removal. <br>
Risk: Cron, session, and log checks may expose local operational details to the active agent context. <br>
Mitigation: Review outputs for sensitive operational information before sharing or persisting them outside the troubleshooting session. <br>


## Reference(s): <br>
- [Token Spike Diagnosis & Post-Incident Checklist](references/diagnosis.md) <br>
- [Cron Cost Guard on ClawHub](https://clawhub.ai/pouria3/cron-cost-guard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and checklist steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces troubleshooting guidance and command suggestions; users should verify job IDs and relevant logs before removing cron jobs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
