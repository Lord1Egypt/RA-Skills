## Description:

Connect OpenClaw to self-hosted Fluxmail and work with Gmail, Outlook, and IMAP mailboxes through its MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[churichard](https://clawhub.ai/user/churichard)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users connect existing Gmail, Outlook, or IMAP mailboxes to Fluxmail to search and summarize messages or prepare drafts, with permission checks before mailbox changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting a mailbox exposes sensitive email to the selected service and account scope.

Mitigation: Install only if you trust Fluxmail; check the connected account and start with the read-only permission profile.

Risk: Sending, deleting, scheduling, or bulk changes can alter mail or reach unintended recipients.

Mitigation: Enable write access only when needed, and confirm recipients and message contents before approving send or bulk actions.

## Reference(s):

- [Fluxmail quickstart](https://fluxmail.ai/docs/quickstart)
- [Fluxmail permission profiles](https://fluxmail.ai/docs/permissions)
- [Fluxmail MCP connection guide](https://fluxmail.ai/docs/connect-an-mcp-client)
- [Fluxmail plans and licensing](https://fluxmail.ai/docs/teams-and-plans)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include mailbox summaries and draft email text.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
