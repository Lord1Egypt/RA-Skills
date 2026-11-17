## Description:

Call EngageLab WhatsApp Business REST APIs to send WhatsApp messages, manage WABA message templates, and handle callback webhooks for delivery status and user responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devengagelab](https://clawhub.ai/user/devengagelab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to integrate EngageLab WhatsApp Business messaging into applications, including template messages, session messages, template lifecycle management, and callback handling for delivery and user-response events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles EngageLab credentials and can affect live WhatsApp messaging resources.

Mitigation: Use scoped credentials, avoid production keys while testing, and review generated API calls before execution.

Risk: The bundled client permits overriding the API base URL.

Mitigation: Override the base URL only in controlled test environments with non-production credentials.

Risk: Template deletion and updates can affect approved business messaging workflows.

Mitigation: Confirm exact template names, template IDs, languages, and intended operation before changing or deleting templates.

Risk: Callback security is not complete in the artifact guidance.

Mitigation: Add independent webhook protections such as a shared-secret gateway, schema validation, replay checks, and rate limiting before trusting callbacks.

## Reference(s):

- [EngageLab WhatsApp Business skill page](https://clawhub.ai/devengagelab/skills/engagelab-whatsapp-business)
- [EngageLab console](https://www.engagelab.com)
- [WhatsApp Callback API Reference](references/callback-api.md)
- [EngageLab WhatsApp API Error Codes](references/error-codes.md)
- [WhatsApp Template Management API Reference](references/template-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples, shell commands, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API request payloads, curl commands, Python client usage, webhook handling guidance, and template-management instructions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
