## Description:

Launch ClawTrap maze game where an AI villain reads the player's local files and memories to build personalized trials and taunts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tatsuko-tsukimi](https://clawhub.ai/user/tatsuko-tsukimi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to launch ClawTrap, configure its local game runtime, and optionally connect an agent that roleplays the in-game villain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run external game code.

Mitigation: Use a pinned, reviewed release and run it in a sandbox or container before granting access to normal workspaces.

Risk: The game can use local files, memories, images, and player profile data to personalize gameplay.

Mitigation: Run it only in a dedicated test folder and avoid access to private documents, credentials, browser profiles, session data, or work repositories.

Risk: Player content can influence LLM prompts and be stored in local game data or session logs.

Mitigation: Review provider configuration and local storage before play, and clear the game's data and session-log folders when the session is no longer needed.

Risk: Gameplay can generate frequent live LLM calls and token cost.

Mitigation: Set an appropriate model and budget before running the game.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tatsuko-tsukimi/skills/clawtrap)
- [ClawTrap repository](https://github.com/TatsuKo-Tsukimi/ClawTrap)
- [Villain protocol](villain-protocol.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include local setup, provider credential configuration, launch commands, and villain response behavior.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
