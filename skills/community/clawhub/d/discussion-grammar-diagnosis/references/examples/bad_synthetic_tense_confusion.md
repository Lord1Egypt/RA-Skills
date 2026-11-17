# Example: Synthetic — Tense Confusion（时态错乱）

## 元数据
- **来源**: Synthetic
- **真实/合成**: synthetic
- **维度**: Grammar（时态与 epistemic stance 错位）
- **类型**: Bad ⭐
- **触发诊断**: grammar-diagnosis 的"时态选择错误"

---

## 合成例句

> *"We **found** that people who score high on X also score high on Y. This **suggests** that there is a relationship between X and Y. **Previous studies have showed** (sic) similar results, which **suggested** that X leads to Y. However, recent meta-analyses **suggests** (sic) that the relationship is not as strong as we **was** (sic) expecting."*

## 问题分析

### 1. Past/Present 错位
- "We **found**" (Past) → "This **suggests**" (Present) —— 后一句是合理的 present claim ✓
- "Previous studies **have showed**" (Present Perfect + 错误动词形式) —— 应该 "have shown" ✗
- "which **suggested**" (Past) → 但这里指一般结论，应该用 Present（"suggest"）✗
- "meta-analyses **suggests**" —— meta-analyses 是复数，应该 "suggest" ✗

### 2. 多处 Subject-Verb Agreement 错误
- "we **was** expecting" —— we 应该配 were
- "meta-analyses **suggests**" —— 复数主语应该配 suggest

### 3. Present Perfect 动词形式错误
- "have **showed**" —— 不规则动词 show 的过去分词是 **shown**，不是 showed
- "have **finded**"（类似错误）

### 4. 与好例对比
- `good_midgley_2020_tense_alignment.md`：时态与立场完美匹配
- `good_costello_2021_present_past_switch.md`：段内合法切换
- 本反例：时态与立场错位 + agreement 错误 + 动词形式错误——**复合错误**

### 5. 这种错误顶刊几乎不会出现
- 这是教学型合成反例（标注 synthetic）
- 主要用于 grammar-diagnosis 测试其能否识别多种基础语法错误
- 真实论文诊断时，grammar 错误主要是"轻微"级别

---

## 用法

当用户上传的 Discussion 出现以下情况时引用此例：

1. **用户问"我的 Discussion 是不是时态错了"** —— 引用此例展示典型时态错乱
2. **用户测试 grammar-diagnosis** —— 引用此例作为"全错"测试用例

---

## 相关诊断资源

- SKILL.md: Tense Principles + Verb Forms
- rubric.md: G1-G7 所有项
- checklist.md 第 1、2、5 条
- 这是**grammar 维度的"基础错误型"反例**——同时也是 conventions 反例（学术写作规范）