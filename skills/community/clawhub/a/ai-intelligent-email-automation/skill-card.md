## Description:

Automates email sending, receiving, classification, and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

External teams and developers can use this skill to support email marketing, customer notifications, automatic replies, mailbox classification, template management, and read/click tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unreviewed remote email-automation code may handle credentials, mailbox contents, and message data.

Mitigation: Review the external repository at a specific commit, inspect dependencies and credential storage, and test with non-production mailboxes before deployment.

Risk: Bulk sending and auto-reply behavior can send unintended or excessive email.

Mitigation: Require explicit confirmation before sending or auto-replying, use rate limits and recipient allowlists, and start in a contained test environment.

Risk: Read and click tracking can create privacy and consent obligations.

Mitigation: Confirm tracking consent, data retention, and applicable policy requirements before enabling tracking features.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yang1002378395-cmyk/skills/ai-intelligent-email-automation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with setup commands and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include email automation workflow guidance that should be reviewed before acting on bulk sending, mailbox access, auto-replies, or tracking.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
