# Example: Synthetic — Over-Claim（过度断言）

## 元数据
- **来源**: Synthetic
- **真实/合成**: synthetic
- **维度**: Vocabulary（over-claim — 缺乏 hedge）
- **类型**: Bad ⭐
- **触发诊断**: vocabulary-diagnosis 的"over-claim detection"、"happy words 过度使用"

---

## 合成例句

> *"Our results **prove** that X causes Y. This is the **first study** to **definitively show** this relationship. **Without a doubt**, X is the most important predictor of Y, **surpassing all previous findings**. This novel discovery **revolutionizes** the field and **unprecedentedly** advances our understanding of Y."*

## 问题分析

### 1. 缺乏任何 hedge
- "prove" —— 强 confident（学术英语中极少用，除非数学定理）
- "definitively show" —— 强 confident
- "without a doubt" —— 强 confident
- "most important" —— 强 superlative
- "surpassing all previous findings" —— 强 comparative
- "revolutionizes" —— 强 happy word
- "unprecedentedly" —— 强 happy word

整段 **7 个 strong claim** —— 没有任何 hedge

### 2. Happy words 过度
- "first study" / "definitively show" / "novel discovery" / "revolutionizes" / "unprecedentedly"
- **同一段内 5 个 happy words** —— 学术写作禁忌
- Unit 4.2.2 Q&A "Is over-claiming OK if my findings are really novel?" 的标准答案：**No**

### 3. 无 epistemic stance 的精确度
- 没有 "may" / "suggest" / "indicate" / "appear" / "could"
- 没有 "Taken together" / "Our preliminary findings"
- 没有 "limited to" / "in this context"
- 这种"绝对化"语言会让 reviewer 警觉

### 4. 与好例对比
- `good_midgley_2020_hedging_variety.md` 中：3 种不同强度的 hedge
- `good_costello_2021_contribution_language.md` 中：低调 happy words
- 本反例：**全部强 claim，无 hedge**——**典型反例**

---

## 用法

当用户上传的 Discussion 出现以下情况时引用此例：

1. **用户全段都是 strong claim** — 引用此例展示 over-claim 问题
2. **用户测试 vocabulary-diagnosis** — 引用此例作为"全错"测试用例
3. **用户问"我觉得我的 finding 很重要，可以怎么写"** — 引用此例 + `good_costello_2021_contribution_language.md` 让用户对比

---

## 相关诊断资源

- SKILL.md: Hedging Principles（Unit 4.4.2）
- rubric.md: V1 (hedge variety), V4 (happy words appropriateness)
- checklist.md 第 2、5 条
- 与 conventions-diagnosis 的"academic claim 规范"维度交叉