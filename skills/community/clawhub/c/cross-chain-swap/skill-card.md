## Description: <br>
Execute a cross-chain token swap via Uniswap's bridge infrastructure. Handles quoting, safety validation, bridge monitoring, and destination confirmation. Use when the user wants to swap tokens across different chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to request token swaps across supported chains, with the agent handling quoting, route checks, bridge monitoring, and a final execution report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delegate real cross-chain fund movement without clearly requiring final approval after the exact quote, fees, slippage, recipient, and transaction data are known. <br>
Mitigation: Require the agent or wallet to show the exact source and destination chains, tokens, amount, recipient, route, estimated received amount, fees, slippage, transaction data, and irreversibility, then obtain explicit user approval or wallet signing before funds move. <br>
Risk: Cross-chain bridge operations can take time to settle and may become stuck or fail. <br>
Mitigation: Monitor bridge status through settlement, report delays clearly, and provide recovery instructions or source-wallet balance checks when settlement is delayed or fails. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/cross-chain-swap) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain-text execution report with source and destination amounts, fees, settlement time, transaction identifiers, and risk or safety status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires exact chain, token, amount, recipient, route, fee, slippage, and transaction details to be reviewed before funds move.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
