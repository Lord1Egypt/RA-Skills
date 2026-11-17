# Aggregator Example: Bad — Synthetic Full Failure

## 元数据
- **来源**: Synthetic（教学型聚合器示范）
- **类型**: Bad（几乎所有维度都有 critical 问题）
- **真实/合成**: synthetic

---

## 合成 Discussion 全文（最差示范）

> **段 1**: We found X correlates with Y. Our results are groundbreaking and unprecedented. We prove that X causes Y. This novel discovery revolutionizes the field. We hope this research will inspire future work. **More research is needed.**

> **段 2**: We tested whether X causes Y. We found that X correlates with Y. **Therefore**, X causes Y. We suggests that interventions targeting X will reduce Y. More research is needed.

---

## 完整诊断

### 1. Structure: 4 / 20
- S1 Move Coverage: 1/5 — 仅 A 部分，无 B/C/D/F/G
- S2 Move Ordering: 1/5 — 完全无序
- S3 Intro-Discussion Symmetry: 0/5 — 无对称（无 Intro 可对照）
- S4 Opening Move Quality: 1/5 — "We found X correlates..." 直接进入 results
- S5 Take-Home Persistence: 1/5 — take-home 模糊
- S6 Limitations Quality: 0/5 — **无 limitations 段**
- S7 Future Work Specificity: 0/5 — "More research is needed" 单独成段

### 2. Cohesion: 4 / 20
- C1 Topic Sentence: 1/5 — 无 topic sentence
- C2 Connective Variety: 1/5 — 仅 "Therefore"
- C3 Connective Density: 1/5 — 无连接词堆叠（因为太短）
- C4 Forward Motion: 1/5 — 不推进
- C5 Narrative Thread: 0/5 — 无主线
- C6 Inter-paragraph Transition: 0/5 — 段间无过渡

### 3. Grammar: 8 / 20
- G1 Tense-Claim Alignment: 2/5 — "We found... prove" 时态乱
- G2 Tense Consistency: 2/5 — "tested / found / causes" 乱
- G3 Epistemic Stance: 1/5 — "prove" 完全无 epistemic
- G4 Modal Verb Forms: 1/5 — "We suggests"（错）
- G5 Modal Variety: 0/5 — 无 modal
- G6 Subject-Verb Agreement: 1/5 — "We suggests"（错）
- G7 Active/Passive Voice: 4/5 — 主动语态（这点反而对）

### 4. Vocabulary: 3 / 20
- V1 Hedging Variety: 0/5 — **无 hedge**
- V2 Hedge-Claim Matching: 0/5 — 全 strong claim 无 hedge
- V3 Cognitive Verb Variety: 1/5 — 仅 "found" / "suggests"
- V4 Happy Words: 1/5 — **happy words 堆叠**（"groundbreaking unprecedented novel revolutionize"）
- V5 Field Terminology: 1/5 — 通用词
- V6 In-line Definitions: 0/5 — 全缺
- V7 Statistical Terms: 0/5 — 无统计
- V8 Hedge Precision: 0/5 — 无 hedge
- V9 Future Work Specificity: 0/5 — "More research is needed"

### 5. Logic: 2 / 20
- L1 Causal Chain: 1/5 — 无 mechanism
- L2 Evidence Specificity: 1/5 — 无 evidence
- L3 Data-Interpretation-Speculation: 1/5 — 三层混乱
- L4 Causal vs Correlational: 0/5 — **causal overreach**（correlational 推因果）
- L5 Alternative Explanations: 0/5 — **无 alternative**
- L6 Claim-Limitation Balance: 0/5 — 无 limitation 段

### 6. Conventions: 2 / 20
- CO1 Contribution Type: 1/5 — 模糊 claim
- CO2 Happy Words: 0/5 — **happy words 堆叠**
- CO3 Achievement-Contribution: 1/5 — 混合
- CO4 Limitations Completeness: 0/5 — **无 limitations**
- CO5 Future Work Specificity: 0/5 — vague
- CO6 Operational Specificity: 0/5 — 全 abstract

---

## 总分计算

| 维度 | 权重 | 分数 | 加权 |
|---|---|---|---|
| Structure | 20% | 4/20 | 4.0 |
| Cohesion | 20% | 4/20 | 4.0 |
| Grammar | 10% | 8/20 | 4.0 |
| Vocabulary | 10% | 3/20 | 1.5 |
| Logic | 20% | 2/20 | 2.0 |
| Conventions | 20% | 2/20 | 2.0 |
| **总分** | | | **17.5 / 100** |

**评级**: **Critical**（重写 Discussion）

---

## Narrative-Coherence Meta-Score: 1 / 10

**Weak** — 无 take-home。

**Take-home（推测）**: "X causes Y, groundbreaking discovery"

**Persistence test**:
- 首段 take-home: ⚠ — "groundbreaking" 无具体内容
- 末段 take-home: ✗ — "More research is needed" 无方向
- 中段一致性: ✗ — 完全无逻辑

---

## Severity-Tagged Issue List

### Critical（10+ 个）

1. **[段 1 - "We prove that X causes Y"]** — Over-claim + causal overreach
   - Flagged by: Vocabulary (V2), Logic (L4), Conventions (CO2)
   - Fix: 用 "suggest" + 加 correlational 限定
   - Example: `bad_synthetic_causal_overreach.md`
   - Severity: Critical

2. **[段 1 - "groundbreaking unprecedented novel revolutionize"]** — Happy words 堆叠
   - Flagged by: Vocabulary (V4), Conventions (CO2)
   - Fix: 删除 happy words；用具体 contribution 替代
   - Example: `bad_synthetic_vague_achievement.md`
   - Severity: Critical

3. **[段 1 - "We hope..."]** — 非学术表达
   - Flagged by: Vocabulary (V3), Conventions (CO1)
   - Fix: 用 "We expect" / "We anticipate"
   - Severity: Critical

4. **[段 1 + 段 2 - "More research is needed"]** — Future work vague
   - Flagged by: Vocabulary (V9), Conventions (CO5), Structure (S7)
   - Fix: 加 what / where / method / variable
   - Example: `bad_synthetic_vague_future.md`
   - Severity: Critical

5. **[整篇 - 无 limitations 段]** — 缺失 D move
   - Flagged by: Structure (S1), Conventions (CO4)
   - Fix: 加 limitations 段
   - Example: `bad_synthetic_no_limitations.md`
   - Severity: Critical

6. **[段 2 - "We suggests"]** — Subject-verb agreement 错误
   - Flagged by: Grammar (G6)
   - Fix: "We suggest" 或 "It suggests"
   - Severity: Critical (load-bearing claim)

7. **[段 2 - "Therefore"]** — 无推理过程的逻辑飞跃
   - Flagged by: Logic (L4)
   - Fix: 删除 "Therefore" 或加推理
   - Severity: Critical

8. **[段 2 - "interventions targeting X will reduce Y"]** — Intervention overreach
   - Flagged by: Logic (L4)
   - Fix: "future experimental studies should test..."
   - Severity: Critical

9. **[整篇 - 无 alternative explanations]** — 单一解释
   - Flagged by: Logic (L5)
   - Fix: 加 alternative
   - Example: `bad_synthetic_ignoring_alternatives.md`
   - Severity: Critical

10. **[整篇 - 无 achievement/contribution claim 实质]** — F move 缺失
    - Flagged by: Structure (S1), Conventions (CO1)
    - Fix: 加具体 contribution
    - Example: `bad_synthetic_vague_achievement.md`
    - Severity: Critical

### Major（10+ 个）
- 无 topic sentence
- 无 hedge
- 三层结构混乱
- 无 intro-discussion 对称
- ...

### Minor（多个）
- 时态细节
- Modal 缺失
- ...

---

## Top-3 Priority Fixes

1. **[Critical] 删除 happy words + 用具体 contribution 替代** — "groundbreaking unprecedented novel revolutionize" 全部删除
2. **[Critical] 修复 causal overreach** — "We prove that X causes Y" → "Our results suggest that X is associated with Y"
3. **[Critical] 加 limitations 段 + 具体 future work** — 不止"More research is needed"

---

## Cross-Dimension Deduplication Notes

合并的 issues:
- Issue 1 被 3 个维度标记 → 合并 Critical
- Issue 2 被 2 个维度标记 → 合并 Critical
- Issue 4 被 3 个维度标记 → 合并 Critical
- Issue 5 被 2 个维度标记 → 合并 Critical
- Issue 10 被 2 个维度标记 → 合并 Critical

总共10+ Critical issues，但合并后为 ~7 个独立 Critical issues

---

## Strengths（几乎没有）

- ✅ **没有过度被动语态**（这反而是仅有的亮点）
- ✅ **使用了"Therefore"作为逻辑连接**（虽然用错了，但至少有连接意图）

---

## Action Plan

### 立即修复（重写整个 Discussion）
1. 重写开篇（去除 "groundbreaking"）
2. 修复 causal overreach
3. 加 limitations 段
4. 加 specific future work
5. 加 alternative explanations
6. 修复 grammar（"We suggests" 等）

### 这段 Discussion 建议完全重写
不要试图修补——它有 10+ 个 critical issues，重写比修改更有效。

### 长期培养
1. 学习本组 6 个 skill 的诊断方法
2. 多读顶刊 Discussion 学习最佳实践
3. 写作时使用 aggregator 自检

---

## 相关诊断资源

- 6 个 single-skill SKILL.md
- `output-template.md`
- `severity-rubric.md`
- `cross-dimension-map.md`
- 各维度的 examples/