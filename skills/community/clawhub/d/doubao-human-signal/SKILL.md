---
name: doubao-human-signal
title: Doubao Human Signal / 豆包人类信号
description: "They spot AI writing at a glance — and it costs you. Score your text's AI-flavor (0-100) before hitting send: boilerplate density, em-dash tics, sentence-length uniformity, robotic lists. 一眼看出是AI写的，扣印象分。触发词：去AI味、人类信号、AI味、human signal、ai-flavor。"
description_en: "They spot AI writing at a glance — and it costs you. Score your text's AI-flavor (0-100) before you send: boilerplate density, em-dash tics, sentence-length uniformity, robotic list patterns. Zero-dependency heuristic hint, not a verdict."
description_zh: "一眼看出是 AI 写的，扣印象分。发送前给文字做个 AI 痕迹体检（0-100 分）：套话密度、破折号滥用、句长均匀度、机械排比清单。零依赖启发式提示，不做判定。"
slug: doubao-human-signal
version: 1.1.1
display_name: 豆包人类信号
display_name_en: Doubao Human Signal
agent_created: true
author: SynomosAI contributors
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见 README「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write
category: writing
platforms: [cross-platform]
copyright: SynomosAI
classification:
  skillhub: ["productivity-writing"]
  iso_25010: ["Usability"]
risk_tier: low
risk_rationale: "零依赖本地只读脚本：无网络、无文件写入、无子进程；密钥零接触。"
tags: [human-signal, de-ai-flavor, writing, ai-flavor, 去AI味, 人类信号]
ai_protocol: true
read_when:
  - 写完文案/简历/邮件/社媒帖子后，怕"一眼被看出是 AI 写的"、想压 AI 痕迹分时
  - 审稿时怀疑某段文字套话太密、破折号太多、句式整齐得不像人写时
  - 需要一个 0-100 的"人类信号分"作为修改参考（启发式，非判定）时
  - 触发词：去AI味、人类信号、AI味、像AI写的、human signal、ai-flavor、de-ai
---
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/ai_reply_heuristics.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: file
    type: string
    description: 文本文件路径
    required: false
  - name: text
    type: string
    description: 内联文本（或 @文件路径）
    required: false
  - name: json
    type: bool
    description: JSON 输出
    required: false
output_schema:
  stdout: AI 痕迹分 0-100 + 三档区间 + 命中套话清单
  rc=0 / rc=2 输入不可读
capabilities:
  - ai_detection
  - text_analysis
  - writing_style
permissions:
  network: false
  filesystem: true
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.0: initial (source: ai-reply-heuristics). 1.1.0: viral repackage doubao-human-signal — bilingual EN-first rewrite, scripts byte-identical. 1.1.1: version bump (1.1.0 occupied on registry, concurrency avoidance)."
> LGD 治理学 · 创造术家族

## English

### When to use

You wrote a pitch, a resume cover note, an email, or a social post. You reread it and it sounds... smooth. Too smooth. The reader will smell the AI flavor in two seconds, and that costs you trust — the exact thing the message was supposed to build. This skill gives your text a 30-second AI-flavor checkup: a 0–100 human-signal score from four mechanical tells — boilerplate density, em-dash tic frequency, sentence-length uniformity, and robotic parallel lists. It is a hint to revise, never a verdict on who wrote it.

Use it when:
- You are about to send anything where "a human wrote this" matters (job applications, client emails, founder posts).
- You are editing someone else's draft and suspect it is machine-polished.
- You need a concrete, repeatable score to compare revisions before/after editing.

### Quick start / demo

```bash
python scripts/ai_reply_heuristics.py --text "在当今时代，综上所述，我们需要深入探讨 AI 技术如何赋能业务闭环。值得注意的是，随着技术的发展，AI 将深刻重塑行业格局——首先提升效率，其次优化体验，最后创造价值。" --json
```

Real output (smoke run 2026-10-17, rc=0):

```json
{
  "score": 56,
  "band": "存疑",
  "cliche_hits": ["深入探讨", "综上所述", "值得注意的是", "在当今", "赋能"],
  "sentences": 2,
  "chars": 84,
  "note": "启发式提示，不构成判定；单独信号均可能误报"
}
```

Same machine, a human sentence:

```bash
python scripts/ai_reply_heuristics.py --text "这稿子客户看完没说话。我猜是数据那页太干了，回头把案例换成上周深圳那单。" --json
# => score 0, band 更像人写 (human-like), rc=0
```

Bands: `<30` reads more human · `30–60` suspicious · `>60` obvious AI flavor.

### Flow

1. Save or inline the text you are about to send.
2. Run `python scripts/ai_reply_heuristics.py --text "..." --json` (or `--file draft.txt`).
3. Read the score and the cliche-hit list.
4. Kill the flagged boilerplate, break the evenly-cut sentences, vary the rhythm.
5. Re-run until the score drops below 30 — then send.

### Evidence & safety

- The score is heuristic-only: no single signal proves AI authorship, and any single signal can false-positive. Never use it to accuse a writer.
- Zero dependencies, stdlib only, works offline.
- Version: 1.1.1. Engine script unchanged from source (sha256 identical).

## 中文

### 何时用

你写了一段提案、一封求职自荐信、一封客户邮件、一条社媒帖子。回头一读——太顺了，顺得不像人写的。读者两秒就闻出 AI 味，而扣掉的恰好是这条消息想建立的那点信任。本技能给你的文字做 30 秒 AI 痕迹体检：从四个机械化信号算出 0–100 的"人类信号分"——套话密度、破折号滥用、句长均匀度、机械排比清单。它是修改提示，不是"谁写的"的判定。

适用场景：
- 任何"人写的"这件事很重要的发送前（求职、客户邮件、创始人发声）。
- 改别人的稿子，怀疑它被机器抛光过。
- 需要一个可复现的分数，对比修改前后。

### 快速上手 / Demo

```bash
python scripts/ai_reply_heuristics.py --text "在当今时代，综上所述，我们需要深入探讨 AI 技术如何赋能业务闭环。值得注意的是，随着技术的发展，AI 将深刻重塑行业格局——首先提升效率，其次优化体验，最后创造价值。" --json
```

实跑输出（2026-10-17 冒烟，rc=0）：

```json
{
  "score": 56,
  "band": "存疑",
  "cliche_hits": ["深入探讨", "综上所述", "值得注意的是", "在当今", "赋能"],
  "sentences": 2,
  "chars": 84,
  "note": "启发式提示，不构成判定；单独信号均可能误报"
}
```

同一台机器，一句人话：

```bash
python scripts/ai_reply_heuristics.py --text "这稿子客户看完没说话。我猜是数据那页太干了，回头把案例换成上周深圳那单。" --json
# => 得分 0，区间 更像人写，rc=0
```

分档：`<30` 更像人写 · `30–60` 存疑 · `>60` AI 痕迹明显。

### 流程

1. 准备好你正要发送的文本（内联或存成文件）。
2. 运行 `python scripts/ai_reply_heuristics.py --text "..." --json`（或 `--file draft.txt`）。
3. 读分数和命中套话清单。
4. 删掉被点名的套话，打散整齐均匀的句式，让节奏有长有短。
5. 复跑直到分数压到 30 以下——再发送。

### 证据与安全声明

- 分数为启发式提示：任何单一信号都不构成"AI 生成"的判定，也都可能误报。请勿据此单独追责任何作者。
- 零依赖，仅标准库，离线可用。
- 版本：1.1.1。引擎脚本与源包逐字节一致（sha256 相同）。
