## Description:

Amazon Ads data retrieval and reporting via amazon-ads-open-cli for checking ad performance, pulling Sponsored Products, Sponsored Brands, Sponsored Display, and DSP data, and generating async performance reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bin-huang](https://clawhub.ai/user/bin-huang)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, advertising operators, and analysts use this skill to retrieve Amazon Ads profiles, campaign entities, DSP objects, audiences, brand-safety lists, and performance reports through a read-only CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing an unpinned third-party CLI that handles Amazon Ads credentials and business data.

Mitigation: Review and verify the CLI before use, prefer a pinned and isolated installation, and avoid global installs when possible.

Risk: Amazon Ads OAuth tokens, client IDs, profile IDs, reports, and report URLs may expose sensitive advertising account information.

Mitigation: Use least-privileged credentials, store tokens with restrictive permissions, and treat profile, campaign, report, and download URL data as sensitive.

## Reference(s):

- [amazon-ads-open-cli documentation](https://github.com/Bin-Huang/amazon-ads-open-cli)
- [Amazon Ads API overview](https://advertising.amazon.com/API/docs/en-us/info/api-overview)
- [Sponsored Products API](https://advertising.amazon.com/API/docs/en-us/sponsored-products/3-0/openapi/prod)
- [Sponsored Brands API](https://advertising.amazon.com/API/docs/en-us/sponsored-brands/3-0/openapi)
- [Sponsored Display API](https://advertising.amazon.com/API/docs/en-us/sponsored-display/3-0/openapi)
- [Amazon DSP API](https://advertising.amazon.com/API/docs/en-us/dsp/openapi)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, markdown]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying CLI produces pretty-printed JSON by default and compact JSON when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
