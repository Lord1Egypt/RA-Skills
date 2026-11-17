## Description:

Работа с API Авито (Авторизация, Мессенджер, Объявления, Статистика). Позволяет получать токены, читать/отправлять сообщения в чатах Авито и управлять объявлениями.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thisisevgeniy](https://clawhub.ai/user/thisisevgeniy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to work with Avito API authentication, messenger workflows, listings, statistics, webhooks, scopes, and CRM integration patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth client secrets and bearer tokens may be exposed through logs, commits, or chat transcripts.

Mitigation: Keep credentials out of shared text, store them in approved secret storage, and redact tokens before sharing agent outputs.

Risk: Agent-generated Avito API calls can send messages, modify listings, or apply paid services when authorized.

Mitigation: Use least-privilege scopes and require explicit human approval before write actions or paid service operations.

## Reference(s):

- [Avito API Documentation](https://developers.avito.ru/)
- [ClawHub Skill Page](https://clawhub.ai/thisisevgeniy/skills/avito-pro)
- [Publisher Profile](https://clawhub.ai/user/thisisevgeniy)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with API endpoint examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OAuth parameters, scope names, webhook details, JSON request bodies, and cURL examples.]

## Skill Version(s):

2026.3.16 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
