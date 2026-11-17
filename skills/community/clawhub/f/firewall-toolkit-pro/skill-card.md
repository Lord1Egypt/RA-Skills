## Description:

防火墙配置工具包专业版 helps enterprise security teams manage firewalls, cloud security groups, nftables rules, multi-host deployment, CIS baseline audits, real-time log analysis, and rule versioning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Security engineers and enterprise operations teams use this skill to ask an agent for firewall administration guidance, configuration examples, cloud security group audits, CIS baseline checks, and deployment or rollback procedures. It is intended for authorized environments only.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-generated firewall or cloud security group changes could alter real network access with root-level or persistent effects.

Mitigation: Require explicit human confirmation before every change, validate generated rules, back up current rules, and test first on non-production hosts.

Risk: Batch deployment examples could propagate a bad rule set across multiple hosts.

Mitigation: Restrict the host list, use staged rollouts, keep rollback plans ready, and avoid running the remote root deployment example as written.

Risk: Cloud credentials used for security group management may grant broad network-control permissions.

Mitigation: Use narrowly scoped credentials, limit target accounts or projects, and review every proposed cloud rule change before applying it.

## Reference(s):

- [Detailed Reference](references/detail.md)
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/firewall-toolkit-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON status examples and inline shell or Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured status, result, execution log, and error fields for agent-facing responses.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
