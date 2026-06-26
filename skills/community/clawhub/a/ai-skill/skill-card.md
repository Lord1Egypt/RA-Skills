## Description: <br>
Enables agents to create and trade shares in prediction markets, query positions and history, and use automated trading strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[watchmer20-ctrl](https://clawhub.ai/user/watchmer20-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to connect to a ClawMarkets prediction-market API, create markets, place buy and sell orders, inspect positions, and evaluate momentum, value, or arbitrage trading signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place prediction-market buy and sell orders and includes automated trading-loop examples. <br>
Mitigation: Use a sandbox or local test backend first, require per-trade confirmation, set position limits, and define a clear stop condition before enabling automation. <br>
Risk: The skill accepts an API key and can send authenticated requests to a configured trading endpoint. <br>
Mitigation: Review the code before using real credentials, restrict the endpoint to trusted HTTPS services, and avoid exposing API keys in prompts, logs, or shared configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/watchmer20-ctrl/ai-skill) <br>
- [Publisher profile](https://clawhub.ai/user/watchmer20-ctrl) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [skill.json](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets, plus JSON-like API responses from helper methods.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate prediction-market API requests when connected to a configured backend.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
