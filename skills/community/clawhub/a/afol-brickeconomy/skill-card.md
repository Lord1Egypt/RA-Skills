## Description: <br>
Use the BrickEconomy API through the included CLI for LEGO set/minifig valuation, collection performance, and sales-ledger analysis from verified Brick Directory references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[musketyr](https://clawhub.ai/user/musketyr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AFOL collectors and LEGO investment analysts use this skill to query BrickEconomy for set and minifig values, collection performance, forecasts, and sales-ledger profit/loss analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server security evidence marks the release verdict as suspicious. <br>
Mitigation: Install only if the publisher is trusted and the workflow is needed; review the skill before installation. <br>
Risk: The skill requires a sensitive BrickEconomy API key for live requests. <br>
Mitigation: Provide the key only through BRICKECONOMY_API_KEY and avoid printing, logging, or pasting the real value. <br>
Risk: Collection and sales-ledger responses can contain private financial or account data. <br>
Mitigation: Call personal collection or sales-ledger endpoints only when the user asks for that analysis, and summarize private fields rather than exposing raw records. <br>


## Reference(s): <br>
- [BrickEconomy OpenAPI reference](references/openapi/brickeconomy.yaml) <br>
- [BrickEconomy tool guidance](references/prompts/brickeconomy-tools.txt) <br>
- [BrickEconomy API](https://www.brickeconomy.com/api/v1) <br>
- [BrickEconomy website](https://www.brickeconomy.com) <br>
- [AFOL BrickEconomy ClawHub listing](https://clawhub.ai/musketyr/afol-brickeconomy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only BrickEconomy CLI workflows; live API calls require BRICKECONOMY_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
