## Description:

Check Point R80+/R81.x rulebase layer analysis with blade activation audit, SmartConsole management plane validation, NAT policy review, identity awareness assessment, and compliance verification for Security Gateways managed by a Management Server or Multi-Domain Server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Network security engineers and auditors use this skill to conduct read-only Check Point firewall policy audits across rulebases, Software Blades, NAT, identity awareness, logging, and compliance posture. It is intended for authorized reviews of R80.x and R81.x environments managed through SmartConsole, Management Server, or Multi-Domain Server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit can reveal sensitive firewall rules, objects, identity roles, and logs.

Mitigation: Run it only in authorized environments, use read-only accounts where possible, and handle outputs as sensitive security data.

Risk: Remediation recommendations could affect production traffic if applied without review.

Mitigation: Treat remediation steps as advisory until approved through a separate change-management window.

## Reference(s):

- [Check Point R80+ Policy Architecture](references/policy-model.md)
- [Check Point CLI and API Reference](references/cli-reference.md)
- [ClawHub skill page](https://clawhub.ai/vahagn-madatyan/skills/checkpoint-firewall-audit)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with inline shell commands, API examples, findings, and audit report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only audit workflow; remediation steps are advisory and should be reviewed before any approved change window.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
