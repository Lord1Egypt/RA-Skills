## Description:

WhatsApp Business API integration with managed OAuth for sending messages, managing templates, and handling conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[faridmalik1](https://clawhub.ai/user/faridmalik1)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to let agents interact with WhatsApp Business through Maton-managed OAuth, including sending customer messages, managing templates, handling media, and managing business profile resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send messages and update or delete WhatsApp Business resources through a live account.

Mitigation: Require explicit confirmation of recipients, phone-number IDs, template names, media IDs, and connection IDs before sending, updating, or deleting anything.

Risk: The skill relies on a Maton API key and OAuth connection authorization URLs.

Mitigation: Use a narrowly scoped Maton key where possible, never expose the full API key, and treat connection authorization URLs as secrets.

Risk: The security evidence reports unsafe examples for handling API keys and OAuth URLs.

Mitigation: Review the skill before installation for real WhatsApp Business accounts and adjust examples to avoid printing, logging, or sharing secrets.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/faridmalik1/skills/faridwahysapp)
- [Maton](https://maton.ai)
- [WhatsApp Business API Overview](https://developers.facebook.com/docs/whatsapp/cloud-api/overview)
- [WhatsApp Cloud API Send Messages](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages)
- [WhatsApp Message Templates](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates)
- [WhatsApp Media Reference](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media)
- [WhatsApp Error Codes](https://developers.facebook.com/docs/whatsapp/cloud-api/support/error-codes)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline Python, JavaScript, HTTP, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and MATON_API_KEY for live API calls]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
