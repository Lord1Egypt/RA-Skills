# Example: Synthetic — Causal Overreach（因果过推）

## 元数据
- **来源**: Synthetic
- **真实/合成**: synthetic
- **维度**: Logic（causal overreach — 数据不支持的因果 claim）
- **类型**: Bad ⭐
- **触发诊断**: logic-diagnosis 的"因果 vs 相关混淆"

---

## 合成例句

> *"Our correlational study **found** that people who score high on X also score high on Y. **Therefore**, X **causes** Y. This **proves** that X is a **direct cause** of Y, and that **interventions targeting X will reduce Y**."*

## 问题分析

### 1. 因果 claim 超出数据范围
- 数据：**相关**（correlational study found X 和 Y 相关）
- Claim：**因果**（"X causes Y"）+ **直接因果**（"direct cause"）+ **干预效果**（"interventions targeting X will reduce Y"）
- 这是 **Unit 4.2.2 Q&A "What if my correlational data show X and Y are related?" 的标准错误答案**

### 2. 三层结构混乱
- 应该是：Data（X 与 Y 相关）→ Interpretation（可能 X 影响 Y）→ Speculation（如果干预 X 可能减少 Y）
- 实际写：Data + 直接跳到 Speculation（甚至更强）

### 3. "Therefore" 的错误使用
- **"Therefore"** 是逻辑推理信号——但这里没有推理过程
- 直接从"相关"到"因果"是**逻辑飞跃**
- 应该用 "**This suggests that X may be related to Y**"（interpretation）

### 4. 干预 claim 的过度推论
- "**interventions targeting X will reduce Y**" —— 这是从 correlational study 推到 RCT 结果
- 是 **causal overreach** 的典型例子
- 顶刊几乎不会这样写（除非是 RCT 或 longitudinal）

### 5. 与好例对比
- `good_midgley_2020_data_interpretation_speculation.md` 中："My studies suggest"（interpretation，不是"prove"）
- `good_costello_2021_causal_chain.md` 中："perhaps mirroring SD's definitional core"（hedge 后的机制描述）
- 本反例：**无 hedge 的因果 claim + 干预推论**

### 6. 修复建议
- 把 "Therefore, X causes Y" 改成 "This suggests that X may be related to Y"
- 把 "interventions targeting X will reduce Y" 改成 "future experimental studies should test whether interventions targeting X reduce Y"
- 加 speculation 标志词（"may" / "could" / "potentially"）

---

## 用法

当用户上传的 Discussion 出现以下情况时引用此例：

1. **用户的 correlational study 推因果** — 引用此例作为反例
2. **用户用 "therefore" / "thus" 但无推理** — 引用此例
3. **用户测试 logic-diagnosis** — 引用此例作为"causal overreach"测试用例

---

## 相关诊断资源

- SKILL.md: Causal Reasoning + 三层结构
- rubric.md: L1 (causal chain), L3 (three-layer structure)
- checklist.md 第 1、3 条
- 与 conventions-diagnosis 的"academic claim 规范"维度交叉