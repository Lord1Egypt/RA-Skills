## Description:

Searches past WhatsApp and chat conversations stored in a local audit-log PostgreSQL database so an agent can find, quote, or reply to previous messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and authorized operators use this skill to let an agent search local WhatsApp/chat history, retrieve conversation context, and reference prior messages by message_id. It is intended for environments where the local audit database is deliberately available to the agent and the user is authorized to search the relevant chats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose broad private chat history if the local audit database is available to the agent without clear authorization controls.

Mitigation: Install only where users are authorized to search the relevant chats and require explicit confirmation before private-history lookups.

Risk: The documented database connection uses a powerful local PostgreSQL role for direct query execution.

Mitigation: Prefer a read-only scoped database role and parameterized or fixed search commands with conservative LIMIT clauses.

Risk: Examples or outputs may reveal personal chat identifiers or sensitive message contents.

Mitigation: Remove real personal identifiers from examples and review retrieved messages for privacy before quoting or replying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/netanel-abergel/skills/chat-history-local)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with shell and SQL command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results should be limited, reviewed for privacy, and used only with authorized local chat data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
