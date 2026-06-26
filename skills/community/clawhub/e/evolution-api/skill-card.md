## Description: <br>
Complete WhatsApp automation via Evolution API v2.3 - instances, messages (text/media/polls/lists/buttons/status), groups, labels, chatbots (Typebot/OpenAI/Dify/Flowise/N8N/EvoAI), webhooks, proxy, S3 storage, and Chatwoot integration <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[impa365](https://clawhub.ai/user/impa365) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure and operate Evolution API v2.3 for WhatsApp messaging, instance management, groups, chatbots, webhooks, storage, and Chatwoot workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through real WhatsApp messaging and administrative Evolution API operations, including sending messages, deleting instances, and changing chat or group state. <br>
Mitigation: Review commands before execution, verify instance names and recipients, and prefer instance-scoped keys for messaging operations. <br>
Risk: Global and instance API keys can grant broad access to Evolution API resources. <br>
Mitigation: Store keys only in environment variables or a secrets manager, restrict access to the global admin key, and rotate credentials if they are exposed. <br>
Risk: Webhook, queue, Chatwoot, chatbot, media forwarding, and triggerType "all" configurations can send message data to external services. <br>
Mitigation: Enable integrations only for trusted destinations with consent, retention controls, and a clear need for the selected event scope. <br>


## Reference(s): <br>
- [Evolution API](https://github.com/EvolutionAPI/evolution-api) <br>
- [Evolution API Documentation](https://doc.evolution-api.com) <br>
- [Chatwoot](https://www.chatwoot.com) <br>
- [Typebot](https://typebot.io) <br>
- [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Evolution API URL, instance name, global admin key, and instance API key.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
