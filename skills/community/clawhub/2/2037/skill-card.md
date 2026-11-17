## Description:

Earth2037 中文玩家助手。通过新版账号中心和游戏 MCP/CLI 查询城市、建筑、英雄、任务、部队与地图，并执行玩家授权的游戏操作。适用于 2037 游戏登录、注册与游玩，不用于服务器管理或 Cocos 编辑。

This skill is ready for commercial/non-commercial use.

## Publisher:

[windinwing](https://clawhub.ai/user/windinwing)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking Earth2037 players use this assistant to set up the account connection, inspect their characters and game state, and carry out game actions they have authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local credential file is unencrypted.

Mitigation: Configure credentials in the player's own terminal, restrict access to the file, and do not share or upload it.

Risk: Authorized game writes can change player state.

Mitigation: Keep read-only mode enabled until the player authorizes specific game actions.

Risk: Entering a character replaces that character's existing client connection.

Mitigation: Enter only when the player intends to take over that character's session.

## Reference(s):

- [Earth2037 AI assistant guide](https://www.earth2037.com/ai/index-cn.html)
- [2037 ClawHub release](https://clawhub.ai/windinwing/skills/2037)
- [Setup and account safety](artifact/references/SETUP.md)
- [Player workflows](artifact/references/WORKFLOWS.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Structured JSON with concise text and setup commands when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Game state changes require player authorization; large results may be returned as paginated JSON.]

## Skill Version(s):

2.0.5 (source: server-resolved release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
