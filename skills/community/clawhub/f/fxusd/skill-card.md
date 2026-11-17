## Description:

fxUSD helps agents plan and compare Base yield workflows for fxSAVE, Hydrex single-sided liquidity, and Morpho supply or borrow, emitting Bankr-ready transaction steps with protocol-specific risk controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huwangtao123](https://clawhub.ai/user/huwangtao123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use fxUSD to compare and prepare Base DeFi yield actions across fxSAVE, Hydrex vaults, and Morpho markets. It is most useful when an agent must turn a wallet-level intent into reviewed planning output or Bankr-ready transaction steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill prepares real wallet transactions for DeFi protocols.

Mitigation: Before submitting any Bankr step, verify the token, spender, destination contract, amount, chain, vault or market, and slippage or minimum-output protections.

Risk: Generated plans rely on third-party services and live protocol data.

Mitigation: Review API-derived routes, market availability, vault selection, balances, allowances, and protocol warnings before execution.

Risk: Morpho borrow workflows can create liquidation exposure.

Mitigation: Use conservative LTV buffers, run risk or alert checks first, and keep the final borrow decision with the user.

Risk: Hydrex single-sided deposits can unwind into mixed-token withdrawals.

Mitigation: Confirm the vault risk class and withdrawal composition risk before recommending or submitting a deposit.

Risk: fxSAVE settlement may lag the source-chain confirmation.

Mitigation: Explain cross-chain settlement timing and quote drift before treating a route as complete.

## Reference(s):

- [fxSAVE app](https://fxsave.up.railway.app/)
- [fxSAVE Shortcut API Reference](artifact/references/api.md)
- [Hydrex Single-Sided Liquidity](artifact/references/hydrex.md)
- [Morpho Planning](artifact/references/morpho.md)
- [Hydrex Platform](https://hydrex.fi)
- [Morpho](https://morpho.org/)
- [Morpho GraphQL API](https://docs.morpho.org/tools/offchain/api/graphql/)
- [Morpho Blue Contract Interface](https://github.com/morpho-org/morpho-blue/blob/main/src/interfaces/IMorpho.sol)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON transaction plans, command examples, and Bankr-ready execution steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans may include live API-derived route, vault, market, balance, allowance, and LTV data that users should review before submitting wallet transactions.]

## Skill Version(s):

1.0.1 (source: evidence.json release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
