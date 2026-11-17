# Example: Synthetic — Vague Future Work（模糊的未来研究方向）

## 元数据
- **来源**: Synthetic
- **真实/合成**: synthetic
- **维度**: Vocabulary（future work 表达的精确度）
- **类型**: Bad ⭐
- **触发诊断**: vocabulary-diagnosis 的"future work 表达规范"、"vague language"

---

## 合成例句

> *"**More research is needed** to better understand the relationship between X and Y. **Future studies should explore** this question in more detail. **It would be interesting** to see whether these findings extend to other populations, such as adolescents or older adults. **Further investigation** is required to fully understand the mechanisms underlying this effect."*

## 问题分析

### 1. 5 种典型 vague future work
| 表达 | 问题 |
|---|---|
| "more research is needed" | generic, 无具体方向 |
| "explore this question in more detail" | "this question" 无所指 |
| "it would be interesting to see whether" | "interesting" 太弱；"whether" 无具体 hypothesis |
| "future studies should" + 无具体方法 | 没说用什么方法 |
| "further investigation is required" | "required" 显得武断；"fully understand" 过于笼统 |

### 2. 没有具体的方法/样本/变量
- 没说什么 sample（adolescents? older adults? clinical?）
- 没说什么 method（longitudinal? experimental? meta-analysis?）
- 没说什么 variable（mechanism? moderator?）

### 3. Unit 4.4.2 警告的"vague language"
- "explore" —— vague verb
- "investigate" —— vague verb
- "understand" —— vague verb
- "examine" —— vague verb（如果无具体说明）
- 这 4 个 verb 占满了整段 future work

### 4. 与好例对比
- `good_schmidt_2016_cognitive_verbs.md` 中：future work 有具体方法（"Simulation 7 will..."）
- `good_midgley_2020_hedging_variety.md` 中：future work 有具体方向
- 本反例：**全 vague**——典型反例

### 5. 修复建议（指向好例）
- 把 "more research is needed" 改成 "future studies using longitudinal designs could examine whether..."
- 把 "explore this question" 改成具体的 hypothesis
- 把 "interesting" 改成 "theoretically informative"
- 加具体 sample / method / variable

---

## 用法

当用户上传的 Discussion 出现以下情况时引用此例：

1. **用户的 future work 段太短** — "More research is needed" 单句结束 → 引用此例展示扩展模式
2. **用户的 future work 全 vague** — 没有具体 sample/method → 引用此例
3. **用户测试 vocabulary-diagnosis** — 引用此例作为"未来方向模糊"测试用例

---

## 相关诊断资源

- SKILL.md: Future Work Expressions（Unit 4.4.2）
- rubric.md: V9 (future work specificity)
- checklist.md 第 7 条
- 与 conventions-diagnosis 的 future work 规范维度交叉