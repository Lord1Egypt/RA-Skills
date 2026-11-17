## Description:

Manage Docker containers securely via docker-socket-proxy by checking status, logs, resource usage, and restarting only explicitly whitelisted containers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elston](https://clawhub.ai/user/elston)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to inspect Docker container status, summarize recent logs, review resource usage, and perform controlled restarts through docker-socket-proxy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included report script can print unsanitized container log excerpts that may expose secrets.

Mitigation: Install only for agents authorized to inspect Docker operational data; avoid or fix scripts/container-report.sh until log excerpts are redacted before display.

Risk: Docker restart authority can disrupt running services if the whitelist is too broad.

Mitigation: Review the whitelist before deployment and keep can_restart=false unless restart authority is intended for that container.

Risk: Large log retrieval can increase load or expose more operational data than needed.

Mitigation: Enforce the documented log limits and 7-day maximum period before using the reporting workflow.

## Reference(s):

- [Docker Commands Reference](references/docker-commands.md)
- [ClawHub Skill Page](https://clawhub.ai/elston/skills/docker-ops)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and operational summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include status summaries, log analysis, restart audit messages, and remediation guidance.]

## Skill Version(s):

0.4.0 (source: server release evidence and changelog, released 2026-03-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
