## Description: <br>
Get China A-share market data (Shanghai/SH and Shenzhen/SZ) via FinanceAgent on OneKey Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to query China A-share quotes for Shanghai and Shenzhen symbols through OneKey Gateway from CLI or HTTP workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends stock query requests through OneKey Gateway and an external FinanceAgent service. <br>
Mitigation: Confirm that the gateway service and @aiagenta2z/onekey-gateway npm package are trusted for the intended environment before use. <br>
Risk: The OneKey API key can be exposed through shared terminals, shell history, verbose command output, or logs. <br>
Mitigation: Keep the API key out of shared logs, prefer local or npx execution where practical, and rotate the key if it is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/cn-stock-market-shanghai-shenzhen) <br>
- [OneKey Gateway agent router endpoint](https://agent.deepnlp.org/agent_router) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with shell snippets and JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a OneKey Gateway API key; response fields depend on the upstream data source.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
