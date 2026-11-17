## Description:

Fetch and compare mainstream coffee prices (latte, americano, etc.) from major chains like Starbucks, Luckin, and Cotti for a given Chinese city and output them as a table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realank](https://clawhub.ai/user/realank)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to estimate and compare reference coffee prices for major chains in Chinese cities, typically returning a table for pricing benchmarks or brand comparisons.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Automatic city inference may contact ipinfo.io when no city is provided.

Mitigation: Provide --city explicitly or set OPENCLAW_CITY when location privacy or restricted network access matters.

Risk: The skill estimates reference prices and is not a live official-price source.

Mitigation: Use official apps or ordering channels for financial, reimbursement, or purchase decisions.

Risk: CSV output can carry spreadsheet-handling risk when city inputs come from untrusted sources.

Mitigation: Review CSV output before opening it in spreadsheet software and prefer Markdown or JSON for routine agent responses.

Risk: The dependency requirement is not fully pinned.

Mitigation: Use a pinned dependency set for reproducible installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/realank/skills/coffee-prices)
- [Publisher profile](https://clawhub.ai/user/realank)
- [IP geolocation endpoint used for optional city inference](https://ipinfo.io/json)

## Skill Output:

**Output Type(s):** [text, markdown, json, csv, shell commands, guidance]

**Output Format:** [Markdown table by default, with optional JSON or CSV output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs CNY reference prices from built-in city-tier and brand price tables.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
