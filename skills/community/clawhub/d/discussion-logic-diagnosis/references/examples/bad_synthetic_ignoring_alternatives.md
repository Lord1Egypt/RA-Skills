# Example: Synthetic — Ignoring Alternative Explanations（忽略替代解释）

## 元数据
- **来源**: Synthetic
- **真实/合成**: synthetic
- **维度**: Logic（alternative explanations 缺失）
- **类型**: Bad ⭐
- **触发诊断**: logic-diagnosis 的"反方观点处理完整性"

---

## 合成例句

> *"Our results clearly show that X causes Y. The mechanism is straightforward: X activates brain regions related to Y, which in turn leads to Y. Future research should explore this mechanism in more detail."*

## 问题分析

### 1. 单一解释，无替代
- 只给了 1 个 mechanism（"X activates brain regions related to Y"）
- 没考虑 alternative：可能是 Z 介导？可能是 reverse causation？可能是 confound？
- 这是**单元化的逻辑论证**——缺乏批判性

### 2. "The mechanism is straightforward" 的过度 confident
- 学术英语中很少说"the mechanism is straightforward"
- 顶刊论文即使有强 claim，也通常用 "may operate through" / "is consistent with"
- 这种 confident expression 是 Unit 4.2.2 Q&A 警告的

### 3. Future work 模糊
- "explore this mechanism in more detail" —— vague
- 没说什么 sample / 什么 method / 什么 variable
- 与 `bad_synthetic_vague_future.md` 同模式

### 4. 与好例对比
- `good_ebert_2020_alternatives_addressed.md` 中：acknowledged limitation + 呈现替代解释 + 反驳替代解释
- `good_schmidt_2016_honest_limitation.md` 中：honest limitation + 立即 claim balance
- 本反例：**单一解释 + 无 alternative**——典型反例

### 5. 修复建议（指向好例）
- 加 2-3 个 alternative explanations
- 对每个 alternative 给出反驳证据（或承认需要 future research）
- 把 "the mechanism is straightforward" 改成 "the mechanism may involve X" 
- 把 "explore this mechanism in more detail" 改成具体的 future study 设计

---

## 用法

当用户上传的 Discussion 出现以下情况时引用此例：

1. **用户只给一个解释** — 引用此例展示 alternative coverage 缺失
2. **用户用 confident mechanism 语言** — 引用此例
3. **用户测试 logic-diagnosis** — 引用此例作为"alternative 缺失"测试用例

---

## 相关诊断资源

- SKILL.md: Alternative Explanations Handling（Unit 4.2.2 Q&A）
- rubric.md: L5 (alternative explanations coverage)
- checklist.md 第 5 条
- 与 conventions-diagnosis 的 limitations 维度交叉