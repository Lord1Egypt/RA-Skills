## Description:

Use the BrickEconomy API through the included CLI for LEGO set/minifig valuation, collection performance, and sales-ledger analysis from verified Brick Directory references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[musketyr](https://clawhub.ai/user/musketyr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query BrickEconomy for LEGO set and minifig valuation, authenticated collection performance, forecasts, ROI, and sales-ledger profit/loss analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The BrickEconomy API key can be sent to an arbitrary configured base URL.

Mitigation: Use the default BrickEconomy API endpoint only, and do not set BRICKECONOMY_BASE_URL or pass --base-url unless the endpoint is confirmed as https://www.brickeconomy.com/api/v1.

Risk: Collection and sales-ledger commands can expose private financial, order, and note data in terminal output or agent logs.

Mitigation: Run authenticated collection or sales-ledger commands only when the user asks for that analysis, summarize results, and avoid pasting full private records into shared reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/musketyr/skills/afol-brickeconomy)
- [BrickEconomy OpenAPI reference](references/openapi/brickeconomy.yaml)
- [BrickEconomy tool guidance](references/prompts/brickeconomy-tools.txt)
- [BrickEconomy API](https://www.brickeconomy.com/api/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI command examples and JSON API-response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live use requires BRICKECONOMY_API_KEY; dry-run commands can show request shape without calling the API.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
