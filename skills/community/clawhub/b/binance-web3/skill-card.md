## Description: <br>
Query token prices, market data, K-line charts, and smart money trading signals via Binance Web3 APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[torchesfrms](https://clawhub.ai/user/torchesfrms) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to query Binance Web3 market data for token discovery, prices, liquidity, holders, candlestick charts, wallet token balances, and smart money signals across BSC, Base, Solana, and Ethereum. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries can disclose token symbols, contract addresses, chain IDs, and wallet addresses to Binance Web3 or related Web3 data providers. <br>
Mitigation: Use the skill only for data you are comfortable sharing with those providers, and avoid querying sensitive wallet addresses. <br>
Risk: The market-rank helper can use an HTTP proxy from the environment or a localhost default. <br>
Mitigation: Review proxy settings before running market-rank.sh and unset or set HTTP_PROXY explicitly when needed. <br>
Risk: Some helper scripts are not described in the public skill overview. <br>
Mitigation: Review the bundled scripts before installation or execution, especially address-info.sh, meme-rush.sh, token-audit.sh, and market-rank.sh. <br>


## Reference(s): <br>
- [ClawHub Binance Web3 skill page](https://clawhub.ai/torchesfrms/binance-web3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and JSON API responses from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, and jq. Some helper scripts send token symbols, contract addresses, chain IDs, and wallet addresses to Web3 data providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
