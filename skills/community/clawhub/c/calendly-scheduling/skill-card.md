## Description: <br>
Manage Calendly events, invitees, scheduling links, webhooks, and availability via the Calendly API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to manage Calendly scheduling workflows from an agent, including events, invitees, event types, availability, scheduling links, webhooks, and organization-related actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to a Calendly account through OAuth and can read or change Calendly resources. <br>
Mitigation: Install only if the user is comfortable connecting Calendly through ClawLink, and keep access scoped to the intended account. <br>
Risk: Write operations can create, update, cancel, delete, invite, revoke, or remove Calendly resources. <br>
Mitigation: Review the write-operation preview and require explicit user confirmation before executing any write or destructive action. <br>
Risk: The integration requires sensitive OAuth credentials for the connected account. <br>
Mitigation: Use the hosted OAuth connection flow and avoid asking the user to paste Calendly credentials or API tokens into chat. <br>


## Reference(s): <br>
- [Calendly API Documentation](https://developer.calendly.com/) <br>
- [Calendly Scheduled Events API](https://developer.calendly.com/api-docs/evedefaultapi/scheduled-events) <br>
- [Calendly Webhook Subscriptions](https://developer.calendly.com/api-docs/webhook-subscriptions) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/calendly-scheduling) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Calendly tool names, JSON parameters, setup steps, previews, and confirmation guidance.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
