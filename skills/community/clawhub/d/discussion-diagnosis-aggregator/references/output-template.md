# Aggregator Output Template — 完整诊断报告模板

## 用途
本文件是 `discussion-diagnosis-aggregator` 的官方输出模板。**直接复制下面的 markdown 到你的报告**。

---

## 模板

```markdown
# Discussion Diagnostic Report

> **论文标题**: [论文标题]
> **作者**: [作者]
> **诊断日期**: YYYY-MM-DD
> **诊断范围**: Discussion 章节（XXX 字）
> **诊断员**: [你的名字 / 自动化工具名]

---

## Overall Score: XX / 100

| 评级 | 评级描述 |
|---|---|
| **Excellent** (90-100) | 接近投稿水平 |
| **Good** (75-89) | 小幅修改可投稿 |
| **Acceptable** (60-74) | 需要结构性修改 |
| **Needs Work** (40-59) | 重大问题 |
| **Critical** (<40) | 重写 Discussion |

### 加权明细
| 维度 | 权重 | 分数 | 加权分 |
|---|---|---|---|
| Structure | 20% | XX / 20 | XX |
| Cohesion | 20% | XX / 20 | XX |
| Grammar | 10% | XX / 20 | XX |
| Vocabulary | 10% | XX / 20 | XX |
| Logic | 20% | XX / 20 | XX |
| Conventions | 20% | XX / 20 | XX |
| **总计** | **100%** | — | **XX / 100** |

---

## Per-Dimension Scores

### 1. Structure（结构完整性）：XX / 20
- **S1 Move Coverage**: X / 5
- **S2 Move Ordering**: X / 5
- **S3 Intro-Discussion Symmetry**: X / 5
- **S4 Opening Move Quality**: X / 5
- **S5 Take-Home Persistence**: X / 5
- **S6 Limitations Quality**: X / 5
- **S7 Future Work Specificity**: X / 5

### 2. Cohesion（连接与衔接）：XX / 20
- **C1 Topic Sentence**: X / 5
- **C2 Connective Variety**: X / 5
- **C3 Connective Density**: X / 5
- **C4 Forward Motion**: X / 5
- **C5 Narrative Thread**: X / 5
- **C6 Inter-paragraph Transition**: X / 5

### 3. Grammar（语法）：XX / 20
- **G1 Tense-Claim Alignment**: X / 5
- **G2 Tense Consistency**: X / 5
- **G3 Epistemic Stance**: X / 5
- **G4 Modal Verb Forms**: X / 5
- **G5 Modal Variety**: X / 5
- **G6 Subject-Verb Agreement**: X / 5
- **G7 Active/Passive Voice**: X / 5

### 4. Vocabulary（学术词汇）：XX / 20
- **V1 Hedging Variety**: X / 5
- **V2 Hedge-Claim Matching**: X / 5
- **V3 Cognitive Verb Variety**: X / 5
- **V4 Happy Words Appropriateness**: X / 5
- **V5 Field-Specific Terminology**: X / 5
- **V6 In-line Definitions**: X / 5
- **V7 Statistical/Methodological Terminology**: X / 5
- **V8 Hedge Precision**: X / 5
- **V9 Future Work Specificity**: X / 5

### 5. Logic（逻辑推理）：XX / 20
- **L1 Causal Chain Completeness**: X / 5
- **L2 Evidence Specificity**: X / 5
- **L3 Data-Interpretation-Speculation Layering**: X / 5
- **L4 Causal vs Correlational Boundary**: X / 5
- **L5 Alternative Explanations Coverage**: X / 5
- **L6 Claim-Limitation Balance**: X / 5

### 6. Conventions（学术规范）：XX / 20
- **CO1 Contribution Type**: X / 5
- **CO2 Happy Words Appropriateness**: X / 5
- **CO3 Achievement-Contribution Distinction**: X / 5
- **CO4 Limitations Completeness**: X / 5
- **CO5 Future Work Specificity**: X / 5
- **CO6 Operational Specificity**: X / 5

---

## Narrative-Coherence Meta-Score: XX / 10

[Strong / Adequate / Weak]

**Take-home message**: "[从 Discussion 提取的核心信息]"

**Persistence test**:
- 首段 take-home: ✓ / ✗
- 末段 take-home: ✓ / ✗
- 中段一致性: ✓ / ✗

---

## Severity-Tagged Issue List

### Critical（必须修复）
1. **[句子 X]** — [问题描述]
   - Flagged by: [dimension1, dimension2]
   - Fix: [修复建议]
   - Positive example: `references/examples/good_XX.md`
   - 严重度理由: [理由]

2. ...

### Major（应当修复）
1. **[句子 X]** — [问题描述]
   - Flagged by: [dimension]
   - Fix: [修复建议]
   - Positive example: ...

2. ...

### Minor（建议修复）
1. **[句子 X]** — [问题描述]
   - Fix: ...

2. ...

---

## Top-3 Priority Fixes

1. **[Critical] [句子 X]** — 问题: ...; 修复: ...; 正例: `references/examples/good_XX.md`
2. **[Major] [句子 Y]** — 问题: ...; 修复: ...; 正例: ...
3. **[Minor] [句子 Z]** — 问题: ...; 修复: ...; 正例: ...

---

## Cross-Dimension Deduplication Notes

- 问题 Y 被 Grammar 和 Vocabulary 同时标记 → 合并处理
- 问题 Z 被 Conventions 和 Cohesion 同时标记 → 合并处理

---

## Strengths（也值得肯定）

- [做得好的方面 1]
- [做得好的方面 2]
- [做得好的方面 3]

---

## Action Plan

### 立即修复（本次提交前）
1. ...
2. ...

### 短期改进（下次写作时）
1. ...

### 长期培养（持续练习）
1. ...
```

---

## 使用说明

1. **复制模板** → 填入实际诊断结果
2. **每维度按 5 分制给出子分数**（参照各维度 rubric.md）
3. **加权公式**: 总分 = Structure×0.20 + Cohesion×0.20 + Grammar×0.10 + Vocabulary×0.10 + Logic×0.20 + Conventions×0.20
4. **Severity 判定**: 参见 `severity-rubric.md`
5. **跨维度合并**: 参见 `cross-dimension-map.md`
6. **正例引用**: 参见 `examples/` 目录

---

## 简化版（如果只想要快速诊断）

如果只想要简化报告，可只用以下三部分：

```markdown
## 快速诊断

**总分**: XX / 100

**Top-3 修复**:
1. [Critical] ...
2. [Major] ...
3. [Minor] ...

**最强项**: [维度]
**最弱项**: [维度]
```

---

## 相关文件

- `severity-rubric.md` — 严重度判定标准
- `cross-dimension-map.md` — 跨维度问题合并
- `examples/` — 正反例对照