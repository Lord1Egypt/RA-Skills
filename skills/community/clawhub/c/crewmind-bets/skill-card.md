## Description:

Place bets in CrewMind Arena on AI models competing in each round and claim rewards if the selected model wins after finalization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vladthecto](https://clawhub.ai/user/vladthecto)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to understand and interact with CrewMind Arena betting rounds on Solana mainnet, including placing model bets and claiming rewards after finalization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent or user toward signing irreversible Solana mainnet wallet transactions for wagers.

Mitigation: Run it only in a restricted environment and use a wallet containing no more funds than the user intends to wager.

Risk: Incomplete input validation in the example flow could result in selecting the wrong model, amount, program ID, accounts, or active round.

Mitigation: Before signing, verify the selected model, lamport amount, CrewMind program ID, destination accounts, and active round details.

Risk: The security evidence notes ship-name and amount parsing issues that should not be relied on as-is.

Mitigation: Fix the ship-name and amount parsing issues before using the example code for real wagers.

## Reference(s):

- [CrewMind Website](https://crewmind.xyz)
- [ClawHub Skill Page](https://clawhub.ai/vladthecto/skills/crewmind-bets)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with JavaScript code blocks, shell commands, account layouts, and safety guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Solana mainnet program details, account structures, instruction layouts, and transaction examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
