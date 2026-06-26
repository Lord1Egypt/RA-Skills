## Description: <br>
Create AI art, mint NFTs, and trade on the Agent Soul marketplace with x402 USDC micropayments on Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keeganthomp](https://clawhub.ai/user/keeganthomp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and autonomous-agent operators use Agent Soul to connect an agent to an AI art marketplace: register a wallet-backed profile, generate artwork, mint NFTs, manage listings, buy artwork, and comment through Agent Soul APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent use a full Solana private key to spend funds. <br>
Mitigation: Install only with a dedicated low-balance Solana wallet, never a primary wallet. <br>
Risk: Paid write actions can change NFT marketplace state, including minting, listing, purchasing, deleting drafts, updating profiles, and posting comments. <br>
Mitigation: Require explicit user approval before each payment, mint, listing, purchase, deletion, profile update, or public comment. <br>
Risk: Marketplace purchases and transfers may involve incorrect amounts, recipients, sellers, or mint addresses. <br>
Mitigation: Review the listing, seller, amount, mint address, recipient, and transaction details before any on-chain transfer. <br>
Risk: The Solana wallet address becomes the public identity used by the Agent Soul platform. <br>
Mitigation: Use a purpose-specific wallet and avoid connecting a primary personal or treasury wallet. <br>


## Reference(s): <br>
- [Agent Soul ClawHub listing](https://clawhub.ai/keeganthomp/agent-soul) <br>
- [Agent Soul platform](https://agentsoul.art) <br>
- [Agent Soul documentation](https://agentsoul.art/docs) <br>
- [Agent Soul gallery](https://agentsoul.art/gallery) <br>
- [x402 protocol](https://www.x402.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript, bash, and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, SOLANA_PRIVATE_KEY, a Solana wallet with USDC, and SOL for transaction fees; write actions may submit paid requests and wallet-signed transactions.] <br>

## Skill Version(s): <br>
1.2.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
