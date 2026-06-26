## Description: <br>
This skill provides integration with the Alpaca Markets API for trading stocks, options, and cryptocurrencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oscraters](https://clawhub.ai/user/oscraters) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading automation users use this skill to query Alpaca account data, retrieve market data, and manage orders or positions through authenticated Alpaca API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent with Alpaca credentials can place, replace, cancel, or close orders and positions, including against live brokerage accounts. <br>
Mitigation: Use paper-trading credentials first, leave ALPACA_BASE_URL unset unless live trading is intended, and require manual review before order placement, replacement, cancellation, or position-closing commands. <br>
Risk: Alpaca API credentials are required for operation and could grant account access if exposed. <br>
Mitigation: Provide credentials only through environment variables, do not hardcode them in files or prompts, and evaluate the skill in an isolated environment before broader use. <br>


## Reference(s): <br>
- [ClawHub Distribution Page](https://clawhub.ai/oscraters/alpaca-markets) <br>
- [Alpaca Markets API Reference](references/api_reference.md) <br>
- [Alpaca API Documentation](https://docs.alpaca.markets/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python helper usage, and JSON or text API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ALPACA_API_KEY and ALPACA_API_SECRET; ALPACA_BASE_URL is optional and defaults to paper trading when unset.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
