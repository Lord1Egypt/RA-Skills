## Description:

Use the BrickEconomy API through the included CLI for LEGO set/minifig valuation, collection performance, and sales-ledger analysis from verified Brick Directory references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[musketyr](https://clawhub.ai/user/musketyr)

### License/Terms of Use:

MIT-0

## Use Case:

LEGO collectors, sellers, and portfolio analysts use this skill to retrieve BrickEconomy valuations, forecasts, authenticated collection performance, and sales-ledger profit/loss summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The BrickEconomy API key can be sent to an arbitrary host when BRICKECONOMY_BASE_URL or --base-url is overridden.

Mitigation: Use the default BrickEconomy API host unless the alternate destination is fully trusted, and rotate the API key if it may have been used with an untrusted base URL.

Risk: Authenticated collection and sales-ledger endpoints can expose private financial or account data.

Mitigation: Call personal collection or sales-ledger endpoints only for user-requested collection, ROI, or sales analysis, and summarize sensitive results minimally.

Risk: BrickEconomy rate limits can be exhausted by broad or repeated lookups.

Mitigation: Prefer collection-level endpoints for portfolio analysis, use dry-run mode to inspect request shape, and avoid large fan-out unless the user accepts the request budget.

## Reference(s):

- [BrickEconomy OpenAPI Reference](references/openapi/brickeconomy.yaml)
- [BrickEconomy Tool Guidance](references/prompts/brickeconomy-tools.txt)
- [BrickEconomy API](https://www.brickeconomy.com/api/v1)
- [BrickEconomy](https://www.brickeconomy.com)
- [ClawHub Skill Page](https://clawhub.ai/musketyr/skills/brickeconomy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call read-only BrickEconomy API endpoints through a CLI when BRICKECONOMY_API_KEY is configured.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
