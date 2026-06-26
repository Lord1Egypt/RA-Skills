## Description: <br>
Telegram Web App for Chia wallet verification via WalletConnect and Sage that enables cryptographic proof of wallet ownership through signature verification using MintGarden API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Koba42Corp](https://clawhub.ai/user/Koba42Corp) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and Telegram community operators use this skill to verify Chia wallet ownership for NFT-gated groups, airdrop eligibility, DAO voting, and Web3-style authentication flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wallet verification flow links Chia addresses to Telegram users with weak disclosure. <br>
Mitigation: Add an explicit consent and privacy notice before collecting or storing wallet and Telegram identity data. <br>
Risk: The included WalletConnect Project ID is a reference value and may not be appropriate for production. <br>
Mitigation: Create and configure an operator-owned WalletConnect Project ID before production deployment. <br>
Risk: Sensitive wallet, signature, or identity data may be exposed through console logging or broad service access. <br>
Mitigation: Remove sensitive console logging, restrict CORS to trusted origins, and authenticate or remove the status endpoint. <br>
Risk: Client-supplied Telegram user IDs can be spoofed if used directly for access or airdrop eligibility decisions. <br>
Mitigation: Bind verification decisions to trusted Telegram bot context instead of trusting user IDs supplied by client JSON. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Koba42Corp/chia-walletconnect) <br>
- [MintGarden API documentation](https://api.mintgarden.io/docs) <br>
- [WalletConnect documentation](https://docs.walletconnect.com/) <br>
- [Telegram Web Apps documentation](https://core.telegram.org/bots/webapps) <br>
- [Sage Wallet](https://www.sagewallet.io/) <br>
- [CHIP-0002](https://github.com/Chia-Network/chips/blob/main/CHIPs/chip-0002.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JavaScript examples, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions and runnable Node.js assets for a Telegram Web App, CLI, and optional Express service.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
