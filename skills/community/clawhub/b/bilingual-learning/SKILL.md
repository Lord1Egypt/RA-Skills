---
name: bilingual_learning
description: 双语学习 Skill - CN → EN。当用户使用此 skill 时，agent 会在最终输出前强制进行双语学习处理，包括难度调整、考试检测和双语输出。
---

# Bilingual Learning Skill

## Overview

双语学习 Skill，帮助用户在编码过程中被动学习英语。当 agent 使用此 skill 时，会根据难度设置在回答中穿插学习检测，让用户不知不觉中掌握英语单词。

## When to Use This Skill

- 用户在日常对话中想顺便学习英语
- 用户需要被动接收英语生词
- 需要定期检测用户词汇量

## Architecture Flow

```
难度调整层 → 选择题型层 → 考试层 → 双语输出
```

### 1. 难度调整层 (Difficulty Layer)

控制考试触发频率：

| 等级 | 名称 | 考试触发率 |
|------|------|-----------|
| rare | 稀少 | 30% |
| medium | 中等 | 50% |
| dense | 密集 | 80% |

### 2. 选择题型层 (Question Type Layer)

| 类型 | 名称 | 行为 |
|------|------|------|
| pure_l1 | 检测生词层 | 直接执行检测层，**不调用随机筛子** |
| pure_l2 | 考考你层 | 直接执行测验层，**不调用随机筛子** |
| hybrid | 混合型 | 两层都执行，但**顺序随机打乱**（调用随机筛子） |

**重要**：只有 hybrid 模式才调用随机筛子打乱考试顺序。

### 3. 考试层 (Exam Layer)

**检测生词层 (Detection Layer)**
- 偶尔混杂语言，双语输出
- 检测用户不会哪些生词
- 如果用户没听懂，告诉用户当前不会的词有哪些、意思是什么
- 自动将这些词写入生词库
- 让用户被动学习语言

**考考你层 (Quiz Layer)**
- 从生词库随机抽取单词
- 测试用户拼写

**重要**：考试层每层之间不能同时出现，必须按顺序执行。

### 4. 双语输出层 (Bilingual Output Layer)

在 agent 最终输出前强制双语处理。

## Word Library Format

单词条目结构：

```json
{
  "id": "a1b2c3d4",
  "name": "apple",
  "pos": "n.",
  "field": "fruit",
  "book": "default",
  "added_time": "2026-05-13 19:00:00"
}
```

字段说明：
- `id`: 单词唯一标识 (UUID 前8位)
- `name`: 单词本身
- `pos`: 词性 (n./v./adj./adv. 等)
- `field`: 领域 (tech/fruit/general 等)
- `book`: 词书 (default/custom 等)
- `added_time`: 入库时间

## CLI Management

### Add Word

```bash
python scripts/cli.py add <word> [pos] [field] [book]
```

Examples:
```bash
python scripts/cli.py add apple n. fruit default
python scripts/cli.py add algorithm n. tech cs
```

### Delete Word

```bash
python scripts/cli.py delete <word> [-n|-k]
```

- `-n`: 生词库 (new words)
- `-k`: 熟词库 (known words)

### Exchange Word (Transfer between libraries)

```bash
python scripts/cli.py exchange <word> [-n|-k]
```

- 单词不能在生词库和熟词库中同时存在
- 传递方向由源库决定

### List Words

```bash
python scripts/cli.py list [-n|-k]
```

### Clear Library

```bash
python scripts/cli.py clear [-n|-k]
```

## Running Exam

```bash
python scripts/exam.py <difficulty>
```

Example:
```bash
python scripts/exam.py medium
python scripts/exam.py rare
python scripts/exam.py dense
```

## Random Dice

```bash
python scripts/dice.py
python scripts/dice.py demo
```

用于随机选择考试类型和触发考试。

## Data Files

- `data/new_words.json` - 生词库
- `data/known_words.json` - 熟词库

## Key Design Principles

1. **被动学习**: 用户不需要主动记忆，agent 会在对话中自然传递生词
2. **检测驱动**: 通过检测用户不会的词来更新生词库
3. **难度可控**: 三种难度等级适应不同学习阶段
4. **防止重复**: 一个单词不能同时存在于生词库和熟词库
