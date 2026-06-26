## Description: <br>
Audit and deploy blockchain smart contracts for Solidity, Sui Move, and Solana projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rzexin](https://clawhub.ai/user/rzexin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to identify smart contract type, run automated and reasoning-based audits, generate audit reports, and prepare deployments across EVM, Sui Move, and Solana ecosystems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle wallet credentials and execute real on-chain deployments that may spend funds. <br>
Mitigation: Review before production use, prefer testnets and dry runs, use dedicated low-balance deploy wallets, and require explicit network and account checks before deployment. <br>
Risk: The Solidity deployment helper can expose private-key material in command execution or error output. <br>
Mitigation: Do not use shared or production private keys with the current Solidity helper unless the private-key error-output issue is fixed; prefer keystores or hardware wallets. <br>
Risk: Mainnet deployments are irreversible and can have real financial cost. <br>
Mitigation: Use the audit gate before deployment, require explicit mainnet confirmation, run compile and balance checks, and perform a dry run before broadcasting transactions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rzexin/chain-audit-deploy-skill) <br>
- [Publisher profile](https://clawhub.ai/user/rzexin) <br>
- [Project homepage](https://git.woa.com/jasonruan/chain-audit-deploy-skill) <br>
- [Multi-Chain Deployment Guide](references/deployment_guide.md) <br>
- [Solidity Audit Rules Reference](references/solidity_audit_rules.md) <br>
- [Sui Move Audit Rules Reference](references/sui_move_audit_rules.md) <br>
- [Solana Audit Rules Reference](references/solana_audit_rules.md) <br>
- [Smart Contract Audit Report Template](assets/report_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown audit reports, JSON audit summaries, shell commands, and deployment guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include contract findings, severity summaries, deployment commands, network/account checks, transaction identifiers, explorer links, and tool installation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
