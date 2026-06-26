## Description: <br>
Openclaw Fomo3d provides an agent-oriented CLI for playing Fomo3D and its slot-machine game on BNB Chain, including wallet setup, game status checks, token trading, share purchases, dividend claims, and slot spins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ErenVance](https://clawhub.ai/user/ErenVance) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate a BNB Chain wallet against the Fomo3D game and slot-machine contracts from an agent-driven CLI. It is intended for checking balances and game state, buying or selling FOMO tokens, purchasing shares, claiming rewards, and submitting slot-machine actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can spend wallet funds on BNB Chain transactions. <br>
Mitigation: Use a dedicated low-balance BSC wallet, start on testnet when possible, verify contract addresses, and review every amount before execution. <br>
Risk: Setup can save a raw private key to config.json. <br>
Mitigation: Do not use a primary wallet key, and avoid setup unless the local config file can be protected. <br>
Risk: Token operations may grant unlimited allowances. <br>
Mitigation: Revoke token allowances after use and review approvals before continuing with buy, sell, purchase, spin, or deposit commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ErenVance/fomo3d) <br>
- [Fomo3D Homepage](https://fomo3d.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can submit BNB Chain transactions and return transaction hashes, balances, game state, token data, and configuration prompts.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
