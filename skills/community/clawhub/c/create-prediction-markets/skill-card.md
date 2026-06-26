## Description: <br>
Create, trade, and settle prediction markets on Base with any ERC20 collateral. Use when building prediction market infrastructure, running contests, crowdsourcing probability estimates, adding utility to tokens, or tapping into true information finance via market-based forecasting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[proxima424](https://clawhub.ai/user/proxima424) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to create, trade, settle, and redeem prediction markets on Base Mainnet with ERC20 collateral. It supports market infrastructure, contests, token utility, and market-based forecasting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a wallet private key to submit live Base Mainnet transactions and move real funds. <br>
Mitigation: Use a dedicated low-balance wallet, avoid primary wallet keys, and manually confirm transaction parameters before broadcasting. <br>
Risk: The artifact documents persistent ERC20 approvals, which can leave token allowances active beyond a single transaction. <br>
Mitigation: Review contract addresses and token allowances before use, and prefer exact approvals over unlimited approvals where practical. <br>


## Reference(s): <br>
- [PNP SDK API Reference](references/api-reference.md) <br>
- [PNP Markets Use Cases](references/use-cases.md) <br>
- [PNP Markets Complete Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CLI workflows and programmatic TypeScript examples for Base Mainnet prediction market transactions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
