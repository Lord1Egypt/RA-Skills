## Description:

A Chinese-language interactive horror mystery text adventure set in a snowed-in mountain hotel, with branching investigation, role play, clue tracking, and multiple endings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ouwenjie03](https://clawhub.ai/user/ouwenjie03)

### License/Terms of Use:


## Use Case:

External users use this skill to play a Chinese-language horror script-kill style interactive fiction game. The agent narrates scenes, manages clues and character information, and adapts story progression to open-ended player actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The game contains horror, violence, and psychological thriller content that may be unsuitable for some users.

Mitigation: Present the content warning before play and limit use to users who intentionally choose this genre.

Risk: The skill may keep fictional local progress in game_state.json.

Mitigation: Use the state file only for the active game session and remove it when persistent local progress is not desired.

Risk: Generic helper phrases from the game references could be invoked outside the intended play context.

Mitigation: Route the skill only for active Banshee's Last Cry game sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ouwenjie03/skills/banshee-s-last-cry)
- [SKILL.md](artifact/SKILL.md)
- [system_game_state.md](artifact/references/system_game_state.md)
- [system_clue_system.md](artifact/references/system_clue_system.md)
- [system_character_info.md](artifact/references/system_character_info.md)
- [ch00_start.md](artifact/references/ch00_start.md)
- [ch4_endings.md](artifact/references/ch4_endings.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Chinese-language interactive Markdown narrative with optional game_state.json state data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Progressive scene output, clue summaries, character status, and branching ending guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
