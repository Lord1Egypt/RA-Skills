## Description:

Provides web content fetching, caching, document OCR, real-time messaging, group chats, file transfers, and webhook integrations via Prismer Cloud APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ooxxxxoo](https://clawhub.ai/user/ooxxxxoo)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to configure Prismer Cloud CLI and SDK access for context loading, document parsing, IM workflows, file transfer, and real-time message delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send selected files, documents, web requests, and messages to Prismer Cloud.

Mitigation: Review data selection before use and only process information appropriate for Prismer Cloud handling.

Risk: The skill asks for live credentials in chat or command arguments, including API keys, JWTs, webhook secrets, and bot tokens.

Mitigation: Use secure local login, environment variables, a secret manager, or interactive prompts; avoid pasting secrets into chat and rotate exposed credentials.

Risk: The install flow uses a mutable global npm package.

Mitigation: Prefer pinned package versions and review the installed package before deployment.

## Reference(s):

- [Prismer Cloud documentation](https://prismer.cloud/docs)
- [Prismer Cloud](https://prismer.cloud)
- [ClawHub skill page](https://clawhub.ai/ooxxxxoo/skills/agent-im)
- [Publisher profile](https://clawhub.ai/user/ooxxxxoo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell, JSON, TOML, TypeScript, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Prismer Cloud CLI or SDK access and may involve external URLs, documents, messages, file uploads, API keys, JWTs, webhook secrets, or bot tokens.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
