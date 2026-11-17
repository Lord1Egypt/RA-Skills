# Example: Mechanical Connective Chain（机械连接词堆叠）

## 元数据
- **来源**: Ayanian, A. H., Tausch, N., Acar, Y. G., Da Costa, S., & Kay, M. (2020). Resistance in repressive contexts. *JPSP*, 119(1), 1–27. DOI: 10.1037/pspi0000285
- **论文编号**: 1.4
- **维度**: Cohesion（连接词密度问题 — 机械堆叠）
- **类型**: Bad（相对较弱）⭐⭐
- **触发诊断**: cohesion-diagnosis 的"连接词密度合理性"、"additive connective 过度使用"
- **真实/合成**: real_corpus

---

## 原句（Discussion 第 3 段，关于 fear 情绪的讨论）

> *"It is further notable that the emotion of fear, which previous laboratory-based research has found to be a strong inhibitor of collective action (Miller et al., 2009), did not emerge as a significant predictor of action in the present research and in one study (Turkey) even positively predicted action intentions. While this seems counter-intuitive and inconsistent with theory on the role of emotions in shaping behavior (Dumont, et al. 2003), a number of approaches can account for this finding. According to emotion theory and previous research, fear can sometimes lead to (defensive) aggressive or confrontational action, especially when the opponent is an out-group threatening one's in-group (Simunovic, Mifune, & Yamagishi, 2013; Spanovic, Lickel, Denson, & Petrovic, 2010). **Moreover**, psychological reactance theory argues that infringements on one's freedom can lead to defensive reactions as well as backlash (Brehm & Brehm, 1981), and Witte (1992, 1996) hypothesized that when the perceived threat and perceived efficacy to confront the threat is high, fear would predispose individuals to be more prone to cognitively and deliberately confront the danger. **Furthermore**, these effects might be particularly strong in repressive contexts, since the existence of the group is directly threatened..."*

## 问题分析

### 1. 连续 4 个 additive connective
- **"It is further notable..."** (句首信号词)
- **"Moreover"** (连接前段)
- **"According to emotion theory..."** (引出新观点)
- **"Furthermore"** (继续叠加)

整段都是**additive connectives**——每句话都在"再加一层"，缺乏因果/对比等深层逻辑连接

### 2. 没有清晰的 logical progression
- 句子之间缺乏明确的"为什么是这样"的推理链
- 读者读完不知道作者要把读者带到哪里
- 这是 "mechanical stacking" 的典型症状——**density 高但 variety 低**

### 3. Citation glue 失效
- 5 个 citation (Miller, Dumont, Simunovic, Brehm, Witte) 几乎都是**drop as parenthetical**——没有 "consistent with / in contrast to / extending" 等 relationship word
- 这是同时命中**structure**（literature dump）和 **conventions**（citation 整合）的双重问题

### 4. 与好例的对比
- `good_ayanian_2020_first_second.md` 中："First, we specified a comprehensive predictive model" —— ordinal 模式清晰
- 同篇但本段：纯 additive chain —— 同一作者在不同段落使用的连接策略不同
- 说明**连接词使用是段落级别**的诊断——不是"全篇都用 furthermore"或"全篇都不用"

### 5. 修复建议
- 用因果连接（"because" / "as a result"）替代部分 additive
- 给每个 citation 加 relationship word（"extending X's theory, ..."）
- 在段尾加 wrap（"Taken together, fear's null effect suggests..."）

---

## 用法

当用户上传的 Discussion 出现以下情况时引用此例：

1. **整段都是 "Furthermore / Moreover / Additionally"** — 缺乏连接词 variety → 引用此例展示机械堆叠问题
2. **段落 connective 密度过高** — 单位长度的"Furthermore" 出现 3+ 次 → 引用此例
3. **用户问"我可以用 furthermore 多少次"** — 引用此例说明密度合理性因段而异

---

## 相关诊断资源

- SKILL.md: L1 Connectives（Density check）
- rubric.md: C1 (density), C3 (variety)
- checklist.md 第 6 条（connective variety）