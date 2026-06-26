## Description: <br>
Interact with ERC-20 smart contracts through read and write functions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justinxai](https://clawhub.ai/user/justinxai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Ethereum RPC access, query ERC-20 contract state, and prepare token write operations such as transfers, approvals, minting, and burns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a raw wallet private key for ERC-20 write transactions. <br>
Mitigation: Use a dedicated low-value wallet key and avoid main wallet credentials. <br>
Risk: Transfers, approvals, minting, and burns can have permanent financial consequences. <br>
Mitigation: Before any write call, manually verify the network, contract address, recipient or spender, amount, gas, and approval impact. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with TypeScript examples and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RPC_URL, PRIVATE_KEY, and CONTRACT_ADDRESS environment configuration before write operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
