## Description: <br>
Use the BrickEconomy API through the included CLI for LEGO set/minifig valuation, collection performance, and sales-ledger analysis from verified Brick Directory references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[musketyr](https://clawhub.ai/user/musketyr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve BrickEconomy valuation, forecast, collection, and sales-ledger data through a read-only CLI. It supports LEGO set and minifig pricing analysis, collection performance review, and profit/loss summaries when the user provides a BrickEconomy API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a BrickEconomy API key and can retrieve private collection or sales-ledger data when those workflows are requested. <br>
Mitigation: Install only when that access is acceptable, keep the API key in the environment, and summarize private account data instead of exposing full records unless the user explicitly needs them. <br>
Risk: Changing the API base URL could send credentials or account data to an untrusted endpoint. <br>
Mitigation: Use the default BrickEconomy API endpoint and avoid base-url overrides unless the endpoint is trusted. <br>
Risk: Pricing and forecast outputs could be mistaken for guaranteed financial results. <br>
Mitigation: Describe forecasts as estimates based on returned BrickEconomy fields and call out missing paid-price or fee data before calculating ROI or profit/loss. <br>
Risk: The skill is intended for read-only valuation and analysis, not marketplace writes or purchase actions. <br>
Mitigation: Use only the documented read-only commands and route buy/sell marketplace requests to an appropriate marketplace-specific workflow. <br>


## Reference(s): <br>
- [BrickEconomy API OpenAPI reference](references/openapi/brickeconomy.yaml) <br>
- [BrickEconomy tool guidance](references/prompts/brickeconomy-tools.txt) <br>
- [BrickEconomy API](https://www.brickeconomy.com) <br>
- [ClawHub BrickEconomy release](https://clawhub.ai/musketyr/brickeconomy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should summarize API response fields and avoid pasting full private collection or sales-ledger records.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
