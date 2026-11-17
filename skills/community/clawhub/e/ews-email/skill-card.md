## Description:

CLI to manage enterprise Outlook emails via Exchange Web Services (EWS).

This skill is ready for commercial/non-commercial use.

## Publisher:

[guyun94](https://clawhub.ai/user/guyun94)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agents with authorized Exchange mailbox access use this skill to list, search, read, send, reply, forward, move, delete, and flag messages, and to download attachments through EWS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Attachment downloads may write outside the chosen folder or overwrite existing files because attachment filenames are not sanitized.

Mitigation: Avoid attachment-download until filename sanitization and overwrite protection are added; use an isolated download directory when handling attachments.

Risk: Headless Linux setup can weaken mailbox credential protection if KEYRING_CRYPTFILE_PASSWORD is stored in readable config, shell profiles, logs, or service files.

Mitigation: Use a platform secret manager or tightly scoped secret injection, and restrict access to any environment or service configuration containing the keyring password.

Risk: The skill has full access to the configured Exchange mailbox and can send, move, delete, and forward messages.

Mitigation: Install only for trusted agents and accounts with the minimum mailbox permissions needed for the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guyun94/skills/ews-email)
- [ClawHub publisher profile](https://clawhub.ai/user/guyun94)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and plain-text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads and changes Exchange mailbox state; message body output is truncated after 8000 characters by the CLI.]

## Skill Version(s):

1.2.0 (source: evidence release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
