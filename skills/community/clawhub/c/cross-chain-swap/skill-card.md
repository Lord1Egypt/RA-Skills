## Description:

Execute a cross-chain token swap via Uniswap's bridge infrastructure, including quoting, safety validation, bridge monitoring, and destination confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to request token swaps between supported chains through a single workflow that validates chains and tokens, obtains a route, monitors bridge settlement, and reports the final destination result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cross-chain swaps can move assets and incur irreversible financial loss if the route, token addresses, chain IDs, fees, slippage, minimum received amount, recipient, or approval transaction are wrong.

Mitigation: Require explicit user review of the complete route and final wallet transaction approval before any swap execution, and test with a small amount first.

Risk: The provided installation paths rely on mutable remote installers or sources.

Mitigation: Use pinned, verified installer versions and immutable skill sources before installing or deploying the skill.

Risk: Bridge settlement can be delayed or fail, requiring user-visible recovery guidance.

Mitigation: Monitor bridge status through completion and surface clear recovery instructions if settlement is delayed or the bridge operation fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/cross-chain-swap)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain-text execution reports with transaction identifiers, amounts, fees, settlement status, warnings, and recovery guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports source and destination amounts, gas and bridge fees, settlement time, source transaction, bridge identifier, destination transaction, and risk and safety status when available.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
