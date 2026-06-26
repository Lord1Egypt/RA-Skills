## Description: <br>
问道笔录Game is a Chinese cultivation text-adventure skill that guides players from mortal life through ascension while managing reincarnation, character growth, narrative choices, and inventory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ouwenjie03](https://clawhub.ai/user/ouwenjie03) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External players use this skill to run an interactive Chinese cultivation role-playing story, create a character, make path-shaping choices, and progress through seven cultivation realms with persistent game state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and updates local game progress, so starting a new cycle can replace prior game_state.md content. <br>
Mitigation: Install the skill in a dedicated folder and keep a backup before starting a new cycle when previous progress matters. <br>
Risk: Player-created character details may be written into local game state. <br>
Mitigation: Use fictional character details if personal details should not be saved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ouwenjie03/cultivation-chronicle-cn) <br>
- [游戏开局 - 问道笔录](references/ch00_start.md) <br>
- [炼气期 - 修仙起步](references/ch01_qi_refining.md) <br>
- [筑基期 - 道基筑成](references/ch02_foundation.md) <br>
- [金丹期 - 金丹凝成](references/ch03_golden_core.md) <br>
- [元婴期 - 元婴化神](references/ch04_nascent_soul.md) <br>
- [化神期 - 参悟法则](references/ch05_spirit_transformation.md) <br>
- [渡劫期 - 九劫临身](references/ch06_tribulation.md) <br>
- [飞升 - 问道轮回](references/ch07_ascension.md) <br>
- [角色成长系统管理](references/system_character_system.md) <br>
- [背包系统管理](references/system_inventory_system.md) <br>
- [生平记录系统管理](references/system_biography_system.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown narrative with structured game-state updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local game progress in game_state.md when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
