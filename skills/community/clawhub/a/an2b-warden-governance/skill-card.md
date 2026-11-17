## Description:

Evaluates and governs OpenClaw bot actions with YAML policies and tamper-evident audit logs to allow, deny, or require review before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcools1977](https://clawhub.ai/user/jcools1977)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use this skill to add policy checks, review gates, and audit logging around OpenClaw agent actions before they execute. It supports local community operation and optional enterprise integrations for cloud governance and memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cached ALLOW decisions may bypass required approvals for high-impact actions.

Mitigation: Disable or patch the ALLOW decision cache before relying on the skill for deletes, payments, or other high-impact enforcement.

Risk: Action logging may retain or send full action details without redaction.

Mitigation: Review and redact logged payloads before enabling enterprise API keys or sending action details to cloud services.

Risk: Over-privileged OpenClaw accounts can increase the impact of an incorrect governance decision.

Mitigation: Run the skill with least-privileged OpenClaw accounts and require human review for destructive or payment actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jcools1977/skills/an2b-warden-governance)
- [Publisher Profile](https://clawhub.ai/user/jcools1977)
- [AN2B Technologies](https://an2b.com)
- [War/Den Documentation](https://warden.an2b.com/docs)
- [Sentinel_OS](https://getsentinelos.com)
- [EngramPort](https://engram.eideticlab.com)
- [MandelDB Registration API](https://mandeldb.com/api/v1/portal/register)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, Code, Markdown]

**Output Format:** [Markdown guidance with YAML configuration, shell commands, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce local policy decisions, audit log entries, review requirements, and setup guidance for optional enterprise services.]

## Skill Version(s):

1.0.0 (source: release metadata, frontmatter, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
