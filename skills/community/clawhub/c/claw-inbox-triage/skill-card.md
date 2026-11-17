## Description:

Automates inbox management by categorizing messages into urgent, normal, or spam, generating daily digests, and drafting responses for low-priority items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigas](https://clawhub.ai/user/indigas)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users use this skill to triage message exports, prioritize urgent items, produce daily digests, and draft responses for non-urgent messages for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes private message exports and may store digests or drafts in user-selected output files.

Mitigation: Run it only on message exports you intentionally provide, avoid sensitive or regulated conversations unless output storage is understood, and review generated files before sharing.

Risk: Rules can downplay account-security, login, password, verification, or recovery messages.

Mitigation: Manually review those messages and do not rely on generated priority labels for account-security decisions.

Risk: Installing or running unverified local scripts can expose users to supply-chain risk.

Mitigation: Pin or verify the installer and review the skill before installing or executing it.

## Reference(s):

- [Priority Classification Rules](references/priority-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/indigas/skills/claw-inbox-triage)

## Skill Output:

**Output Type(s):** [text, markdown, json, configuration, guidance]

**Output Format:** [Markdown or JSON daily digest with optional text draft responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes urgent, normal, and spam categories; outputs should be reviewed before action.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
