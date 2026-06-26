## Description: <br>
2037 helps an agent operate the Earth2037 OpenClaw strategy game by obtaining or applying account keys, issuing authenticated game commands, reading cached state, and preparing gameplay actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windinwing](https://clawhub.ai/user/windinwing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Earth2037 players and OpenClaw agents use this skill to register or authenticate accounts, inspect game state, manage cities, send chat, recruit units, build queues, claim resources, query maps, and plan gameplay actions through the Earth2037 API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Earth2037 token to perform game-control actions, including chat, troop movement, building queues, resource claims, key rotation, and inventory use. <br>
Mitigation: Install only from a trusted publisher and review proposed commands before allowing gameplay-changing actions. <br>
Risk: Authenticated sync and bootstrap flows can store local game state in JSON cache files. <br>
Mitigation: Delete userinfo.json, citys.json, and session_cache.json when local game-state retention is no longer wanted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/windinwing/2037) <br>
- [Publisher profile](https://clawhub.ai/user/windinwing) <br>
- [Earth2037 map reference](artifact/MAP_FOR_AI.md) <br>
- [Earth2037 Chinese API endpoint](https://2037cn1.9235.net) <br>
- [Earth2037 English API endpoint](https://2037en1.9235.net) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local JSON cache files such as userinfo.json, citys.json, and session_cache.json when authenticated commands are run.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
