## Description: <br>
Trade stocks and crypto via Alpaca API for market data, order placement, positions, portfolio management, account information, watchlists, streaming data, and price alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vamzi](https://clawhub.ai/user/vamzi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query Alpaca market and account data, manage watchlists and alerts, and place or cancel stock and crypto trades through Alpaca accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Alpaca accounts and perform live trading actions, including placing orders and cancelling orders. <br>
Mitigation: Start with paper trading, keep live API keys tightly controlled, and require explicit user approval before live orders or cancellations. <br>
Risk: Force mode and bulk cancellation can bypass or reduce safeguards around destructive trading actions. <br>
Mitigation: Avoid --force and cancel all unless the user deliberately intends that exact action and has confirmed the target account and effect. <br>


## Reference(s): <br>
- [Alpaca API Reference](references/api.md) <br>
- [ClawHub release page](https://clawhub.ai/vamzi/alpaca) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and text output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke Alpaca API actions that read account data, place orders, cancel orders, manage watchlists, stream market data, or store local alert configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
