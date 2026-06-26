## Description: <br>
Enables agents to interact with the eToro API to access market data, portfolio and social features, and execute trades programmatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marian2js](https://clawhub.ai/user/marian2js) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to guide eToro API requests for market data, portfolio and watchlist management, social feed operations, and trade execution. It is suitable when an agent needs structured guidance for OAuth or API-key authenticated eToro workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward real-money trades and other account-changing eToro actions. <br>
Mitigation: Use demo or read-only credentials unless live trading is explicitly intended, and require confirmation with the exact account, environment, instrument, size, and target ID before any trade, close, cancellation, feed post, or deletion. <br>
Risk: OAuth tokens, API keys, and user keys can expose account access if mishandled. <br>
Mitigation: Store credentials in a secret store, avoid including them in prompts or logs, and grant only the minimum eToro permissions needed for the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marian2js/etoro-apps) <br>
- [eToro API portal](https://api-portal.etoro.com/) <br>
- [eToro public API base](https://public-api.etoro.com/api/v1) <br>
- [eToro API MCP server](https://api-portal.etoro.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API endpoint descriptions, JSON examples, and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may involve authenticated eToro API actions, including live trading and account changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
