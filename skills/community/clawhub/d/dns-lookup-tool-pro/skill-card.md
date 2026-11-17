## Description:

DNS查询专业版 helps operations teams and SREs perform batch DNS diagnostics, DNSSEC validation, structured reporting, history tracking, latency monitoring, and alerting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, SREs, and operations teams use this skill to inspect DNS records across one or many domains, validate DNSSEC and CAA-related configuration, generate structured reports, and configure DNS monitoring or alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run DNS-related shell commands and its activation scope may invite unrelated automation tasks.

Mitigation: Restrict use to DNS diagnostics and monitoring, and require separate review before using it for deployment, log analysis, or general automation.

Risk: The skill may write reports, create scheduled monitoring, store history, or send webhook and email notifications.

Mitigation: Require explicit approval before enabling file writes, scheduled tasks, persistent history, or outbound alert channels.

Risk: DNS diagnostics can produce misleading conclusions when network reachability, resolver choice, or DNSSEC support is misconfigured.

Mitigation: Review generated reports before operational action and verify failures against known-good resolvers or manual DNS tooling.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/dns-lookup-tool-pro)
- [ClawHub Publisher Profile](https://clawhub.ai/user/thcjp)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, YAML configuration examples, and JSON or CSV report descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write DNS reports, store query history, and send webhook or email notifications when the user configures those workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
