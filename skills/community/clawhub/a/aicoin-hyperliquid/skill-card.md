## Description: <br>
Hyperliquid on-chain perpetuals analytics from AiCoin Open API v3 for whale positions, liquidations, open interest, trader analytics, taker flow, and funding history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[procaross](https://clawhub.ai/user/procaross) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External crypto analysts, developers, and agents use this skill to query AiCoin Open API v3 for Hyperliquid market, whale, liquidation, trader, and smart-money analytics. It helps answer user questions with live API data instead of fabricated market observations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can call broad AiCoin API endpoints beyond a narrow Hyperliquid-only surface. <br>
Mitigation: Review the requested endpoint before execution and prefer catalog-filtered Hyperliquid endpoints for Hyperliquid analytics tasks. <br>
Risk: The local tool reads OpenClaw or workspace environment files and can save AiCoin credentials to plaintext .env files. <br>
Mitigation: Use limited AiCoin credentials, avoid shared workspaces, and review local .env contents before and after running credential setup. <br>
Risk: Some paid AiCoin endpoints may return HTTP 403 when the configured key lacks plan access. <br>
Mitigation: Treat 403 as an access limitation, avoid retry loops, and tell the user that the configured AiCoin plan does not cover the endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/procaross/aicoin-hyperliquid) <br>
- [AiCoin Open Data](https://www.aicoin.com/opendata) <br>
- [Declared OpenClaw source link](https://github.com/aicoincom/coinos-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands invoke a local Node script that returns a unified JSON envelope with ok, data, error, and meta fields.] <br>

## Skill Version(s): <br>
4.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
