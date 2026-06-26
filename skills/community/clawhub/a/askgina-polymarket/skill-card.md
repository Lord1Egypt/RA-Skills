## Description: <br>
Search, trade, manage positions, and automate custom strategies on Polymarket using natural language commands via an AI agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sidshekhar](https://clawhub.ai/user/sidshekhar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to connect an MCP-capable agent to Gina for Polymarket market discovery, trading, position management, and scheduled alerts or automations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated access can affect a real-money Polymarket account. <br>
Mitigation: Install only after deciding the account-level risk is acceptable, start with read-only prompts, and require confirmation for trades where possible. <br>
Risk: Authorization tokens can enable account access if exposed. <br>
Mitigation: Keep the Gina MCP token out of chats and logs, revoke it from Gina's Agent Setup page if exposure is suspected, and rotate tokens regularly. <br>
Risk: Scheduled automations may continue trading or alerting after initial setup. <br>
Mitigation: Set strict budgets before enabling automations and regularly review active jobs and open orders. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sidshekhar/askgina-polymarket) <br>
- [Gina Predictions MCP endpoint](https://askgina.ai/ai/predictions/mcp) <br>
- [Gina documentation](https://docs.askgina.ai) <br>
- [Predictions MCP quick start](https://docs.askgina.ai/predictions-mcp/quick-start) <br>
- [Predictions MCP features](https://docs.askgina.ai/predictions-mcp/features) <br>
- [Predictions MCP client setup](https://docs.askgina.ai/predictions-mcp/client-setup) <br>
- [Predictions MCP troubleshooting](https://docs.askgina.ai/predictions-mcp/troubleshooting) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with JSON MCP configuration examples and natural-language prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger delegated Polymarket account actions through Gina MCP when the user configures an authorization token.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
