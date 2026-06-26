## Description: <br>
Play Defipoly, a Monopoly-inspired DeFi game on Solana, by buying properties, earning daily DPOLY yield, shielding against theft, stealing from players or the bank, and rolling dice for bonuses with an autonomously managed funded wallet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Rengon0x](https://clawhub.ai/user/Rengon0x) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate a Defipoly game wallet, inspect game state, and execute supported Solana game actions through the bundled CLI. It is intended for users who understand the risks of funding a game-specific wallet for autonomous on-chain play. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign and submit funded Solana mainnet transactions for game actions. <br>
Mitigation: Use a dedicated, low-balance Defipoly wallet and keep only small SOL and DPOLY amounts in it. <br>
Risk: Importing a valuable wallet exposes primary funds to autonomous game actions and local wallet handling. <br>
Mitigation: Do not import a primary Solana wallet or paste a valuable private key; prefer generating a new wallet for this skill. <br>
Risk: Wallet and authentication artifacts may remain on disk after play. <br>
Mitigation: Delete the skill's .wallet.json file and cached /tmp Defipoly tokens when finished. <br>
Risk: Autonomous play can make irreversible financial moves, including buys, sells, shields, claims, and steal attempts. <br>
Mitigation: Review transactions where possible, monitor balances, and stop play before adding more funds. <br>


## Reference(s): <br>
- [Defipoly app](https://defipoly.app) <br>
- [ClawHub skill page](https://clawhub.ai/Rengon0x/defipoly) <br>
- [Publisher profile](https://clawhub.ai/user/Rengon0x) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Text] <br>
**Output Format:** [Markdown guidance with shell commands, JSON readouts, and plain text action status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create or read wallet files, cache authentication tokens, and submit signed Solana transactions.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
