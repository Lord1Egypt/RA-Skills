# AI味检测 / Detect AI Flavor

> 判断中文长文是AI写的还是人写的 —— 6维度评估框架，逐段分析，给出改进建议。
> Judge whether Chinese long-form articles are AI-generated or human-written — 6-dimension evaluation framework with detailed analysis and improvement suggestions.

---

## 中文介绍

### 这是什么？

一个用于检测中文长文中「AI味」的 WorkBuddy 技能。通过对文章进行六个维度的系统评估，判断文本是纯AI生成、AI生成后人工修改、人写后AI润色，还是纯人写。

### 能检测什么？

| 维度 | 检测内容 |
|------|---------|
| **结构模式** | 是否有编号强迫症？章节是否过于整齐对称？ |
| **句式节奏** | 句子长度是否千篇一律？有没有单句段落？ |
| **用词风格** | 是否堆砌术语（赋能/生态/底层逻辑）？ |
| **逻辑推进** | 是否每句话都在"一方面…另一方面…"？ |
| **表达温度** | 有没有幽默？有没有具体人物？有没有作者人格？ |
| **信息密度** | 是否每句都在输出，零呼吸感？ |

### 怎么用？

1. 对 WorkBuddy 说「这篇文章有没有AI味」，贴入文章内容
2. 或者贴钛媒体/其他网站的链接，Skill 会自动抓取文本
3. 结果会输出六维度评估表 + 原文证据 + 改进建议

### 评估案例

已积累3篇评估案例，覆盖「AI味重」到「纯人写」的光谱：
- Satispay融资分析 → ❌ AI味偏高
- 即时零售三巨头 → ⚠️ AI味中低
- 堂食回归时代 → ✅ AI味极低
- 大厂AI「包身工困境」 → ✅ 纯人写

---

## English Introduction

### What is this?

A WorkBuddy skill for detecting "AI flavor" in Chinese long-form articles. It evaluates text across six dimensions to distinguish pure AI generation, AI-with-human-editing, human-with-AI-polishing, and pure human writing.

### What does it detect?

| Dimension | What it checks |
|-----------|---------------|
| **Structure** | Overly symmetric sections? Number compulsion? |
| **Sentence Rhythm** | Uniform sentence length? No short punchy lines? |
| **Word Choice** | Buzzword stacking? Abstract nouns without context? |
| **Logic Flow** | "On one hand… on the other hand" everywhere? |
| **Human Warmth** | Any humor? Named sources? Author personality? |
| **Density & Breath** | Every sentence advancing? No breathing room? |

### How to use

1. Tell WorkBuddy: "Check this article for AI味" and paste the text
2. Or drop a URL (e.g., tmtpost.com), the skill auto-fetches content
3. Output: 6-dimension scorecard + quoted evidence + writing fixes

### Sample Evaluations

4 real-world articles evaluated, covering the full spectrum from heavy AI to pure human writing.

---

## 安装 / Installation

### 从 ClawHub 安装
```
在 WorkBuddy 中搜索 skill: detect-ai-flavor
或直接访问: https://clawhub.ai/vivian8725118/detect-ai-flavor
```

### 从源码安装
```bash
cp -r detect-ai-flavor ~/.workbuddy/skills/
```

---

## 文件结构 / File Structure

```
detect-ai-flavor/
├── SKILL.md                          # 核心技能定义（WorkBuddy 执行用）
├── README.md                         # 本文件（人类阅读用）
└── references/
    ├── indicator-checklist.md        # 32项快速检测指标
    └── evaluation-examples.md        # 已评估案例集（供校准）
```
