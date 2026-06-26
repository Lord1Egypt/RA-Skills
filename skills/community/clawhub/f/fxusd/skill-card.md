## Description: <br>
fxUSD helps agents deploy, unwind, and compare fxUSD-related yield strategies on Base across fxSAVE, Hydrex, and Morpho, producing planning outputs and Bankr-ready transaction steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huwangtao123](https://clawhub.ai/user/huwangtao123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, DeFi operators, and wallet agents use this skill to plan fxUSD yield actions on Base, including fxSAVE mint or redeem flows, Hydrex vault deposits and withdrawals, and Morpho supply, borrow, repay, or collateral-management workflows. It is intended to prepare human-reviewable plans and transaction steps before wallet execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill prepares executable DeFi wallet transactions using third-party data. <br>
Mitigation: Review chain, token, spender, recipient, amount, calldata target, and slippage or minimum-output assumptions before signing. <br>
Risk: Hydrex actions may include zero minimum output fields or withdrawal composition that differs from the entry asset. <br>
Mitigation: Confirm the vault, expected output shape, and user acceptance of withdrawal composition risk before execution. <br>
Risk: Morpho borrow and collateral-management flows can create liquidation exposure. <br>
Mitigation: Require explicit collateral, market, oracle, and liquidation-buffer checks, and keep the final borrow or collateral decision with the user. <br>
Risk: Bankr execution can submit high-impact wallet actions. <br>
Mitigation: Use Bankr execution only after explicit human approval of the prepared transaction details. <br>


## Reference(s): <br>
- [fxUSD Skill Page](https://clawhub.ai/huwangtao123/fxusd) <br>
- [fxSAVE App](https://fxsave.up.railway.app/) <br>
- [fxSAVE Shortcut API Reference](references/api.md) <br>
- [Hydrex Single-Sided Liquidity](references/hydrex.md) <br>
- [Morpho Lend / Borrow](references/morpho.md) <br>
- [Hydrex Platform](https://hydrex.fi) <br>
- [Morpho](https://morpho.org/) <br>
- [Morpho GraphQL API](https://docs.morpho.org/tools/offchain/api/graphql/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON transaction plans and Bankr-ready command or request steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include executable wallet transaction details that require explicit human review before signing.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
