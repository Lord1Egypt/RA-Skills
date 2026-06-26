## Description: <br>
Apple Search Ads data analysis and reporting via apple-ads-cli for campaign, ad group, keyword, budget, app eligibility, and account structure queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bin-huang](https://clawhub.ai/user/bin-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and analysts use this skill to query Apple Search Ads account structure and performance data through the apple-ads-cli read-only command-line tool. It helps inspect campaigns, ad groups, ads, keywords, budget orders, reports, and app eligibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Apple Ads credentials and organization access. <br>
Mitigation: Use least-privileged Apple Ads access, verify credentials with apple-ads-cli me, and keep access tokens, private keys, and credential files out of chat and logs. <br>
Risk: Reports can contain sensitive advertising performance and budget data. <br>
Mitigation: Treat generated campaign, keyword, budget, and app eligibility reports as sensitive business data and share them only with authorized users. <br>
Risk: Global installation depends on the external npm package apple-ads-cli. <br>
Mitigation: Verify the npm package and source before global installation. <br>


## Reference(s): <br>
- [apple-ads-cli documentation](https://github.com/Bin-Huang/apple-ads-cli) <br>
- [Apple Search Ads API overview](https://developer.apple.com/documentation/apple_ads) <br>
- [Apple Search Ads OAuth setup guide](https://developer.apple.com/documentation/apple_ads/implementing-oauth-for-the-apple-search-ads-api) <br>
- [Apple Search Ads Campaign Management API v5](https://developer.apple.com/documentation/apple_ads/apple-search-ads-campaign-management-api-5) <br>
- [Apple Search Ads Reports API](https://developer.apple.com/documentation/apple_ads/reports) <br>
- [ClawHub skill page](https://clawhub.ai/bin-huang/apple-ads-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Analysis, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON-oriented reporting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying CLI returns pretty-printed JSON by default and supports compact JSON for piping.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
