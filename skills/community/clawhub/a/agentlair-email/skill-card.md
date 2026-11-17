## Description:

Give your agent a real email address via REST API. Claim @agentlair.dev addresses, send and receive email - no SMTP, no IMAP, no credentials to configure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hawkaa](https://clawhub.ai/user/hawkaa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to claim an AgentLair email identity, send email, check inboxes, and read messages through REST API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email content and recipient data are sent through AgentLair and its email processing path.

Mitigation: Use the skill only for user-approved email activity and avoid regulated or sensitive information unless the organization has approved AgentLair and Amazon SES as processors.

Risk: AGENTLAIR_API_KEY grants access to the email API for the associated account.

Mitigation: Treat AGENTLAIR_API_KEY as a secret, keep it in environment or secret storage, and avoid logging or committing it.

Risk: Sending email has external side effects and may contact unintended recipients if parameters are wrong.

Mitigation: Review recipients, sender address, subject, and message body before executing send requests.

## Reference(s):

- [AgentLair homepage](https://agentlair.dev)
- [ClawHub skill page](https://clawhub.ai/hawkaa/skills/agentlair-email)
- [Publisher profile](https://clawhub.ai/user/hawkaa)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline curl commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and AGENTLAIR_API_KEY for authenticated email API calls.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
