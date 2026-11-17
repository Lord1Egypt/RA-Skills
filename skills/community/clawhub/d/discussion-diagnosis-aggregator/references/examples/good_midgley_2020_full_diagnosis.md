# Aggregator Example: Good Full Diagnosis（Midgley 2020）

## 元数据
- **来源**: Midgley et al. (2020). When every day is a high school reunion. *JPSP*, 119(2).
- **论文编号**: 1.3
- **类型**: Good（接近投稿水平）
- **真实/合成**: real_corpus

---

## 完整 Discussion 评分（6 维度）

### 1. Structure: 18 / 20
- S1 Move Coverage: 5/5 — A/B/C/D/E/F/G 全有
- S2 Move Ordering: 5/5 — Opening → A → B → C → D → E 清晰
- S3 Intro-Discussion Symmetry: 4/5 — 大部分对称
- S4 Opening Move Quality: 5/5 — Achievement opening（"Taken together, these studies provide..."）
- S5 Take-Home Persistence: 5/5 — "social media comparisons have greater impact" 贯穿
- S6 Limitations Quality: 4/5 — 多个 limitations，部分有反驳
- S7 Future Work Specificity: 4/5 — 具体方向

### 2. Cohesion: 18 / 20
- C1 Topic Sentence: 5/5 — 每段有 claim
- C2 Connective Variety: 4/5 — 多种连接词
- C3 Connective Density: 5/5 — 密度合适
- C4 Forward Motion: 5/5 — 每段推进
- C5 Narrative Thread: 5/5 — 主线清晰
- C6 Inter-paragraph Transition: 4/5 — 段间过渡好

### 3. Grammar: 17 / 20
- G1 Tense-Claim Alignment: 5/5 — 时态精确匹配
- G2 Tense Consistency: 5/5 — 一致
- G3 Epistemic Stance: 4/5 — 大体精确
- G4 Modal Verb Forms: 5/5 — 形式正确
- G5 Modal Variety: 3/5 — "may" 略多
- G6 Subject-Verb Agreement: 5/5 — 全正确
- G7 Active/Passive Voice: 5/5 — 主动语态主导

### 4. Vocabulary: 18 / 20
- V1 Hedging Variety: 5/5 — 多种 hedge
- V2 Hedge-Claim Matching: 4/5 — 多数匹配
- V3 Cognitive Verb Variety: 4/5 — suggest / indicate 等
- V4 Happy Words: 5/5 — 适度
- V5 Field Terminology: 4/5 — 领域术语精准
- V6 In-line Definitions: 3/5 — 部分缺
- V7 Statistical Terms: N/A — 不适用
- V8 Hedge Precision: 4/5 — 较精确
- V9 Future Work Specificity: 4/5 — 较具体

### 5. Logic: 17 / 20
- L1 Causal Chain: 4/5 — 大部分完整
- L2 Evidence Specificity: 4/5 — 多数具体
- L3 Data-Interpretation-Speculation: 5/5 — 三层清晰
- L4 Causal vs Correlational: 4/5 — 区分好
- L5 Alternative Explanations: 3/5 — 部分缺
- L6 Claim-Limitation Balance: 4/5 — 较好平衡

### 6. Conventions: 18 / 20
- CO1 Contribution Type: 5/5 — 3 种 contribution（results / impact / application）
- CO2 Happy Words: 5/5 — 适度
- CO3 Achievement-Contribution: 4/5 — 较清晰
- CO4 Limitations Completeness: 4/5 — 多个具体
- CO5 Future Work Specificity: 4/5 — 4 元素
- CO6 Operational Specificity: 3/5 — 部分 operational

---

## 总分计算

| 维度 | 权重 | 分数 | 加权 |
|---|---|---|---|
| Structure | 20% | 18/20 | 18.0 |
| Cohesion | 20% | 18/20 | 18.0 |
| Grammar | 10% | 17/20 | 8.5 |
| Vocabulary | 10% | 18/20 | 9.0 |
| Logic | 20% | 17/20 | 17.0 |
| Conventions | 20% | 18/20 | 18.0 |
| **总分** | | | **88.5 / 100** |

**评级**: **Good**（接近投稿水平）

---

## Narrative-Coherence Meta-Score: 9 / 10

**Strong** — Take-home 清晰且一致。

**Take-home**: "Social media comparisons are more frequent and more impactful than classic comparison models predict, especially upward comparisons on self-esteem."

**Persistence test**:
- 首段 take-home: ✓ "social media comparisons have changed the ways..."
- 末段 take-home: ✓ "vulnerable groups... implications for health"
- 中段一致性: ✓ 每段都在讨论 social media 的独特性

---

## Severity-Tagged Issue List

### Critical（0 个）
无 critical issues。

### Major（3 个）

1. **[句子 X - 关于 alternative explanations 段]** — 缺少 explicit alternative explanations
   - Flagged by: Logic (L5)
   - Fix: 加 1-2 个 alternative explanations（如 "It is also possible that..."）
   - Example: `good_ebert_2020_alternatives_addressed.md`
   - Severity: Major

2. **[句子 Y - 关于 field terminology 段]** — 缺部分 in-line definitions
   - Flagged by: Vocabulary (V6)
   - Fix: 关键术语首次使用加 "(i.e., ...)"
   - Example: `good_ebert_2020_field_specific_terms.md`

3. **[句子 Z - 关于 future work 段]** — Future work 部分缺 method 具体化
   - Flagged by: Conventions (CO5)
   - Fix: 部分 future work 加具体 method（如 "longitudinal designs"）
   - Example: `good_ebert_2020_limitations_future.md`

### Minor（5+ 个）
- Modal variety 略低（"may" 略多）
- 部分 claim 与 hedge 略弱匹配
- 部分 recommendation 略 abstract
- ...

---

## Top-3 Priority Fixes

1. **[Major] 加 alternative explanations** — 在 Limitations 段附近加 1-2 个 alternative explanations + 反驳证据
2. **[Major] 关键术语加 in-line definition** — 在关键术语首次使用时加 "(i.e., ...)"
3. **[Minor] 增加 modal variety** — 部分 "may" 替换为 "could" / "might" / "should"

---

## Cross-Dimension Deduplication Notes

- V5 + V6 + V9（field terminology + in-line definitions + future work）部分交叉 → 合并到 Major #2
- L1 + L2（causal chain + evidence specificity）相关但独立 → 保持独立

---

## Strengths（也值得肯定）

- ✅ **Outstanding opening**: "Taken together, these studies provide..." — 教科书式 achievement opening
- ✅ **Excellent take-home persistence**: 核心信息贯穿全 Discussion
- ✅ **Strong evidence specificity**: 多数 claim 有具体 evidence（studies 编号 + finding）
- ✅ **Good three-layer structure**: Data / Interpretation / Speculation 边界清晰
- ✅ **Appropriate hedging variety**: 5 种 hedge 形式都有使用

---

## Action Plan

### 立即修复（本次提交前）
1. 加 1-2 个 alternative explanations
2. 关键术语首次使用加 in-line definition

### 短期改进（下次写作时）
1. 增加 modal variety
2. Future work 加具体 method

### 长期培养（持续练习）
1. 在 more studies 中保持 evidence specificity
2. 加深 alternative explanations 的反思

---

## 相关诊断资源

- 6 个 single-skill SKILL.md
- 6 个 rubric.md
- `output-template.md`
- `severity-rubric.md`
- `cross-dimension-map.md`