---
name: english-daily
description: "Daily English learning with spaced repetition — built-in A1–B2 word bank, new words daily, quiz mode (MCQ/fill-in/spelling), streak tracking, level progression."
keywords: 学英语, 英语单词, 今日单词, 英语练习, 英语学习, 词汇, 测验, 打卡, 连续学习, 进度, 间隔重复, 每日推送, English learning, vocabulary, daily words, quiz, streak, spaced repetition, English practice, CEFR, word bank
metadata:
  openclaw:
    runtime:
      node: ">=18"
---

# English Daily

> 私人英语学习助手 — 每日单词 · SRS复习 · 测验打卡 · 进度追踪

## 何时使用

- 用户说"学英语""英语单词""今日单词""英语练习"
- 用户想背单词、做填空、做选择题
- 用户说"测验""我的进度""连续打卡""学习报告"
- 用户说"开启推送""每天推英语单词"

---

## 核心命令

```bash
# 注册（首次使用）
node scripts/register.js <userId> <姓名> [等级 A1/A2/B1/B2] [每日目标 1-20]

# 今日学习（每日推送内容）
node scripts/daily-push.js <userId>

# 测验练习
node scripts/quiz.js <userId> [vocab|sentence|mixed]

# 记录测验积分（Claude 在测验完成后调用）
node scripts/quiz.js <userId> --score <正确题数×10>

# 查看进度
node scripts/progress.js <userId>

# 推送管理
node scripts/push-toggle.js on <userId> [--morning 08:00] [--channel telegram]
node scripts/push-toggle.js off <userId>
node scripts/push-toggle.js status <userId>
```

---

## 学习流程

1. **注册** → `register.js` 创建学习档案（等级、每日目标）
2. **每日学习** → `daily-push.js` 输出今日复习词 + 新词列表
3. **测验** → `quiz.js` 生成5题（词义选择或句子填空），Claude 逐题互动
4. **记分** → 测验完成后 Claude 调用 `--score` 记录积分并更新SRS进度
5. **进度** → `progress.js` 显示连续打卡、掌握词数、升级进度

---

## 推送设置

```bash
node scripts/push-toggle.js on <userId>                # 默认 08:00
node scripts/push-toggle.js on <userId> --morning 07:30 --channel feishu
node scripts/push-toggle.js off <userId>
```

支持渠道：`telegram` / `feishu` / `slack` / `discord`

---

## 等级体系

| 等级 | 词汇量 | 升级条件（掌握词数） |
|------|--------|---------------------|
| A1   | ~40词  | 掌握40词 → 升A2      |
| A2   | ~50词  | 掌握90词 → 升B1      |
| B1   | ~40词  | 掌握130词 → 升B2     |
| B2   | ~30词  | 最高等级              |

掌握标准：SRS间隔 ≥ 7天（即多次正确复习）

---

## SRS算法说明

采用简化SM-2间隔重复：
- 质量1（遗忘）/ 质量2（困难）→ 明天复习
- 质量3（掌握）→ 间隔 × 1.5
- 质量4（轻松）→ 间隔 × 2.0
- 最大间隔30天

---

## 注意事项

- 数据存储在 `data/users/<userId>.json`，无外部API依赖
- 内置单词库（A1-B2共约160词），`data/wordbank.json`
- 所有脚本仅使用 Node.js 内置模块（fs/path），无需 npm install
- 用户ID仅允许字母、数字、连字符、下划线（防路径穿越）
