## Description: <br>
NFT operations on BNB Chain: get NFT metadata, check ownership, list NFTs by owner, transfer ERC-721 tokens, and get collection information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CLAWZAI](https://clawhub.ai/user/CLAWZAI) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and agents use this skill to inspect ERC-721 collections and tokens on BNB Chain, including collection metadata, token ownership, wallet balances, and owned token lists. It can also submit NFT transfers and approval transactions when configured with a wallet private key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign real BNB Chain NFT transfers and approval transactions when a private key is provided. <br>
Mitigation: Use a dedicated low-value wallet, confirm the contract, recipient, token ID, and operator before signing, and test write actions on testnet first. <br>
Risk: The approve-all operation can grant broad transfer authority over an NFT collection until revoked. <br>
Mitigation: Avoid approve-all unless required, verify the operator address independently, and revoke collection-wide approvals when they are no longer needed. <br>
Risk: Passing a private key with a command-line flag may expose it through shell history or local process inspection. <br>
Mitigation: Prefer a short-lived environment variable or a dedicated secret-handling workflow, and never commit private keys to source control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CLAWZAI/bnb-nft) <br>
- [ethers package](https://registry.npmjs.org/ethers/-/ethers-6.16.0.tgz) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from command-line operations with setup and usage guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read operations use a BNB Chain JSON-RPC provider; write operations require a private key supplied by environment variable or command-line flag.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
