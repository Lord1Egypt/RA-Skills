## Description:

DevOps Agent helps operators deploy services, configure monitoring, schedule backups, and diagnose faults with dry-run, logging, snapshot, and rollback guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fullstackcrew-alpha](https://clawhub.ai/user/fullstackcrew-alpha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and site reliability engineers use this skill to turn common service deployment, monitoring, backup, and troubleshooting work into guided agent workflows. It is intended for environments where privileged system changes are reviewed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose persistent privileged changes to services, cron jobs, Nginx, monitoring components, and backup or rollback paths.

Mitigation: Use dry-run output first, review each privileged command, and run only in a disposable or tightly controlled environment unless the scripts have been audited and hardened.

Risk: The release security guidance flags unsafe installation patterns such as curl-to-shell, apt-key use, and unverified binary downloads.

Mitigation: Replace those patterns with verified package sources, pinned versions, checksum or signature validation, and distribution-supported keyring handling before production use.

Risk: Monitoring setup may expose default Grafana credentials or bind Prometheus, Grafana, and exporters too broadly.

Mitigation: Require non-default Grafana credentials, restrict listening interfaces and firewall rules, and review all monitoring endpoints before exposing them.

Risk: Backup and rollback workflows can copy, overwrite, delete, or schedule operations against sensitive paths or remote destinations.

Mitigation: Validate target, snapshot, and destination inputs; test restore procedures; and inspect every cron, systemd, sudo, and deletion action before approving execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fullstackcrew-alpha/skills/devops-agent)
- [Nginx configuration templates](artifact/references/nginx-templates.md)
- [systemd service templates](artifact/references/systemd-templates.md)
- [Grafana dashboard templates](artifact/references/grafana-dashboards.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with inline shell commands, generated shell scripts, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce deployment reports, monitoring setup notes, backup scripts, rollback commands, and diagnosis reports depending on the selected command.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
