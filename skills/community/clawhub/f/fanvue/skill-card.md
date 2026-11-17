## Description:

Manage content, chats, subscribers, and earnings on the Fanvue creator platform via OAuth 2.0 API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igorls](https://clawhub.ai/user/igorls)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to integrate with Fanvue creator accounts for OAuth authentication, chat and message operations, post management, media access, subscriber data, and earnings insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad access to OAuth tokens, private media links, subscriber identities, spending and earnings data, posts, and messages.

Mitigation: Use it only for Fanvue accounts where the agent is explicitly allowed to handle that data, and avoid logging or retaining tokens, signed media URLs, subscriber lists, or financial data.

Risk: The skill includes account-facing write operations such as posting, deleting, sending messages, and mass messaging.

Mitigation: Require explicit confirmation before posting, deleting, sending any message, or mass messaging.

Risk: Over-broad OAuth scopes may expose more account data or actions than a workflow needs.

Mitigation: Request only the OAuth scopes required for the specific task and review creator-account-only endpoints before use.

## Reference(s):

- [Fanvue API Documentation](https://api.fanvue.com/docs)
- [Fanvue OAuth 2.0 Guide](https://api.fanvue.com/docs/authentication/quick-start)
- [Fanvue Developer Portal](https://fanvue.com/developers/apps)
- [Fanvue App Starter Kit](https://github.com/fanvue/fanvue-app-starter)
- [Skill source: SKILL.md](artifact/SKILL.md)
- [Skill source: API reference](artifact/api-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript examples, HTTP endpoint references, and environment variable instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Fanvue OAuth credentials, access tokens, appropriate scopes, and API version header X-Fanvue-API-Version: 2025-06-26.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
