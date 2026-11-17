## Description:

Manage Amazon Advertising campaigns through the official Advertising API by reading live performance data, calculating ad metrics, and supporting keyword, bid, state, and negative-keyword changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linbeihanda](https://clawhub.ai/user/linbeihanda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and advertisers use this skill to inspect Amazon Ads account performance, produce optimization reports, and carry out campaign-management actions after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses long-lived Amazon Ads credentials and documents storing them in a skill-root .env file.

Mitigation: Use a secure secret store or tightly permissioned environment variables, grant the least privilege possible, and rotate credentials if they are exposed.

Risk: The skill can make live campaign changes such as bid updates, keyword pauses, archives, and negative-keyword additions.

Mitigation: Require explicit user confirmation before executing business-impacting changes and review proposed actions against account goals before running them.

## Reference(s):

- [Amazon Ads API onboarding](https://advertising.amazon.com/API/docs/en-us/onboarding/overview)
- [ClawHub skill page](https://clawhub.ai/linbeihanda/skills/amazon-ads-manager)
- [Publisher profile](https://clawhub.ai/user/linbeihanda)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with tables, JSON command output, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Amazon Ads API credentials and account profile configuration before live API commands can run.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
