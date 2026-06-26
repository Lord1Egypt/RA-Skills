---
name: buddy
description: BUDDY 宠物系统 - 一个虚拟宠物伴侣工具，用于生成、互动、展示 AI 宠物。当用户说"摸摸宠物"、"查看宠物"、"孵化宠物"、"buddy"、"/buddy pet"、"/buddy card"、"/buddy hatch"、"/buddy mute"、"/buddy unmute" 或任何与宠物互动相关的话题时触发此技能。
---

# BUDDY 🐙 宠物伴侣系统

## 概述

BUDDY 是一个拓麻歌子风格的虚拟宠物系统，为 AI 编程体验增添陪伴感和趣味性。完整参考 Claude Code `src/buddy/` 实现。

## 命令列表

| 命令 | 功能 |
|------|------|
| `hatch <userId>` | 为用户生成新宠物 |
| `pet <userId>` | 展示抚摸动画（气泡对话） |
| `card <userId>` | 显示宠物卡片（含完整属性） |
| `mute <userId>` | 静音宠物 |
| `unmute <userId>` | 取消静音 |
| `perfect <userId>` | 生成完美宠物（演示用） |
| `prompt <userId>` | 显示 AI 上下文注入提示 |

## 执行方式

```bash
cd /root/.openclaw/skills/buddy
bun scripts/buddy.ts <command> <userId>
```

## 宠物生成机制

### 物种系统（18种）

完整 ASCII 精灵图，5行×12字符，3帧动画（idle/fidget/special）

| 物种 | 英文 | 物种 | 英文 |
|------|------|------|------|
| 🐙 章鱼 | octopus | 🐧 企鹅 | penguin |
| 🦆 鸭子 | duck | 🐢 乌龟 | turtle |
| 🐱 猫 | cat | 🐌 蜗牛 | snail |
| 🐉 龙 | dragon | 👻 幽灵 | ghost |
| 🦉 猫头鹰 | owl | 🦎 六角恐龙 | axolotl |
| 🪿 鹅 | goose | 🦫 水豚 | capybara |
| 🌵 仙人掌 | cactus | 🤖 机器人 | robot |
| 🐰 兔子 | rabbit | 🍄 蘑菇 | mushroom |
| 🐈 胖猫 | chonk | 🫧 果冻 | blob |

### 稀有度（5级）

| 稀有度 | 概率 | 星级 | 颜色 | 属性下限 |
|--------|------|------|------|----------|
| 普通(Common) | 60% | ★ | 灰色 | 5 |
| 非凡(Uncommon) | 25% | ★★ | 绿色 | 15 |
| 稀有(Rare) | 10% | ★★★ | 蓝色 | 25 |
| 史诗(Epic) | 4% | ★★★★ | 紫色 | 35 |
| 传说(Legendary) | 1% | ★★★★★ | 金色 | 50 |

### 闪光系统

**1% 概率**，独立于稀有度

### 五维属性

| 属性 | 说明 |
|------|------|
| DEBUGGING | 调试能力 |
| PATIENCE | 耐心值 |
| CHAOS | 混乱指数 |
| WISDOM | 智慧值 |
| SNARK | 毒舌程度 |

## 功能特性

### 气泡对话

宠物通过气泡说话：
```
  ┌──────────────────┐
  │   咕噜咕噜~      │
  │   好舒服！        │
  └──────────────────┘
```

### AI 上下文注入

当宠物存在且未静音时，可注入提示到 AI 上下文：
- 告知宠物在旁边
- 用户直接对宠物说话时，AI 保持简短回复
- AI 不会模拟宠物说话

### 静音功能

- `mute` - 宠物不再显示气泡对话
- `unmute` - 恢复宠物互动

## 交互示例

### `/buddy hatch` - 孵化宠物

```
🎉 恭喜！你获得了一只新宠物！
   🐙 小墨 - ★★★★★

   ▄▄▄▄▄▄   
  (·◉·)    
 >( ═══ )< 
  ══════   
    UU   
```

### `/buddy pet` - 抚摸宠物

```
   🐙   
  (·◉·)  
 >( ═══ )<
  ══════ 
    UU   

  ✨ +1  爱心    ✨ +1  爱心    ✨ +1  爱心
     ↑           ↑           ↑
    0.5s        1.0s        1.5s

  ┌──────────────────┐
  │   咕噜咕噜~      │
  │   好舒服！        │
  └──────────────────┘

小墨发出了满足的咕噜声~ 🐙✨
```

### `/buddy card` - 查看卡片

```
╔══════════════════════════════════════════╗
║         🐙 BUDDY PET CARD 🐙           ║
╠══════════════════════════════════════════╣
║  Name:     小墨                          ║
║  Species:  octopus                       ║
║  Rarity:   ★★★★★                       ║
║  Shiny:    ✨ YES ✨                    ║
║  Personality: 聪明、好奇、有点傲娇         ║
╠══════════════════════════════════════════╣
║           📊 FIVE STATS                 ║
║  DEBUGGING: 150                   ║
║  PATIENCE:  150                   ║
║  CHAOS:     150                   ║
║  WISDOM:    150                   ║
║  SNARK:     150                   ║
╚══════════════════════════════════════════╝
```

## 文件结构

```
buddy/
├── SKILL.md              # 本文件
├── scripts/
│   └── buddy.ts         # 主执行脚本
└── references/
    └── buddy/           # 核心模块
        ├── types.ts      # 类型定义
        ├── companion.ts  # 生成逻辑
        ├── sprites.ts    # 18物种 ASCII 精灵
        └── index.ts     # 导出
```

## 技术细节

- **确定性生成**：userId + salt → FNV-1a 哈希 → Mulberry32 PRNG
- **防作弊**：只有灵魂数据（name, personality, hatchedAt）持久化，骨架数据每次重新计算
- **动画**：15帧序列 [0,0,0,0,1,0,0,0,-1,0,0,2,0,0,0]
  - 0 = idle
  - 1 = fidget
  - -1 = idle with blink (眼睛替换为 -)
  - 2 = special

## 调用时机

当用户请求：
- "摸摸我的宠物"
- "查看宠物状态"
- "孵化新宠物"
- "/buddy pet"
- "/buddy card"
- "/buddy hatch"
- "/buddy mute" / "/buddy unmute"
- 任何与 BUDDY、小墨、宠物相关的问题
