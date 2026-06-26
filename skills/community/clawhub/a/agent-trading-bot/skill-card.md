## Description: <br>
AI-powered trading bot framework for OpenClaw that connects to crypto exchanges and prediction markets, supports strategy templates, and can run paper or live trading workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-agent builders use this skill to configure and run crypto trading workflows, inspect exchange connectivity, simulate strategies, and review risk status before considering live execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be used in real-money trading workflows and the server security review flags the financial framing as under-scoped. <br>
Mitigation: Use paper mode only unless the script has been inspected, start with limited balances, and require human review before any live execution. <br>
Risk: Exchange API credentials may grant account access if configured too broadly. <br>
Mitigation: Use restricted API keys with withdrawals disabled, store them only in environment variables, and rotate keys after testing. <br>
Risk: The documented live trading, backtesting, kill-switch, and risk controls may overstate actual completeness. <br>
Mitigation: Do not rely on these controls as complete; validate behavior manually and monitor positions outside the skill. <br>


## Reference(s): <br>
- [Built-in Trading Strategies](references/strategies.md) <br>
- [ClawHub Release Page](https://clawhub.ai/stevojarvisai-star/agent-trading-bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read exchange credentials from environment variables and write local trading state under the user's OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
