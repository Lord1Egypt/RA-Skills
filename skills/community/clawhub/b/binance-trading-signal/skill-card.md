## Description: <br>
Retrieves Binance Web3 on-chain Smart Money trading signal data, including buy/sell direction, trigger and current prices, max gain, exit rate, token tags, and supported chain filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[viktor-huang](https://clawhub.ai/user/viktor-huang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents can fetch Binance Web3 smart-money signal data to inspect trading activity, compare trigger and current prices, and monitor token signal status on BSC or Solana. Treat the data as informational market data, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading signals are volatile market data and may be wrong, stale, manipulated, or misread as financial advice. <br>
Mitigation: Treat all signals as informational references and require explicit user review before any trading decision. <br>
Risk: The skill relies on an external Binance Web3 endpoint and third-party publisher context. <br>
Mitigation: Verify the publisher and endpoint independently before installation or use. <br>


## Reference(s): <br>
- [Binance Web3 smart-money signal endpoint](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/web/signal/smart-money) <br>
- [ClawHub skill listing](https://clawhub.ai/viktor-huang/binance-trading-signal) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, JSON] <br>
**Output Format:** [Markdown guidance with curl examples and JSON response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only reference workflow; no credentials declared.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
