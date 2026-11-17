## Description:

Apple Search Ads data analysis and reporting via apple-ads-cli for campaign, ad group, keyword, budget, and app eligibility workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bin-huang](https://clawhub.ai/user/bin-huang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and analysts use this skill to query Apple Search Ads account structure, pull performance reports, and investigate campaigns, ad groups, keywords, budgets, ads, and app eligibility through a read-only CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to globally install an unpinned third-party CLI that handles Apple Ads credentials.

Mitigation: Review before installing, use a pinned and verified apple-ads-cli version, and run it in an isolated environment where possible.

Risk: Apple Ads access tokens and organization credentials may be exposed through broad environment inheritance or weak local credential storage.

Mitigation: Avoid broad inherited environment variables for tokens, store credentials with owner-only permissions, and use the least-privileged Apple Ads access available.

## Reference(s):

- [apple-ads-cli documentation](https://github.com/Bin-Huang/apple-ads-cli)
- [Apple Search Ads API overview](https://developer.apple.com/documentation/apple_ads)
- [OAuth setup guide](https://developer.apple.com/documentation/apple_ads/implementing-oauth-for-the-apple-search-ads-api)
- [Campaign Management API v5](https://developer.apple.com/documentation/apple_ads/apple-search-ads-campaign-management-api-5)
- [Reports API](https://developer.apple.com/documentation/apple_ads/reports)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Analysis, Guidance]

**Output Format:** [Markdown guidance with shell command examples and pretty-printed JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Apple Search Ads queries; listing commands support pagination, and report output may be truncated by the CLI at 1000 rows.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
