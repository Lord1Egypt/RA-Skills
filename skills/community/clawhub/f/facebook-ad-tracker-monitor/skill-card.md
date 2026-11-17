## Description:

Monitor Facebook advertisers, campaigns, products, landing pages, and copy changes using PipiAds monitoring tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanyanggod](https://clawhub.ai/user/fanyanggod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create and manage ongoing Facebook advertiser monitoring tasks, review monitored ads, products, landing pages, and copy trends, and organize monitor groups and notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a PIPIADS_API_KEY for PipiAds MCP access.

Mitigation: Use a revocable key with the narrowest account permissions available and rotate it when the integration is removed or no longer trusted.

Risk: PipiAds API calls can consume paid account credits.

Mitigation: Use exact advertiser names before creating monitoring tasks and confirm billing or recharge settings in the PipiAds account.

Risk: The setup installs a third-party npm package for MCP access.

Mitigation: Install only after reviewing and trusting the PipiAds MCP package and its publisher.

## Reference(s):

- [PipiAds](https://www.pipiads.com)
- [PipiAds Dashboard](https://pipiads.com/)
- [PipiSpy API and Billing Portal](https://www.pipispy.com/)
- [ClawHub Skill Page](https://clawhub.ai/fanyanggod/skills/facebook-ad-tracker-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tool names, setup steps, and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses PIPIADS_API_KEY for PipiAds MCP access; API calls may consume account credits.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
