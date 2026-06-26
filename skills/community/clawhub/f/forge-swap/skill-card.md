## Description: <br>
Cross-chain swap routing via THORChain that helps agents get quotes and build non-custodial swap transaction details across supported assets, with a disclosed 0.5% affiliate fee. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morebetterclaw](https://clawhub.ai/user/morebetterclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request THORChain swap quotes, supported asset information, and transaction details that can be reviewed before execution in the user's own wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hosted API prepares swap details for cryptocurrency transfers, so incorrect or tampered asset, amount, destination, vault, memo, slippage, or fee details could lead to loss of funds. <br>
Mitigation: Before sending funds, manually verify every transaction field in the wallet or another trusted THORChain interface, including the disclosed 0.5% affiliate fee. <br>
Risk: Users may misunderstand non-custodial transaction preparation as execution by the skill. <br>
Mitigation: Treat FORGE output as transaction preparation guidance only; the user's wallet remains responsible for reviewing and executing any transfer. <br>
Risk: Sharing private keys or seed phrases with any hosted service would compromise funds. <br>
Mitigation: Never provide private keys or seed phrases; use the skill only for quotes, supported asset data, and transaction details. <br>


## Reference(s): <br>
- [FORGE ClawHub skill page](https://clawhub.ai/morebetterclaw/forge-swap) <br>
- [morebetterclaw publisher profile](https://clawhub.ai/user/morebetterclaw) <br>
- [MoreBetter Studios homepage](https://morebetterstudios.com) <br>
- [FORGE API](https://forge-api-production-50de.up.railway.app) <br>
- [FORGE MCP endpoint](https://forge-api-production-50de.up.railway.app/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns swap quote guidance and transaction preparation details; the user's wallet executes any transfer.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
