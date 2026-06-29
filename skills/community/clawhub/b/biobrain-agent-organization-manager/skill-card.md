## Description: <br>
Helps agents design and operate multi-department agent organizations with rosters, communication channels, scheduled reporting, learning workflows, and audits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ygq19901001](https://clawhub.ai/user/ygq19901001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to structure an agent team into departments, define responsibilities, set communication routes, and plan scheduled reporting and inspection workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional scheduled jobs can write reports and share summaries across sessions, which may expose sensitive prompts, customer data, or secrets if those details are included. <br>
Mitigation: Review cron templates before enabling them, confirm file destinations and report recipients, and keep shared summaries free of secrets, customer data, and private prompts. <br>
Risk: Autonomous reporting or inspection routines can keep running with stale, low-quality, or failed outputs if cron health is not monitored. <br>
Mitigation: Use the skill's inspection guidance to monitor consecutive failures, review generated reports, and require human approval before relying on a newly automated workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ygq19901001/skills/biobrain-agent-organization-manager) <br>
- [Server-resolved source repository](https://github.com/Ygq19901001/biobrain-agent-organization-manager) <br>
- [Communication patterns reference](https://github.com/Ygq19901001/biobrain-agent-organization-manager/blob/08d78b62a09f87a29095a3538cbfc74774a7766b/references/communication-patterns.md) <br>
- [Cron templates reference](https://github.com/Ygq19901001/biobrain-agent-organization-manager/blob/08d78b62a09f87a29095a3538cbfc74774a7766b/references/cron-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with roster templates, communication patterns, and cron-style JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scheduled job templates and operational checklists that should be reviewed before use.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
