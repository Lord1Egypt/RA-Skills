## Description: <br>
Help developers write code that interacts with Alkahest escrow contracts using the TypeScript, Rust, or Python SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mlegls](https://clawhub.ai/user/mlegls) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate applications, bots, agents, custom arbiters, and obligation contracts with Alkahest escrow workflows across TypeScript, Rust, and Python SDKs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples include private-key placeholders and RPC setup patterns that could be copied into source files. <br>
Mitigation: Use dedicated secret storage and testnet credentials; never paste real private keys into source files or chat. <br>
Risk: Blockchain examples include token approvals and transaction-sending workflows that can move or lock assets. <br>
Mitigation: Require explicit human review of approvals, contract addresses, token amounts, arbiters, and target networks before sending transactions. <br>
Risk: SDK package names and contract addresses may be security-sensitive integration points. <br>
Mitigation: Verify package names and contract addresses against official Alkahest sources before installing dependencies or deploying integrations. <br>


## Reference(s): <br>
- [Alkahest Contract Reference](references/contracts.md) <br>
- [Alkahest TypeScript SDK API Reference](references/typescript-api.md) <br>
- [Alkahest Rust SDK API Reference](references/rust-api.md) <br>
- [Alkahest Python SDK API Reference](references/python-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with SDK code examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for blockchain SDK integration; examples require user review before transaction execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
