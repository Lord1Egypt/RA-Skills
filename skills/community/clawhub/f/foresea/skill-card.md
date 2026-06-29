## Description: <br>
Add Foresea forecasting tools to OpenClaw agents through Foresea's public remote MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pareelamre](https://clawhub.ai/user/pareelamre) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route forecasting and prediction-market questions to Foresea's remote MCP tools for probability estimates, market analysis, market scans, edge boards, and track-record checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Forecasting or prediction-market prompts and any user-provided context are sent to Foresea's external service. <br>
Mitigation: Use the skill only when external forecasting is appropriate, and avoid sending sensitive or unnecessary context. <br>
Risk: Forecasts and market edge analysis may be mistaken for financial advice or guaranteed outcomes. <br>
Mitigation: Present forecasts as decision support, preserve evidence links, and state that live market performance is still accumulating. <br>


## Reference(s): <br>
- [Foresea ClawHub listing](https://clawhub.ai/pareelamre/foresea) <br>
- [Foresea homepage](https://foresea.ink) <br>
- [Foresea agent guide](https://foresea.ink/agents) <br>
- [Foresea MCP endpoint](https://foresea.ink/mcp/) <br>
- [Foresea agent manifest](https://foresea.ink/.well-known/agent.json) <br>
- [Foresea OpenAPI](https://foresea.ink/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Forecast outputs should preserve evidence links and frame results as decision support, not financial advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
