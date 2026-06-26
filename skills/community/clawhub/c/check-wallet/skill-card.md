## Description: <br>
Query OpenAnt wallet addresses and on-chain balances for Solana, EVM, native assets, and token holdings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ant-1984](https://clawhub.ai/user/ant-1984) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check OpenAnt wallet status, wallet addresses, SOL or ETH balances, token holdings, and insufficient-balance issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose wallet addresses and balances from a local OpenAnt session. <br>
Mitigation: Review before installing and require explicit confirmation before revealing full wallet identifiers or holdings. <br>
Risk: The allowed wallet command access is broader than a read-only balance checker needs. <br>
Mitigation: Narrow allowed commands to status, wallet addresses, and wallet balance where the host agent supports command restrictions. <br>
Risk: The skill invokes an external CLI with the latest version selector. <br>
Mitigation: Pin or review the OpenAnt CLI version before use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the local OpenAnt CLI session and on-chain RPC queries to return wallet addresses and balances.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
