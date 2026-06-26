---
name: daily-brain
description: |
  每日脑力训练 — 逻辑推理、数学速算、记忆挑战、文字谜题，游戏化精美卡片呈现，
  含难度自适应分级和连续打卡追踪。每天一道精选题目锻炼大脑，保持思维敏锐。
  Daily brain training: logic puzzles, math speed drills, memory challenges, and word games
  with adaptive difficulty, streak tracking, and beautiful visual cards.
  Trigger on：每日脑力、今日脑力、脑力训练、逻辑题、数学题、记忆挑战、
  brain training、daily brain、daily puzzle、brain teaser、logic puzzle、
  math challenge、word game、memory game、今天的题、做道题、脑筋急转弯。
keywords:
  - daily-brain
  - 每日脑力
  - 脑力训练
  - 逻辑推理
  - 数学速算
  - 记忆挑战
  - 文字谜题
  - brain training
  - daily puzzle
  - brain teaser
  - logic puzzle
  - math challenge
  - word game
  - memory game
  - 脑筋急转弯
  - 思维训练
  - 认知训练
  - 打卡
  - streak
  - 难度分级
  - adaptive difficulty
  - gamification
  - 游戏化学习
  - 每日挑战
  - daily challenge
  - cognitive training
  - mental fitness
  - 智力题
  - puzzle of the day
  - 益智游戏
  - 头脑风暴
requirements:
  node: ">=18"
---

# Daily Brain — 每日脑力训练

> 每天一道精选脑力题，逻辑/数学/记忆/文字四类轮换，难度自适应，打卡追踪成就

---

## Purpose & Capability

daily-brain 是一个**每日认知训练技能**，通过游戏化的脑力题目帮助用户保持思维敏锐。

**核心能力：**

| 能力 | 说明 |
|------|------|
| 四类题目轮换 | 逻辑推理、数学速算、记忆挑战、文字谜题，按日期自动轮换 |
| 难度自适应 | Easy/Medium/Hard 三档，根据连续正确率自动调整 |
| 精美视觉卡片 | HTML 格式题目卡片和解析卡片，支持浅色/深色主题 |
| 打卡追踪 | 连续天数、最长纪录、正确率、类别分布统计 |
| 成就系统 | 解锁里程碑徽章（首次答题、连续7天、满分周等） |
| 答案解析 | 每题配详细解题思路和知识扩展 |

**能力边界（不做的事）：**
- 不联网获取题目 — 全部题库内置，无需 API
- 不生成实时竞技或多人对战
- 不提供专业心理学/医学认知评估
- 不修改任何系统设置或 shell 配置

---

## Instruction Scope

**在 scope 内（会处理）：**
- "今天的脑力题" / "来道逻辑题" / "每日脑力训练"
- "做一道数学速算" / "来个记忆挑战" / "文字谜题"
- "查看我的脑力训练统计" / "连续打卡多少天了"
- "答案是 42" / "我选 B"
- "重置训练进度"

**不在 scope 内（不处理）：**
- 专业智力测试或 IQ 评估
- 学校考试题解答
- 竞赛编程题（请用 daily-code 类技能）
- 心理健康咨询

**凭证缺失时的行为：** 本 skill 无需任何凭证，所有功能开箱即用。

---

## Credentials

本 skill **无需任何凭证**。

| 操作 | 凭证 | 范围 |
|------|------|------|
| 生成题目 | 无 | 本地题库读取 |
| 记录进度 | 无 | 本地 JSON 文件读写 |
| 显示统计 | 无 | 本地数据读取 |

**不做的事：**
- 不读取、传输、记录任何凭证或 token
- 不访问网络或外部服务
- 不收集用户个人信息

---

## Persistence & Privilege

**持久化写入的内容：**

| 路径 | 内容 | 触发条件 |
|------|------|---------|
| `data/progress.json` | 用户训练进度（打卡天数、正确率、成就） | 每次提交答案时更新 |

**不写入的路径：**
- 不修改 shell 配置文件
- 不写入 skill 目录以外的任何路径
- 不创建 cron 任务（推送由外部调度）

**权限级别：**
- 以当前用户身份运行，不需要 sudo
- 仅读写 `data/progress.json` 一个文件
- 卸载方法：`rm -rf ~/.claude/skills/daily-brain`

---

## Install Mechanism

### 标准安装

```bash
# 复制到 skills 目录
cp -r daily-brain ~/.claude/skills/daily-brain/
```

### 验证安装

```bash
node ~/.claude/skills/daily-brain/scripts/today.js
# 应输出：今日脑力训练题目 HTML 卡片
```

### 可选：启用每日推送

在 Claude Code 中设置 cron：
```
每天上午 9:03 自动推送今日脑力训练
```

---

## Usage

```bash
# 获取今日题目
node scripts/today.js

# 指定难度
node scripts/today.js --difficulty hard

# 指定类别
node scripts/today.js --category logic

# 提交答案
node scripts/answer.js --answer "B"

# 查看统计
node scripts/stats.js

# 重置进度
node scripts/reset.js --confirm
```

---

*Version: 1.0.0 · Created: 2026-04-12*