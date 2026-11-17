## Description:

Helps an agent use Fastmail's JMAP API for mail search and triage, sending, masked email, contacts, calendars, sync, migrations, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to operate Fastmail through JMAP: search and triage mail, prepare and send messages, manage masked addresses, contacts, calendars, sync, and migrations while preserving account scope and reversible operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The session command can send the Fastmail bearer token to an endpoint controlled by FASTMAIL_API_BASE.

Mitigation: Use a narrowly scoped Fastmail API token, keep FASTMAIL_API_BASE unset or restricted to the official Fastmail session URL, and revoke the token immediately if it may have been sent to a non-Fastmail endpoint.

Risk: Bulk mail writes can affect the wrong account, mailbox, thread set, or object count.

Mitigation: Resolve account and mailbox ids from the session, state affected counts before writes, snapshot prior state, use ifInState, and require confirmation above the configured threshold.

Risk: The skill creates durable local records for account state, mailbox ids, identities, operations, snapshots, contacts, domains, bookings, and subscriptions.

Mitigation: Review the configured local paths before installation and keep credentials out of Clawic data files, storing only pointers such as env:FASTMAIL_API_TOKEN.

Risk: Sending mail and editing calendar events with participants can produce external side effects that are difficult or impossible to undo.

Mitigation: Verify recipients, identities, participants, and notification effects before execution; use delayed-send cancellation only when the account supports it.

## Reference(s):

- [ClawHub Fastmail API skill](https://clawhub.ai/ivangdavila/skills/fastmail-api)
- [Clawic Fastmail API skill page](https://clawic.com/skills/fastmail-api)
- [Fastmail JMAP session endpoint](https://api.fastmail.com/jmap/session)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and FASTMAIL_API_TOKEN; may create persistent local records under configured Clawic data paths for account ids, mailbox ids, operations, snapshots, bookings, contacts, domains, and subscriptions.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
