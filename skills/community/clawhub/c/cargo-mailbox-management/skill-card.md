## Description:

Guides Cargo CLI users through provisioning and managing mailboxes, warm-up, sending controls, and email activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to provision and manage Cargo sending inboxes, monitor warm-up and send allowances, and review sends, replies, and suppressions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sending commands take effect immediately, and the CLI has no dry run.

Mitigation: Test with your own address, including suppression tests, before sending to others.

Risk: Mailbox provisioning creates recurring monthly charges, and removal deletes the mailbox at the provider.

Mitigation: Confirm the active workspace and get approval for recurring costs before provisioning; confirm the intended mailbox before deletion.

Risk: Cargo handles mailbox credentials, messages, replies, and tracking data.

Mitigation: Redact secrets from support reports and pin a reviewed CLI version.

## Reference(s):

- [Sending domains](references/sending-domains.md)
- [Sending](references/sending.md)
- [Warm-up and allowance](references/warmup-and-allowance.md)
- [Troubleshooting](references/troubleshooting.md)
- [Cargo Skills repository](https://github.com/getcargohq/cargo-skills)
- [ClawHub skill page](https://clawhub.ai/cargo-ai/skills/cargo-mailbox-management)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with Bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mailbox setup, warm-up, sending, and activity review workflows.]

## Skill Version(s):

1.5.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
