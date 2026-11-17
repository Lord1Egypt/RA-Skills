## Description:

Autonomous manager and executive operator guidance for the ARGOS crypto trading-bot ecosystem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felix1983](https://clawhub.ai/user/felix1983)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to guide ARGOS bot monitoring, debugging, user and payment administration, marketing operations, scheduled reporting, and operational documentation. It is intended for a tightly controlled ARGOS environment because the guidance covers credentials, process restarts, persistent jobs, and external notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad autonomous control over a trading-bot system, including credentials, persistent jobs, and external Telegram reporting.

Mitigation: Install only in a tightly controlled ARGOS environment and require explicit approval before code changes, restarts, cron jobs, payments, or public posts.

Risk: Credential discovery across home directories can expose secrets and expand operational access.

Mitigation: Replace broad /home .env discovery with a fixed secret source and grant only the minimum required filesystem access.

Risk: Telegram reports and marketing workflows can expose user identifiers, payment details, or operational status externally.

Mitigation: Disable or gate Telegram reporting and redact user IDs, payment details, and sensitive operational information before sending notifications.

Risk: Whole-system or sudo-level access can allow unintended changes outside the ARGOS application.

Mitigation: Avoid sudo and whole-filesystem access unless separately approved for a specific maintenance action.

## Reference(s):

- [Atlas Argos ClawHub skill page](https://clawhub.ai/felix1983/skills/atlas-argos)
- [felix1983 ClawHub publisher profile](https://clawhub.ai/user/felix1983)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Portuguese operational procedures for ARGOS, including monitoring, restart, reporting, marketing, and payment-management workflows.]

## Skill Version(s):

0.1.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
