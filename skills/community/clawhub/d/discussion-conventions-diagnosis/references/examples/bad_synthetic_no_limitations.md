# Example: Synthetic — Missing Limitations（缺失局限性段）

## 元数据
- **来源**: Synthetic
- **真实/合成**: synthetic
- **维度**: Conventions（limitations 段完全缺失）
- **类型**: Bad ⭐
- **触发诊断**: conventions-diagnosis 的"limitations 段完整性"

---

## 合成例句（模拟缺失 limitations 的 Discussion）

> *"Our results show that X predicts Y. This is consistent with previous findings (Author A, 2010; Author B, 2015). We contribute to the literature by demonstrating that X is an important predictor of Y. Future studies should explore this relationship in more detail."*

## 问题分析

### 1. 完全没有 limitations 段
- 整段只说：results + literature + contribution + future work
- **缺失 limitations**——这是 Unit 4.2.3 Generic Discussion Model 的必需 move

### 2. "This is consistent with previous findings" 的无差别 confirm
- 没有文献对比的细节
- 没有 alternative explanation
- 没有 limitation 段

### 3. "We contribute" 的过度 confident
- "We contribute" 没有具体内容（贡献了什么？给谁用？怎么用？）
- 这是 Unit 4.2.2 Q&A "Achievement vs Contribution" 警告的**空洞贡献声明**

### 4. Future work 的 vague 模式
- "explore this relationship in more detail" —— 与 `bad_synthetic_vague_future.md` 同问题
- 没说什么 sample / 什么 method / 什么 variable

### 5. 与好例对比
- `good_ebert_2020_limitations_future.md` 中：3 个 limitations + 对应 future work
- 本反例：**0 个 limitations**——这是顶刊最忌讳的写法

### 6. 修复建议（指向好例）
- 加 limitations 段（"First, our study is cross-sectional..."）
- 加 alternative explanation（"Third variables may account for..."）
- 加 future work 具体化（"Studies should test..."）
- 把空洞的 "We contribute" 改成具体的贡献描述

---

## 用法

当用户上传的 Discussion 出现以下情况时引用此例：

1. **用户完全没写 limitations** — 引用此例展示缺失问题
2. **用户的 "future work" 只有 1-2 句** — 引用此例展示完整结构
3. **用户测试 conventions-diagnosis** — 引用此例作为"缺 limitations"测试用例

---

## 相关诊断资源

- SKILL.md: Limitations + Future Work（Unit 4.2.3）
- rubric.md: CO4 (limitations completeness)
- checklist.md 第 4 条
- 这是 conventions 维度的**核心缺失反例**——通常被自动标为 major severity