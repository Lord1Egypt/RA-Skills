## Description:

Play Blinko (on-chain Plinko) headlessly on Abstract chain, including game play, stats, leaderboards, honey rewards, API authentication, on-chain game creation, simulation, and settlement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tolibear](https://clawhub.ai/user/tolibear)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to play Blinko on-chain Plinko games with a wallet-backed hot wallet and to inspect profile, game, leaderboard, and honey reward data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent wallet-backed authority to spend ETH and gas on an on-chain gambling game without per-transaction approval or cumulative limits.

Mitigation: Install only with a dedicated hot wallet funded with the maximum amount the user is willing to lose, and require explicit approval for each gameplay transaction where possible.

Risk: Gameplay invocations may repeatedly spend funds through autonomous agent use.

Mitigation: Set daily or session limits outside the skill, keep read-only stats workflows separate from gameplay, and avoid using a main wallet private key.

Risk: Transaction parameters returned by the external API influence on-chain game creation and settlement.

Mitigation: Review transaction details before signing and prefer versions that validate API-returned transaction parameters before submission.

## Reference(s):

- [ClawHub Blinko skill page](https://clawhub.ai/tolibear/skills/blinko)
- [Blinko game site](https://blinko.gg)
- [Abstract RPC endpoint](https://api.abs.xyz)
- [Blinko API endpoint](https://api.blinko.gg)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Gameplay requires WALLET_PRIVATE_KEY and can submit real ETH transactions; stats commands can run with a wallet address.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
