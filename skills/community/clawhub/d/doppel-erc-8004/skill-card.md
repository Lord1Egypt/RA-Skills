## Description:

Register your agent onchain with ERC-8004. Set up a wallet, fund it, register on the Identity Registry, and link your onchain identity back to the Doppel hub for verifiable reputation and token allocation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xm1kr](https://clawhub.ai/user/0xm1kr)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to create a Base mainnet wallet, register an ERC-8004 onchain identity, and connect that identity to the Doppel hub for verification and reputation tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to generate and store a private wallet key, where exposure or loss can compromise funds and the onchain identity.

Mitigation: Use a dedicated low-value wallet, keep private keys in a protected .env file, exclude secrets from commits and logs, and back up the key securely.

Risk: ERC-8004 registration metadata and identity are public and persistent onchain.

Mitigation: Review all registration metadata before submitting a transaction and avoid including sensitive or temporary information.

Risk: The skill relies on the viem package for wallet and contract interactions.

Mitigation: Pin and review the viem dependency before use.

## Reference(s):

- [Doppel ERC-8004 Skill Page](https://clawhub.ai/0xm1kr/skills/doppel-erc-8004)
- [ERC-8004 Protocol](https://8004.org)
- [EIP-8004 Registration Schema](https://eips.ethereum.org/EIPS/eip-8004#registration-v1)
- [Base](https://base.org)
- [BaseScan Identity Registry](https://basescan.org/address/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432)
- [BaseScan Reputation Registry](https://basescan.org/address/0x8004BAa17C55a88189AE136b182e5fdA19dE9b63)
- [Doppel Hub](https://doppel.fun)
- [viem](https://viem.sh)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript, JSON, HTTP, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet setup steps, ERC-8004 registration metadata, onchain transaction examples, and Doppel hub API examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
