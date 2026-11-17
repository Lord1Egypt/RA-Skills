## Description:

Helps an agent operate an authorized Famulor workspace through its hosted MCP server, from assistants and conversation history to campaigns, telephony, automations, billing, and settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bekservice](https://clawhub.ai/user/bekservice)

### License/Terms of Use:

MIT-0

## Use Case:

Famulor workspace users and administrators use this skill to inspect workspace data and perform authorized assistant, customer communication, telephony, automation, and account-management tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad workspace permissions could permit consequential changes to messages, calls, campaigns, billing, and account settings.

Mitigation: Limit OAuth scopes and workspace roles; require explicit confirmation of the target and action before high-impact operations.

Risk: Exports and conversation history can contain sensitive customer information.

Mitigation: Confirm workspace authorization and purpose, retrieve only necessary data, and share exports only with the authorized user.

Risk: Unattended routines and credit-consuming actions may continue or incur charges after initiation.

Mitigation: Review schedule, scope, and costs with the user, obtain explicit approval, and check the returned task status.

## Reference(s):

- [Famulor skill release on ClawHub](https://clawhub.ai/bekservice/skills/famulor-skill)
- [Project homepage listed in skill metadata (not verified as release provenance)](https://github.com/bekservice/Famulor-Skill)
- [Assistant design and onboarding](references/assistant-design.md)
- [Messaging toolset](references/toolsets/messaging.md)
- [Billing toolset](references/toolsets/billing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language summaries, action confirmations, and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report workspace resource IDs, links, and asynchronous task status when relevant and authorized.]

## Skill Version(s):

2.1.3 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
