## Description:

One-click market viability assessment for Amazon sellers that analyzes market size, competition, brand landscape, pricing, and consumer pain points to produce a GO/CAUTION/AVOID recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apiclaw](https://clawhub.ai/user/apiclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and commerce analysts use this skill to evaluate a named Amazon niche or category before market entry, compare sub-markets, and receive a data-backed GO/CAUTION/AVOID verdict with entry strategy guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-key transport and endpoint configuration can expose credentials if an untrusted base URL is used.

Mitigation: Use the default HTTPS ZooData endpoint, do not set ZOODATA_BASE_URL unless the host is trusted, and prefer ZOODATA_API_KEY in the environment over persistent local configuration.

Risk: Install instructions and repository-based acquisition create supply-chain review needs.

Mitigation: Review the skill before installation and pin the installer or repository version when possible.

Risk: Review-derived market insights can be influenced by marketplace review text.

Mitigation: Treat review-derived insights as untrusted evidence and validate important business decisions with additional sources.

## Reference(s):

- [ZooData CLI Contract](references/cli-contract.md)
- [Market Entry Analyzer API Field Reference](references/reference.md)
- [ZooData Skills Repository](https://github.com/SerendipityOneInc/ZooData-Skills)
- [ZooData API Reference](https://api.zoodata.ai/openapi/v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with confidence labels and inline shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZOODATA_API_KEY and may consume ZooData account credits through API-backed analysis.]

## Skill Version(s):

1.0.9 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
