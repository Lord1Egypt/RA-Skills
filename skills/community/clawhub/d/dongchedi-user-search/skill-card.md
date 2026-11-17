## Description:

Search Dongchedi creators by keyword, review their published works and engagement, and subscribe to daily updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, brands, and automotive analysts use this skill to find Dongchedi accounts, assess their public works and engagement, and follow new posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTTPS certificate checks are disabled while the RedFox API key is sent, exposing the key on untrusted networks.

Mitigation: Fix certificate validation before routine use; rotate any key already used with this version.

Risk: Subscriptions create recurring daily automations that access the RedFox service.

Mitigation: Create subscriptions only with user consent and review or remove scheduled tasks when no longer needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/redfox-data/skills/dongchedi-user-search)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown tables and summaries with links to creator profiles and works]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [User search supports pagination; work lists show 20 entries initially, with an option to show the rest; subscriptions send daily updates.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
