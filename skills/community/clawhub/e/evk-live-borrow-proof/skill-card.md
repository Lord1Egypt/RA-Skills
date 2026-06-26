## Description: <br>
Prove that a deployed Euler EVK market can really borrow against the intended collateral path with tiny live canaries or dry-run previews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daav3](https://clawhub.ai/user/daav3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to validate whether a deployed Euler EVK market can actually borrow against a target collateral path on an EVM chain. It supports preview-first checks and tiny live canary transactions for controller rotation, collateral isolation, debt cleanup, and chain-specific borrow proof reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can send real on-chain transactions from the configured signer. <br>
Mitigation: Run preview mode first, use a dedicated low-value wallet, require explicit live mode acknowledgement, keep canary amounts tiny, and verify that the configured account matches the signer before sending. <br>
Risk: Signer material or wallet credentials could be exposed or misused. <br>
Mitigation: Keep signer material in environment variables or local runtime configuration, never commit secrets, and use the declared LIVE_SIGNER_ENV only for the intended proof wallet. <br>
Risk: Incorrect contract addresses, router settings, amounts, approvals, or slippage limits can produce failed or unsafe transactions. <br>
Mitigation: Verify every contract address, token decimal, amount, router, fee tier, and slippage setting; require nonzero swap protection for live swaps and use exact approvals unless unlimited approval is explicitly chosen. <br>
Risk: A tiny borrow canary does not prove large borrow sizing, liquidation safety, cross-chain router portability, or production monitoring readiness. <br>
Mitigation: Report exactly what was proven, keep live checks small, identify chain-specific assumptions, and treat production sizing and monitoring as separate reviews. <br>


## Reference(s): <br>
- [EVK live borrow checklist](references/live-borrow-checklist.md) <br>
- [Arbitrum eUSDC-1 isolated example configuration](references/arbitrum-eusdc1-isolated-example.json) <br>
- [Agentic lending project](https://github.com/daav3/agentic-lending-project) <br>
- [ClawHub skill page](https://clawhub.ai/daav3/evk-live-borrow-proof) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples, configuration guidance, and transaction proof summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports chain, account, mode, vaults, debt state, collateral state, liquidity snapshot, live transaction hashes when applicable, and remaining unproven assumptions.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
