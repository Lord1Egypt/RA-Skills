## Description:

Evolution Api v2 helps agents guide WhatsApp automation with Evolution API v2.3, including instance management, messaging, groups, chatbots, webhooks, proxy, S3 storage, and Chatwoot integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[impa365](https://clawhub.ai/user/impa365)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure and operate Evolution API v2.3 WhatsApp automation workflows, including messaging, groups, chatbots, webhooks, and Chatwoot handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide administration of live WhatsApp automation servers, including delete, logout, group, and profile operations.

Mitigation: Use least-privilege instance keys and require explicit confirmation before destructive or account-changing operations.

Risk: Webhook and chatbot workflows may forward message content or media to external services.

Mitigation: Prefer HTTPS endpoints, avoid public webhook collectors for real data, narrow webhook events and chatbot triggers, and confirm consent before broadcasts or imports.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/impa365/skills/evolution-api)
- [Evolution API Documentation](https://doc.evolution-api.com)
- [Evolution API Repository](https://github.com/EvolutionAPI/evolution-api)
- [WhatsApp Business API Documentation](https://developers.facebook.com/docs/whatsapp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, and API endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Evolution API endpoint and global or instance API keys supplied through environment variables.]

## Skill Version(s):

2.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
