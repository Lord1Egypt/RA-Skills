## Description: <br>
Diagnose and triage cron job failures by checking job state, identifying error patterns, prioritizing incidents, and generating health reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suryast](https://clawhub.ai/user/suryast) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and site reliability engineers use this skill to inspect cron jobs, review recent cron logs, triage failed scheduled tasks by impact, and produce a health report with recommended fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cron configuration, logs, and generated reports may expose sensitive job names, local paths, errors, backup workflows, or security automation details. <br>
Mitigation: Treat reports and copied log excerpts as sensitive, store them only in approved locations, and redact operational details before sharing. <br>
Risk: The skill suggests commands that inspect system cron files and logs, including commands that may require sudo. <br>
Mitigation: Review each proposed command before approval, run it only on the intended host, and limit elevated access to the specific diagnostic checks needed. <br>


## Reference(s): <br>
- [Cron Doctor on ClawHub](https://clawhub.ai/suryast/cron-doctor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports with shell command suggestions and diagnostic guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local cron job names, file paths, log excerpts, priorities, errors, and recommended fixes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
