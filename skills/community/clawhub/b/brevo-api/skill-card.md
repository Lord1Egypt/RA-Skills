## Description:

Connects an agent to Brevo for managing contacts, lists, campaigns, templates, transactional email, and SMS through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers use this skill to retrieve Brevo account data and, with explicit approval, manage marketing contacts, send messages, and run campaigns. Optional automations can perform approved Brevo actions on a schedule or in response to events from separately connected sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorizing an account may grant access to sensitive Brevo contact and message data.

Mitigation: Approve each new connection, review OAuth scopes, and disclose only the data needed for the requested task.

Risk: Sending campaigns or deleting records can have irreversible customer-facing effects.

Mitigation: Confirm every write or send action; before a campaign send, review its audience, sender, subject, and recipient count.

Risk: Functions, triggers, destinations, and event-watch handlers can create ongoing actions or data forwarding.

Mitigation: Create automation only with explicit approval, limit event scope and destinations, and review any handler before it runs.

## Reference(s):

- [Brevo skill on ClawHub](https://clawhub.ai/byungkyu/skills/brevo-api)
- [Maton](https://maton.ai)
- [Brevo API documentation](https://developers.brevo.com/)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with CLI commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may contain contact details and message content; return only fields needed for the user's task.]

## Skill Version(s):

1.2.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
