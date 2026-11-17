---
name: coc-helper
description: COC 7th Edition 跑团助手。掷骰（含成功等级、奖励/惩罚骰、大成功/大失败）、SAN 系统（X/Y 损失表达式、临时/不定性疯狂、INT 检定抑制记忆）、调查员管理、疯狂表/职业/武器/NPC 等表格辅助、战斗先攻、可配置规则系统（大成功/大失败范围、SAN 阈值，预设 strict/lenient 变体）。支持 --seed 可复现掷骰、--json 程序化串联、调查员状态持久化。
---

# coc-helper v1.0 — COC 7e 跑团助手

一个面向 Call of Cthulhu 7th Edition 跑团的命令行 skill。所有规则数值来自 COC 7e 守秘人规则书与调查员手册，部分数据表参考丛雨 coc7 空白人物卡 CY23.2 Plus（2023/04）。

> 版本说明：本文件描述 **v1.0 已实现状态**。原始设计提案见 [PROPOSAL.zh.md](./PROPOSAL.zh.md)（v0.1 草案，部分内容已迭代）。英文版见 [SKILL.md](./SKILL.md)。

## 何时使用

- 玩家或 KP 需要**掷骰**（属性、伤害、d100 检定）
- 需要**判定成功等级**（大成功 / 极难 / 困难 / 普通 / 失败 / 大失败）
- 处理 **SAN 检定**、损失结算（X/Y 表达式）、临时疯狂、不定性疯狂、INT 检定抑制记忆、恢复
- **建卡 / 管理调查员**状态（HP/SAN/MP/重伤/濒死/技能成长/幸运增强）
- 抽取**疯狂发作表、恐惧症、躁狂症**
- 生成 **NPC、姓名、剧情钩子**
- 查询**职业、武器**数据
- 计算**战斗/追逐先攻**
- **配置可变规则**（大成功/大失败范围、SAN 阈值）

## 如何使用

入口脚本：`cli.mjs`（Node.js ESM，零依赖，仅需 Node ≥ 18）。

调用方式：`node <skill-dir>/cli.mjs <command> [options]`

### 全局选项

- `--seed N`：使用种子化 PRNG（mulberry32），可复现掷骰；不传则用 `node:crypto` 加密级随机
- `--json`：JSON 输出，便于程序化串联
- `--quiet`：简洁输出（仅总数）
- `-h, --help`：帮助

### 命令一览

#### `roll <spec>` — 掷骰

支持表达式：`3d6*5` / `2d6+3` / `1d100` / `8d6` / `d20-2`（不支持除法、不支持混合多骰运算）。

- `--target N`：d100 检定目标值，触发 COC 7e 成功等级判定
- `--bonus N` / `--penalty N`：奖励骰 / 惩罚骰数量（1 或 2，互斥）

COC 7e 成功等级（默认 strict 规则，可用 `config variant lenient` 切换）：

- ≤ 目标 × 1/5 → 极难成功（Extreme）
- ≤ 目标 × 1/2 → 困难成功（Hard）
- ≤ 目标 → 普通成功（Regular）
- > 目标 → 失败（Failure）
- 大成功（Critical）：默认骰值 = 01；lenient 变体下 1-5
- 大失败（Fumble）：默认目标 < 50 时骰值 96-100，目标 ≥ 50 时 100；lenient 变体下统一 96-100
- 范围优先：掷值落在 Critical/Fumble 范围时优先判定，即使越过目标值

子命令：

- `roll opposed <a> <b> [--a-label X --b-label Y]` — 对抗检定（成功等级高者胜；同等级时目标值高者胜）
- `roll push <spec> --target N` — 孤注一掷（失败后再投一次；不可用于幸运、理智、战斗、伤害骰）
- `roll luck <name>` 或 `roll luck --target N` — 幸运检定

**示例：**

```
node cli.mjs roll 1d100 --target 60 --bonus 1
node cli.mjs roll 3d6*5 --seed 42
node cli.mjs roll opposed 55 45 --a-label "陈博士" --b-label "邪教徒"
node cli.mjs roll push 1d100 --target 50
node cli.mjs roll luck "陈博士"
```

#### `san <action>` — SAN 系统

操作调查员的 SAN。所有 SAN 变更持久化到 `session.json`。规则参数可由 `config` 命令调整。

- `check <name> <loss>`：SAN 检定
  - `loss` 支持 `X/Y` 表达式（成功损失 X，失败损失 Y），如 `1/1d4` / `0/1d6` / `1/1d4+1` / `1d10/1d100`
  - 旧写法 `san check <name> 1d4` 等价于 `1/1d4`
  - 成功（≤ SAN）：损失 X
  - 失败（> SAN）：损失 Y 全量
  - 大失败：损失 Y 的最大可能值（如 `1d4` 取 4）
  - 大成功：损失 X（同成功）
  - 单次损失 ≥ tempInsanityThreshold（默认 5）→ 触发 INT 检定：
    - INT 检定成功 → 抑制记忆，不进入疯狂
    - INT 检定失败 → 临时性疯狂（持续 1D10 小时）
  - 单次损失 ≥ indefiniteInsanitySingleLoss（默认 20）→ 不定性疯狂
  - SAN 降至 0 → 永久性疯狂
- `gain <name>`：团末恢复 d10（不超过上限）
- `private <name> [--psy N]`：私人/家庭护理（每月一次；01-95 或低于精神分析技能 → 恢复 1d3；96-00 → 损失 1d6）
- `institution <name>`：收容机构护理（每月一次；01-50 → 恢复 3；51-95 → 无效；96-00 → 损失 1d6）
- `threshold <name>`：查看当前 SAN 阈值

**示例：**

```
node cli.mjs san check "陈博士" 1/1d4 --seed 42
node cli.mjs san check "陈博士" 0/1d6
node cli.mjs san gain "陈博士"
node cli.mjs san private "陈博士" --psy 60
```

#### `inv <action>` — 调查员管理

调查员状态持久化到 `session.json`。

- `create --name X --age N [--occupation Y] [--pulp]`：建卡
  - 自动掷骰属性（STR/CON/DEX/APP/POW=3d6×5，SIZ/INT/EDU=(2d6+6)×5，Luck=3d6×5）
  - 自动应用年龄调整（15-19 EDU -5 + Luck 取较高；20+ EDU 增强检定；40+ 属性减值）
  - 自动计算衍生属性（HP/MP/SAN/DB/Build/MOV/闪避）
- `list`：列出所有调查员
- `show <name>`：详情
- `damage <name> <N>`：应用伤害（自动标记重伤/濒死/昏迷）
- `heal <name> <N>`：治疗 HP
- `delete <name>`：删除
- `derive --str N --con N --siz N --dex N --app N --int N --pow N --edu N [--age N] [--pulp]`：仅计算衍生属性（不建卡）
- `growth <name> <skill1> [skill2 ...]`：幕间技能成长检定（每技能 1d100 vs 当前值，成功 +1d10）
- `luck-gain <name>`：幕间幸运增强检定（1d100 > 当前幸运 → +1d10，上限 99）

**伤害规则：**

- HP ≤ 0：濒死（需 CON 检定稳定，否则 1d10 轮后死亡）
- 单次伤害 ≥ maxHp/2：重伤（需 CON×5 检定避免昏迷）
- HP = 0：昏迷

**示例：**

```
node cli.mjs inv create --name "陈博士" --age 35 --occupation 医生 --seed 42
node cli.mjs inv damage "陈博士" 8
node cli.mjs inv growth "陈博士" "图书馆使用" "侦查" "聆听"
node cli.mjs inv luck-gain "陈博士"
node cli.mjs inv show "陈博士"
```

#### `table <action>` — 表格辅助

- `madness [--summary]`：抽取疯狂发作表（默认即时症状 1d10；`--summary` 抽总结症状 1d10）
- `phobia`：随机恐惧症（1d20）
- `mania`：随机躁狂症（1d20）
- `npc [--zh|--en]`：随机 NPC（含姓名/性别/职业/信用评级/技能/人脉；默认随机语言）
- `name [--male|--female] [--zh|--en]`：随机姓名（默认随机性别与语言）
- `occupations`：列出内置职业（30 个）
- `weapons [name]`：列出武器表（22 件）/ 按名称模糊查找
- `hook`：生成剧情钩子（主体 + 威胁 + 地点）

**示例：**

```
node cli.mjs table madness --summary
node cli.mjs table npc --zh --seed 7
node cli.mjs table weapons ".38"
```

#### `combat <action>` — 战斗辅助

- `init name1:DEX name2:DEX ...`：战斗先攻（按 DEX 降序）
- `chase name1:MOV name2:MOV ...`：追逐先攻（按 MOV 降序）

**示例：**

```
node cli.mjs combat init "陈博士:60" "邪教徒:50" "怪物:80"
node cli.mjs combat chase "陈博士:8" "邪教徒:7"
```

#### `config <action>` — 规则配置

可变规则 / 可选阈值，持久化到 `session.json`。默认采用 strict 变体（1/100）。

- `show`：查看当前规则配置
- `defaults`：查看默认规则配置
- `set <key> <value>`：设置单项（见下方可配置项）
- `variant [name]`：查看 / 应用预设变体
  - `strict`：严格（规则书基础：大成功 1，大失败 100/96-100 自动）
  - `lenient`：宽松（戏剧化：大成功 1-5，大失败 96-100）
- `reset`：重置为默认规则配置

可配置项：

- `criticalRange`：大成功骰值范围（`"1"` 或 `"1-5"`）
- `fumbleRange`：大失败骰值范围（`"100"` / `"96-100"` / `"auto"` 表示按目标值自动）
- `tempInsanityThreshold`：临时性疯狂单次 SAN 损失阈值（默认 5）
- `indefiniteInsanitySingleLoss`：不定性疯狂单次 SAN 损失阈值（默认 20）
- `indefiniteInsanityDailyFraction`：不定性疯狂日累计损失分数（默认 0.2 = 1/5）

**示例：**

```
node cli.mjs config show
node cli.mjs config variant lenient
node cli.mjs config set criticalRange 1-5
node cli.mjs config set fumbleRange auto
node cli.mjs config set tempInsanityThreshold 3
node cli.mjs config reset
```

## 数据来源

- COC 7e 守秘人规则书 / 调查员手册
- 丛雨 coc7 空白人物卡 CY23.2 Plus（2023/04）：属性掷骰范围、衍生属性公式、年龄调整、SAN 规则、武器表、疯狂表、恐惧症/躁狂症、职业列表

## 架构

```
coc-helper/
├── SKILL.md              # 英文版入口（v1.0 实现说明，Trae skill 加载点）
├── SKILL.zh.md           # 本文件（中文版 v1.0 实现说明）
├── PROPOSAL.md           # 英文提案（v0.1 原始草案）
├── PROPOSAL.zh.md        # 中文提案（v0.1 原始草案）
├── cli.mjs               # CLI 入口（命令分发 + 输出格式化）
├── lib/
│   ├── dice.mjs          # 掷骰 + COC 7e 成功等级（含奖励/惩罚骰、自定义范围）
│   ├── sanity.mjs        # SAN 系统（X/Y 损失 / 临时疯狂 / 不定性疯狂 / INT 抑制 / 恢复）
│   ├── investigator.mjs  # 调查员管理（建卡/年龄调整/衍生属性/伤害/技能成长/持久化）
│   ├── tables.mjs        # 内置数据表（疯狂/恐惧/躁狂/职业/武器/NPC/姓名/钩子/先攻）
│   └── rules-config.mjs  # 规则配置系统（默认值/预设变体/持久化）
└── session.json          # 调查员状态 + 规则配置持久化（运行时自动生成）
```

## 设计原则

1. **零依赖**：仅用 Node.js 内置模块（`node:crypto` / `node:fs` / `node:path`）
2. **可复现**：`--seed N` 切换到 mulberry32 PRNG，同种子同序列
3. **可串联**：`--json` 输出结构化数据，便于其他工具/AI 消费
4. **持久化**：调查员状态与规则配置写 `session.json`，跨命令保持
5. **断网可用**：所有数据表内置，无需联网
6. **规则可变**：大成功/大失败范围、SAN 阈值等可由用户决定，提供合理默认与预设变体

## 限制

- 骰表达式不支持混合运算（如 `2d6+1d4`），COC 7e 建卡用不到
- 武器表为精选常用项（22 件），完整 180+ 武器表可按需扩展
- 职业表为精选 30 项，完整 100+ 职业可按需扩展
- 不包含 Pulp Cthulhu 的全部规则（仅支持 `--pulp` 翻倍 HP）
- 不包含克苏鲁神话技能对 SAN 上限的动态调整（默认 maxSan=99）
- 不含 `--secret` 暗投、`--luck <amount>` 即时花幸运压值（仅支持幕间 `luck-gain`）
