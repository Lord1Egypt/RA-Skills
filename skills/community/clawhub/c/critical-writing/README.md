# critical-writing v2.0

> 多角色辩论写作工作流 · Multi-Persona Debate Writing Workflow

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-brightgreen)]()
[![SkillHub](https://img.shields.io/badge/SkillHub-critical--writing-blue)](https://www.skillhub.club/)
[![ClawHub](https://img.shields.io/badge/ClawHub-critical--writing-green)](https://clawhub.ai/)

**核心差异：不是一个名人单向批评，而是多个批评者互相对抗。**

文章在争论中被打磨，而不只是被单方面审判。

---

## 和其他写作 skill 的区别

| | 普通 AI 写作 | 单人批评写作 | **本 skill（v2）** |
|--|--|--|--|
| 批评方式 | 无 | 一个名人单向审稿 | **2-3个批评者互相辩论** |
| 改写依据 | 无 | 一方观点 | **争论后的共识 + 分歧交由作者决定** |
| 覆盖盲区 | 无 | 取决于单一视角 | **不同维度交叉覆盖** |
| 用户参与 | 低 | 中 | **高（参与仲裁决策）** |

---

## 快速安装

```bash
# SkillHub
npx @skill-hub/cli install critical-writing --agent claude

# ClawHub / OpenClaw
clawhub install critical-writing

# 手动（Claude Code）
cp -r critical-writing ~/.claude/skills/
```

---

## 工作流程

```
前置三问 → 规划确认 → 分步写作 → 辩论法庭 → 综合改写 → 交付
                                      │
                            ┌─────────┴─────────┐
                       第一轮：各自陈述     第二轮：互相反驳
                                      │
                                 仲裁：提炼共识与分歧
```

### 辩论法庭示例

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚖️ 辩论法庭开庭（鲁迅 × Steve Jobs）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【鲁迅 陈述】
总体判断：这篇文章在回避最重要的问题。
核心问题：
- 第二段提到"挑战"但完全没有说清楚挑战是什么
- 结论部分在喊口号，没有说真话

【Steve Jobs 陈述】
总体判断：信息太多，重点全被淹没了。
核心问题：
- 三个论点可以合并成一个
- 开头太长，第一句话就应该是你的结论

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 交叉辩论
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

鲁迅 回应 Jobs：
"你说要删掉两个论点，但问题不是论点太多，
是每个论点都没说到位。删掉之前先把剩下的写清楚。"

Jobs 回应鲁迅：
"说清楚是对的，但不等于要写更多。
用一句话说清楚比用三段话说模糊强得多。"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏛️ 仲裁结论
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

共识（优先改写）：
1. 第二段的"挑战"必须具体化
2. 结论要有真实判断，不能只喊口号

分歧（交由作者）：
- 是否合并论点 → 建议先把每个论点写深，再判断是否合并
```

---

## 内置批评者与推荐配对

| 配对 | 适合类型 | 张力来源 |
|------|---------|---------|
| Jobs × 马斯克 | 科技 / 产品 | 极简美学 vs 第一性原理 |
| 鲁迅 × 王朔 | 观点 / 评论 | 批判现实 vs 反矫情 |
| 芒格 × 德鲁克 | 商业 / 战略 | 逆向思维 vs 成果导向 |
| Ogilvy × Jobs | 营销 / 文案 | 读者利益 vs 极简聚焦 |
| 鲁迅 + Jobs + 芒格 | 深度打磨 | 真相 × 简洁 × 逻辑 |

---

## 文件结构

```
critical-writing/
├── SKILL.md                         # 核心工作流（AI 读取）
├── README.md                        # 本文件（人类读取）
├── references/
│   └── critics.md                   # 批评者风格 + 辩论配对手册
├── examples/
│   └── example-debate-session.md    # 完整辩论对话示例
└── tests/
    └── test-cases.md                # 测试用例
```

---

## 许可证

MIT — 自由使用、修改、分发。
