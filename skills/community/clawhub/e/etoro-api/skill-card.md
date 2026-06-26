## Description: <br>
Enables agents to interact with the eToro API to access market data, portfolio and social features, and execute trades programmatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marian2js](https://clawhub.ai/user/marian2js) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to access eToro market data, portfolio information, watchlists, social feeds, and trading endpoints through the eToro Public API. It supports both demo and real account workflows when the user supplies appropriate eToro API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable an agent to place or cancel real-money trades without built-in confirmation safeguards. <br>
Mitigation: Prefer a Virtual/Demo or read-only eToro key, and require explicit user approval for the real environment, instrument, side, amount or units, leverage, and exact order or position before any live trading action. <br>
Risk: eToro API credentials may grant account access beyond market-data lookups. <br>
Mitigation: Keep public and user keys in secure secret storage and use the least-privileged key permissions suitable for the task. <br>
Risk: Using a real endpoint with a real-account key can execute financial actions when the user expected a demo workflow. <br>
Mitigation: Check that the selected User Key environment matches the endpoint family, and use endpoints containing /demo/ for testing and paper trading. <br>


## Reference(s): <br>
- [eToro API Portal](https://api-portal.etoro.com/) <br>
- [eToro Public API Base URL](https://public-api.etoro.com/api/v1) <br>
- [eToro API MCP Server](https://api-portal.etoro.com/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/marian2js/etoro-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown reference with endpoint lists, curl commands, and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes demo and real trading endpoint guidance; live trading actions should be confirmed explicitly before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
