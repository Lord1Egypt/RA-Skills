# Cohesion Rubric — Discussion 连接与衔接评分

## 用途
本文件是 `discussion-cohesion-diagnosis` 的官方评分标准。

## 评分维度（共 6 项）

### 维度 C1: Topic Sentence Presence（段首主题句存在性）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | 每段首句是清晰的 claim/topic sentence，不是 results 重复 |
| **4 - Good** | 多数段有 topic sentence；个别段是 results 复述 |
| **3 - Acceptable** | 一些段有 topic sentence；一些段直接进入 details |
| **2 - Needs Work** | 多数段无 topic sentence |
| **1 - Critical Fail** | 无任何 topic sentence |

#### 反模式
- ❌ "We found that X correlates with Y." （直接 results 复述）
- ✅ "Our results have important implications for understanding X." （topic sentence）

---

### 维度 C2: Connective Variety（连接词多样性）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | 4+ 种类型连接词（temporal / additive / causal / contrastive）混合 |
| **4 - Good** | 3 种类型 |
| **3 - Acceptable** | 2 种类型 |
| **2 - Needs Work** | 1 种类型主导（大量 "Furthermore"）|
| **1 - Critical Fail** | 无连接词；纯拼接 |

#### 连接词类型清单
| 类型 | 例子 |
|---|---|
| Sequential | First / Second / Third / Finally |
| Causal | Because / As a result / Thus / Therefore |
| Contrastive | However / Nevertheless / In contrast / Yet |
| Additive | Moreover / Furthermore / In addition |
| Exemplifying | For example / Specifically / In particular |
| Concessive | Although / Even though / Despite |

---

### 维度 C3: Connective Density Appropriateness（连接词密度合理性）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | 每段 2-4 个连接词；密度均匀 |
| **4 - Good** | 偶尔密度过高或过低，但总体合适 |
| **3 - Acceptable** | 1-2 段密度过高（"Furthermore" 出现 3+ 次）|
| **2 - Needs Work** | 多段密度过高 |
| **1 - Critical Fail** | 全篇密度失控；每句 1 个 connective |

#### 测试
- "Furthermore" / "Moreover" 在一段出现 ≥3 次 → density 过高
- 一段无任何 connective → density 过低
- 适当密度：每 3-5 句 1 个连接词

---

### 维度 C4: Forward Motion（前向推进感）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | 每段都在推动叙事前进；不重复 Results |
| **4 - Good** | 多数段有 forward motion；个别段重复 |
| **3 - Acceptable** | 有 1-2 处"原地踏步"段 |
| **2 - Needs Work** | 多段重复 Results 无新 claim |
| **1 - Critical Fail** | Discussion = Results 精简版 |

#### 反模式
- ❌ "Studies 1-5 demonstrated that..." （Results 重复）
- ❌ "We found that X, Y, Z." （数据复述，无 so what）
- ✅ "Our finding that X has three implications..." （forward motion）

---

### 维度 C5: Narrative Thread（叙事主线）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | 一条清晰主线贯穿全 Discussion |
| **4 - Good** | 主线清晰；个别段偏离 |
| **3 - Acceptable** | 主线可见但不够突出 |
| **2 - Needs Work** | 多条主线交织；读者难跟随 |
| **1 - Critical Fail** | 无主线；段落独立 |

#### 测试
- 能否用 1 句话总结 Discussion 主线？
- 段间是否清晰连接（不仅靠连接词，还靠逻辑递进）？

---

### 维度 C6: Inter-paragraph Transition（段间过渡）

#### 评分标准

| 分数 | 标准 |
|---|---|
| **5 - Excellent** | 每段到下一段有过渡（topic sentence + 衔接）|
| **4 - Good** | 多数段有过渡 |
| **3 - Acceptable** | 一些段突然跳转 |
| **2 - Needs Work** | 多段无过渡；读者感突兀 |
| **1 - Critical Fail** | 每段独立；无段间连接 |

#### 反模式
- ❌ 段落 1 谈 X，段落 2 突然谈 Y（完全无关主题）
- ✅ 段落 2 开篇："Building on this finding, we now turn to..."

---

## 总分计算

**总分 = (C1 + C2 + C3 + C4 + C5 + C6) / 6 × 20** （满分 100）

| 总分区间 | 评级 |
|---|---|
| 90-100 | Excellent |
| 75-89 | Good |
| 60-74 | Acceptable |
| 40-59 | Needs Work |
| <40 | Critical |

---

## 相关 example 文件

- `examples/good_ayanian_2020_first_second.md` — C1 topic sentence 范例
- `examples/good_costello_2021_unpack_sequence.md` — C5 narrative thread 范例
- `examples/good_ebert_2020_however_transition.md` — C6 过渡范例
- `examples/good_midgley_2020_sequential_connectives.md` — C2 variety 范例
- `examples/bad_ayanian_2020_mechanical_chain.md` — C3 反例
- `examples/bad_synthetic_abrupt_transitions.md` — C6 全错反例