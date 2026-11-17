# Example: Synthetic — Tense Consistency Violation（时态一致违反）

## 元数据
- **来源**: Synthetic
- **真实/合成**: synthetic
- **维度**: Grammar（同一 move 内时态不一致）
- **类型**: Bad ⭐
- **触发诊断**: grammar-diagnosis 的"时态一致性"——同一论证功能内不应无理由切换

---

## 合成例句

> *"We **tested** whether X predicts Y. Our results **showed** that X is associated with Y. We **find** that the effect size is moderate. The relationship **suggested** that X might be a causal factor. We **conclude** that X is an important predictor of Y."*

## 问题分析

### 1. 同一段内 5 个 verb，时态混乱
- **tested** (Past)
- **showed** (Past)
- **find** (Present) ❌ 应该用 found
- **suggested** (Past)
- **conclude** (Present) ❌ 应该用 concluded

### 2. 无 epistemic 理由的切换
- 整段都是**本研究结果** —— 应该统一用 Past Simple
- 但中途 "find" / "conclude" 用了 Present——违反了"study-specific findings 用 Past"原则
- 这是 Unit 4.2.2 Q&A 警告的"随意切换时态"

### 3. 与好例对比
- `good_costello_2021_present_past_switch.md` 中：段内 4 种时态都有，但每个都有 epistemic 理由
- 本反例：段内时态无理由切换——纯粹的不一致

### 4. 严重性评估
- 这类错误在顶刊论文中**极少见**
- 一旦出现，会让读者困惑："这个 claim 是已成立的还是只是本研究提出的？"
- 错误严重性：**Minor to Major**（取决于切换位置）

---

## 用法

当用户上传的 Discussion 出现以下情况时引用此例：

1. **用户同一段内时态不一致** —— 引用此例展示 tense consistency violation
2. **用户问"我可以在同一段里用不同的时态吗"** —— 引用此例说明"可以，但必须有 epistemic 理由"

---

## 相关诊断资源

- SKILL.md: Tense Consistency（同 move 内）
- rubric.md: G2 (consistency)
- checklist.md 第 3 条
- 与 vocabulary-diagnosis 的"verb tense + epistemic"维度交叉