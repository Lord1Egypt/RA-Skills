## Description:

Automates competitor ad scraping from ForePlay or Anstrex, AI-based creative adaptation with Kie.ai, and paused Facebook Ads campaign creation for e-commerce brands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harvnk](https://clawhub.ai/user/harvnk)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce marketers, growth teams, and ad operations engineers use this skill to monitor competitor ads, adapt creatives for their brand, and prepare paused Facebook campaigns for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Competitor or source creatives may be uploaded to third-party ad and AI services.

Mitigation: Confirm that this data handling is acceptable before installation and limit uploaded content to approved creative assets.

Risk: The workflow can create Facebook ad campaigns on a schedule.

Mitigation: Use restricted API credentials, keep created ads paused by default, review campaigns before activation, and enable cron only after account permissions and limits are clear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harvnk/skills/ad-spy-pipeline)
- [Publisher profile](https://clawhub.ai/user/harvnk)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API credential setup and campaign-review guidance; generated Facebook ads should remain paused for manual activation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
