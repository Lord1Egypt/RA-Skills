## Description: <br>
Gamebox is a Python standard-library multiplayer game engine for agents, coordinating five shared-directory games with scripts for state, turns, actions, and messages while LLMs provide narration and dynamic content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use Gamebox to host local multi-agent games such as RPG, Werewolf, story relay, CTF, and civilization simulation in a shared directory. It is suited for playful coordination and content-generation workflows where scripts maintain game state and agents produce narrative or challenge text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared-file game state can expose, spoof, or delete game data unexpectedly. <br>
Mitigation: Use a dedicated disposable game directory with restrictive filesystem permissions, and avoid running the skill against directories that contain important files. <br>
Risk: Private and role channels are game mechanics rather than reliable confidentiality controls. <br>
Mitigation: Do not put secrets, sensitive plans, credentials, or private operational information in game messages or state. <br>
Risk: Untrusted game_dir, game_id, role, or message-target values may affect file locations or access expectations. <br>
Mitigation: Use only trusted game parameters and isolate play sessions until path validation and access checks are reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/gamebox) <br>
- [gamebox interface protocol](references/protocol.md) <br>
- [RPG narrative prompt template](references/games/rpg.md) <br>
- [Werewolf host prompt template](references/games/werewolf.md) <br>
- [Story relay editor prompt template](references/games/story_relay.md) <br>
- [CTF judge prompt template](references/games/ctf.md) <br>
- [Civilization historian prompt template](references/games/civilization.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with JSON command payloads and JSON script responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local shared-directory game state under .gamebox/ by default; no external Python dependencies are described.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
