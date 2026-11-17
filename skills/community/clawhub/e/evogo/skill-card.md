## Description:

Complete WhatsApp automation via Evolution API Go v3 - instances, messages (text/media/polls/carousels), groups, contacts, chats, communities, newsletters, and real-time webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[impa365](https://clawhub.ai/user/impa365)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to configure and operate Evolution API Go v3 workflows for WhatsApp instances, messaging, groups, contacts, chats, communities, newsletters, and webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact WhatsApp administration, messaging, contact, and profile operations.

Mitigation: Install it only when the agent should have real WhatsApp automation authority, and require human confirmation before deleting instances or changing profile, privacy, or group settings.

Risk: The global admin key and instance API key grant meaningful control over Evolution API Go instances and messaging.

Mitigation: Keep the global admin key tightly scoped and stored in environment variables, and use separate test and production instances.

Risk: Broadcast or mass messaging workflows can contact recipients at scale.

Mitigation: Send broadcasts only to recipients who have opted in, test with small groups first, and use delays or backoff as described by the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/impa365/skills/evogo)
- [Evolution API Go](https://github.com/EvolutionAPI/evolution-api)
- [WhatsApp Business API Documentation](https://developers.facebook.com/docs/whatsapp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request bodies and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Evolution API URL, global admin key, instance name, and instance API key.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
