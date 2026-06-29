## Description: <br>
Use when creating, validating, backtesting, deploying, sizing, or troubleshooting Aerodrome/Base spot trading strategies through the Superior Trade API, especially Freqtrade configs using exchange.name "aerodrome", AERO/USDC or CHECK/USDC pairs, AMM market swaps, wallet/gas balance checks, no-orderbook pricing, or Aerodrome live deployment safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superior-ai](https://clawhub.ai/user/superior-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading operators use this skill to create, validate, backtest, deploy, size, and troubleshoot Aerodrome spot trading strategies on Base through the Superior Trade API. It focuses on supported AERO/USDC and CHECK/USDC AMM market swaps, wallet and gas checks, and live deployment safety. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live deployment can trade with real funds through Aerodrome on Base. <br>
Mitigation: Require explicit user confirmation before starting a live bot, verify wallet token balances and Base ETH gas, and review the generated configuration and strategy. <br>
Risk: API keys or wallet secrets could be exposed if pasted into commands, files, logs, or chat. <br>
Mitigation: Use environment variables for the Superior Trade API key, prefer a limited key where possible, and never include wallet private keys in generated configs or commands. <br>
Risk: Incorrect Freqtrade settings could propose unsupported leverage, shorting, futures, order-book pricing, or unsupported pairs. <br>
Mitigation: Keep Aerodrome configs spot-only, restrict pairs to AERO/USDC and CHECK/USDC, use AMM market orders with order-book pricing disabled, and backtest before live deployment. <br>


## Reference(s): <br>
- [Superior Trade API](https://api.superior.trade) <br>
- [Base Mainnet RPC](https://mainnet.base.org) <br>
- [Aerodrome skill release page](https://clawhub.ai/superior-ai/aerodrome) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON, Python, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Freqtrade configuration, strategy code, API curl commands, backtest interpretation, deployment checklists, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
