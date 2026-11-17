## Description:

Queries and analyzes public business, company, industry-chain, and A-share datasets through Volcengine data-source discovery and query tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to discover available Volcengine data sources, inspect field definitions and enum values, and run filtered, grouped, aggregated, or paginated queries for company and industry-chain research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that cloud access keys can be exposed to a caller-supplied gateway URL.

Mitigation: Use only an approved HTTPS Volcengine gateway, avoid overriding --url unless reviewed, and rotate any key that may have been used with an untrusted endpoint.

Risk: The skill requires cloud credentials for data access.

Mitigation: Provision credentials with the minimum required permissions and prefer environment variables instead of command-line secrets.

Risk: Returned public data is described as reference material and may be unsuitable as the sole basis for decisions.

Mitigation: Review important query results against authoritative sources before using them for business, legal, financial, or operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-data-search)
- [Volcengine AK/SK user guide](https://www.volcengine.com/docs/6291/65568?lang=zh)
- [Volcengine high-quality dataset console](https://console.volcengine.com/high-quality-dataset)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-formatted query results from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Volcengine access credentials; query results depend on the selected data source, filters, aggregation, grouping, sorting, and pagination.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
