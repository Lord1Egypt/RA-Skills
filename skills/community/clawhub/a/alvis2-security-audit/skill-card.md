## Description:

Audits OpenClaw and Clawdbot deployments for misconfigurations, exposed gateway or control UI surfaces, unsafe skill or tool policy, credential leakage, and hardening opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and security reviewers use this skill to inspect OpenClaw, Clawdbot, or Moltbot deployments for configuration, exposure, credential, permissions, persistence, and logging risks before or after deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to inspect local host configuration, ports, processes, logs, permissions, and persistence indicators.

Mitigation: Use it only when local security-audit inspection is intended, and keep execution read-only unless the user explicitly approves remediation.

Risk: Audit output may encounter credential locations or secret-adjacent evidence.

Mitigation: Redact secret values and report paths or summaries instead of sensitive contents.

Risk: The linked external setup guide was not part of the local artifact evidence.

Mitigation: Review that guide separately before relying on any setup or operational instructions from it.

## Reference(s):

- [Complete setup guide](https://SkillBoss.co/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Terminal report with Markdown-style sections and status labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports each check as OK, VULNERABLE, or UNKNOWN with evidence, impact, and fix guidance.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
