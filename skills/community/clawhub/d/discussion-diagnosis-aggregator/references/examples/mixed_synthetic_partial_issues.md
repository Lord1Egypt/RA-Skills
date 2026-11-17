# Aggregator Example: Mixed — Synthetic Discussion with Partial Issues

## 元数据
- **来源**: Synthetic（教学型聚合器示范）
- **类型**: Mixed（部分好，部分坏）
- **真实/合成**: synthetic

---

## 合成 Discussion 全文（用于示范诊断）

> *(Note: This is a teaching synthetic Discussion. Each paragraph demonstrates different issues for aggregator training.)*

> **段 1**: In this study, we investigated the relationship between X and Y. We found that X correlates with Y (r = .35, p < .001). This is consistent with Author (2010).

> **段 2**: Our results suggest that X may cause Y. Furthermore, X is associated with Y. Moreover, X predicts Y. Furthermore, this suggests that X is important for understanding Y. Furthermore, our findings are novel.

> **段 3**: More research is needed to explore this relationship in more detail.

> **段 4**: Our study has limitations. First, our sample is small. Second, our measure is not perfect. Third, we used a cross-sectional design.

---

## 完整诊断

### 1. Structure: 9 / 20
- S1 Move Coverage: 2/5 — 仅 A 有，B/C/D/F 部分有
- S2 Move Ordering: 1/5 — 严重混乱
- S3 Intro-Discussion Symmetry: 1/5 — 无对称
- S4 Opening Move Quality: 1/5 — "In this study, we..." 反模式
- S5 Take-Home Persistence: 2/5 — take-home 模糊
- S6 Limitations Quality: 3/5 — 3 个但都 generic
- S7 Future Work Specificity: 1/5 — "more research is needed"

### 2. Cohesion: 7 / 20
- C1 Topic Sentence: 1/5 — 段 2 无 topic sentence
- C2 Connective Variety: 1/5 — 全是 "Furthermore"
- C3 Connective Density: 1/5 — 段 2 "Furthermore" 出现 4 次
- C4 Forward Motion: 1/5 — 段 1 = Results 重复
- C5 Narrative Thread: 2/5 — 主线模糊
- C6 Inter-paragraph Transition: 2/5 — 段 3 突然

### 3. Grammar: 14 / 20
- G1 Tense-Claim Alignment: 3/5 — 时态基本对齐
- G2 Tense Consistency: 4/5 — 一致
- G3 Epistemic Stance: 2/5 — "X may cause Y" 用 "may" 但 "X is important" 强 claim
- G4 Modal Verb Forms: 4/5 — 形式基本正确
- G5 Modal Variety: 2/5 — "may" + "more research is needed" 无 modal
- G6 Subject-Verb Agreement: 5/5 — 全正确
- G7 Active/Passive Voice: 4/5 — 主动语态

### 4. Vocabulary: 8 / 20
- V1 Hedging Variety: 2/5 — "may" 为主
- V2 Hedge-Claim Matching: 2/5 — 强 claim（"X is important"）无 hedge
- V3 Cognitive Verb Variety: 1/5 — 全 "suggest" / "consistent with"
- V4 Happy Words: 2/5 — "novel" 1 处
- V5 Field Terminology: 2/5 — 通用词
- V6 In-line Definitions: 1/5 — 全缺
- V7 Statistical Terms: 2/5 — 仅 r 值
- V8 Hedge Precision: 2/5 — 粗略
- V9 Future Work Specificity: 1/5 — "more research is needed"

### 5. Logic: 9 / 20
- L1 Causal Chain: 2/5 — 无 mechanism 层
- L2 Evidence Specificity: 2/5 — 仅 r 值无具体
- L3 Data-Interpretation-Speculation: 2/5 — 三层混乱
- L4 Causal vs Correlational: 2/5 — "X may cause Y"（correlational data）
- L6 Claim-Limitation Balance: 2/5 — pure self-flagellation
- L5 Alternative Explanations: 1/5 — 完全无

### 6. Conventions: 8 / 20
- CO1 Contribution Type: 1/5 — 无显式 claim
- CO2 Happy Words: 2/5 — "novel" 略少
- CO3 Achievement-Contribution: 1/5 — 混合
- CO4 Limitations Completeness: 3/5 — 3 个但 generic
- CO5 Future Work Specificity: 1/5 — vague
- CO6 Operational Specificity: 1/5 — 全 abstract

---

## 总分计算

| 维度 | 权重 | 分数 | 加权 |
|---|---|---|---|
| Structure | 20% | 9/20 | 9.0 |
| Cohesion | 20% | 7/20 | 7.0 |
| Grammar | 10% | 14/20 | 7.0 |
| Vocabulary | 10% | 8/20 | 4.0 |
| Logic | 20% | 9/20 | 9.0 |
| Conventions | 20% | 8/20 | 8.0 |
| **总分** | | | **44.0 / 100** |

**评级**: **Needs Work**（重大问题）

---

## Narrative-Coherence Meta-Score: 3 / 10

**Weak** — Take-home 几乎不可识别。

**Take-home（推测）**: "X 与 Y 相关，可能因果"

**Persistence test**:
- 首段 take-home: ✗ — "In this study, we..." 反模式
- 末段 take-home: ✗ — "More research is needed" 无具体方向
- 中段一致性: ⚠ — 段 2 是堆叠

---

## Severity-Tagged Issue List

### Critical（5 个）

1. **[段 1 - "In this study, we..."]** — Anti-pattern 开篇
   - Flagged by: Structure (S4)
   - Fix: 用 achievement opening（"Our results provide..."）或 reboot
   - Example: `examples/good_midgley_2020_narrative_wrap.md` (Structure)
   - Severity: Critical (opening 位置加权)

2. **[段 2 - "X may cause Y"]** — Causal overreach from correlational data
   - Flagged by: Logic (L4), Vocabulary (V2)
   - Fix: 用 "X may be related to Y" / "X is associated with Y"
   - Example: `bad_synthetic_causal_overreach.md` (Logic)
   - Severity: Critical

3. **[段 2 - 4 个 "Furthermore"]** — Connective density 严重过高
   - Flagged by: Cohesion (C3)
   - Fix: 减少到 1-2 个；增加 causal / contrastive
   - Example: `bad_ayanian_2020_mechanical_chain.md` (Cohesion)
   - Severity: Critical

4. **[段 3 - "More research is needed"]** — Future work 完全 vague
   - Flagged by: Conventions (CO5), Vocabulary (V9), Structure (S7)
   - Fix: 加 what / where / method / variable 4 元素
   - Example: `bad_synthetic_vague_future.md` (Vocabulary)
   - Severity: Critical

5. **[整篇 - 无 achievement/contribution claim]** — 缺失 F move
   - Flagged by: Structure (S1), Conventions (CO1)
   - Fix: 加 contribution statement（说明做了什么 / 对 field 价值）
   - Example: `bad_synthetic_vague_achievement.md` (Conventions)
   - Severity: Critical

### Major（6 个）

6. **[段 2 - 强 claim 无 hedge]** — "X is important" 缺 hedge
7. **[段 1 - 无 topic sentence]** — 直接进入 results
8. **[整篇 - 无 alternative explanations]** — 单一解释
9. **[整篇 - 三层结构混乱]** — Data / Interpretation / Speculation 不分
10. **[段 2 - "novel" 单独使用]** — 缺具体内容
11. **[段 4 - generic limitations]** — "sample is small" 无具体含义

### Minor（8+ 个）
- Modal variety 不足
- Field terminology 缺失
- In-line definitions 缺失
- ...

---

## Top-3 Priority Fixes

1. **[Critical] 重写开篇** — 删除 "In this study, we..." 改为 achievement 或 reboot
2. **[Critical] 修复 causal overreach** — "X may cause Y" → "X is associated with Y"
3. **[Critical] 重写 future work** — 删除 "More research is needed" 改为具体的"未来 5 年研究方向..."

---

## Cross-Dimension Deduplication Notes

合并的 issues:
- Issue 2 被 Logic + Vocabulary 同时标记 → 合并为一条 Critical
- Issue 3 被 Cohesion 标记（独立）
- Issue 4 被 Conventions + Vocabulary + Structure 同时标记 → 合并为一条 Critical（取最高严重度）
- Issue 5 被 Structure + Conventions 同时标记 → 合并为一条 Critical

---

## Strengths（也值得肯定）

- ✅ **没有语法错误**：时态基本对齐，主谓一致
- ✅ **主动语态主导**：没有过度被动
- ✅ **有 r 值**：至少有数据
- ✅ **有 3 个 limitations**（虽然 generic）

---

## Action Plan

### 立即修复（重写整个 Discussion）
1. 重写开篇（删除 "In this study, we..."）
2. 重构段 2（减少 Furthermore，分层）
3. 重写 future work（加具体方向）
4. 加 achievement/contribution claim
5. 加 alternative explanations

### 短期改进
1. 学习本组 6 个 skill 的诊断方法
2. 多读优秀 Discussion 找标杆

### 长期培养
1. 持续写多篇 Discussion
2. 每次投稿前用 aggregator 自检

---

## 相关诊断资源

- 6 个 single-skill SKILL.md
- `output-template.md`
- `severity-rubric.md`
- `cross-dimension-map.md`
- 各维度的 examples/