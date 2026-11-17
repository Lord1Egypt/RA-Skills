# Logic Rubric — Discussion 逻辑推理评分

## 用途
本文件是 `discussion-logic-diagnosis` 的官方评分标准。

## 评分维度（共 6 项）

### 维度 L1: Causal Chain Completeness（因果链完整性）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | 完整 mechanism → evidence → conclusion 三层因果链 |
| **4 - Good** | 大部分完整 |
| **3 - Acceptable** | 基本完整；个别 claim 缺 mechanism |
| **2 - Needs Work** | 多处因果链不完整 |
| **1 - Critical Fail** | 因果链断裂；data 直接跳到 conclusion |

#### 因果链 3 层
1. **Mechanism**（机制）：为什么 X 导致 Y
2. **Evidence**（证据）：支持机制的具体 evidence
3. **Conclusion**（结论）：从机制 + 证据推出的 claim

---

### 维度 L2: Evidence Specificity（证据具体性）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | 每个 claim 都有具体 evidence（i.e., 数据 / 文献 / 例子）|
| **4 - Good** | 多数 claim 有具体 evidence |
| **3 - Acceptable** | 部分 claim 具体；部分抽象 |
| **2 - Needs Work** | 多数 claim 抽象 |
| **1 - Critical Fail** | 无 evidence；纯 claim |

#### 反模式
- ❌ "X is similar to Y" （无具体说明相似之处）
- ✅ "X is similar to Y in that both have low agreeableness, low honesty-humility..."

---

### 维度 L3: Data-Interpretation-Speculation Layering（三层结构清晰度）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | Data / Interpretation / Speculation 三层清晰，标志词明显 |
| **4 - Good** | 大部分清晰 |
| **3 - Acceptable** | 三层有混合但可识别 |
| **2 - Needs Work** | 三层混乱 |
| **1 - Critical Fail** | 三层完全混合（data 与 speculation 不分）|

#### 三层标志词（Unit 4.2.2）
| 层 | 标志词 |
|---|---|
| Data | "I found", "The data show", "We observed" |
| Interpretation | "suggest", "indicate", "This means", "We interpret" |
| Speculation | "may", "might", "could", "possibly", "perhaps" |

---

### 维度 L4: Causal vs Correlational Boundary（因果vs相关边界）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | 完全区分因果与相关；claim 与方法匹配 |
| **4 - Good** | 大体区分 |
| **3 - Acceptable** | 偶尔 boundary 不清 |
| **2 - Needs Work** | 多处混淆 |
| **1 - Critical Fail** | 完全混淆（correlational study claim 因果）|

#### 反模式
- ❌ Correlational study claim "X causes Y"
- ❌ Cross-sectional claim "interventions will reduce..."
- ✅ "X is associated with Y" / "X may be related to Y"

---

### 维度 L5: Alternative Explanations Coverage（替代解释覆盖度）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | 2-3 个 alternative explanations + 反驳证据 |
| **4 - Good** | 1-2 个 alternatives + 部分反驳 |
| **3 - Acceptable** | 1 个 alternative |
| **2 - Needs Work** | 无 explicit alternative；只给 1 个解释 |
| **1 - Critical Fail** | 完全无 alternative（单一解释）|

#### 测试
- 主要 claim 是否有 alternative explanation？
- 是否对 alternative 给出反驳或承认？

---

### 维度 L6: Claim-Limitation Balance（Claim 与 Limitation 平衡）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | Limitation 后立即有 claim balance（"Importantly, however, we demonstrate..."）|
| **4 - Good** | 大体平衡 |
| **3 - Acceptable** | 偶尔纯 limitation 无 claim 配套 |
| **2 - Needs Work** | 多处纯 limitation 无 claim |
| **1 - Critical Fail** | 纯 self-flagellation；limitation 段削弱 claim |

#### 反模式
- ❌ "Of course, we cannot prove anything, our study is limited, we acknowledge major flaws..." （自我贬低）
- ✅ "Of course, we certainly do not suggest... Importantly, however, we demonstrate..." （平衡）

---

## 总分计算

**总分 = (L1 + L2 + L3 + L4 + L5 + L6) / 6 × 20** （满分 100）

| 总分区间 | 评级 |
|---|---|
| 90-100 | Excellent |
| 75-89 | Good |
| 60-74 | Acceptable |
| 40-59 | Needs Work |
| <40 | Critical |

---

## 相关 example 文件

- `examples/good_costello_2021_causal_chain.md` — L1/L2 范例
- `examples/good_midgley_2020_data_interpretation_speculation.md` — L3 范例
- `examples/good_ebert_2020_alternatives_addressed.md` — L5 范例
- `examples/good_schmidt_2016_honest_limitation.md` — L6 范例
- `examples/bad_synthetic_causal_overreach.md` — L4 全错反例
- `examples/bad_synthetic_ignoring_alternatives.md` — L5 反例