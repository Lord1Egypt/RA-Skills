## Description: <br>
Manage Amazon Advertising campaigns via the official Advertising API by reading live campaign, keyword, and search-term performance, calculating ACOS, ROAS, and CTR, identifying wasted spend, adjusting bids, pausing keywords, and adding negatives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linbeihanda](https://clawhub.ai/user/linbeihanda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Amazon Ads operators, sellers, and marketing teams use this skill to inspect live Sponsored Products campaign performance, produce optimization reports, and apply confirmed bid, state, and negative-keyword changes through the Amazon Advertising API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires live Amazon Ads OAuth credentials and can access sensitive advertising account data. <br>
Mitigation: Install it only for intended Amazon Ads accounts, store credentials locally in the skill .env file, and use the narrowest practical profile access. <br>
Risk: Bid, pause, archive, and negative-keyword operations can change live campaign performance and spend. <br>
Mitigation: Review reports before acting and require an explicit summary and confirmation before applying bid, state, archive, or negative-keyword changes. <br>


## Reference(s): <br>
- [Amazon Ads API onboarding](https://advertising.amazon.com/API/docs/en-us/onboarding/overview) <br>
- [ClawHub skill page](https://clawhub.ai/linbeihanda/amazon-ads-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown reports with tables, inline shell commands, and JSON-backed API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Amazon Ads OAuth credentials and profile configuration before commands can access account data or modify campaigns.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
