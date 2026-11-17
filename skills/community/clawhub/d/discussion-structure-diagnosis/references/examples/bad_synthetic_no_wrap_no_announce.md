# Example: Synthetic — No Wrap, No Announcement（典型错误）

## 元数据
- **来源**: Synthetic（教学型合成反例）
- **真实/合成**: synthetic（标注清楚）
- **维度**: Structure（缺 roadmap + 缺 narrative wrap + move 顺序乱）
- **类型**: Bad ⭐
- **触发诊断**: structure-diagnosis 的多重问题（roadmap / wrap / move ordering）

---

## 合成例句（基于常见写作错误构造）

> *"Our results show that people who score high on X also score high on Y. This is interesting because previous studies have found similar results (Author A, 2010; Author B, 2012; Author C, 2015). It would be interesting to see whether these findings extend to other populations, such as adolescents or older adults. The relationship between X and Y might be due to several factors, including genetics, environment, and lifestyle. Future studies should explore this question further."*

## 问题分析（多重结构问题）

### 1. 没有开篇 roadmap
- 第一句直接说"our results show..."，**没有预告后续要讲什么**
- 读者不知道接下来会讨论 literature、limitations、implications 还是 future work
- 违反 Unit 4.2.2 的 "opening move" 模式

### 2. Citation 链再次出现（"前人研究堆叠"）
- "(Author A, 2010; Author B, 2012; Author C, 2015)" —— **没有 relationship word**
- 这是与 `bad_midgley_2020_literature_dump.md` 同模式的 citation 整合问题

### 3. 没有 narrative wrap
- 整个段落没有"in sum / taken together / overall"
- 段与段之间无衔接词（"first / second / third"）
- 段落只是简单"罗列要点"，不是"叙事推进"

### 4. Move 顺序混乱
- 第一句：results（Move A）✓
- 第二句：literature（Move B）✓
- 第三句：**future work / other populations**（Move E）—— 这就跳过了 implications、limitations、contribution！
- 第四句：**机制推测**（causal speculation）—— 应该在 Move B 之后
- 第五句：**future studies should explore**——再次 future work

**正确的顺序应是**：achievement → results → literature → implications → limitations → future work → closing

### 5. 没有 contribution statement
- 整段没有"first / new / novel / we demonstrate" 等 contribution 信号词
- 违反了 Unit 4.2.2 "Achievement vs Contribution" 区分

### 6. "Future studies should explore this question" 是 weakness
- 这是 Unit 4.4 / 4.5 警告的"vague future work"
- "should explore this question further" 是非具体、敷衍的 future direction
- 应该是 "future studies should examine X in Y population using Z method"

---

## 用法

当用户上传的 Discussion 出现以下情况时引用此例（**作为多个问题的复合反例**）：

1. **Discussion 整体结构散乱** — 缺 roadmap + 缺 wrap + move 顺序乱 → 引用此例展示全错是什么样子
2. **用户问"我的 Discussion 结构对不对"** — 引用此例作为"反面教材"，让用户对比自查

---

## 修复建议（指向 4 个 good example）

要把这段改成 good example，参考：

1. **加开篇 roadmap** —— 参考 `good_costello_2021_announce_moves.md` 的"In the following sections, we..."
2. **加 achievement statement** —— 参考 `good_marsh_2018_achievement_reboot.md` 的"one of the most comprehensive..."
3. **citation 加 relationship word** —— 参考 `good_midgley_2020_narrative_wrap.md` 的"would predict...however, I demonstrate..." 对比结构
4. **move 顺序重新排列** —— 参考 `good_schmidt_2016_method_structured.md` 的清晰 sub-section 结构
5. **future work 具体化** —— "Future studies using Z method with Y population could examine whether..." 而不是"explore this question further"

---

## 相关诊断资源

- SKILL.md: 整体结构完整性检查（所有诊断点）
- rubric.md: 所有项（S1-S7）
- checklist.md: 大部分条目都会命中
- 这是"全维度红旗"型反例——同时也是 aggregator 的优先级测试样本