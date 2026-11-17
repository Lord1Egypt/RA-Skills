## Description:

Amazon niche market analysis tool for cross-border e-commerce product selection that retrieves demand scores, competition analysis, price ranges, brand concentration, and sales metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctzys](https://clawhub.ai/user/ctzys)

### License/Terms of Use:

MIT-0

## Use Case:

External users, product researchers, and cross-border e-commerce sellers use this skill to query Amazon niche-market data, compare demand and competition, and identify product-selection opportunities in the US, Japan, and Germany markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-research keywords and filters are sent to LinkFoxAgent for external processing.

Mitigation: Use the skill only when external processing is acceptable, and avoid entering confidential product ideas unless that sharing is approved.

Risk: The skill requires a LinkFoxAgent API key.

Mitigation: Store the API key in a protected secret manager or secured configuration, and avoid printing the full key in terminal output.

Risk: The release does not include a pinned dependency file for the Python client examples.

Mitigation: Run the client in a virtual environment and pin dependencies before production use.

## Reference(s):

- [API Overview](references/API-Overview.md)
- [Jiimore API Reference](references/Jiimore.md)
- [Jiimore endpoint](https://test-tool-gateway.linkfox.com/jiimore/getNicheInfoByKeyword)
- [Skill release page](https://clawhub.ai/ctzys/skills/amazon-asin-data)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON data, Python examples, shell commands, and tabular analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a LinkFoxAgent API key and sends Amazon market-research keywords and filters to an external API.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
