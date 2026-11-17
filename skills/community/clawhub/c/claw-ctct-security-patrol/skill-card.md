## Description:

Claw Ctct Security Patrol guides an OpenClaw agent through host security checks, optional scheduled audits, and concise report interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamwang-wh](https://clawhub.ai/user/williamwang-wh)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to run local or network-assisted security patrols, generate audit reports, configure recurring checks, and receive plain-language interpretation of scan results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs broad host inspection during security audits.

Mitigation: Run it only when host-wide inspection is intended, prefer local-only mode first, and avoid running it as root.

Risk: The network-assisted mode can send device identifiers, installed-skill metadata, and summarized findings to a remote service.

Mitigation: Use the local scan mode unless remote threat intelligence and reporting are explicitly acceptable.

Risk: Scheduled audits can repeatedly run the network-assisted command if automation is enabled.

Mitigation: Review the OpenClaw cron command, recipient, timeout, and push setting before enabling recurring audits.

## Reference(s):

- [OpenClaw Security Patrol Cron Setup Guide](references/cron-setup.md)
- [ClawHub Skill Page](https://clawhub.ai/williamwang-wh/skills/claw-ctct-security-patrol)
- [Publisher Profile](https://clawhub.ai/user/williamwang-wh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and concise text with shell commands and report paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes scan counts, security score, report location, and optional report interpretation instead of returning full audit logs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
