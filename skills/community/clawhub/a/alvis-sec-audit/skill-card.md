## Description:

Audit OpenClaw/Clawdbot deployments for misconfigurations and attack vectors, including gateway exposure, skill safety, credential leakage, and hardening gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect OpenClaw, Clawdbot, or Moltbot environments for common security misconfigurations and produce an actionable terminal audit report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may gather broad host-level security posture details.

Mitigation: Run it in a controlled session and limit checks to OpenClaw paths unless broader inspection is explicitly approved.

Risk: Configuration secrets may be exposed to the agent context during inspection.

Mitigation: Ask the agent to inspect non-secret fields by default and redact any detected secrets in reports.

Risk: Whole-host enumeration or complete config-file reads can expose unnecessary sensitive information.

Mitigation: Require explicit approval before broad enumeration or full config-file reads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/alvis-sec-audit)
- [Publisher profile](https://clawhub.ai/user/alvisdunlop)
- [Setup guide](https://SkillBoss.co/skill.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown terminal report with command-output summaries and remediation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are labeled OK, VULNERABLE, or UNKNOWN and should redact detected secrets.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
