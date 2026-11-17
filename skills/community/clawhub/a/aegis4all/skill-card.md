## Description:

Audits OpenClaw security settings, explains hardening steps, and offers user-confirmed fixes and persistent guardrail rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaozheng-jc](https://clawhub.ai/user/xiaozheng-jc)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and administrators, including non-technical users, can check security settings, review a scored audit, follow hardening guides, and opt into repairs or persistent guardrail rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audits may inspect local configuration and workspace text containing sensitive settings or credentials.

Mitigation: Review what is accessed and keep credential values out of reports and shared output.

Risk: Optional repairs may alter communication, pairing, tool, or credential-handling settings and disrupt access.

Mitigation: Review each proposed change before approving it and validate configuration after edits.

Risk: Rule injection persists behavioral instructions in AGENTS.md and TOOLS.md.

Mitigation: Review the exact rule block and approve each file write separately.

## Reference(s):

- [Aegis4All on ClawHub](https://clawhub.ai/xiaozheng-jc/skills/aegis4all)
- [Understanding and mitigating the risks of OpenClaw for non-technical users](https://arxiv.org/abs/2606.11007)
- [Security guide](guides/security-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown audit report and step-by-step security guides]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scored 20-checkpoint audit; optional, separately confirmed changes to configuration or persistent workspace rules.]

## Skill Version(s):

4.0.3 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
