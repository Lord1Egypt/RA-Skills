## Description:

Guides Aave V3 position risk checks, borrow sizing, and repay or collateral withdrawal planning with eMode and isolation constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

DeFi users and developers use this skill to assess an Aave V3 account's health factor, size a proposed borrow, and plan a repay or collateral withdrawal using current pool and reserve data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect chain, pool, account, token amounts, or stale position data could lead to an unsafe borrowing or withdrawal decision.

Mitigation: Verify deployment and account, reconcile fresh pool and reserve reads at a recorded block, and check amounts and assumptions before acting.

Risk: A proposed transaction could require allowances or change position risk before it is signed.

Mitigation: Verify allowances and simulate the exact action and subsequent position; never provide private keys or seed phrases.

## Reference(s):

- [Aave V3 MCP procedure](references/mcp.md)
- [Aave read recipe and worked decision](references/recipe.md)
- [Aave V3 Pool interface](https://aave.com/docs/aave-v3/smart-contracts/pool)
- [Aave health factor and liquidations](https://aave.com/help/borrowing/liquidations)
- [Aave address book](https://github.com/bgd-labs/aave-address-book)
- [Aave MCP tool documentation](https://aave.com/docs/mcp/tools)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown decision record with calculations and optional unsigned transaction steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records the deployment, block, assumptions, and missing reads; distinguishes estimates, simulations, and confirmed transactions.]

## Skill Version(s):

0.3.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
