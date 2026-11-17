## Description:

Provides Fastmail JMAP command-line tools for agents to read, search, send, move, mark, trash, and list email, plus list, search, and read contacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tassiedaddy](https://clawhub.ai/user/tassiedaddy)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent interact with a Fastmail mailbox through CLI commands for inbox review, search, message reading, mailbox management, and sending email after approval. It can also access contacts when a Fastmail token includes Contacts scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad Fastmail token can enable sensitive email or contact access.

Mitigation: Use a least-privilege Fastmail token and avoid granting Contacts scope unless contact access is intentional.

Risk: Send, move, trash, and bulk contact commands can change account data with limited built-in safeguards.

Mitigation: Require explicit human approval before send, move, trash, or bulk contact commands.

Risk: Email and contact output may place private data into agent logs or transcripts.

Mitigation: Limit transcript retention and redact sensitive mailbox or contact details before sharing logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tassiedaddy/skills/fastmail-jmap-disabled)
- [JMAP protocol](https://jmap.io/)
- [Fastmail API token settings](https://app.fastmail.com/settings/security/tokens)
- [The Agent Wire](https://theagentwire.ai)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI output as plain text, JSON, or email/contact identifiers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FASTMAIL_TOKEN; FASTMAIL_IDENTITY can override the sender address for email sending.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
