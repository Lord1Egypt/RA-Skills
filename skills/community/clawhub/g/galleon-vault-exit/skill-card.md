## Description:

Helps assess how to exit an ERC4626 vault by checking withdrawal limits, previews, fees, liquidity, and asynchronous exit requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and vault holders use this skill to assess whether an ERC4626 vault exit is feasible, compare withdrawal and redemption options, and prepare a documented exit decision without signing a transaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vault exits may receive less than expected or fail because previews do not guarantee current liquidity or fees.

Mitigation: Check current withdrawal limits, fees, and execution conditions; review and simulate the proposed sequence before signing.

Risk: Unexplained approvals or key disclosure could compromise a wallet.

Mitigation: Keep signing in the user's own wallet, never provide private keys, and do not approve unexplained routers.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/galleonlabs/skills/galleon-vault-exit)
- [ERC4626 read recipe and worked exit](references/recipe.md)
- [ERC4626 standard](https://eips.ethereum.org/EIPS/eip-4626)
- [ERC7540 asynchronous vaults](https://eips.ethereum.org/EIPS/eip-7540)
- [OpenZeppelin ERC4626 guidance](https://docs.openzeppelin.com/contracts/5.x/erc4626)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown decision record with optional unsigned transaction steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Identifies chain, vault, block, amounts, assumptions, limits, and missing evidence.]

## Skill Version(s):

0.2.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
