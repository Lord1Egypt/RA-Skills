# Example: Literature Dump（相对较弱 — 同篇对比）

## 元数据
- **来源**: 同 `good_midgley_2020_narrative_wrap.md` 同一论文（Midgley 2020）
- **论文编号**: 1.3
- **维度**: Structure（叙事推进缺失 / Literature dump 段）
- **类型**: Bad（相对较弱）⭐⭐
- **触发诊断**: structure-diagnosis 的"段落是否推进 narrative"、"是否每段都有 in-sum 整合"
- **真实/合成**: real_corpus（同篇论文内的"相对较差"段落）

---

## 原句（Discussion 第 6 段，对应 narrative wrap 段之前的过渡段）

> *"These studies also provide significant new insights into social comparison processes more generally. In past research, investigators typically have examined the outcome of a single comparison, or have compared an upward to a downward comparison on various outcomes such as self-evaluation (e.g., Gibbons & Gerrard, 1989; Lockwood & Kunda, 1999; Morse & Gergen, 1970), motivation (e.g., Lockwood & Kunda, 1997; Lockwood, Marshall, & Sadler, 2005; Lockwood & Pinkus, 2008) and affect (e.g., Buunk et al., 1990; Salovey & Rodin, 1984). In the present studies, I was able to test the cumulative effects of a series of comparisons, examining the relative impact of multiple upward and downward comparisons on self-evaluations, life satisfaction, and mood."*

## 问题分析

### 1. 缺乏 narrative 推进
- 这段开头说"provide significant new insights"——但**没有立刻说明"什么 insight"**
- 紧跟的是一个**罗列前人研究的清单**（Gibbons 1989, Lockwood 1999, Morse 1970, ...）——这是典型的 **literature dump**
- **整段没有"so what"**：看完这段，读者不知道作者要 argument 什么

### 2. Citation 链断裂
- 6 个 citation 一口气列出（Gibbons、Gerrard、Lockwood、Kunda、Morse、Gergen、Buunk、Salovey、Rodin）—— 但**没有 relationship word** 解释每个 citation 与论点关系
- 这是 cohesion-diagnosis 也会命中的问题（**citation 整合生硬**）

### 3. 没有 narrative wrap 信号
- 这段结尾直接进入下一段（"My studies suggest..."），**没有 in-sum 整合**
- 与同论文第 7 段（"In sum, these studies provide..."）形成**强对比**

### 4. Take-home 不明确
- 读完这段不知道"the cumulative effect is X"——take-home 延迟到下一段才说
- 违反 Unit 4.1.1 "Wrapping the discussion in a narrative"——narrative 应该是**向前推进**而非**背景铺垫**

### 5. 对比同篇好例
- 同论文第 7 段（`good_midgley_2020_narrative_wrap.md`）开头就是 "In sum"，立刻收束 → 形成对比
- 这就是为什么同一篇顶刊论文里，**好/坏段落可以并存**——为我们的反例提供真实可信的来源

---

## 用法

当用户上传的 Discussion 出现以下情况时引用此例：

1. **段落以"past research shows..."开头** — 缺少 narrative 推进 → 引用此例展示什么是 literature dump
2. **段落内连续引用 5+ citation** — 没有 relationship word → 引用此例展示 citation 整合问题
3. **take-home 延迟到第 3 段才出现** — 违反"narrative forward motion"原则 → 引用此例

---

## 修复建议（指向 good example）

要把这段改成 good example：

1. **去掉 citation 链的"清单"模式** —— 用 "consistent with..."、"in contrast to..."、"extending..." 等 relationship word 整合每个 citation
2. **加 in-sum 段** —— 在段尾或下段开头用"in sum / taken together / overall" 等显式 wrap
3. **把 take-home 提前** —— 第一句就直接说"these studies show X"，而非"provide new insights"

参考同论文第 7 段（`good_midgley_2020_narrative_wrap.md`）作为修复目标。

---

## 相关诊断资源

- SKILL.md: "Forward motion" 检查
- rubric.md: S2 (narrative wrap), S7 (citation integration)
- 同时也是 cohesion-diagnosis 的反例（citation glue）