## Description: <br>
Executes multiple token swaps in sequence for rebalancing or multi-step trading plans, with each swap independently safety-validated. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and wallet operators use this skill to plan and execute a sequence of Uniswap token swaps, such as portfolio rebalancing or multi-leg trading plans, while checking safety and balances for each leg. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate multiple wallet-affecting trades in one workflow. <br>
Mitigation: Require explicit user confirmation for the full batch and for each swap, including token contracts, chain, input amounts, expected outputs, slippage, gas, and maximum total spend. <br>
Risk: A trusted wallet and trade-executor setup is required for safe operation. <br>
Mitigation: Use only trusted wallet and trade-executor configurations with strict spending limits before enabling batch execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/batch-swap) <br>
- [Publisher profile](https://clawhub.ai/user/wpank) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, markdown] <br>
**Output Format:** [Markdown summary with swap outcomes, transaction identifiers, gas totals, and error messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses sequential execution with independent safety and balance checks; default behavior halts remaining swaps after the first failure.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
