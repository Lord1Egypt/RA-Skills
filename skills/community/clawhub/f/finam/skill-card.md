## Description: <br>
Execute trades, manage portfolios, access real-time market data, browse and search market assets, scan volatility, and answer questions about Finam Trade API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexander-panov](https://clawhub.ai/user/alexander-panov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, traders, and analysts use this skill to interact with the Finam Trade API for market data, portfolio review, asset discovery, volatility scanning, and explicitly confirmed order workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses brokerage credentials and supports account, portfolio, and order workflows. <br>
Mitigation: Use the narrowest available API permissions, keep credentials out of chat and logs, and prefer read-only credentials for research or portfolio viewing. <br>
Risk: Incorrect order parameters can place or cancel unintended trades. <br>
Mitigation: Confirm the symbol, side, quantity, order type, price, and account before any order placement or cancellation. <br>


## Reference(s): <br>
- [Finam Trade API](https://tradeapi.finam.ru/) <br>
- [REST Reference](references/REST.md) <br>
- [gRPC Python Reference](references/GRPC.md) <br>
- [FinamPy](https://github.com/cia76/FinamPy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell, JSON, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses FINAM_API_KEY and FINAM_ACCOUNT_ID environment variables; order workflows require explicit user confirmation before execution.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
