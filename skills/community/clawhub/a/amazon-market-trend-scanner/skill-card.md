## Description:

Scans Amazon category landscapes to discover trending subcategories, emerging niches, and market shifts using ZooData API market and product data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apiclaw](https://clawhub.ai/user/apiclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, ecommerce operators, and product research teams use this skill to scan Amazon parent categories for demand surges, emerging niches, brand concentration, price shifts, and new entrant activity. It supports full discovery scans and opt-in recurring checks that compare current results with retained local baselines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a ZooData API key and sends category, keyword, ASIN, marketplace, date, and numeric filter values to ZooData.

Mitigation: Use the ZOODATA_API_KEY environment variable or trusted local config, avoid placing sensitive user profile text in scan inputs, and review what category and product research queries will be sent before running scans.

Risk: The scanner can consume account credits, especially for broad full scans or recurring monitoring.

Mitigation: Confirm estimated credit cost before multi-call scans, use narrower category paths when possible, and monitor returned credit metadata.

Risk: Local scan state can retain watchlists, baselines, alerts, and historical snapshots between runs.

Mitigation: Prune or delete the skill's scan-data files when monitoring history is no longer needed.

Risk: The security summary classifies the release as suspicious because API-key handling and optional diagnostics are broader than the main workflow.

Mitigation: Install only when comfortable with the ZooData API integration, avoid setting ZOODATA_BASE_URL unless the endpoint is controlled, and do not use check endpoint probes unless diagnostics and credit use are intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apiclaw/skills/amazon-market-trend-scanner)
- [Publisher profile](https://clawhub.ai/user/apiclaw)
- [Skill homepage](https://github.com/SerendipityOneInc/ZooData-Skills)
- [ZooData](https://zoodata.ai)
- [ZooData API keys](https://zoodata.ai/en/api-keys)
- [ZooData API reference](https://api.zoodata.ai/openapi/v2)
- [Market Trend Scanner API Field Reference](references/reference.md)
- [ZooData CLI Contract](references/cli-contract.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with trend tables, endpoint provenance, API usage summaries, and optional monitoring configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include confidence labels for conclusions and may write local scan state for baseline comparison when monitoring workflows are used.]

## Skill Version(s):

1.0.8 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
