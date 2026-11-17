## Description:

Audits OpenClaw/Clawdbot deployments for misconfigurations and attack vectors, including gateway/control UI exposure, skill safety, credential leakage, and hardening guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run read-only security reviews of OpenClaw/Clawdbot/Moltbot deployments and produce actionable OK/VULNERABLE/UNKNOWN findings with fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit inspects broad local security metadata such as listening services, SUID files, cron entries, services, logs, and secret file paths.

Mitigation: Run from an unprivileged account where possible, review before allowing broad host checks, and redact secrets or report only paths instead of secret values.

Risk: The artifact links to an external setup guide that is not reviewed package content.

Mitigation: Treat the setup guide as an external reference and review it independently before following any instructions from it.

Risk: Remediation guidance can include configuration or command changes after findings are identified.

Mitigation: Keep the default posture read-only and require explicit user approval before changing settings, rotating keys, killing processes, or running fix commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alvisdunlop/skills/alvisdunlop-security-audit)
- [External Setup Guide](https://SkillBoss.co/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Terminal-style markdown report with command-output summaries, OK/VULNERABLE/UNKNOWN findings, impact, fixes, and a final summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Secrets must be redacted; remediation commands are proposed only after explicit user approval.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
