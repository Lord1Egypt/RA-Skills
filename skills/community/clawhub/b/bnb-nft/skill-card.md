## Description:

NFT operations on BNB Chain -- get NFT metadata, check ownership, list NFTs by owner, transfer ERC-721 tokens, get collection info.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawzai](https://clawhub.ai/user/clawzai)

### License/Terms of Use:

ISC

## Use Case:

External developers and NFT operators use this skill to inspect ERC-721 collection details, ownership, balances, metadata, approvals, and BNB Chain NFT transfers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transfer and approval commands can move NFTs or grant another address permission to transfer them.

Mitigation: Use a dedicated low-value wallet, verify every contract and recipient or operator address, test transfer flows on testnet first, and avoid approve-all unless it is necessary.

Risk: Private keys are required for write operations and can be exposed through command history or process listings when passed as CLI arguments.

Mitigation: Prefer short-lived environment variables or a safer wallet workflow, avoid passing private keys on the command line, and never commit keys to source control.

Risk: Metadata lookups may contact URLs controlled by NFT contracts.

Mitigation: Treat fetched metadata as untrusted content and run metadata inspection only in environments where outbound network access is acceptable.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, ethers.js, BNB Chain RPC access, and a wallet private key for transfer or approval operations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
