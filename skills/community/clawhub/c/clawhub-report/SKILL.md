---
name: clawhub
description: Draft Chinese daily reports, weekly/monthly summaries, meeting recaps, study notes, and concise research digests from rough notes, links, chat logs, documents, or web research. Use when the user asks to 写日报、周报、月报、总结、复盘、学习笔记，or to research and explain networking and cybersecurity topics for learning, internal sharing, or defensive understanding.
---

# Clawhub

## Overview

Turn rough input into clean Chinese reports, summaries, study notes, and research digests.

Prefer short sections, high information density, and accurate terminology. When networking or security topics depend on current versions, advisories, or best practices, verify freshness from the web before writing.

## Core workflow

1. Determine the target output.
   - 日报
   - 周报 / 月报
   - 项目总结 / 复盘
   - 学习笔记
   - 技术调研 / 知识卡片
2. Collect source material.
   - User notes
   - Task lists
   - Chat logs
   - Documents
   - URLs
   - Fresh web research
3. Extract signal.
   - What was done
   - What changed
   - What mattered
   - What is blocked
   - What should happen next
4. Rewrite for the audience.
   - Manager-facing: progress, impact, risk, next steps
   - Peer-facing: technical facts, tradeoffs, conclusions
   - Personal learning: concepts, terms, examples, open questions
5. Polish the result.
   - Remove repetition
   - Preserve uncertainty
   - Do not invent missing work or unsupported claims

## Output modes

### 日报 / 站会更新

Use when the user asks for 日报, 今日进展, worklog, standup note, or a brief progress sync.

Preferred structure:
- 今日完成
- 当前进展
- 问题 / 风险
- 明日计划

If the source material is weak, keep it concise and clearly indicate incomplete input instead of fabricating accomplishments.

### 周报 / 月报

Use when the user asks for a broader summary over time.

Preferred structure:
- 周期重点
- 已完成事项
- 阶段成果 / 影响
- 问题与风险
- 下阶段计划

Prefer outcomes over raw activity lists.

### 总结 / 复盘

Use when the user asks for 总结, recap, review, retrospective, or takeaways.

Preferred structure:
- 背景
- 核心过程
- 关键结论
- 做得好的地方
- 可改进点
- 后续建议

### 学习笔记

Use when the user wants to study and retain knowledge.

Preferred structure:
- 主题
- 一句话总结
- 核心概念
- 关键术语
- 典型场景
- 常见误区
- 可继续深入的问题

### 技术调研 / 安全研究摘要

Use when the user asks to search, compare, or explain networking and cybersecurity topics.

Preferred structure:
- 主题
- 背景
- 关键发现
- 技术要点
- 风险与限制
- 建议 / 结论
- 参考来源

Read `references/security-research.md` for the research checklist and `references/report-templates.md` for reusable templates.

## Networking and security research rules

When the task involves 网络, 安全, 协议, 漏洞, 架构, hardening, attack surface, or defensive operations:

1. Fetch current sources when freshness matters.
2. Separate facts from interpretation.
3. Prefer official or primary sources first.
4. Note versions, dates, and scope.
5. Prefer defensive and educational framing.
6. Avoid detailed offensive procedures unless the user clearly requests authorized defensive testing support.

## Writing rules

- Prefer Chinese unless the user asks otherwise.
- Be compact and readable.
- Use bullets and short sections.
- Preserve technical accuracy.
- Translate jargon only when it improves clarity.
- End with actionable next steps when useful.
- If the audience is unclear, default to an internal professional tone.

## Quality bar

Before finishing, check:
- Did the output capture all important source points?
- Did it avoid invented facts and overclaiming?
- Is the structure easy to scan quickly?
- Are networking or security claims fresh enough for the task?
- Are sources cited when research mattered?

## Bundled references

- `references/report-templates.md` — Chinese templates for 日报 / 周报 / 月报 / 复盘 / 学习总结 / 技术调研
- `references/security-research.md` — checklist for current, defensible networking and security research
- `references/publish-copy.md` — ready-to-use ClawHub listing copy
