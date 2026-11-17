## Description:

系统监控专业版 helps operations teams monitor distributed servers, Docker/Kubernetes environments, logs, dashboards, alerts, and capacity trends through Chinese-language agent guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Operations teams, developers, and automation users use this skill to configure and operate multi-node server monitoring, container monitoring, log search, Grafana dashboards, alerting, and capacity planning workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for high-impact system, network, and credential access for monitoring workflows.

Mitigation: Install only in a controlled environment and provide read-only or least-privilege monitoring credentials.

Risk: Remote host access, log export, callbacks, webhooks, Docker socket access, or kubeconfig use could expose sensitive systems or data.

Mitigation: Require explicit user confirmation before those actions and scope access to approved hosts, clusters, logs, and endpoints.

Risk: The artifact describes local credential storage for optional integrations.

Mitigation: Prefer environment variables or protected secret stores, and avoid unprotected local config files for API keys, webhooks, and service credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/auto-monitor-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured status, result, and log summaries for monitoring workflows]

## Skill Version(s):

1.0.1 (source: evidence.release.version; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
