## Description:

Send and receive email as an AI agent, including checking inboxes, sending messages, replying, setting up aliases, and managing agent email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent manage an Agnic email alias, check recent inbox messages, send email, and reply to messages through the Agnic CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can read inbox contents and send email through the configured Agnic account.

Mitigation: Install only after review, use a scoped and revocable token, and require user confirmation before sending or replying to email.

Risk: The skill uses npx agnic@latest, so the executed CLI can change after review.

Mitigation: Pin and review the Agnic CLI version before deployment instead of relying on the latest npm release.

Risk: Passing tokens on the command line can expose credentials through shell history or process listings.

Mitigation: Provide credentials through a managed AGNIC_TOKEN environment secret and rotate or revoke the token when access is no longer needed.

Risk: Unvalidated recipient, subject, body, or message ID values could alter shell command behavior.

Mitigation: Validate email addresses and message IDs, reject shell metacharacters where required, and quote or escape subject and body values before constructing commands.

## Reference(s):

- [Agnic app](https://app.agnic.ai)
- [ClawHub skill listing](https://clawhub.ai/agnicpay-prog/skills/agnic-agent-email)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-producing CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that read inbox contents, configure an email alias, send messages, or reply to messages.]

## Skill Version(s):

2.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
