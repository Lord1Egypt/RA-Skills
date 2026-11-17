## Description:

Self-healing infrastructure guardian. Monitors services, diagnoses failures, executes recovery playbooks, and learns from incidents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peres84](https://clawhub.ai/user/peres84)

### License/Terms of Use:

MIT-0

## Use Case:

Infrastructure operators and developers use this skill to check Tailscale Funnel, website availability, disk usage, and service health, then run documented recovery actions and report the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make recurring privileged system changes through sudo-level cleanup, restart, and recovery commands.

Mitigation: Review and constrain the playbooks before deployment, verify referenced helper scripts, and require approval before destructive cleanup or recurring cron creation.

Risk: The skill can learn fixes from untrusted web results when an error is not covered by a playbook.

Mitigation: Avoid automatic use of web-sourced fixes; require human review before applying or appending newly discovered recovery steps.

Risk: Incorrect diagnosis or recovery could restart the wrong service, remove useful logs, or mask a deeper outage.

Mitigation: Keep the diagnostic order, validate nginx configuration before reloads, preserve application and database files, and escalate repeated failures for manual investigation.

## Reference(s):

- [Dead Man's Switch ClawHub skill page](https://clawhub.ai/peres84/skills/deadmans-switch)
- [Disk Space Recovery playbook](artifact/playbooks/disk.md)
- [Nginx and Website Monitoring playbook](artifact/playbooks/nginx.md)
- [Generic Crashed Process Recovery playbook](artifact/playbooks/process.md)
- [Tailscale Funnel Recovery playbook](artifact/playbooks/tailscale.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown health reports with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May log incidents, propose or create recurring cron checks after repeated failures, and generate voice alerts if configured.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
