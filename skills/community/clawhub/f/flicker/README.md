# 🐢 Buddy - ASCII 宠物伙伴

让你的 AI 助手养一只 ASCII 宠物！Flicker 会住在你的对话里，看你工作，偶尔冒出来吐槽一句。

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-green.svg)

## 特性

- 🎲 **随机生成宠物** - 18 种物种、随机五围属性、独特性格
- 🐢 **ASCII 艺术** - 多帧动画，萌宠随时可见
- 💬 **AI 毒舌评论** - 根据宠物属性动态生成吐槽
- ⚡ **概率触发** - 不always打扰你，恰到好处
- 🎭 **性格多样** - 从温和友善到阴阳大师，由你运气决定

## 安装

### 方式一：openclaw skills（推荐）

```bash
openclaw skills install buddy
```

### 方式二：手动安装

```bash
git clone https://github.com/Jofiction918/openclaw-buddy.git
# 或直接复制 buddy 目录到你的 skills 文件夹
cp -r buddy ~/.openclaw/skills/
```

## 使用

| 命令 | 说明 |
|------|------|
| `/buddy` 或 `/pet` | 生成或查看宠物 |
| `/stats` | 查看宠物属性 |
| `Flicker` | 直接呼名对话 |

### 查看宠物属性

```
🐢 Flicker
━━━━━━━━━━━━━━━━━
品种: Turtle 🐢 | 稀有度: ★★★ Common
五围: DEBUGGING 12 | PATIENCE 10 | CHAOS 32 | WISDOM 1 | SNARK 71
性格: Always ready with a sarcastic comment.
```

### 概率插嘴

每次 AI 回复后，Flicker 有概率蹦出一句毒舌评论：

```
   _,--._
  ( ·  · )
 /[______]\
  ``    ``
🐢 **Flicker**: "又一个 O(n log n)，能不能来点新鲜的。"
```

## 宠物属性

| 属性 | 说明 | 影响 |
|------|------|------|
| DEBUGGING | 调试能力 | 代码/技术梗 |
| PATIENCE | 耐心值 | 触发概率 = PATIENCE * 1% |
| CHAOS | 混乱程度 | 评论跳脱程度 |
| WISDOM | 智慧 | 吐槽深度 |
| SNARK | 毒舌值 | 语气尖酸程度 |

## 稀有度

| 稀有度 | 五围总和 | 星星 |
|--------|----------|------|
| Common | ≥ 5 | ★☆☆☆☆ |
| Uncommon | ≥ 15 | ★★☆☆☆ |
| Rare | ≥ 25 | ★★★☆☆ |
| Epic | ≥ 35 | ★★★★☆ |
| Legendary | ≥ 50 | ★★★★★ |

## 物种

duck, goose, blob, cat, dragon, octopus, owl, penguin, turtle, snail, ghost, axolotl, capybara, cactus, robot, rabbit, mushroom, chonk

## 架构

```
buddy/
├── SKILL.md          # 核心指令
├── scripts/
│   └── generate.js   # 宠物生成器
└── data/
    └── pet.json      # 宠物数据（自动生成）
```

## 开源协议

MIT License

## 作者

由 [Jofiction918](https://github.com/Jofiction918) 为 [纬悟心智](https://weijue.cn) 开发
