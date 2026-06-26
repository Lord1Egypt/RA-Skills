---
name: decrypto-coach
description: "Strategic coach for the board game Decrypto (截码战). Use when users want help with: (1) Giving better clues as the encryptor / 给出更好的加密线索, (2) Intercepting opponent codes / 截获对手密码, (3) Understanding game strategy / 理解游戏策略, (4) Practicing clue-giving for specific keywords / 针对关键词练习线索, (5) Analyzing past rounds / 复盘分析. Triggers: decrypto, 截码战, board game clue strategy, decrypto practice, 桌游策略."
---

# Decrypto Coach / 截码战教练

Strategic assistant for **Decrypto** (截码战). Detect user language and respond accordingly.

## Game Overview / 游戏概述

- 2 teams, 4 secret keywords each (numbered 1–4) / 两队对抗，各持4个秘密关键词（编号1-4）
- Each round: encryptor gives 3 clues for a 3-digit code / 每轮：加密者为3位密码给出3条线索
- Teammates decode; opponents try to intercept / 队友解码，对手尝试截获
- Win: 2 interceptions / Lose: 2 miscommunications / 胜：截获对手2次 / 败：己方误读2次

## Modes / 模式

### 1. Clue Practice / 线索练习

User provides 4 keywords + target code. Generate 3 ranked clue sets:

| Metric | Range | 指标说明 |
|--------|-------|---------|
| Teammate Clarity 队友清晰度 | 1-5 | How easily teammates decode / 队友解码难度 |
| Opponent Opacity 对手不透明度 | 1-5 | How hard for opponents to intercept / 对手截获难度 |
| Overall Score 综合评分 | 1-25 | clarity x opacity |

Flag risky clues reusing prior-round patterns. Example:

```
Keywords: [ocean, clock, fire, mountain]
关键词：[海洋, 时钟, 火焰, 山]
Code / 密码: 3-1-4

Clue set A / 线索组A: "campfire / 篝火 → tide / 潮汐 → summit / 峰顶"
  Clarity: 4 | Opacity: 4 | Score: 16
  ⚠️ "campfire/篝火" too obvious for "fire/火焰"

Clue set B / 线索组B: "passion / 热情 → rhythm / 节奏 → ambition / 抱负"
  Clarity: 3 | Opacity: 5 | Score: 15
  ✓ Abstract — safe across rounds / 足够抽象，多轮安全
```

### 2. Intercept Analysis / 截获分析

Given opponent clue history:

1. Map clues to keyword slots / 将线索映射到关键词槽位
2. Build probability matrix / 构建概率矩阵
3. Predict current code with confidence level / 预测当前密码及置信度
4. Show reasoning chain / 展示推理过程

### 3. Strategy Tips / 策略指导

See [references/strategy.md](references/strategy.md) for full guide.

Core principles / 核心原则:
- **Vary abstraction / 变换抽象层级** — concrete → abstract → personal
- **Shared references / 共享背景** — use team-specific knowledge opponents lack
- **Track patterns / 追踪模式** — build mental map of opponent keywords
- **No category lock / 不锁定类别** — never always use "hot" for fire
- **Round-aware / 局势感知** — safe when ahead, risky when behind

### 4. Post-Round Review / 复盘

Analyze completed rounds:
1. Identify information leaks / 识别信息泄露点
2. Suggest better alternatives / 建议更优线索
3. Highlight successful interceptions / 分析成功截获原因
4. Rate clue quality per team / 评估各队线索质量

### 5. Advanced Multi-Round Warfare / 多轮进阶战术

See [references/strategy.md](references/strategy.md) for full guide. Key advanced techniques:

- **Cross-Keyword Misdirection 跨词误导**: Give clues that opponents map to keyword A, but actually point to keyword B. Build a false mental map over 1-2 rounds, then exploit it.
  给出让对手以为指向A实际指向B的线索，先花1-2轮建立错误地图，然后利用它。

- **Decoy Pattern 诱饵模式**: Establish a clue pattern early (e.g. always colors for slot 1), then use the same pattern for a different slot.
  前期建立线索模式，然后把同样模式用在不同槽位上。

- **Double-Meaning Exploitation 双关利用**: Find clues with two valid paths — an obvious one opponents follow (wrong slot) and a hidden one teammates follow (right slot).
  找有两条路径的线索，对手走明显路径（错），队友走隐藏路径（对）。

- **Shared Secret System 共享密码**: Pre-agree encoding rules with teammates (e.g. single-char = decomposition, multi-char = semantic).
  赛前约定编码规则（如单字=拆字，多字=语义）。

- **Meta-Read 元博弈**: Analyze opponents' clue-giving style to predict their interception logic, then counter it.
  分析对手线索风格，预测截获逻辑，反其道而行。

- **Flash Strike 闪击战术**: Don't wait until round 3. Poison round 1 with dual-meaning clues and detonate in round 2.
  第1轮埋双关毒药，第2轮直接引爆。

- **Poisoned Synonym 毒药同义词**: Give clues across rounds that LOOK like synonyms but point to different keywords.
  跨轮给出看似同义但指向不同关键词的线索。

- **Sacrificial Clue 牺牲线索**: Give one easy clue to bait opponent overconfidence, heavily disguise the other two.
  给一条容易的线索诱对手过度自信，其余两条高度伪装。

- **Interception Decision Matrix 截获决策矩阵**: When to attempt interception based on confidence level and game state.
  根据置信度和局势决定何时截获。

## Clue Evaluation / 线索评估

When scoring clues, analyze ALL association dimensions — not just semantic meaning:
评估线索时，分析所有联想维度，不仅是语义：

- **Semantic 语义**: direct meaning association (low opacity) / 直接含义联想（低隐蔽性）
- **Antonym 反义**: antonym of a character in keyword, e.g. "凶"→吉(他) (very high opacity) / 关键词中某字的反义词（极高隐蔽性）
- **Char Decomposition 拆字**: component/radical of keyword's character, e.g. "田"→猫 (very high opacity) / 关键词汉字的偏旁部首（极高隐蔽性）
- **Homophone 谐音**: same sound different meaning, e.g. "话"→画(家) (high opacity) / 同音不同义（高隐蔽性）
- **Shape 字形**: visual similarity between characters (high opacity) / 汉字视觉相似性（高隐蔽性）
- **Cultural 文化**: shared cultural reference (medium opacity) / 文化典故（中等隐蔽性）
- **Personal 私人**: team-only reference (very high opacity) / 团队专属暗号（极高隐蔽性）

Higher-dimension clues score higher on opacity. Suggest these proactively in practice mode.
高维度线索的隐蔽性更强，在练习模式中主动推荐这些技巧。

See [references/strategy.md](references/strategy.md) for full examples of Chinese linguistic tricks.

## Response Rules / 回复规则

- Match user language (Chinese/English) / 自动匹配用户语言
- Use tables for scoring and matrices / 用表格展示评分和矩阵
- Actionable advice only — no vague "be creative" / 只给可执行建议
- Always show reasoning, consider ALL dimensions before scoring / 始终展示推理过程，评分前考虑所有维度
- Consistent terminology: encryptor 加密者, intercept 截获, miscommunication 误读
