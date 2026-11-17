# Cross-Dimension Map — 跨维度问题合并规则

## 用途
本文件是 `discussion-diagnosis-aggregator` 合并多维度 issue 的官方标准。

当同一个 issue 被多个维度同时标记时，aggregator 应**合并为一条**，避免重复报告。

---

## 合并规则

### Rule 1: 同一现象从不同视角被标记 → 合并

例子："We prove that X causes Y"
- Vocabulary 标记：V2 hedge-claim 不匹配（prove 是 over-claim）
- Logic 标记：L4 causal vs correlational boundary（causal overreach）
- **合并为一条**：Critical issue — "Over-claim + causal overreach"

### Rule 2: 严重度取最高

参见 `severity-rubric.md` 的"跨维度 issue 的严重度"。

### Rule 3: 修复建议只给一次

合并后的 issue 应给**一个综合的修复建议**，不是多个独立的修复建议。

---

## 常见的跨维度 issue 模式

### 模式 1: Over-claim × Causal Overreach

| 触发维度 | 标记 | 严重度 |
|---|---|---|
| Vocabulary | "prove" / "definitely show" / "without a doubt" | Critical |
| Logic | Correlational study claim 因果 | Critical |

**合并后**: Critical — "Over-claim in causal claim"

**合并修复**:
- 用 "suggest" / "indicate" 替代 "prove"
- 加 modal verb（may / might / could）
- 加 "correlational" / "cross-sectional" 限定

**指向 example**: `bad_synthetic_causal_overreach.md`

---

### 模式 2: Modal Form × Hedging

| 触发维度 | 标记 | 严重度 |
|---|---|---|
| Grammar | "should looks"（modal 形式错）| Major |
| Vocabulary | Modal variety 不足 | Minor |

**合并后**: Major — "Modal verb 形式错 + 单一 modal"

**合并修复**:
- 修正 modal + bare infinitive 形式
- 增加 modal variety

**指向 example**: `good_epskamp_2018_modal_present.md` (Grammar)

---

### 模式 3: Tense × Cognitive Verb

| 触发维度 | 标记 | 严重度 |
|---|---|---|
| Grammar | 时态错位 | Major |
| Vocabulary | cognitive verb 选词不精确 | Minor |

**合并后**: Major — "Tense 与 epistemic stance 不匹配"

**合并修复**:
- 时态反映 claim 强度
- cognitive verb 选词精确

**指向 example**: `good_midgley_2020_tense_alignment.md` (Grammar) + `good_schmidt_2016_cognitive_verbs.md` (Vocabulary)

---

### 模式 4: Limitations Missing × Conventions

| 触发维度 | 标记 | 严重度 |
|---|---|---|
| Structure | D move 缺失 | Critical |
| Conventions | CO4 limitations 缺失 | Critical |

**合并后**: Critical — "Limitations 段完全缺失"

**合并修复**:
- 加 Limitations 段（3 元素：First / Second / Third）

**指向 example**: `good_ebert_2020_limitations_future.md` (Conventions) + `good_ayanian_2020_limitation_rebuttal.md` (Structure)

---

### 模式 5: Happy Words × Contribution Type

| 触发维度 | 标记 | 严重度 |
|---|---|---|
| Vocabulary | happy words 堆叠 | Major |
| Conventions | contribution claim 模糊 | Major |

**合并后**: Major — "Happy words 替代了具体 contribution"

**合并修复**:
- 用具体 achievement 替代 happy words
- 描述具体 contribution（method / results / impact / application）

**指向 example**: `bad_synthetic_vague_achievement.md` + `good_costello_2021_contribution_language.md`

---

### 模式 6: Topic Sentence × Forward Motion

| 触发维度 | 标记 | 严重度 |
|---|---|---|
| Cohesion | C1 topic sentence 缺失 | Major |
| Cohesion | C4 forward motion 缺失 | Major |

**合并后**: Major — "Discussion 像 Results 精简版"

**合并修复**:
- 每段加 topic sentence（claim 而非 results 复述）
- 加 "so what" 推进

**指向 example**: `bad_synthetic_abrupt_transitions.md` + `good_ayanian_2020_first_second.md`

---

### 模式 7: Connective Density × Narrative Thread

| 触发维度 | 标记 | 严重度 |
|---|---|---|
| Cohesion | C3 connective density 过高 | Minor |
| Cohesion | C5 narrative thread 弱 | Major |

**合并后**: Major — "高密度 connective 反映 narrative thread 弱"

**合并修复**:
- 减少 additive connective（Furthermore）
- 增加 causal / contrastive connective
- 用因果连接替代堆叠

**指向 example**: `bad_ayanian_2020_mechanical_chain.md` + `good_costello_2021_unpack_sequence.md`

---

### 模式 8: Alternative Explanations × Claim-Limitation Balance

| 触发维度 | 标记 | 严重度 |
|---|---|---|
| Logic | L5 alternative 缺失 | Major |
| Logic | L6 claim-limitation 不平衡 | Major |

**合并后**: Major — "Alternative 与 limitation 处理不完整"

**合并修复**:
- 加 alternative explanation + 反驳证据
- Limitations 后立即有 claim balance

**指向 example**: `bad_synthetic_ignoring_alternatives.md` + `good_ebert_2020_alternatives_addressed.md`

---

## 合并决策树

```
Issue 被标记
├── 几个维度? 
│   ├── 1 个 → 不合并
│   └── 2+ 个 → 合并
├── 严重度?
│   ├── 取最高严重度
│   └── 位置加权（opening/closing → +1 级）
└── 修复?
    ├── 综合 1 个修复建议
    └── 指向 1 个最相关 example
```

---

## 不应合并的情况

以下情况即使被多维度标记也应**保持独立**：

1. **同一句话有 2 个不同问题**（如 "should looks" 同时是 modal 形式错 + tense 不一致）
   - 实际: 这种情况通常 1 个修复就能解决，应合并
2. **同一段的不同句子被不同维度标记**
   - 实际: 应作为同一段的多 issue 处理（不合并但位置相同）
3. **take-home 丢失**（Cohesion）+ **核心 claim over-claim**（Vocabulary/Logic）
   - 实际: 应合并，因为修复 take-home 通常也修复 over-claim

---

## 合并示例（完整流程）

**输入**:
- Grammar: G1 — "We prove that X causes Y" 时态错位
- Vocabulary: V2 — "prove" 是 over-claim
- Logic: L4 — Correlational study claim 因果

**合并过程**:
1. 3 个维度都标记同一句子 → 合并
2. 严重度：3 个都是 Critical → 取 Critical
3. 修复建议：综合 3 维度的修复
4. Example: 指向 `bad_synthetic_causal_overreach.md`

**输出**:
```markdown
### Critical
1. **[句子 3]** — "We prove that X causes Y"
   - Flagged by: Grammar, Vocabulary, Logic (3 个维度)
   - Severity: Critical
   - Fix: 用 "suggest" 替代 "prove"; 加 modal verb; 加 correlational 限定
   - Example: `references/examples/bad_synthetic_causal_overreach.md`
```

---

## 相关文件

- `severity-rubric.md` — 严重度判定
- `output-template.md` — 报告模板（含 Cross-Dimension Deduplication Notes 段）
- `examples/` — 正反例对照（每维度都有）