## Description:

Diagnose and triage cron job failures by checking job states, identifying error patterns, prioritizing failures by criticality, and generating health reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geq1fan](https://clawhub.ai/user/geq1fan)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to inspect cron jobs, investigate failed or missing scheduled-task executions, prioritize failures by operational impact, and produce a cron health report with suggested fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can lead an agent to inspect system-wide cron files and logs with elevated access before clear user approval.

Mitigation: Start with user-scoped diagnostics such as crontab -l, request explicit approval before using sudo or broad log access, and limit system-wide review to cases where it is necessary.

Risk: Cron logs and generated reports can expose sensitive paths, usernames, command arguments, or secrets.

Mitigation: Review and redact sensitive values before saving or sharing generated health reports.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/geq1fan/skills/cron-doctor-clawra)
- [Publisher Profile](https://clawhub.ai/user/geq1fan)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and a cron health report template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a dated cron health report under ~/workspace/reports when the agent follows the skill workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 1.1.0 and artifact _meta.json says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
