# Example: Synthetic — Abrupt Transitions（段间断裂）

## 元数据
- **来源**: Synthetic（教学型合成反例）
- **真实/合成**: synthetic
- **维度**: Cohesion（段间断裂 — 缺少 topic sentence + 缺过渡信号）
- **类型**: Bad ⭐
- **触发诊断**: cohesion-diagnosis 的"段间衔接"、"topic sentence 缺失"

---

## 合成例句（4 个段落，模拟段间断裂）

> **段落 1**: Studies 1-5 demonstrated that social media use is associated with upward social comparisons. We found that frequency of upward comparisons was related to lower self-esteem (Study 3).
>
> **段落 2**: The Stroop asymmetry was replicated in our data. Power curves for stimulus-response binding fit the PEP model predictions.
>
> **段落 3**: Our network analysis using LASSO regularization identified a sparse partial correlation network. The edges between depression symptoms and sleep quality were consistent with previous findings.
>
> **段落 4**: Limitations include the cross-sectional nature of the data. Future studies should use longitudinal designs.

## 问题分析

### 1. 段间无任何过渡信号
- 段落 1 → 段落 2：从"social media"突然跳到"Stroop asymmetry"——**主题断裂**
- 段落 2 → 段落 3：从"PEP model"突然跳到"network analysis"——**完全不同论文的话题**
- 段落 3 → 段落 4：从"结果描述"突然跳到"limitations"——**没有任何 wrap**

### 2. 缺失 topic sentence
- 每段第一句直接进入结果细节，没有"X happens" 或 "We now turn to..." 的导航
- 段落 1 第一句"Studies 1-5 demonstrated..."——这是**Results 的重复**，不是 Discussion 的 claim
- 段落 4 第一句"Limitations include..."——这是 generic statement，缺乏 context

### 3. Discussion 与 Results 重叠
- "Studies 1-5 demonstrated..."（段落 1）——这是 Results 的写法
- "The Stroop asymmetry was replicated..."（段落 2）——也是 Results 重复
- 段落 3 类似
- **整段 Discussion 几乎只是 Results 的精简版**

### 4. 缺乏 forward motion
- 没有"so what"——读者不知道作者要把读者带到哪里
- 段落 1 说"social media → self-esteem"——但没说"这意味着什么"
- 段落 4 直接跳到 limitations——前面没有"in sum"的 wrap

### 5. 对照好例
- `good_midgley_2020_sequential_connectives.md` 用 "First / Second / Third" 显式 ordinal 串联
- `good_costello_2021_unpack_sequence.md` 用开篇 roadmap
- 本反例**完全相反**——没有任何段间信号

---

## 用法

当用户上传的 Discussion 出现以下情况时引用此例：

1. **Discussion 像 Results 的精简版** — 段间无新的 claim 推进 → 引用此例展示什么是"Discussion vs Results 重叠"
2. **段间主题断裂** — 段落之间无任何衔接 → 引用此例展示段间断裂问题
3. **用户问"我的 Discussion 段间衔接够吗"** — 引用此例作为"全错"反面教材

---

## 修复建议（指向 4 个 good example）

要把这段改成 good example，参考：

1. **加段间 topic sentence** —— 每段第一句是 claim 而非 results 重复
2. **加段间过渡信号** —— "Building on this, ..." / "Turning to the methodological implications, ..."
3. **Discussion 段不重复 Results** —— 应"interpret"而非"re-state"
4. **加 in-sum / taken together 段** —— 在 limitations 前先做 wrap

参考 `good_midgley_2020_sequential_connectives.md` 的 ordinal 模式 + `good_costello_2021_unpack_sequence.md` 的 roadmap 模式。

---

## 相关诊断资源

- SKILL.md: L1 Topic sentence + L2 Forward motion
- rubric.md: C4 (forward motion), C5 (narrative thread)
- checklist.md 第 3、5 条
- 这是**cohesion 维度的"全错"代表**——同时也是 structure 反例（Discussion vs Results 重叠）