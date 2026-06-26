## Description: <br>
DevOps Agent helps operators deploy services, configure monitoring, schedule backups, and diagnose faults with dry-run, confirmation, rollback, and audit logging support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fullstackcrew-alpha](https://clawhub.ai/user/fullstackcrew-alpha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site reliability engineers, and operations teams use this skill to perform routine server operations such as application deployment, Prometheus and Grafana monitoring setup, scheduled database or directory backups, and incident diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent root-level deployment, systemd, cron, monitoring, backup, and diagnostic changes. <br>
Mitigation: Use dry-run first, review every sudo, systemctl, cron, and file-write command, and run it only on servers where those operational changes are intended. <br>
Risk: Monitoring setup examples can expose Prometheus, Grafana, exporters, or default Grafana credentials if deployed without hardening. <br>
Mitigation: Bind monitoring endpoints to localhost or a private network, change Grafana default credentials before API use, and review generated dashboards and alert configuration. <br>
Risk: Installer flows may download binaries or add repository keys for monitoring components. <br>
Mitigation: Verify downloaded binaries, release sources, checksums, and repository keys before installation. <br>
Risk: Generated backup scripts can move sensitive data to local or remote destinations and schedule recurring jobs. <br>
Mitigation: Inspect generated scripts, destinations, retention settings, encryption settings, and notification targets before scheduling backups. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fullstackcrew-alpha/devops-agent) <br>
- [Grafana Dashboard JSON Templates](references/grafana-dashboards.md) <br>
- [Nginx Configuration Templates](references/nginx-templates.md) <br>
- [Systemd Service Templates](references/systemd-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with shell commands, code snippets, generated scripts, and configuration templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce deployment, monitoring, backup, rollback, and diagnosis reports; may also generate shell scripts and service configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
