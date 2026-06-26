## Description: <br>
A multi-chain wallet skill for AI agents, with local sandbox signing, secure PIN handling, and configurable risk controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawwalletteam](https://clawhub.ai/user/clawwalletteam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use ClawWallet to install and operate a local multi-chain wallet sandbox, inspect wallet status and balances, bind wallets, and sign or transfer assets through user-confirmed flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles wallet bearer tokens and local identity files. <br>
Mitigation: Keep .env.clay and identity.json private, and do not print or share AGENT_TOKEN or CLAY_AGENT_TOKEN. <br>
Risk: The skill runs remote installers and sandbox binaries whose server-resolved GitHub import provenance is unavailable. <br>
Mitigation: Install only when the publisher is trusted and the installer and sandbox binary provenance can be verified. <br>
Risk: The skill can sign transactions and transfer assets. <br>
Mitigation: Require explicit user confirmation and check recipient, chain, amount, fees, and contract details before approving wallet transactions. <br>
Risk: Reinstall, upgrade, and uninstall flows can rewrite or remove persistent wallet files. <br>
Mitigation: Run those flows only after explicit user approval, and back up .env.clay, identity.json, and share3.json before uninstalling. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/clawwalletteam/claw-wallet-pro) <br>
- [Claw Wallet website](https://www.clawwallet.cc) <br>
- [Claw Wallet skill repository](https://github.com/ClawWallet/Claw-Wallet-Skill) <br>
- [Claw Wallet binary repository](https://github.com/ClawWallet/Claw_Wallet_Bin) <br>
- [Claw Wallet distribution host](https://www.clawwallet.cc/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, PowerShell commands, API request examples, and configuration paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local sandbox URL and bearer token; wallet-changing actions require explicit user confirmation.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata and skill.yml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
