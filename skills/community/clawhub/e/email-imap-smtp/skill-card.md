## Description:

Connect to mainstream email providers and perform reliable send/receive workflows through IMAP and SMTP with password or OAuth2 authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wazixuan](https://clawhub.ai/user/wazixuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect mailbox accounts, test IMAP/SMTP access, list or search messages, read selected email bodies, refresh OAuth2 tokens, generate OAuth2 authorization URLs, and send emails with optional HTML or attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox passwords, app passwords, OAuth2 access tokens, refresh tokens, and client secrets can be exposed through command history, logs, repository files, or terminal output.

Mitigation: Use environment variables or another protected secret mechanism, avoid storing credentials in repository files, and do not use token-display options unless disclosure is intentional.

Risk: OAuth token refresh can send sensitive token material to a configured token endpoint.

Mitigation: Use only known HTTPS OAuth token endpoints from trusted providers or tenant-controlled identity systems.

Risk: The send workflow can transmit email content and attachments to unintended recipients.

Mitigation: Preview recipients, subject, body, HTML content, and attachment list before sending mail.

## Reference(s):

- [Provider presets](artifact/references/provider-presets.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-style command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or request email credentials, OAuth2 token material, OAuth2 authorization URLs, mailbox summaries, message content, attachment names, and send-status results.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
