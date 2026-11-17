## Description:

This skill provides script-based email operations for an agent, including mailbox management, email reading and search, sending, replying, forwarding, and attachment handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tyxiang](https://clawhub.ai/user/tyxiang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let an agent work with a configured email account for mailbox review, message reading, sending, replies, forwarding, and folder organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent using this skill can operate the configured mailbox, including sending mail and deleting messages or folders.

Mitigation: Install only for intended mailbox operation, use a dedicated account, app password, or narrowly scoped OAuth grant where possible, and require human review before sends, forwards, deletes, expunges, and folder deletion.

Risk: Mailbox contents and credentials may be exposed if TLS or certificate verification is weakened or if OAuth2 token endpoints are not trusted.

Mitigation: Keep TLS and certificate verification enabled and configure only trusted OAuth token endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tyxiang/skills/ai-agent-email-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance and JSON-over-stdin/stdout script contracts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured IMAP/SMTP account settings and email credentials or OAuth2 environment variables.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
