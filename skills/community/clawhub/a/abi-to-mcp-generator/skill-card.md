## Description:

Interact with ERC20 smart contracts through read and write functions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justinxai](https://clawhub.ai/user/justinxai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Web3 engineers use this skill to query ERC20 token state and prepare contract-changing calls such as transfers, approvals, minting, and burning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private key configuration can expose or misuse funds if the key is shared, stored insecurely, or connected to the wrong contract.

Mitigation: Use a dedicated low-balance key or secure signer and verify the RPC endpoint and contract address before any write operation.

Risk: Transfers, approvals, minting, and burning can be irreversible or privileged token-changing actions.

Mitigation: Review every recipient, spender, amount, and permission before execution, avoid broad approvals, and confirm that mint or burn applies to the target token.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justinxai/skills/abi-to-mcp-generator)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RPC_URL, PRIVATE_KEY, and CONTRACT_ADDRESS configuration before use.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
