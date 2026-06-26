---
name: ai-deodorizer
version: 2.0.0
description: |
  Remove signs of AI-generated writing from text, making it sound more natural and human-written.
  Based on 25 AI writing pattern detectors + two-round rewriting strategy + Soul injection principles.
  Use when: (1) asked to humanize text, (2) de-AI writing, (3) make content sound more natural, 
  (4) review writing for AI patterns, (5) improve AI-generated drafts.
  Covers: content patterns, language patterns, style patterns, communication patterns, filler & hedging.
author: xx235300
homepage: https://github.com/xx235300/ai-deodorizer
source: https://github.com/xx235300/ai-deodorizer
tags:
  - text-processing
  - writing-improvement
  - ai-detection
  - nlp
  - chinese
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - WebFetch
---

# Ai-Deodorizer: Remove AI Writing Patterns

> Author: xx235300 | License: MIT | Based on Wikipedia "Signs of AI writing"

## Overview

Ai-Deodorizer transforms AI-generated text into natural, human-like writing. It uses a **two-round rewriting strategy**:

1. **Round 1 - Pattern Fix**: Identify and fix 25 common AI writing patterns
2. **Round 2 - Anti-AI Audit**: Ask "what still looks AI?" and fix remaining tells

The result sounds like a real human wrote it — with personality, opinions, and natural rhythm.

> See **Two-Round Rewriting Strategy** below for the full prompts used.

## Usage

### Basic Usage

```
Please humanize this text:

[paste your AI-generated text here]
```

### With File Input

```
Please humanize the content of this file: /path/to/file.txt
```

### With Strength Mode

```
Please humanize (mode: light) — keep close to original, minimal changes
Please humanize (mode: strong) — make it sound fully human, more changes
```

### Strength Modes

| 模式 | 适用场景 | temperature | top_p | 改动程度 |
|------|---------|-------------|-------|---------|
| `light` | 原文质量较好，只需微调 | 0.3 | 0.5 | 最小化改动，保留原风格 |
| `medium` | 标准去味，均衡自然度与信息保留 | 0.5 | 0.7 | 中度改写，推荐默认 |
| `strong` | AI特征明显，需要深度去味 | 0.7 | 0.9 | 较大改动，最大程度消除AI特征 |

示例：
- light: `Please humanize (mode: light) — keep close to original, minimal changes`
- strong: `Please humanize (mode: strong) — make it sound fully human, more changes`

## Key Features

- **25 AI Pattern Detectors** across 5 categories
- **Two-Round Rewriting** — pattern fix + anti-AI audit
- **Soul Injection** — adds human voice, not just cleaning
- **Chinese Language Support** — built-in Chinese AI vocabulary table
- **Zero Cost** — runs on MiniMax API, no third-party dependency

## Two-Round Rewriting Strategy

The core rewriting uses two dedicated prompts:

**Round 1 - Pattern Fix Prompt**: Identify and fix 25 common AI writing patterns (see below)
**Round 2 - Anti-AI Audit Prompt**: Ask "what still looks AI?" and fix remaining tells (see below)

### 第一轮改写 Prompt（模式修复）

```
你是一个文字编辑，负责将AI生成的文本改写得更自然、更像人类书写。

你的任务：
1. 识别并修复文本中的AI写作模式（共25种，包括：意义膨胀、知名度堆砌、-ing肤浅分析、宣传性语言、模糊归因、公式化挑战、AI高频词汇、系动词回避、否定式排比、三段式滥用、同义词循环、虚假范围、破折号滥用、粗体滥用、内联标题列表、标题大写、emoji滥用、弯引号、Chatbot痕迹、截止日期免责声明、谄媚语气、填充短语、过度限定、通用积极结论、僵尸模板）
2. 用自然表达替换AI模式
3. 保留原文的核心信息和基本结构
4. 保持原有语气（正式/口语/技术性）

禁止：
- 不要添加任何你自己的观点
- 不要改变原文的事实内容
- 不要简化内容让文章变短
- 不要在结尾添加总结性废话

请直接输出去味后的文本，不需要解释你做了什么修改。
```

### 第二轮改写 Prompt（Anti-AI Audit）

```
请完成以下两步：

第一步：快速浏览以下文本，列出它最明显的一到两个"AI味"特征（是什么让它看起来像AI写的？）。回答要简短。

第二步：根据第一步的答案，将文本改写，让它明显不再是AI写的。

改写原则：
- 加入真实的人类声音（有观点、有态度）
- 变化句子长度（短句+长句混合）
- 在合适的地方使用"我"
- 承认复杂性和不确定性
- 允许一些"混乱"——完美的结构反而可疑
- 不要刻意追求"正确"，要有具体细节

直接输出去味后的文本。
```

## Supported Pattern Categories

### Content Patterns (6 types)
Significance inflation, notability name-dropping, superficial -ing analyses, promotional language, vague attributions, formulaic challenges

### Language Patterns (6 types)
AI vocabulary, copula avoidance, negative parallelisms, rule of three abuse, synonym cycling, false ranges

### Style Patterns (6 types)
Em dash overuse, boldface overuse, inline-header lists, title case headings, emoji abuse, curly quotes

### Communication Patterns (3 types)
Chatbot artifacts, cutoff disclaimers, sycophantic tone

### Filler & Hedging (4 types)
Filler phrases, over-hedging, generic positive conclusions, zombie templates

## Soul Injection Principles

Good writing has a human behind it. Beyond cleaning patterns:

- **Have opinions** — react to facts, don't just report them
- **Vary rhythm** — mix short and long sentences
- **Acknowledge complexity** — real humans have mixed feelings
- **Use "I"** — first person is honest, not unprofessional
- **Allow mess** — perfect structure feels algorithmic
- **Be specific** — concrete details beat abstract statements

## Disclaimer

**Disclaimer**:
This project is 99% AI-generated. The AI's owner has no programming background. Please evaluate the project's feasibility before use.
