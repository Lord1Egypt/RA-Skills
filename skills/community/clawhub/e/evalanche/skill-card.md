## Description:

A multi-EVM agent wallet SDK for on-chain identity, payments, cross-chain transfers, trading, market data, and DeFi operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ijaack](https://clawhub.ai/user/ijaack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Evalanche to create or connect an EVM wallet and obtain wallet, identity, payment, bridge, trading, market-data, and DeFi capabilities across supported networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet keys or mnemonics can authorize transfers, trades, and other on-chain actions.

Mitigation: Protect credentials in the encrypted keystore or an approved secret store, use a dedicated wallet with limited funds, and review transaction details before signing.

Risk: An exposed HTTP MCP endpoint could make wallet tools reachable to unintended callers.

Mitigation: Keep HTTP mode bound to localhost, require its authentication token, and apply additional network controls before any remote access.

## Reference(s):

- [Evalanche repository](https://github.com/iJaack/evalanche)

## Skill Output:

**Output Type(s):** [API data, Transaction and signature data, Configuration]

**Output Format:** [Structured responses and transaction or signature results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some operations can sign or submit financial transactions and incur network or venue costs.]

## Skill Version(s):

1.18.0 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
