## Description:

Finds affiliate marketers and performance marketing creators on Instagram and TikTok using apidojo's scrapers, returning creator handles, platforms, affiliate signal strength, niche focus, engagement rate, and promo code counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Affiliate program managers, e-commerce brands, and network managers use this skill to identify social media creators who appear to run affiliate or performance marketing campaigns in a product category, niche, brand program, or competitor market.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify tokens can be exposed through example URLs, shell history, logs, or copied command output.

Mitigation: Use a dedicated low-privilege Apify token through environment variables, header-based authentication, or a managed secret store; avoid putting tokens directly in URLs.

Risk: Social media scraping may send campaign, competitor, or personal data to Apify and third-party actors.

Mitigation: Use the skill only with data approved for Apify processing, and avoid submitting confidential campaign details or sensitive personal data.

Risk: The artifact describes Instagram and TikTok discovery, but the current workflow is primarily Instagram-focused.

Mitigation: Confirm platform coverage before relying on TikTok results, and disclose any platform-specific gaps in the agent's output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-affiliate-marketers-on-social-media)
- [API Dojo publisher profile](https://clawhub.ai/user/apidojo-io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown results table with summary guidance and optional CSV or JSON files from Apify actor runs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include creator handle, platform, affiliate signal strength, niche focus, engagement rate, promo code count, classification, and relevance score.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
