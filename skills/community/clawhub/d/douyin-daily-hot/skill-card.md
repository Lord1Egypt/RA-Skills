## Description:

Queries daily Douyin popular-work rankings by category or date and presents linked results in a Markdown table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

People tracking Douyin content trends can use the skill to review daily like-ranked works across categories or historical dates. It returns a linked Markdown ranking and offers subscription options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install payment software and initiate a recharge using payment details returned by the API.

Mitigation: Require user approval before installing payment software or starting a recharge, use a reviewed fixed software version, and independently verify the payment destination and exact amount before proceeding.

## Reference(s):

- [API Configuration](references/api-config.md)
- [Payment Flow and Safeguards](references/alipay-recharge.md)
- [Interaction Guide](references/interaction-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/douyin-daily-hot)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown table with linked Douyin works]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows up to 20 entries by default and up to 50 on request; rankings can be filtered by category or date. Engagement figures reflect collection-time snapshots and may differ from live totals.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
