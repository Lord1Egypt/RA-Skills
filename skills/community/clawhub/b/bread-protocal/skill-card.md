## Description: <br>
Bread Protocal helps agents and users participate in Bread Protocol on Base by proposing meme coins, backing proposals, claiming rewards, and following daily competitions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChrisSorrell](https://clawhub.ai/user/ChrisSorrell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agents use this skill to understand Bread Protocol participation flows and prepare Base mainnet contract interactions for proposals, backing, withdrawals, token claims, and refunds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill discusses raw wallet-key use for signing transactions. <br>
Mitigation: Do not paste a main-wallet private key into an agent; use a dedicated low-balance wallet or a wallet flow that requires manual signing. <br>
Risk: The skill guides real Base mainnet transactions involving ETH, BREAD approvals, proposal IDs, and gas costs. <br>
Mitigation: Independently verify the website, Base chain, contract addresses, approval amounts, proposal IDs, ETH values, and gas before every transaction. <br>
Risk: Token approvals and backing actions can leave ongoing permissions or expose funds to irreversible transaction outcomes. <br>
Mitigation: Use limited approval amounts, confirm transaction details before signing, and revoke allowances when participation is complete. <br>


## Reference(s): <br>
- [Contract Reference](references/contracts.md) <br>
- [Workflows](references/workflows.md) <br>
- [Bread Protocol Website](https://getbread.fun) <br>
- [ClawHub Skill Page](https://clawhub.ai/ChrisSorrell/bread-protocal) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JavaScript and contract interaction examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Base mainnet contract addresses, function selectors, wallet setup guidance, and transaction flow examples.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
