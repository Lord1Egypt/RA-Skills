## Description: <br>
Core trading skill for AION Market prediction market agents, covering wallet setup, market search, pre-trade checks, order execution, position monitoring, and settlement workflows for Polymarket and Kalshi. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssj124](https://clawhub.ai/user/ssj124) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-agent operators use this skill to connect an agent to AION Market, configure user-provided wallets, inspect prediction markets, place or cancel trades, monitor positions, and run settlement-related flows. It is intended for agents that already have explicit trading intent and user-provided credentials. <br>

### Deployment Geography for Use: <br>
Global, subject to AION Market, Polymarket, Kalshi, account, KYC, and venue restrictions. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use wallet keys to approve spending, place trades, and collect platform fees automatically. <br>
Mitigation: Use a dedicated low-balance trading wallet and require manual review of every trade, token approval, spender or delegate, fee recipient, fee amount, and allowance scope before execution. <br>
Risk: The skill handles sensitive API keys, wallet private keys, and derived trading credentials. <br>
Mitigation: Store credentials only in local environment variables or a local .env file, never commit or log them, rotate API keys, and avoid exposing derived CLOB credentials. <br>
Risk: External SDK packages and venue-specific signing flows can affect live orders and approvals. <br>
Mitigation: Pin and verify the aion-sdk and py-clob-client packages, test with small amounts first, and independently confirm venue execution when responses are ambiguous. <br>


## Reference(s): <br>
- [AION Market Documentation](https://docs.aionmarket.com/) <br>
- [AION Market Homepage](https://www.aionmarket.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/ssj124/aionmarket-trading) <br>
- [aion-sdk on PyPI](https://pypi.org/project/aion-sdk/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided API keys and wallet private keys; outputs are operational trading workflow guidance, setup steps, and code examples.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata; artifact metadata reports 0.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
