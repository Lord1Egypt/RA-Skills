## Description: <br>
Manage contacts, campaigns, automations, lists, and marketing workflows in ActiveCampaign via the ActiveCampaign API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, sales, and operations teams use this skill to manage ActiveCampaign contacts, lists, campaigns, automations, deals, webhooks, and related marketing workflows from an agent chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform chat-driven writes to marketing, sales, and customer records, including bulk imports, deletions, webhooks, and campaign or deal changes. <br>
Mitigation: Review ClawLink previews carefully and require explicit user confirmation before any create, update, delete, bulk, webhook, or campaign action. <br>
Risk: Using the skill requires connecting an ActiveCampaign account through ClawLink, which grants access to account marketing data according to the connected user's permissions. <br>
Mitigation: Install only when the user is comfortable with the ClawLink OAuth connection and scope access to the intended ActiveCampaign account. <br>


## Reference(s): <br>
- [ActiveCampaign Skill Page](https://clawhub.ai/hith3sh/activecampaign-marketing) <br>
- [ActiveCampaign API Overview](https://developers.activecampaign.com/reference/overview) <br>
- [ActiveCampaign Contacts API](https://developers.activecampaign.com/reference/create-contact) <br>
- [ActiveCampaign Deals API](https://developers.activecampaign.com/reference/deals) <br>
- [ActiveCampaign Automations API](https://developers.activecampaign.com/reference/automations) <br>
- [ClawLink Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool-call parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected ActiveCampaign account through ClawLink; write operations should be previewed and explicitly confirmed.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
