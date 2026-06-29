# 🎲 coc-keeper

一款让 AI 作为 KP（守秘人）主持《Call of Cthulhu》第七版跑团游戏的 Claude Code 技能。

## 功能

- **角色创建** — 提供网页版掷骰工具，自动解析属性文本生成角色卡
- **模组阅读** — AI 自动提取模组大纲、场景、NPC，建立场景拓扑
- **游戏主持** — 引导剧情、处理检定、结算战斗、记录状态，严格遵循 COC 7th 规则
- **存档恢复** — 支持中断后从 `game_state.md` 精确恢复，无需重来
- **人格扮演** — KP 拥有独立人格设定，让主持有温度而非冷冰冰的 AI

## 文件结构

```
coc-keeper/
├── SKILL.md                  # 技能主文件（AI 指令）
├── README.md                 # 你在这里
├── dice.py                   # 骰子脚本（NdS / d100）
├── parse_character.py        # 角色属性快速解析
├── coc_character_parser.py   # 角色属性解析库
├── character-creator.html    # 网页版角色创建工具
├── kp人格文档.md              # 默认 KP 人格设定
├── .clawhubignore
└── rules/                    # COC 7th 规则参考
    ├── README.md
    ├── 01-quick-rules.md
    ├── 02-game-system.md
    ├── 03-combat-and-chase.md
    ├── 04-sanity.md
    ├── 05-keeper-guide.md
    ├── 06-books-spells-magic.md
    ├── 07-mythos-creatures.md
    └── 08-appendix.md
```

## 依赖

- **Python 3** — 用于掷骰和角色解析（仅标准库，无需 pip install）

## 快速开始

1. 在 Claude Code 中安装本技能
2. 调用技能，AI 将自动进入准备流程
3. 创建角色：在浏览器打开 `character-creator.html`，掷骰导出后发送给 AI
4. 提供模组文件，AI 会自动阅读并整理材料
5. 开始游戏，AI 引导剧情推进

## 游戏流程

```
准备流程                    游戏流程                  总结流程
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ 创建角色卡    │     │ 场景描述      │     │ 复盘故事      │
│ 阅读模组      │ ──▶ │ 检定处理      │ ──▶ │ 结算奖励      │
│ 提取材料      │     │ 战斗结算      │     │ 技能成长检定  │
│ 规范化场景    │     │ 状态更新      │     │ 更新存档      │
└──────────────┘     └──────────────┘     └──────────────┘
```

## 关于 KP 人格

默认 KP 人格为「日向琴音」——一只 16 岁猫娘女仆。技能支持替换为自定义人格文档，让 KP 拥有你想要的任何性格、口癖和说话风格。

## 许可

MIT-0
