## Description:

Amazon Pricing Command Center is a ZooData-backed pricing strategy skill for Amazon sellers that auto-detects leaf categories from ASINs and produces RAISE, HOLD, or LOWER guidance with profit simulation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apiclaw](https://clawhub.ai/user/apiclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and ecommerce operators use this skill to evaluate product pricing from one or more ASINs, compare competitors, simulate profit scenarios, and decide whether to raise, hold, or lower prices. Developers and agents use it to run a scoped ZooData CLI workflow that requires a ZOODATA_API_KEY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured ZooData API key could be exposed if ZOODATA_BASE_URL is overridden unsafely.

Mitigation: Keep ZOODATA_BASE_URL unset so the default HTTPS ZooData endpoint is used, or set it only to an endpoint you fully control and have reviewed.

Risk: The skill sends ASINs, keywords, category paths, marketplace/date filters, and numeric filters to ZooData and consumes API credits.

Mitigation: Install and run the skill only if you trust ZooData and the publisher with that data, and confirm estimated credit usage before broad or batch analyses.

Risk: A floating install command can pull a different release than the reviewed artifact.

Mitigation: Prefer a pinned or otherwise verified release whose hash and version match the reviewed evidence.

Risk: Pricing recommendations can be incomplete or misleading if treated as the sole basis for business decisions.

Mitigation: Use the report as decision support, review its confidence labels and provenance table, and validate material pricing changes with additional sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apiclaw/skills/amazon-pricing-command-center)
- [Skill metadata homepage](https://github.com/SerendipityOneInc/ZooData-Skills)
- [ZooData](https://zoodata.ai)
- [ZooData API documentation](https://api.zoodata.ai/api-docs)
- [ZooData CLI Contract](references/cli-contract.md)
- [ZooData API Field Reference](references/reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown pricing report with endpoint provenance, API usage tables, and inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports match the user's language and include confidence labels, data provenance, API credit usage, and a decision-support disclaimer.]

## Skill Version(s):

1.1.8 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
