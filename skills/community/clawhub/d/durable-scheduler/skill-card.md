## Description: <br>
Use when the user needs durable, audited job scheduling beyond OpenClaw's built-in cron -- SQLite-backed scheduler with shell + agent steps, retries, approvals, and full run history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amittell](https://clawhub.ai/user/amittell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and manage persistent OpenClaw job scheduling, audited shell and agent workflows, retries, approvals, and run history on hosts that need more durability than built-in cron. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports a persistent host-side scheduler that can keep running jobs outside the OpenClaw gateway lifecycle. <br>
Mitigation: Install it only when persistent host-side scheduling is intended, pin a trusted package version, and review the package/source before use. <br>
Risk: Shell workflows can execute privileged or destructive host commands. <br>
Mitigation: Run jobs with the least privilege possible, test workflows non-destructively, and keep cleanup or remediation commands narrow and reversible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/amittell/durable-scheduler) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scheduler setup steps, job definitions, workflow commands, and operational cautions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
