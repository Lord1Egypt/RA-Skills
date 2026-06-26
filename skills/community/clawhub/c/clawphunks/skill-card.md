## Description: <br>
Mint and trade ClawPhunks NFTs. The first collection designed for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jefdiesel](https://clawhub.ai/user/jefdiesel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use Clawphunks to inspect the NFT collection, mint ClawPhunks with x402 USDC payments, and retrieve trading instructions for Ethereum L1 escrow workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet and payment actions can move funds or assets. <br>
Mitigation: Use only a dedicated low-value wallet, set strict spending limits, and require explicit human approval before minting, buying, listing, transferring, or rescue actions. <br>
Risk: Remote endpoints may return executable scripts or transaction code. <br>
Mitigation: Review returned scripts before use and do not automatically execute code fetched from remote endpoints. <br>
Risk: Evidence reports an exposed Coinbase API secret. <br>
Mitigation: Treat the exposed key as compromised and avoid relying on the package until the publisher rotates the credential and removes wallet-enumeration code. <br>


## Reference(s): <br>
- [Clawphunks homepage](https://clawphunks.vercel.app) <br>
- [ClawHub release page](https://clawhub.ai/jefdiesel/clawphunks) <br>
- [Publisher profile](https://clawhub.ai/user/jefdiesel) <br>
- [Skills documentation](https://clawphunks.vercel.app/skills) <br>
- [Escrow contract](https://etherscan.io/address/0x3e67d49716e50a8b1c71b8dEa0e31755305733fd) <br>
- [Ethscriptions collection](https://ethscriptions.com/collections/0xb432d8c446afefb98651e05c8eee22a8617bd7a0b239dfab70e1fb3a02aa9e8a) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-like tool responses with inline TypeScript, Python, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet setup, x402 payment, minting, rarity, and escrow trading guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
