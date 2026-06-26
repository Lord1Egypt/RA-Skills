## Description: <br>
Agnic lets an AI agent manage a wallet, payments, token trades, email, on-chain identity, AI chat, and image generation through the Agnic CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent authenticate to Agnic, inspect wallet status, make X402 payments, send USDC, trade supported tokens, manage agent email, check identity, and call AI gateway features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet, trading, payment, transfer, and email commands can perform high-impact external actions. <br>
Mitigation: Require explicit user confirmation before every payment, trade, transfer, or email, and use only low-value or test wallets until the integration is reviewed. <br>
Risk: The skill can expose wallet, identity, email, or prompt content to Agnic and AI gateway providers. <br>
Mitigation: Avoid sending private identity, wallet, email, or sensitive prompt content unless the user trusts the provider and understands the data flow. <br>
Risk: The security verdict is suspicious because broad wallet, trading, email, identity, AI-chat, and image-generation powers are not narrowly scoped in the artifact. <br>
Mitigation: Review the allowed `npx agnic@latest` command surface before installation and restrict use to approved Agnic CLI operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/agnicpay-prog/agnic) <br>
- [Publisher profile](https://clawhub.ai/user/agnicpay-prog) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples, CLI text or JSON responses, and optional generated image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Agnic OAuth authentication and wallet access; some commands can initiate payments, trades, transfers, emails, AI chat calls, or image generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
