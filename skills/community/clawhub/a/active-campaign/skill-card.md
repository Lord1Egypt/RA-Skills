## Description:

Helps agents manage ActiveCampaign contacts, deals, campaigns, and automations through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing and CRM teams use this skill to look up and manage ActiveCampaign contacts, deals, tags, lists, email campaigns, and automations. Agents require user approval before creating connections or changing data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An overly broad connection could expose more ActiveCampaign data than needed.

Mitigation: Review OAuth scopes and connect only the account needed for the task.

Risk: Writes or administrative changes may affect shared business data and access.

Mitigation: Confirm the exact account, target, and intended change with the user before each write.

Risk: Webhooks, trigger destinations, or hosted functions can cause persistent downstream effects.

Mitigation: Review the destination and behavior with the user and obtain explicit approval before enabling them.

## Reference(s):

- [Active Campaign skill release](https://clawhub.ai/byungkyu/skills/active-campaign)
- [Maton](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [ActiveCampaign API overview](https://developers.activecampaign.com/reference/overview)
- [Event trigger reference catalogs](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, API calls, Guidance]

**Output Format:** [Markdown and structured API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and new connections require explicit user approval.]

## Skill Version(s):

1.2.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
