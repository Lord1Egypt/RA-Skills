---
name: argument-audit
description: 论点审计 - An analytical tool that evaluates the logical structure, evidence quality, and persuasiveness of arguments. Use when user asks about 论点分析、论证评估、逻辑审查、观点评估, or wants to analyze the strength and validity of an argument.
version: v1.0.0
tags: argument-analysis, critical-thinking, logical-fallacy, debate-preparation
---

# Argument Audit (论点审计)


## Usage Scenarios

### Scenario 1: Analyze an Article's Argument
**User input:** "帮我分析这篇文章的论证逻辑。"

**Expected output:** Argument structure diagram identifying main claim and supporting premises, evidence quality assessment with credibility/relevance/sufficiency ratings, logical fallacy detection, and overall strength score (1-10).

### Scenario 2: Prepare for a Debate
**User input:** "找出我论点中的薄弱环节，我要准备辩论。"

**Expected output:** Vulnerability scan identifying unsupported assumptions, missing evidence, potential counterarguments, and 3-5 concrete improvement suggestions to strengthen the position.

### Scenario 3: Evaluate a Business Proposal
**User input:** "这个商业提案的论证是否严谨？"

**Expected output:** Multi-dimension audit (clarity, validity, soundness, completeness, fairness) with scores for each, specific weaknesses called out, and actionable recommendations for strengthening the proposal before presentation.
### Scenario 4: 分析我跟同事在微信上的吵架记录
**User input:** "我跟同事在微信群里因为一个需求吵起来了，他说的我觉得不对但是又不知道怎么反驳，帮我分析一下。"
**Expected output:** 导出微信聊天记录，进行论证分析：1）识别双方的论点、论据和结论；2）发现逻辑谬误（如人身攻击、滑坡谬误、虚假两难）；3）评估证据强度。给出结构化反驳建议：先承认对方合理部分，再用事实/数据支持自己的立场，最后建议私下沟通而非群内争论。

## Overview

This skill provides systematic analysis and evaluation of arguments. It helps users understand the logical structure of arguments, assess the quality of evidence, identify logical fallacies, and evaluate overall persuasiveness. Useful for critical thinking, debate preparation, writing analysis, and decision-making.

## When to Use This Skill

- Analyzing essays, articles, or opinion pieces
- Preparing for debates or discussions
- Evaluating business proposals or recommendations
- Reviewing academic arguments
- Self-checking own arguments before presenting
- Understanding propaganda or misleading content

## What This Skill Analyzes

### 1. Logical Structure
- **Argument identification** — Main claim vs. supporting points
- **Reasoning chains** — How conclusions follow from premises
- **Argument type** — Deductive, inductive, abductive reasoning
- **Structure flaws** — Missing links, unsupported assumptions

### 2. Evidence Quality
- **Source credibility** — Authority, expertise, potential bias
- **Evidence relevance** — Direct support vs. tangential
- **Evidence sufficiency** — Adequate support for claim
- **Data quality** — Sample size, methodology, recency

### 3. Logical Fallacies
- Ad hominem attacks
- Straw man arguments
- False dilemmas
- Slippery slope
- Circular reasoning
- Appeal to authority/emotion
- Hasty generalizations
- Post hoc ergo propter hoc
- Red herring
- Tu quoque

### 4. Persuasiveness Assessment
- Overall argument strength (1-10 scale)
- Emotional vs. rational appeal balance
- Counterargument consideration
- Balance and objectivity

## Audit Framework

| Dimension | Criteria | Questions |
|-----------|----------|-----------|
| **Clarity** | Is the main argument clear? | What exactly is being argued? |
| **Validity** | Does the reasoning hold? | Do conclusions follow from premises? |
| **Soundness** | Are premises true? | Is the evidence credible? |
| **Completeness** | Are key points covered? | What's missing? |
| **Fairness** | Are alternatives considered? | Are counterarguments addressed? |

## Workflow

1. **Input Analysis** — Parse the argument into components
2. **Structure Mapping** — Diagram the logical structure
3. **Evidence Review** — Assess each piece of supporting evidence
4. **Fallacy Check** — Scan for common logical fallacies
5. **Strength Rating** — Evaluate overall persuasiveness
6. **Improvement Suggestions** — Recommend ways to strengthen

## Usage Examples

### Analyzing Written Arguments
```
"帮我分析这篇文章的论点"
"这篇论文的论证有什么问题?"
"这个商业计划书的逻辑是否严密?"
```

### Debate Preparation
```
"帮我找出对方论点中的漏洞"
"如何反驳这个观点?"
"我的论点有什么薄弱环节?"
```

### Critical Evaluation
```
"这个说法有什么逻辑问题?"
"这个专家的观点可信吗?"
"这段内容有哪些隐藏的假设?"
```

## Output Format

For each audit, provide:

```
## Argument Summary
[1-2 sentence description of the main argument]

## Structure Analysis
[Diagram or breakdown of reasoning structure]

## Evidence Assessment
| Evidence | Source | Credibility | Relevance | Rating |
|----------|--------|-------------|-----------|--------|
| ...      | ...    | ...         | ...       | ...    |

## Fallacy Detection
- [List any logical fallacies found with explanations]

## Strength Rating
- Clarity: X/10
- Validity: X/10
- Soundness: X/10
- Completeness: X/10
- Overall: X/10

## Recommendations
[Suggestions for strengthening the argument]
```

## Limitations

- Cannot access external sources to verify evidence claims
- Assessment is based on provided text only
- Context-dependent factors may not be fully captured
- Subjective elements exist in persuasiveness ratings

## Related Skills

- `summarize` — For summarizing argument content
- `cognitive-reframe` — For rephrasing arguments
- `decision-fatigue-reliever` — For simplifying complex arguments
