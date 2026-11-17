## Description:

Comprehensive AI email attendant for OpenClaw agents that checks and organizes inboxes, surfaces important messages, manages spam, supports replies, and maintains email-related state when an email MCP or equivalent tool is already connected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to delegate recurring inbox triage, spam routing, important-message tracking, reply drafting, and daily email summaries to an OpenClaw agent with existing email tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically move emails, create standard folders, and maintain email-derived state.

Mitigation: Review mailbox permissions before installation and require explicit user approval for new non-standard folders and state-changing actions.

Risk: Scheduled email checks can change how often an agent scans inboxes.

Mitigation: Use explicit opt-in for scheduling changes and confirm the affected inboxes and interval with the user.

Risk: Spam rules and domain blocking can permanently affect future routing decisions.

Mitigation: Prefer address-level blocking for broad mail providers, review permanent spam additions, and provide a clear way to reverse incorrect spam classifications.

Risk: When phone tooling is available, sender, subject, and summary details may be sent through SMS or WhatsApp.

Mitigation: Require opt-in for external notifications and limit alert content to what the user has approved for that channel.

## Reference(s):

- [Rules and State Reference](artifact/references/rules-and-state.md)
- [ClawHub Skill Listing](https://clawhub.ai/encryptshawn/skills/email-manager-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and operational guidance for email tool actions, folder routing, state updates, notifications, and reply drafts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an already connected email MCP or equivalent email tool; may update mailbox folders, persistent state, schedules, and notification logs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
