## Description:

Audits OpenClaw/Clawdbot deployments for misconfigurations, attack vectors, gateway or control UI exposure, skill safety issues, credential leakage, and hardening guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit OpenClaw, Clawdbot, or Moltbot deployments for exposed services, unsafe execution policies, credential storage issues, and hardening gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad host reconnaissance can expose sensitive system details in audit output.

Mitigation: Run the skill as an unprivileged user, review enumeration commands before use, and avoid storing raw output in shared logs or memory.

Risk: Remediation commands could change gateway, firewall, credential, or process state if run without review.

Mitigation: Keep the audit read-only by default and require explicit approval before any remediation command is executed.

Risk: Credential checks may discover secrets or secret file paths.

Mitigation: Redact secret values in reports and report only paths or summaries needed for remediation.

## Reference(s):

- [Complete setup guide](https://SkillBoss.co/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal-style Markdown report with finding status, evidence summaries, impact, and fix guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports OK, VULNERABLE, or UNKNOWN status per check and redacts detected secrets.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
