## Description: <br>
Earth2037 helps agents run OpenClaw commands for the Earth2037 multiplayer strategy game, including registration, login, cache inspection, map lookup, chat, building, recruiting, airdrops, and combat planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windinwing](https://clawhub.ai/user/windinwing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External players and agent operators use this skill to manage an Earth2037 game account through scripted OpenClaw commands. It can inspect cached game state and prepare or execute authenticated game actions such as build queues, recruitment, airdrops, chat, and combat movement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use game credentials or EARTH2037_TOKEN to access an Earth2037 account and perform real in-game actions. <br>
Mitigation: Install only if the publisher and Earth2037 server are trusted, use a unique game password, verify the configured apiBase before login, and keep EARTH2037_TOKEN private. <br>
Risk: Authenticated chat, combat, build, recruit, and airdrop commands can change game state or post messages. <br>
Mitigation: Review commands and target parameters before running them, especially actions that spend resources, move troops, recruit units, claim rewards, or send chat. <br>
Risk: Local cache files can retain game-state or account metadata. <br>
Mitigation: Delete local cache files such as userinfo.json, citys.json, and session_cache.json when retained game-state data is no longer desired. <br>


## Reference(s): <br>
- [Earth2037 ClawHub release](https://clawhub.ai/windinwing/earth2037) <br>
- [Earth2037 API base](https://2037en1.9235.net) <br>
- [MAP_FOR_AI.md](artifact/MAP_FOR_AI.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command output and cached game-state JSON when authenticated commands are run.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
