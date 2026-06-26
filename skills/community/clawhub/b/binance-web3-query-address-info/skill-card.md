## Description: <br>
Queries a wallet address on a supported chain and returns current token holdings with token name, symbol, price, 24-hour price change, and quantity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binance-skills-hub](https://clawhub.ai/user/binance-skills-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect the token holdings of an explicitly provided EVM or Solana wallet address on supported chains. It is suited for portfolio snapshots and balance breakdowns, not transaction signing or trade execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [CLI Reference](references/cli.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, API calls, Guidance] <br>
**Output Format:** [JSON CLI responses that agents may summarize as text or Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an explicit wallet address, chainId, and pagination offset. Wallet addresses may reveal financial activity and may be sent to Binance Web3 when the CLI is used.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release; artifact metadata version 2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
