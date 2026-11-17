## Description:

Multi-account email management skill for IMAP/SMTP that fetches, reads, searches, composes, sends, replies, forwards, and organizes emails across multiple accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[borgcube](https://clawhub.ai/user/borgcube)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to manage email workflows across multiple IMAP/SMTP accounts, including reading, searching, sending, replying, forwarding, folder management, rules, archival, mail merge, calendar invitations, and conversation threading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles email credentials and message content.

Mitigation: Use trusted configuration files, prefer 1Password, macOS Keychain, or environment-variable credential references, and avoid plaintext secrets.

Risk: OAuth token endpoints and webhook actions can send sensitive data to external services.

Mitigation: Restrict OAuth token_uri and webhook URLs to trusted HTTPS providers before enabling rules or account profiles.

Risk: Rules can send, forward, reply to, move, archive, and expose metadata about emails.

Mitigation: Review processing rules before automation and limit rule actions to expected accounts, folders, and recipients.

Risk: Transport or state-file choices can weaken email confidentiality or reliability.

Mitigation: Keep IMAP/SMTP TLS enabled and avoid shared or /tmp state files for queues, drafts, or processing state.

## Reference(s):

- [claw-mail on ClawHub](https://clawhub.ai/borgcube/skills/claw-mail)
- [API Reference](references/REFERENCE.md)
- [Processing Rules Reference](references/RULES.md)
- [Email Templates Reference](references/TEMPLATES.md)
- [Example Configuration](assets/config.example.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, YAML configuration examples, and JSON or CLI-formatted command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include email metadata, rendered message content, draft or send results, mailbox operation results, processing results, and configuration guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter metadata.version is 0.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
