## Description: <br>
Interact with 100+ cryptocurrency exchanges to fetch markets, order books, tickers, place orders, check balances, and more using the CCXT CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pcriadoperez](https://clawhub.ai/user/pcriadoperez) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to guide agent-assisted cryptocurrency exchange operations through the CCXT CLI, including public market data queries and private account or trading actions when credentials are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger immediate live cryptocurrency account actions through a broad CLI interface. <br>
Mitigation: Use sandbox mode first and require explicit user confirmation before private or account-changing commands, including order creation, cancellation, or unfamiliar CCXT methods. <br>
Risk: Private exchange operations require API credentials that may grant financial account access. <br>
Mitigation: Use least-privileged API keys, avoid withdrawal permissions, and configure credentials only for exchanges and accounts the user intends to operate. <br>


## Reference(s): <br>
- [CCXT Documentation](https://docs.ccxt.com) <br>
- [ClawHub ccxt Skill Page](https://clawhub.ai/pcriadoperez/ccxt) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide commands that return JSON from the CCXT CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
