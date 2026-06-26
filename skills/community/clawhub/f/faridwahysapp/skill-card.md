## Description: <br>
WhatsApp Business API integration with managed OAuth for sending messages, managing templates, handling media, and managing conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Faridmalik1](https://clawhub.ai/user/Faridmalik1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and business-operations teams use this skill to interact with WhatsApp Business through Maton-managed OAuth, including sending customer messages, managing message templates, and working with media, phone numbers, and business profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires credentialed WhatsApp Business access through Maton. <br>
Mitigation: Use it only when the publisher and Maton are trusted with the account, store MATON_API_KEY securely, and scope connections to the intended WhatsApp Business account. <br>
Risk: Examples include high-impact operations such as sending messages and deleting connections, media, or templates. <br>
Mitigation: Require explicit confirmation before executing send or delete actions, and replace all sample IDs and phone numbers with account-specific values. <br>
Risk: Server evidence identifies the publisher as Faridmalik1, while artifact metadata and license content reference Maton. <br>
Mitigation: Verify publisher authorization and the intended license before installation or publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Faridmalik1/faridwahysapp) <br>
- [Publisher profile](https://clawhub.ai/user/Faridmalik1) <br>
- [WhatsApp Business API Overview](https://developers.facebook.com/docs/whatsapp/cloud-api/overview) <br>
- [Send Messages](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages) <br>
- [Message Templates](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates) <br>
- [Media](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media) <br>
- [Phone Numbers](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/phone-numbers) <br>
- [Business Profiles](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/business-profiles) <br>
- [Webhooks](https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks) <br>
- [Error Codes](https://developers.facebook.com/docs/whatsapp/cloud-api/support/error-codes) <br>
- [Maton](https://maton.ai) <br>
- [Maton settings](https://maton.ai/settings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline Python, JavaScript, bash, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an authorized WhatsApp Business OAuth connection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
