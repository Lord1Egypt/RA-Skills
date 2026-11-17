## Description:

Plans, launches, and optimizes Apple Search Ads campaigns for iOS apps, including bids, keywords, budgets, CPA, attribution, API automation, reporting, troubleshooting, and scaling strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, marketers, and growth teams use this skill to plan and operate paid iOS user acquisition through Apple Search Ads, including campaign structure, keyword workflows, attribution setup, reporting, and API-assisted campaign changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provided mutation scripts can change live Apple Ads spend without enforcing the confirmation gate promised by the skill.

Mitigation: Review generated campaign, bid, budget, status, and keyword changes before execution; keep confirmation enabled and treat mutation scripts as unsafe until they add explicit confirmations, JSON-safe payload construction, input validation, and safer defaults such as creating campaigns paused.

Risk: Apple private keys, client secrets, and access tokens may be exposed through local workspaces, shell history, logs, or source control.

Mitigation: Keep credentials in a secure secret store or environment variables, avoid writing secrets to skill memory or reports, and rotate credentials if accidental exposure occurs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/apple-search-ads)
- [Clawic Skill Page](https://clawic.com/skills/apple-search-ads)
- [Apple Search Ads Campaign Management API v5](https://api.searchads.apple.com/api/v5)
- [Apple OAuth Token Endpoint](https://appleid.apple.com/auth/oauth2/token)
- [Apple AdServices API](https://api-adservices.apple.com/api/v1/)
- [Apple Search Ads API Certificates](https://app.searchads.apple.com/cm/app/settings/apicertificates)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks, shell commands, API payload examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute Apple Search Ads API calls when the user provides credentials; campaign mutations should be reviewed before execution.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
