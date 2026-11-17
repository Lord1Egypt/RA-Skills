## Description:

Manage contacts, campaigns, automations, lists, and marketing workflows in ActiveCampaign via the ActiveCampaign API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing operators use this skill to manage ActiveCampaign contacts, lists, campaigns, automations, deals, webhooks, and bulk marketing workflows from an agent chat using ClawLink-hosted OAuth authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and persistently allowlists an external OAuth-backed ClawLink plugin.

Mitigation: Install only after trusting the publisher and plugin, and check the plugin version and removal path before enabling it.

Risk: ActiveCampaign write operations can create, update, or delete contacts, deals, lists, campaigns, webhooks, connections, and bulk records.

Mitigation: Require live tool discovery, preview the exact action, and obtain explicit user approval before every write, delete, webhook, connection, bulk import, or bulk delete call.

Risk: Direct write examples may be executed without enough context if an agent skips the skill's confirmation workflow.

Mitigation: Use read, list, search, get, and describe operations before writes, then execute only after the preview matches the user's stated intent.

## Reference(s):

- [ActiveCampaign API Overview](https://developers.activecampaign.com/reference/overview)
- [ActiveCampaign Contact API](https://developers.activecampaign.com/reference/create-contact)
- [ActiveCampaign Deal API](https://developers.activecampaign.com/reference/deals)
- [ActiveCampaign Automation API](https://developers.activecampaign.com/reference/automations)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with inline bash commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live ClawLink tool discovery; write, delete, webhook, connection, bulk import, and bulk delete actions require preview and explicit user approval.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
