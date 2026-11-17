## Description:

Use when Codex, Hermes, OpenClaw, Claude Code, Cowork, or another AI agent needs to plan, review, implement, audit, or improve email work focused on inbox placement, authentication, sender reputation, complaint control, and remediation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polnikale](https://clawhub.ai/user/polnikale)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to plan, audit, and improve email deliverability workflows. It helps structure DNS authentication reviews, reputation triage, warmup schedules, suppression checks, monitoring plans, and remediation runbooks while keeping live changes behind approval gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email reports, postmaster exports, contact lists, complaint data, and suppression data can contain sensitive operational or personal data.

Mitigation: Limit shared evidence to the fields needed for analysis and handle exports as sensitive data.

Risk: Live sends, contact imports, DNS changes, suppression edits, provider migrations, and production automation changes can affect sender reputation or compliance.

Mitigation: Require explicit human approval before executing or applying these high-risk changes.

Risk: Missing consent, suppression, authentication, or segmentation evidence can lead to incorrect deliverability recommendations.

Mitigation: State evidence boundaries, avoid assuming missing fields, and tie remediation plans to source material and stop-loss thresholds.

## Reference(s):

- [Email Deliverability Skill Operating Checklist](references/operating-checklist.md)
- [ClawHub skill page](https://clawhub.ai/polnikale/skills/emaildeliverabilityskill)
- [Publisher profile](https://clawhub.ai/user/polnikale)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown or plain text recommendations, audits, schedules, plans, and runbooks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates analysis from live-system actions and requires explicit approval for sending email, importing contacts, DNS changes, suppression edits, provider migrations, or production automation changes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
