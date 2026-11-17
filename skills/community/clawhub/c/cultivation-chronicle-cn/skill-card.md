## Description:

问道笔录 - 修仙文字冒险游戏。玩家从凡人开始修炼，经历炼气、筑基、金丹、元婴、化神、渡劫、飞升七大境界，通过选择塑造道心，最终成就修仙之路。支持转世传承、角色成长、物品系统。适用于修仙题材、角色扮演、文字冒险等场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ouwenjie03](https://clawhub.ai/user/ouwenjie03)

### License/Terms of Use:


## Use Case:

External players use this Chinese-language skill to run a persistent cultivation-themed text adventure in an agent chat, creating a character, making story choices, and tracking realms, inventory, biography, reincarnation, and endings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gameplay may modify or reset local save-state content, including inventory, companion inventory, and new-cycle state.

Mitigation: Keep backups of game_state.md before important runs if preserving progress matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ouwenjie03/skills/cultivation-chronicle-cn)
- [Game Start and Initialization](references/ch00_start.md)
- [Qi Refining Realm Journey](references/ch01_qi_refining.md)
- [Foundation Establishment Realm](references/ch02_foundation.md)
- [Golden Core Realm](references/ch03_golden_core.md)
- [Nascent Soul Realm](references/ch04_nascent_soul.md)
- [Spirit Transformation Realm](references/ch05_spirit_transformation.md)
- [Tribulation Realm](references/ch06_tribulation.md)
- [Ascension and Reincarnation](references/ch07_ascension.md)
- [Managing Character System](references/system_character_system.md)
- [Managing Inventory System](references/system_inventory_system.md)
- [Managing Biography System](references/system_biography_system.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Chinese-language Markdown narrative with local game-state file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local game_state.md save file for persistent character, inventory, biography, and new-cycle state.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
