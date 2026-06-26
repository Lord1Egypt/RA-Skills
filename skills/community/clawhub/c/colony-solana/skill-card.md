## Description: <br>
Play Colony game on Solana -- buy lands, upgrade, claim $OLO earnings, swap tokens via Jupiter, and use ROI-based strategy optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manylov](https://clawhub.ai/user/manylov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage a dedicated Colony game wallet on Solana mainnet, including land purchases, upgrades, claims, swaps, and ROI-oriented recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an autonomous agent control over a Solana hot wallet with real funds. <br>
Mitigation: Use a new low-balance wallet dedicated to this skill and never use a primary wallet. <br>
Risk: Swaps, land purchases, and upgrades can spend tokens without strong built-in spending limits or approval controls. <br>
Mitigation: Require manual review for swaps, purchases, and upgrades until spending limits and protocol admin risks are clear. <br>
Risk: The private key is required for write commands and may be exposed if copied into logs or shared files. <br>
Mitigation: Keep the private key in a protected environment variable and out of logs, chat transcripts, and repository files. <br>
Risk: Program and token addresses are used for mainnet transactions. <br>
Mitigation: Verify program and token addresses independently before funding the wallet or executing write commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/manylov/colony-solana) <br>
- [Publisher profile](https://clawhub.ai/user/manylov) <br>
- [Colony game](https://colony.game) <br>
- [Jupiter portal](https://portal.jup.ag) <br>
- [Solana mainnet RPC endpoint](https://api.mainnet-beta.solana.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, API calls] <br>
**Output Format:** [Markdown instructions with shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may require SOLANA_PRIVATE_KEY, SOLANA_RPC_URL, and JUPITER_API_KEY depending on the action.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
