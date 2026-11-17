## Description:

Play Defipoly, a Monopoly-inspired DeFi game on Solana, by checking game state and using a funded SOL wallet to buy properties, earn DPOLY yield, shield assets, steal, and roll dice for bonuses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rengon0x](https://clawhub.ai/user/rengon0x)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to play Defipoly from a funded Solana wallet, inspect balances and game state, and submit game transactions through the Defipoly service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access a funded Solana wallet and submit irreversible transactions.

Mitigation: Use a new low-value wallet, avoid importing existing private keys, and review proposed actions before allowing transactions.

Risk: The backend transaction build and submit flow requires high trust in the Defipoly service.

Mitigation: Install only if comfortable with the Defipoly service trust model and keep SOL/DPOLY exposure limited.

Risk: The artifact behavior includes searching for wallet files during setup.

Mitigation: Do not allow filesystem wallet discovery; provide an explicit low-value wallet only when needed.

## Reference(s):

- [Defipoly app](https://defipoly.app)
- [ClawHub Defipoly skill page](https://clawhub.ai/rengon0x/skills/defipoly)
- [Publisher profile](https://clawhub.ai/user/rengon0x)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands; CLI commands return JSON or OK/FAIL text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js/npm and a funded Solana wallet; game actions may submit irreversible on-chain transactions.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
