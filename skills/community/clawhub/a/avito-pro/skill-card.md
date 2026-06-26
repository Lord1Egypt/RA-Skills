## Description: <br>
Provides Avito API guidance for OAuth authorization, messenger chats, listings, statistics, scopes, and request examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thisisevgeniy](https://clawhub.ai/user/thisisevgeniy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to draft and review Avito API integrations for authentication, messaging workflows, listing information, statistics, paid services, and webhook management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Avito client secrets and bearer tokens may be exposed when real credentials are pasted into prompts, command examples, or logs. <br>
Mitigation: Use the minimum required scopes, keep secrets and bearer tokens out of prompts and logs, and substitute placeholders in examples. <br>
Risk: Messaging, media upload, webhook, and paid-service endpoints can affect real Avito accounts or customers. <br>
Mitigation: Require explicit user approval before sending messages, uploading media, changing webhooks, or applying VAS services. <br>
Risk: Webhook subscriptions may continue receiving account events after they are no longer needed. <br>
Mitigation: Track webhook subscriptions and unsubscribe when an integration is retired or no longer requires event delivery. <br>


## Reference(s): <br>
- [Avito Developer Documentation](https://developers.avito.ru/) <br>
- [Avito Pro on ClawHub](https://clawhub.ai/thisisevgeniy/avito-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API request examples] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; the skill describes API usage and request shapes but does not execute API calls by itself.] <br>

## Skill Version(s): <br>
2026.3.16 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
