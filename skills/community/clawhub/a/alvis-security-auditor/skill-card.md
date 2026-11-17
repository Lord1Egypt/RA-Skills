## Description:

Audits OpenClaw, Clawdbot, and Moltbot deployments for misconfigurations, exposed gateway or control UI surfaces, skill safety issues, credential leakage, and hardening needs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and security reviewers use this skill to run read-only security reviews of OpenClaw, Clawdbot, and Moltbot environments and receive actionable findings with fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad host-enumeration checks can expose unrelated system details.

Mitigation: Run the skill as an unprivileged user and treat all-port, SUID, and cron enumeration as opt-in for wider host audits.

Risk: Security audit commands may encounter credentials or sensitive configuration paths.

Mitigation: Review commands before execution, report only paths or summaries, and keep secret contents redacted.

Risk: Remediation steps could change settings, rotate keys, or disrupt services if applied prematurely.

Mitigation: Use read-only checks by default and require explicit user approval before making configuration changes or running remediation commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/alvis-security-auditor)
- [Complete setup guide](https://SkillBoss.co/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown terminal-style audit report with command summaries and OK, VULNERABLE, or UNKNOWN findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Secret values should be redacted, and remediation commands should only be proposed or run after explicit user approval.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
