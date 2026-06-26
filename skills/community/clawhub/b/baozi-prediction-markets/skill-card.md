## Description: <br>
Access Solana prediction markets on Baozi to check market odds, get betting quotes, list active markets, analyze opportunities, or place bets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aratox666-max](https://clawhub.ai/user/aratox666-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to discover Baozi prediction markets on Solana, inspect odds and market details, request betting quotes, check wallet positions, and prepare user-signed betting transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead to wallet-linked betting workflows involving SOL and prediction-market exposure. <br>
Mitigation: Keep BAOZI_LIVE unset until live betting is intentional, test on devnet first, and require the user to inspect and sign each wallet transaction. <br>
Risk: The skill depends on the external @baozi.bet/mcp-server package for market and transaction tooling. <br>
Mitigation: Install and run it only in environments where the Baozi package and service are trusted. <br>
Risk: First use may automatically register a wallet-linked affiliate code. <br>
Mitigation: Avoid first-use affiliate registration unless the user explicitly wants the wallet address associated with an affiliate code. <br>
Risk: Prediction-market odds, fees, market status, and balances can change quickly. <br>
Mitigation: Refresh market details, quotes, wallet balances, and final transaction prompts before taking action. <br>


## Reference(s): <br>
- [Baozi REST API](https://baozi.bet/api/) <br>
- [Baozi Prediction Markets on ClawHub](https://clawhub.ai/aratox666-max/baozi-prediction-markets) <br>
- [Publisher profile](https://clawhub.ai/user/aratox666-max) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON MCP arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose wallet-linked betting workflows that require user review and signing outside the agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
