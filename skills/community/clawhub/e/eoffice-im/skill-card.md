## Description:

泛微 e-office 即时通讯（IM）WebSocket API - 私聊、群聊等

This skill is ready for commercial/non-commercial use.

## Publisher:

[quanruxiaohong](https://clawhub.ai/user/quanruxiaohong)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, developers, and operators use this skill to guide an agent through e-office IM WebSocket workflows for private chat, group chat, message state changes, online status checks, offline message retrieval, and group membership management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad authenticated messaging and group-management actions can expose message content or affect users and groups if used without clear authorization.

Mitigation: Install only for a trusted e-office IM environment, use narrowly scoped and revocable tokens, and require explicit confirmation before sending, reading, deleting, withdrawing, changing status, or modifying group membership.

Risk: Insecure endpoint examples and token handling could expose credentials or message content.

Mitigation: Prefer wss/https endpoints and avoid placing real tokens in prompts, examples, logs, or shared configuration.

## Reference(s):

- [e-office IM API reference](artifact/references/im-api.md)
- [Project homepage from ClawHub metadata](https://github.com/yourname/eoffice-im-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Socket.IO examples, configuration snippets, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EOFFICE_IM_BASE_URL and EOFFICE_IM_TOKEN configuration for a trusted e-office IM environment.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
