## Description:

Amazon Listing Audit Pro audits Amazon listings across eight dimensions, benchmarks them against category leaders, identifies keyword gaps, and generates data-backed optimization recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apiclaw](https://clawhub.ai/user/apiclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers, agencies, and their agents use this skill to assess single or bulk ASIN listing quality, compare against category leaders, and generate prioritized listing improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-key handling and endpoint override settings can create avoidable credential exposure risk.

Mitigation: Review before installing, use the default ZooData endpoint, avoid setting ZOODATA_BASE_URL, and prefer an environment variable over a persistent config file for the API key.

Risk: Review-analysis outputs can be influenced by adversarial product reviews.

Mitigation: Treat listing recommendations as decision support and validate material conclusions with additional sources before acting.

Risk: The README installer command may resolve an unpinned installation path.

Mitigation: Pin or otherwise verify the installer path before using the README npx command.

## Reference(s):

- [Listing Audit Pro API Field Reference](artifact/references/reference.md)
- [ZooData CLI Contract](artifact/references/cli-contract.md)
- [ZooData API Documentation](https://api.zoodata.ai/api-docs)
- [ZooData](https://zoodata.ai)
- [Skill Homepage](https://github.com/SerendipityOneInc/ZooData-Skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with scorecards, tables, suggested rewrites, data provenance, and API usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZOODATA_API_KEY and uses credit-consuming ZooData API calls; normal reports include confidence labels and should be validated against additional sources before business decisions.]

## Skill Version(s):

1.0.8 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
