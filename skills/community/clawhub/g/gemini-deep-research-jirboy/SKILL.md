---
name: gemini-deep-research
description: [已整合] Gemini 深度研究已整合到 research 统一入口技能
argument-hint: "[研究主题]"
---

# ⚠️ 已整合 - 请使用 research 统一入口

> **本技能保留用于向后兼容，功能已整合到 `research` 统一入口技能**
>
> **推荐使用：** `research deep [主题]` 或直接使用本技能（自动转发）

---

# Gemini Deep Research（兼容层）

Use Gemini's Deep Research Agent to perform complex, long-running context gathering and synthesis tasks.

## 迁移指南

**新用法：**
```
research deep 竞争分析 电动汽车电池
research deep 市场调研 人工智能
```

**旧用法（仍然可用）：**
```
deep 竞争分析 电动汽车电池
```

## Prerequisites
- `GEMINI_API_KEY` environment variable (from Google AI Studio)
- **Note**: Does NOT work with Antigravity OAuth tokens

## How It Works
1. Breaks down complex queries into sub-questions
2. Searches the web systematically
3. Synthesizes findings into comprehensive reports
4. Provides streaming progress updates

## Output
- `deep-research-YYYY-MM-DD-HH-MM-SS.md` - Final report in markdown
- `deep-research-YYYY-MM-DD-HH-MM-SS.json` - Full interaction metadata
