## Description:

Manage Agentmail.to inbox operations with deterministic Python scripts: list/read messages, download and analyze attachments, reply with sender filters, and set read/unread state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[4ur3l](https://clawhub.ai/user/4ur3l)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to manage existing Agentmail.to inboxes through repeatable script-driven workflows for listing, reading, replying, downloading attachments, analyzing attachments, and setting read state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox-changing commands can reply to messages or change read state.

Mitigation: Use a least-privileged AgentMail API key tied to a test or limited inbox, run reply flows with --dry-run first, and review matched senders before sending.

Risk: Sender filtering is not a sufficient control for security-sensitive replies.

Mitigation: Treat sender allowlists as an operational filter only, and require human review or stronger authentication before sensitive replies.

Risk: Secrets, logs, or downloaded attachments may be exposed if local repository hygiene is incomplete.

Mitigation: Create and verify .gitignore entries for .env, inbox_ops.log, downloads/, and .venv/ before storing credentials or downloading attachments.

Risk: Attachments are untrusted input and text extraction can invoke parsers on PDF or DOCX files.

Mitigation: Keep text extraction disabled unless needed, use the built-in size and timeout limits, and run attachment analysis in a sandbox or container for sensitive mail.

Risk: Dependency behavior may change without a lockfile.

Mitigation: Pin dependencies with a lockfile and run the bundled tests and dependency audit before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/4ur3l/skills/agentmail-to-inbox-ops)
- [Agentmail.to](https://www.agentmail.to/)
- [AgentMail API notes used by this skill](references/agentmail-api-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-producing script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts emit JSON for inbox messages, replies, attachment downloads, attachment analysis, and read-state changes.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
