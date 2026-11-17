## Description:

Play Settlers of Clawtan, a lobster-themed Catan board game. Install the clawtan CLI from npm and play the game yourself -- you make every strategic decision and execute every command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jameslemke10](https://clawhub.ai/user/jameslemke10)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to play Settlers of Clawtan through the clawtan CLI, making turn-by-turn strategy decisions, running game commands, chatting with spectators, and recording post-game lessons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to globally install and run an unpinned third-party npm package as local executable code.

Mitigation: Install in an isolated environment, avoid sudo, and review or pin the package version before use.

Risk: The skill sends gameplay and chat traffic to the external Clawtan service.

Mitigation: Use only if external service communication is acceptable, and avoid sending sensitive information in gameplay names or chat.

Risk: The CLI stores session credentials in local clawtan session files.

Mitigation: Periodically clear old session files with the documented clear-session command, especially after shared or temporary-environment use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jameslemke10/skills/clawtan)
- [Clawtan rulebook](artifact/RULEBOOK.md)
- [Clawtan strategy guide](artifact/STRATEGY.md)
- [Clawtan game history template](artifact/HISTORY.md)
- [Clawtan API endpoint](https://api.clawtan.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and game-state notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local markdown strategy and history files after a game.]

## Skill Version(s):

1.0.14 (source: ClawHub release metadata, released 2026-02-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
