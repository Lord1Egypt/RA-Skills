## Description: <br>
A Chinese-language interactive horror mystery text adventure where an agent narrates a snowbound hotel murder story, tracks clues and character state, and branches toward multiple endings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ouwenjie03](https://clawhub.ai/user/ouwenjie03) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and game-oriented agent workflows use this skill to run an immersive Chinese horror script-kill adventure with progressive narration, free-form player input, clue investigation, character interaction, and multiple endings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or update a local game_state.json file containing gameplay choices, progress, player names, or notes. <br>
Mitigation: Avoid entering real personal information during play, and review or delete game_state.json if local gameplay history should not be retained. <br>
Risk: The story contains horror, violence, murder mystery, and psychological thriller content. <br>
Mitigation: Use with an appropriate audience and follow the skill's own 18+ content warning. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ouwenjie03/banshee-s-last-cry) <br>
- [Start chapter](references/ch00_start.md) <br>
- [Game state system](references/system_game_state.md) <br>
- [Clue system](references/system_clue_system.md) <br>
- [Character information system](references/system_character_info.md) <br>
- [Endings chapter](references/ch4_endings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Chinese-language narrative text and Markdown status or clue summaries, with local JSON game-state updates when play progresses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Progressive 200-400 character narration segments; may create or update game_state.json for local save state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
