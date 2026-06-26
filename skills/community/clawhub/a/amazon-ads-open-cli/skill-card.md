## Description: <br>
Amazon Ads data retrieval and reporting via amazon-ads-open-cli for checking ad performance, pulling Sponsored Products, Sponsored Brands, Sponsored Display, and DSP data, managing audiences, and generating async reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bin-huang](https://clawhub.ai/user/bin-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External advertisers, agencies, analysts, and developers use this skill to configure and run amazon-ads-open-cli commands for Amazon Ads account exploration, campaign structure inspection, DSP review, audience checks, and performance reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Amazon Ads OAuth credentials and a client ID, which could expose advertising account access if mishandled. <br>
Mitigation: Use least-privileged, short-lived credentials, avoid printing tokens or credential file contents, and protect credential files with restrictive permissions. <br>
Risk: Report downloads, report URLs, and ad performance data may contain sensitive business information. <br>
Mitigation: Treat generated reports and returned URLs as sensitive data and share outputs only with authorized users. <br>
Risk: The skill depends on an external npm CLI that will call Amazon Ads APIs in the user's environment. <br>
Mitigation: Install and run the CLI only when the user trusts the package and understands the permissions granted to its Amazon Ads credentials. <br>


## Reference(s): <br>
- [amazon-ads-open-cli documentation](https://github.com/Bin-Huang/amazon-ads-open-cli) <br>
- [Amazon Ads API overview](https://advertising.amazon.com/API/docs/en-us/info/api-overview) <br>
- [Sponsored Products API](https://advertising.amazon.com/API/docs/en-us/sponsored-products/3-0/openapi/prod) <br>
- [Sponsored Brands API](https://advertising.amazon.com/API/docs/en-us/sponsored-brands/3-0/openapi) <br>
- [Sponsored Display API](https://advertising.amazon.com/API/docs/en-us/sponsored-display/3-0/openapi) <br>
- [Amazon DSP API](https://advertising.amazon.com/API/docs/en-us/dsp/openapi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON credential examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When executed, the referenced CLI commands return pretty-printed or compact JSON from Amazon Ads APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
